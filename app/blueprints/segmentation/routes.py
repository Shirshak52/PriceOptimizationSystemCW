from flask import request, redirect, render_template, url_for, flash
from flask_login import login_required, logout_user, current_user
from app.blueprints.segmentation.forms.file_upload_form import FileUploadForm
from app.blueprints.segmentation import segmentation_bp
from app.blueprints.segmentation.services import DatasetFileService
from werkzeug.exceptions import RequestEntityTooLarge


@segmentation_bp.route("/", methods=["GET", "POST"])
@login_required
def segmentation_dashboard():
    form = FileUploadForm()
    file_is_uploaded = False

    if form.validate_on_submit():
        print("FORM VALIDATION PASSED?!")
        try:
            file = form.file.data  # File data

            if DatasetFileService.validate_datasetfile(file):
                file_is_uploaded = DatasetFileService.save_datasetfile(file)
                return redirect(url_for("main.index"))
            else:
                flash(
                    "Upload unsuccessful. Ensure that all mentioned columns exist and that their datatypes are appropriate.",
                    "error",
                )

        except RequestEntityTooLarge:
            flash("The file is too large. Please upload a smaller file.", "error")

    else:
        print("FORM VAL FAILED", form.errors)

    return render_template(
        "segmentation.html", form=form, file_is_uploaded=file_is_uploaded
    )
