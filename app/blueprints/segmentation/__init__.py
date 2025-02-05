from flask import Blueprint

segmentation_bp = Blueprint(
    "segm", __name__, template_folder="templates", url_prefix="/segmentation"
)
