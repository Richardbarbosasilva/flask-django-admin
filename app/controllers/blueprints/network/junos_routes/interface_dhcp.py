from flask import session
import os
from app import db
from dotenv import load_dotenv
from app.models import Routers
from app.controllers.forms import AddressAssignmentForm
from app.controllers.forms import set_access_address_assignment  # Fixed function name
from flask import Blueprint, request, render_template, flash
from flask_login import current_user, login_required, fresh_login_required

# load_dotenv()

# Inicializa o Blueprint
int_dhcp_bp = Blueprint('int_dhcp_bp', __name__)

@int_dhcp_bp.route('/set_access_address_assignment_page', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def set_access_address_assignment_page():
    form = AddressAssignmentForm()
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
                'network/junos/set_access_address_assignment.html',
                form=form,
                output=None,
                devices=devices,
            )

        output = set_access_address_assignment(  # Fixed function call
            hostname, username, user_password
        )

        flash('Command sent successfully!', category='success')

    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", category='danger')

    return render_template(
        'network/junos/set_access_address_assignment.html',
        form=form,
        output=output,
        devices=devices,
    )
