from flask import Blueprint

prediction_bp = Blueprint(
    "pred",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/prediction",
)
