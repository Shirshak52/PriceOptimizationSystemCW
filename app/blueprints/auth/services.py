from flask import redirect, flash, request, url_for
from flask_login import login_user
from app.models.Branch.crud import BranchUserCrud


class LoginService:
    @staticmethod
    def handle_login(form):
        """Validates the login credentials."""

        # Get the user with the entered email
        user = BranchUserCrud.get_user_by_email(form.email.data)

        # If user exists, allow login
        if user and BranchUserCrud.check_password(user, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.index"))

        # If user does not exist, flash error message
        flash("Invalid username/password.")
        return redirect(url_for("auth.login"))
