import os
import click
from flask import Flask
from config import Config
from .extensions import csrf, db, migrate

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    if not app.config.get("SECRET_KEY"):
        if app.config.get("FLASK_ENV") == "production":
            raise RuntimeError("SECRET_KEY must be set in production.")
        app.config["SECRET_KEY"] = "development-only-do-not-use-in-production"
    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app); migrate.init_app(app, db); csrf.init_app(app)
    from .auth.routes import bp as auth_bp
    from .admin.routes import bp as admin_bp
    from .student.routes import bp as student_bp
    app.register_blueprint(auth_bp); app.register_blueprint(admin_bp); app.register_blueprint(student_bp)
    @app.context_processor
    def inject_user():
        from .utils import current_user
        return {"current_user": current_user()}
    register_commands(app)
    return app

def register_commands(app):
    @app.cli.command("create-admin")
    @click.option("--email", prompt=True)
    @click.option("--name", prompt=True)
    @click.password_option(confirmation_prompt=True)
    def create_admin(email, name, password):
        """Create the first administrator without exposing a default password."""
        from .models import User
        if User.query.filter_by(email=email.strip().lower()).first():
            raise click.ClickException("An account with that email already exists.")
        user = User(name=name.strip(), email=email.strip().lower(), role="admin")
        user.set_password(password)
        db.session.add(user); db.session.commit()
        click.echo("Administrator created. You may now sign in.")
