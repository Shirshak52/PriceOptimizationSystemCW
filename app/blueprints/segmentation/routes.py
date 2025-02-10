from flask import request, redirect, render_template, url_for, flash, session
from flask_login import login_required, logout_user, current_user
from app.blueprints.segmentation.forms.file_upload_form import FileUploadForm
from app.blueprints.segmentation.forms.segmentation_parameters_form import (
    SegmentationParametersForm,
)
from app.blueprints.segmentation import segmentation_bp
from app.services.datasetfile_services import DatasetFileService
from werkzeug.exceptions import RequestEntityTooLarge


@segmentation_bp.route("/", methods=["GET"])
@login_required
def segmentation_dashboard():
    file_upload_form = FileUploadForm()
    segmentation_parameters_form = (
        SegmentationParametersForm() if session.get("file_uploaded") else None
    )
    file_is_uploaded = False
    return render_template(
        "segmentation.html",
        file_upload_form=file_upload_form,
        segmentation_parameters_form=segmentation_parameters_form,
        file_uploaded=session.get("file_uploaded"),
    )


@segmentation_bp.route("/upload", methods=["POST"])
def upload_dataset_file():

    form = FileUploadForm()

    if form.validate_on_submit():
        print("FORM VALIDATION PASSED?!")
        try:
            file = form.file.data  # File data

            if DatasetFileService.validate_datasetfile(file):
                session["file_uploaded"] = DatasetFileService.save_datasetfile(file)
                # return redirect(url_for("main.index"))
            else:
                flash(
                    "Upload unsuccessful. Ensure that all mentioned columns exist and that their datatypes are appropriate.",
                    "error",
                )

        except RequestEntityTooLarge:
            flash("The file is too large. Please upload a smaller file.", "error")

    else:
        print("FORM VAL FAILED", form.errors)

    return redirect(url_for("segm.segmentation_dashboard"))


@segmentation_bp.route("/change_file", methods=["POST"])
def change_dataset_file():
    session["file_uploaded"] = False
    return redirect(url_for("segm.segmentation_dashboard"))
