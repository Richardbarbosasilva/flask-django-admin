from flask import session
import os
from app import db
from dotenv import load_dotenv
from app.controllers.forms import BgpManagerSessionForm
from app.models import Routers, NeighborBgpIpv4, NeighborBgpIpv6
from app.controllers.netmiko import bgp_manager_session  # Ensure this import exists
from flask import Blueprint, request, render_template, flash, jsonify
from flask_login import current_user, login_required, fresh_login_required

# load_dotenv()

# Inicializa o Blueprint
bgp_manager_session_bp = Blueprint('bgp_manager_session_bp', __name__)

# Rota: bgp_manager_session_bp
@bgp_manager_session_bp.route('/bgp_manager_session', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def bgp_manager_session():
    form = BgpManagerSessionForm()
    hosts = db.session.execute(db.select(Routers).order_by(Routers.id)).scalars().all()
    form.hostname.choices = [(host.ip_address, host.hostname) for host in hosts]

    output = None

    if form.validate_on_submit():
        hostname = form.hostname.data
        username = current_user.username

        # Salva a senha do usuário na sessão (se existir no formulário)
        if form.password.data:
            session['user_password'] = form.password.data

        # Recupera a senha armazenada na sessão
        user_password = session.get('user_password')

        if not user_password:
            flash('User password is missing. Please log in again.', category='danger')
            return render_template(
                'network/junos/bgp_manager_session.html',
                form=form,
                output=None,
            )

        action = form.action.data
        group = form.group.data
        neighbor = form.neighbor.data

        output = bgp_manager_session(
            hostname, username, user_password,
            action, group, neighbor
        )

        flash('Command sent successfully!', category='success')

    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", category='danger')

    return render_template(
        'network/junos/bgp_manager_session.html',
        form=form,
        output=output,
    )


@bgp_manager_session_bp.route('/get_neighbors', methods=['POST'])
@login_required
def get_neighbors():
    data = request.json
    group = data.get("group")

    if not group:
        return jsonify({"error": "O campo 'group' é obrigatório"}), 400

    if group == 'Sessoes_Transito_IPv4':
        neighbors = db.session.execute(db.select(NeighborBgpIpv4).order_by(NeighborBgpIpv4.id)).scalars().all()
    else:
        neighbors = db.session.execute(db.select(NeighborBgpIpv6).order_by(NeighborBgpIpv6.id)).scalars().all()

    response = jsonify([{"neighbor": n.neighbor, "description": n.description} for n in neighbors])
    return response
