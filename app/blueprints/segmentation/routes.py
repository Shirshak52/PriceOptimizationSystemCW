from flask import jsonify, redirect, render_template, request, url_for, flash, session
from flask_login import login_required
from werkzeug.exceptions import RequestEntityTooLarge

from app.forms.file_upload_form import FileUploadForm

from app.services.datasetfile_services import DatasetFileService
from app.services.segmentation.segmentation_services import SegmentationService

from app.blueprints.segmentation import segmentation_bp
from app.blueprints.segmentation.forms.segmentation_parameters_form import (
    SegmentationParametersForm,
)


@segmentation_bp.route("/", methods=["GET"])
@login_required
def segmentation_dashboard():
    """Presents the segmentation page with the file-uploading form."""

    # File-uploading form
    file_upload_form = FileUploadForm()

    # Form to input number of clusters and clustering metric
    segmentation_parameters_form = SegmentationParametersForm()

    segmentation_file_uploaded = request.args.get("uploaded", "False").lower() == "true"

    # Render segmentation.html with the 2 forms
    return render_template(
        "segmentation.html",
        file_upload_form=file_upload_form,
        segmentation_parameters_form=segmentation_parameters_form,
        # Boolean that shows only one of the forms
        segmentation_file_uploaded=segmentation_file_uploaded,
    )


@segmentation_bp.route("/upload", methods=["POST"])
@login_required
def upload_segmentation_dataset_file():
    """Validates the file-uploading form and saves it after preprocessing."""

    # File-uploading form
    file_upload_form = FileUploadForm()

    if file_upload_form.validate_on_submit():
        print("FORM VALIDATION PASSED")
        try:
            # Retrieve the file
            file = file_upload_form.file.data

            is_valid_file, validation_message = DatasetFileService.validate_datasetfile(
                file
            )

            # Validate and save the file
            if is_valid_file:
                file_is_saved, dataset_file_id = DatasetFileService.save_datasetfile(
                    file, "segmentation"
                )
                session["segmentation_file_uploaded"] = file_is_saved
                session["dataset_file_id"] = dataset_file_id

            else:
                flash(
                    validation_message,
                    "error",
                )

        except RequestEntityTooLarge:
            flash("The file is too large. Please upload a smaller file.", "error")

    else:
        print("FORM VAL FAILED", file_upload_form.file.errors)
        return redirect(url_for("segm.segmentation_dashboard"))

    return redirect(
        url_for(
            "segm.segmentation_dashboard",
            uploaded=session.get("segmentation_file_uploaded"),
        )
    )


@segmentation_bp.route("/change_file", methods=["POST"])
@login_required
def change_segmentation_dataset_file():
    """Redirects user back to the file-uploading form."""
    session["segmentation_file_uploaded"] = False
    return redirect(
        url_for(
            "segm.segmentation_dashboard",
            uploaded=session.get("segmentation_file_uploaded"),
        )
    )


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
        session["chosen_metric"] = (
            chosen_metric  # Set the chosen metric into the session
        )

        # Cluster the dataset and set cluster counts in the session
        cluster_counts, metric_averages = SegmentationService.segment_customers(
            df, num_of_clusters, chosen_metric
        )
        if cluster_counts is None or metric_averages is None:
            return jsonify(
                {"success": False, "message": "Insufficient variation in data."}
            )

        session["cluster_counts"] = cluster_counts
        session["metric_averages"] = metric_averages
        print(cluster_counts)
        print(metric_averages)
        return jsonify({"success": True})
    else:
        print("segm form not passedd", form.errors)
        return jsonify({"success": False}), 400


@segmentation_bp.route("/get_cluster_profiles", methods=["GET"])
@login_required
def get_cluster_profiles():
    """Returns the chosen metric, cluster counts, and metric averages stored in the session."""

    # Get the chosen metric, cluster counts, and metric averages from the session
    chosen_metric = session.get("chosen_metric", "Metric not chosen")
    cluster_counts = session.get("cluster_counts", {})
    metric_averages = session.get("metric_averages", {})

    total_customers = sum(cluster_counts.values())
    cluster_percentages = {
        cluster: (count / total_customers * 100) if total_customers > 0 else 0
        for cluster, count in cluster_counts.items()
    }
    return jsonify(
        {
            "cluster_counts": cluster_counts,
            "metric_averages": metric_averages,
            "cluster_percentages": cluster_percentages,
            "chosen_metric": chosen_metric,
        }
    )


@segmentation_bp.route("save_to_db", methods=["POST"])
@login_required
def save_segmentation_to_db():
    # Get the dataset file ID, chosen metric, cluster counts, and metric averages
    dataset_file_id = session.get("dataset_file_id")
    chosen_metric = session.get("chosen_metric", "Metric not chosen")
    cluster_counts = session.get("cluster_counts", {})
    metric_averages = session.get("metric_averages", {})

    try:
        # Save the data to the database
        SegmentationService.save_to_db(
            dataset_file_id, chosen_metric, cluster_counts, metric_averages
        )

        # Return a success response
        print("Segmentation report saved successfully!")
        return jsonify({"message": "Segmentation report saved successfully!"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"Error": str(e)}), 500
