from flask import redirect, url_for, render_template
from app.blueprints.auth.forms.loginform import LoginForm
from flask_security import login_user, logout_user, login_required
from app.blueprints.auth import auth_bp
from app.blueprints.auth.services import LoginService
from app.models.Branch.model import Branch


@auth_bp.route("/login/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error_message = None

    # On form submit
    if form.validate_on_submit():
        # Fetch the Branch user with the entered email
        branch = Branch.query.filter_by(email=form.email.data).first()

        # Check if user exists and handle login
        if branch is None:
            error_message = "Invalid email"  # Email doesn't exist in the database
        else:
            # Check if password is correct only if email exists
            if LoginService.verify_password(
                email=form.email.data, password=form.password.data
            ):
                login_user(branch)
                return redirect(url_for("main.index"))
            else:
                error_message = "Invalid password"  # Invalid password

    # Pass the form into the login page and display it
    return render_template("login.html", form=form, error_message=error_message)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()  # This will log the user out
    return redirect(url_for("auth.login"))
