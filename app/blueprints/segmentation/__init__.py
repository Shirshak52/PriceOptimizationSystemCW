from flask import Blueprint

segmentation_bp = Blueprint(
    "segm",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/segmentation",
)
