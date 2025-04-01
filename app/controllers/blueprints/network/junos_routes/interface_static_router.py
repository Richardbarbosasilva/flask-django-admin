from flask import session
import os
from app import db
from dotenv import load_dotenv
from app.models import Routers
from app.controllers.forms import StaticRouteForm
from app.controllers.netmiko import set_static_route
from flask import Blueprint, request, render_template, flash
from flask_login import current_user, login_required, fresh_login_required

# load_dotenv()

# Inicializa o Blueprint
int_static_route_bp = Blueprint('int_static_route_bp', __name__)

@int_static_route_bp.route('/set_static_route', methods=['GET', 'POST'])

@login_required
@fresh_login_required
def set_static_route_page():
    form = StaticRouteForm()
    devices = db.session.execute(db.select(Routers)).scalars().all()
    output = None

    if form.validate_on_submit():
        hostname = request.form.get('hostname')
        username = current_user.username

        # Salva a senha do usuário na sessão (se existir no formulário)
        if form.password.data:
            session['user_password'] = form.password.data

        # Recupera a senha armazenada na sessão
        user_password = session.get('user_password')

        if not user_password:
            flash('User password is missing. Please log in again.', category='danger')
            return render_template(
                'network/junos/set_static_route.html',
                form=form,
                output=None,
                devices=devices,
            )

        network_dest = form.network_dest.data + form.prefix_dest.data
        next_hop = form.next_hop.data

        output = set_static_route(
            hostname, username, user_password,
            network_dest, next_hop,
        )

        flash('Command sent successfully!', category='success')

    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", category='danger')

    return render_template(
        'network/junos/set_static_route.html',
        form=form,
        output=output,
        devices=devices,
    )
