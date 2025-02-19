from flask import render_template
from app.blueprints.main import main_bp
from flask_login import login_required


@main_bp.route("/")
@main_bp.route("/index")
@login_required
def index():
    """Displays the home page."""
    return render_template("index.html")
