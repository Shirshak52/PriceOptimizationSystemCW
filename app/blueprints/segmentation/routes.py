from flask import jsonify, request, redirect, render_template, url_for, flash, session
from flask_login import login_required, logout_user, current_user
from app.blueprints.segmentation.forms.file_upload_form import FileUploadForm
from app.blueprints.segmentation.forms.segmentation_parameters_form import (
    SegmentationParametersForm,
)
from app.blueprints.segmentation import segmentation_bp
from app.services.datasetfile_services import DatasetFileService
from werkzeug.exceptions import RequestEntityTooLarge

from app.services.segmentation_services import SegmentationService


@segmentation_bp.route("/", methods=["GET"])
@login_required
def segmentation_dashboard():
    """Presents the segmentation page with the file-uploading form."""

    # File-uploading form
    file_upload_form = FileUploadForm()

    # Form to input number of clusters and clustering metric
    segmentation_parameters_form = (
        SegmentationParametersForm() if session.get("file_uploaded") else None
    )

    # Render segmentation.html with the 2 forms
    return render_template(
        "segmentation.html",
        file_upload_form=file_upload_form,
        segmentation_parameters_form=segmentation_parameters_form,
        # Boolean that shows only one of the forms
        file_uploaded=session.get("file_uploaded"),
    )


@segmentation_bp.route("/upload", methods=["POST"])
@login_required
def upload_dataset_file():
    """Validates the file-uploading form and saves it after preprocessing."""

    # File-uploading form
    form = FileUploadForm()

    if form.validate_on_submit():
        print("FORM VALIDATION PASSED")
        try:
            # Retrieve the file
            file = form.file.data

            # Validate and save the file
            if DatasetFileService.validate_datasetfile(file):
                file_is_saved = DatasetFileService.save_datasetfile(
                    file, "segmentation"
                )
                session["file_uploaded"] = file_is_saved

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
@login_required
def change_dataset_file():
    """Redirects user back to the file-uploading form."""
    session["file_uploaded"] = False
    return redirect(url_for("segm.segmentation_dashboard"))


@segmentation_bp.route("/cluster_customers", methods=["POST"])
@login_required
def cluster_customers():
    """Takes input from Segmentation Parameters form and returns cluster counts after segmentation."""

    # Form to input number of clusters and clustering metric
    form = SegmentationParametersForm()

    if form.validate_on_submit():
        print("segm form passedd")

        # Get the dataset inside the submitted file
        df = DatasetFileService.get_session_dataframe()

        # Retrieve number of clusters and clustering metric from the form
        num_of_clusters = form.number_choice.data
        chosen_metric = form.metric.data

        # Cluster the dataset and set cluster counts in the session
        cluster_counts = SegmentationService.segment_customers(
            df, num_of_clusters, chosen_metric
        ).to_dict()
        session["cluster_counts"] = cluster_counts
    else:
        print("segm form not passedd", form.errors)

    return redirect(url_for("segm.segmentation_dashboard"))


@segmentation_bp.route("/get_cluster_counts", methods=["GET"])
@login_required
def get_cluster_counts():
    """Returns the cluster counts stored in the session."""

    # Get the cluster counts from the session, if none get an empty dict
    cluster_counts = session.get("cluster_counts", {})
    return jsonify(cluster_counts)
