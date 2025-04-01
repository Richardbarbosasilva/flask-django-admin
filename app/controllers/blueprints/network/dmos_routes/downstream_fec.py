from flask import session, Blueprint, render_template, flash
import os
from app import db
from dotenv import load_dotenv
from app.models import Users, Olts
from app.controllers.forms import Downstream_fec_form
from flask_login import current_user, login_required, fresh_login_required
from app.controllers.netmiko.dmos.no_downstream_fec import no_downstream_fec

# load_dotenv()

downstream_fec_bp = Blueprint('downstream_fec_bp', __name__)

@downstream_fec_bp.route('/downstream_fec', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def downstream_fec():
    form = Downstream_fec_form()
    hosts = db.session.execute(db.select(Olts).order_by(Olts.id)).scalars()
    form.hostname.choices = [(host.ip_address, host.hostname) for host in hosts]

    output = None

    if form.validate_on_submit():
        # If the form includes a password field, save it in the session.
        if hasattr(form, 'password') and form.password.data:
            session['user_password'] = form.password.data

        # Retrieve the user password from the session
        user_password = session.get('user_password')

        if not user_password:
            flash('User password is missing. Please log in again.', category='danger')
            return render_template(
                'network/dmos/downstream_fec.html',
                form=form,
                output=None,
            )

        output = no_downstream_fec(
            hostname=form.hostname.data,
            username=current_user.username,
            password=user_password,
            chassis=form.chassis.data,
            slot=form.slot.data,
            port_id=form.port_id.data,
            dmos_command=form.dmos_command.data
        )

        flash('Command sent successfully!', category='success')

    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", category='danger')

    return render_template(
        'network/dmos/downstream_fec.html',
        form=form,
        output=output,
    )
