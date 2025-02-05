from flask import request, redirect, render_template, url_for, flash
from flask_login import login_required, logout_user, current_user
from app.blueprints.segmentation.forms.file_upload_form import FileUploadForm
from app.blueprints.segmentation import segmentation_bp
from app.blueprints.segmentation.services import DatasetFileService


@segmentation_bp.route("/", methods=["GET", "POST"])
@login_required
def segmentation_dashboard():
    form = FileUploadForm()

    if form.validate_on_submit():
        file = form.file.data  # File data

        if DatasetFileService.validate_datasetfile(file):
            return redirect(url_for("main.index"))

    return render_template("segmentation.html", form=form, file_is_uploaded=False)
