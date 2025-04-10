from flask import redirect, render_template, url_for, flash
from flask_login import login_required, logout_user, current_user

from app.blueprints.auth import auth_bp
from app.blueprints.auth.services import LoginService
from app.blueprints.auth.forms.loginform import LoginForm


@auth_bp.route("/login/", methods=["GET"])
@auth_bp.route("/login", methods=["GET"])
def show_login():
    """Displays the login page."""
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    # Pass the form into the login page and display it
    return render_template("login.html", form=form)


@auth_bp.route("/handle_login", methods=["POST"])
def handle_login():
    """Validates the login credentials."""
    form = LoginForm()

    # On form submit
    if form.validate_on_submit():
        # Handle login
        return LoginService.handle_login(form)

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """Logs the user out."""
    logout_user()
    return redirect(url_for("auth.show_login"))


# User loader and Unauthorized handler
from app import login_manager
from app.models.Branch.model import Branch


@login_manager.user_loader
def load_user(user_id):
    """Checks if user is logged-in on every page load."""
    if user_id is not None:
        return Branch.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirects unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("auth.show_login"))
