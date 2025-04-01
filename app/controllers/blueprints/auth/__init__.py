import os
import sqlite3
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, UserMixin
from app.controllers.forms import LoginForm, RegisterForm
from django.contrib.auth.hashers import check_password  # ✅ Correct Django import
import django
import sys

# Configurando Django
# caminho para o diretório do projeto Django

sys.path.insert(0, '/var/www/django-admin/elevate')

# chamando e carregando o arquivo de configuração do Django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevate.settings')
django.setup()

auth_bp = Blueprint('auth', __name__)

# Caminho do banco de dados Django

SQLITE_PATH = "/var/www/django-admin/elevate/db.sqlite3"

class DjangoUser(UserMixin):

    """Class to store Django user data in Flask-Login"""

    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email
        self.password = 'Ri21851619!' # string password, NEED TO ADJUST IT FOR PRODUCTION! 

    def get_id(self):
        return str(self.id)    

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        try:
            conn = sqlite3.connect(SQLITE_PATH)
            cursor = conn.cursor()
            print("Successfully connected to Django database")

            # Buscar usuário no banco Django
            cursor.execute("SELECT id, username, email, password FROM auth_user WHERE username = ?", (username,))
            user_data = cursor.fetchone()

            if user_data:
                user_id, db_username, email, db_password = user_data
                print(f"Fetched user: {db_username}")

                # Verifica se a senha está presente antes de validar

                if db_password and check_password(password, db_password):

                    print("Senha válida")

                    user = DjangoUser(user_id, db_username, email)

                    login_user(user)

                    print (f"{user} logged in")

                    flash(f'Login successful, welcome {db_username}!', category='success')
                    
                    print (f"redirecting user to the main page")
                    print (f"User redirected to the main page (get_interface_ae0_summary.py) successfully!")

                    return redirect(url_for('int_summary_bp.interface_summary'))
              
                else:
                    flash('Incorrect password', category='danger')
                    print("Incorrect password")
            else:
                flash('User not found', category='danger')

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            flash("Database connection error!", category='danger')
        finally:
            if conn:
                conn.close()

    if form.errors:
        for field_name, error_messages in form.errors.items():
            for error_message in error_messages:
                flash(f'Error in {field_name}: {error_message}', category='danger')

    return render_template('accounts/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Login out!!!', category='info')
    return redirect(url_for('auth.login'))
