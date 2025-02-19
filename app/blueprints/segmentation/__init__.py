from flask import Blueprint
from flask_login import login_required

segmentation_bp = Blueprint(
    "segm", __name__, template_folder="templates", url_prefix="/segmentation"
)
