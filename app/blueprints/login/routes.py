# from flask import redirect, url_for, render_template
# from flask_security.forms import LoginForm
# from flask_security import login_user
# from app.blueprints.login import login_bp
# from app.blueprints.login.services import LoginService
# from app.models.Branch.model import Branch


# @login_bp.route("/", methods=["GET", "POST"])
# def login():
#     form = LoginForm()

#     # On form submit
#     if form.validate_on_submit():
#         # Fetching the Branch user with the entered email
#         branch = Branch.query.filter_by(email=form.email.data).first()

#         # Check if user exists and verify password
#         if branch and LoginService.verify_password(form.email.data, form.password.data):
#             login_user(branch)
#             return redirect(url_for("main.index"))

#     # Pass the form into the login page and display it
#     return render_template("login/login.html", form=form)
