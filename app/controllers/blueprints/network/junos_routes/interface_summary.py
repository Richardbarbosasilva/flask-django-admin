from flask import session
import os
from app import db
from dotenv import load_dotenv
from app.models import Routers
from app.controllers.forms import NetworkForm
from app.controllers.netmiko import get_interface_ae0_summary
from flask import Blueprint, request, render_template, flash
from flask_login import current_user, login_required, fresh_login_required

#load_dotenv()

# Inicializa o Blueprint

int_summary_bp = Blueprint('int_summary_bp', __name__)

@int_summary_bp.route('/get_interface_ae0_summary', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def interface_summary():
    form = NetworkForm()

    devices = db.session.execute(db.select(Routers)).scalars().all()
    output = None

    if request.method == 'POST':
        selected_hostname = form.hostname.data
        logged_username = current_user.username

        # Salva a senha do usuário na sessão (se existir no formulário)
        if form.password.data:
            session['user_password'] = form.password.data

        # Recupera a senha armazenada na sessão
        user_password = session.get('user_password')

        if not user_password:
            flash('User password is missing. Please log in again.', category='danger')
            return render_template(
                'network/junos/get_interface_ae0_summary.html',
                form=form,
                output=None,
                devices=devices,
            )

        output = get_interface_ae0_summary(
            selected_hostname,
            logged_username,
            user_password,
        )

        flash('Command sent successfully!', category='success')

    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", category='danger')

    return render_template(
        'network/junos/get_interface_ae0_summary.html',
        form=form,
        output=output,
        devices=devices,
    )
