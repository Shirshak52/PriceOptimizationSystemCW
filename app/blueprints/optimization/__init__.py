from flask import Blueprint

optimization_bp = Blueprint(
    "opt",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/optimization",
)
