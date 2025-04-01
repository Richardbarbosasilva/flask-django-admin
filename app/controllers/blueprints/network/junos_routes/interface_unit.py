from flask import session
import os
from app import db
from dotenv import load_dotenv
from app.models import Routers
from app.controllers.forms import NetworkForm
from flask import Blueprint, render_template, flash
from app.controllers.netmiko import set_interface_unit
from flask_login import current_user, login_required, fresh_login_required

# load_dotenv()

# Inicializa o Blueprint
int_unit_bp = Blueprint('int_unit_bp', __name__)

# Rota: set_interface_unit
@int_unit_bp.route('/set_interface_unit', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def interface_unit():
    form = NetworkForm()

    output = None

    hosts = db.session.execute(db.select(Routers).order_by(Routers.id)).scalars()
    form.hostname.choices = [(host.ip_address, host.hostname) for host in hosts]

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
                'network/junos/set_interface_unit.html',
                form=form,
                output=None,
            )

        unit = form.unit_vlan.data
        description = form.description.data
        bandwidth = form.bandwidth.data
        ipv4_gw = form.ipv4_gw.data
        ipv6_gw = form.ipv6_gw.data
        ipv6_cli = form.ipv6_cli.data
        inet6_48 = form.ipv6_48.data

        output = set_interface_unit(
            hostname, username, user_password, unit, description,
            bandwidth, ipv4_gw, ipv6_gw, ipv6_cli, inet6_48
        )

        flash('Command sent successfully!', category='success')

    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", category='danger')

    return render_template(
        'network/junos/set_interface_unit.html',
        form=form,
        output=output,
    )
