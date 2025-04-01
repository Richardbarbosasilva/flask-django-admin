from flask import session
import os
from app import db
from dotenv import load_dotenv
from app.models import Routers
from app.controllers.forms import NetworkForm
from app.controllers.netmiko import get_interface_ae0_config
from flask import Blueprint, request, render_template, flash
from flask_login import current_user, login_required, fresh_login_required

#load_dotenv()

# Inicializa o Blueprint
int_conf_bp = Blueprint('int_conf_bp', __name__)

# Rota: get_interface_ae0_config
@int_conf_bp.route('/get_interface_ae0_config', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def interface_configuration():
    form = NetworkForm()

    devices = db.session.execute(db.select(Routers)).scalars().all()
    output = None

    if request.method == 'POST':
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
                'network/junos/get_interface_ae0_config.html',
                form=form,
                output=None,
                devices=devices,
            )

        unit = request.form.get('unit')

        output = get_interface_ae0_config(
            hostname, username, user_password, unit
        )

        flash('Command sent successfully!', category='success')

    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", category='danger')

    return render_template(
        'network/junos/get_interface_ae0_config.html',
        form=form,
        output=output,
        devices=devices,
    )
