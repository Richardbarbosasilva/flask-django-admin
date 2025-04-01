from flask_admin import Admin, AdminIndexView
from livereload import Server  # noqa: F401
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, render_template
from sqlalchemy.orm import DeclarativeBase
from flask import Flask
from flask_assets import Environment, Bundle

# def run_unauthorizedadmin2():
# call (["python", "unauthorizedadmin.py"])

# run_unauthorizedadmin2()


# Declarative base class for SQLAlchemy
# This class serves as the base for all SQLAlchemy models, enabling table creation in the database.
class Base(DeclarativeBase):
    pass


# Initializing Flask extensions
db = SQLAlchemy(model_class=Base)  # Manages database interactions
lm = LoginManager()  # Manages user sessions and authentication
migrate = Migrate()


# unauthorizedadmin = importlib.import_module("unauthorizedadmin.py")

# Custom admin index view to restrict access
class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        """Allow access only to authenticated users."""
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        """Redirect to login page if user is not authenticated."""
        return render_template("admin/admin_access_error.html")


# Flask-Admin instance with secured access

admin = Admin(index_view=SecureAdminIndexView())


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')  # Carrega a configuração

    # Inicializando as extensões
    db.init_app(app)
    lm.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db)

    # Configurações do Flask-Login
    lm.login_view = 'auth.login'
    lm.login_message = 'Please log in to access this page.'
    lm.login_message_category = 'info'
    lm.session_protection = "strong"
    lm.refresh_view = "auth.login"
    lm.needs_refresh_message = (
        u"To protect your account, please reauthenticate to access this page."
    )
    lm.needs_refresh_message_category = "info"

    # Função user_loader para carregar o usuário a partir do ID armazenado na sessão
    @lm.user_loader
    def load_user(user_id):
        import sqlite3
        from app.controllers.blueprints.auth.__init__ import DjangoUser, SQLITE_PATH
        try:
            conn = sqlite3.connect(SQLITE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, email, password FROM auth_user WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                user_id, username, email, db_password = user_data
                return DjangoUser(user_id, username, email)
        except sqlite3.Error as e:
            print(f"Database error on load_user: {e}")
        finally:
            if conn:
                conn.close()
        return None

    # Registro dos blueprints
    from app.controllers.blueprints import register_blueprints
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def page_home():
        return redirect(url_for('int_summary_bp.interface_summary'))

    return app

# Registrando o manipulador de erro 404 fora da função create_app()
app = create_app()  # Cria a instância do Flask
@app.errorhandler(404)
def page_not_found(e):
    return render_template("admin_access_error.html"), 404