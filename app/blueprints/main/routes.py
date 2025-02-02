from flask import render_template, redirect, url_for
from app.blueprints.main import main_bp
from flask_login import current_user, login_required, logout_user


@main_bp.route("/")
@main_bp.route("/index")
@login_required
def index():
    return render_template("index.html")
