from flask import jsonify, render_template, session
from flask_login import login_required
import pandas as pd
from werkzeug.exceptions import RequestEntityTooLarge

from app.forms.file_upload_form import FileUploadForm

from app.services.datasetfile_services import DatasetFileService


from app.blueprints.optimization import optimization_bp
from app.services.optimization.optimization_services import OptimizationService


@optimization_bp.route("/", methods=["GET"])
@login_required
def optimization_dashboard():
    """Presents the optimization page with the file-uploading form."""

    # File-uploading form
    file_upload_form = FileUploadForm()

    # Render optimization.html with the 2 forms
    return render_template(
        "optimization.html",
        file_upload_form=file_upload_form,
    )


@optimization_bp.route("/upload", methods=["POST"])
@login_required
def upload_prediction_dataset_file():
    """Validates the file-uploading form and saves it after preprocessing."""

    # File-uploading form
    form = FileUploadForm()

    session.pop("_flashes", None)

    if form.validate_on_submit():
        print("FORM VALIDATION PASSED")
        try:
            # Retrieve the file
            file = form.file.data

            is_valid_file, validation_message = DatasetFileService.validate_datasetfile(
                file
            )

            # Validate and save the file
            if is_valid_file:
                file_is_saved, dataset_file_id = DatasetFileService.save_datasetfile(
                    file, "optimization"
                )
                session["optimization_file_uploaded"] = file_is_saved
                session["dataset_file_id"] = dataset_file_id

                # print(f"File saved successfully, file id: {dataset_file_id}")

                return jsonify(
                    {
                        "success": True,
                        "message": "Successfully uploaded optimization file.",
                    }
                )

            else:
                print(f"File save failed: {validation_message}")
                return jsonify(
                    {
                        "success": False,
                        "message": validation_message,
                    }
                )

        except RequestEntityTooLarge:
            print("File too large")
            return jsonify(
                {
                    "success": False,
                    "message": "Optimization file too large.",
                }
            )

    else:
        print("Form val failed")
        return jsonify(
            {
                "success": False,
                "message": "Form validation failed.",
            }
        )


@optimization_bp.route("/predict_sales", methods=["GET"])
@login_required
def predict_sales():
    try:
        df_weekly = pd.DataFrame(session.get("prediction_df_weekly"))
        df_monthly = pd.DataFrame(session.get("prediction_df_monthly"))
        df_quarterly = pd.DataFrame(session.get("prediction_df_quarterly"))

        prediction_weekly, prediction_monthly, prediction_quarterly = (
            OptimizationService.predict_sales(df_weekly, df_monthly, df_quarterly)
        )

        # Set the predictions in the session
        session["prediction_weekly"] = float(prediction_weekly)
        session["prediction_monthly"] = float(prediction_monthly)
        session["prediction_quarterly"] = float(prediction_quarterly)

        if not all(
            k in session
            for k in [
                "prediction_weekly",
                "prediction_monthly",
                "prediction_quarterly",
            ]
        ):
            print("Prediction data unavailable")
            return jsonify(
                {
                    "success": False,
                    "message": "Prediction data not available.",
                }
            )
        print(
            f"Succesfully predicted sales, predictions: {prediction_weekly, prediction_monthly, prediction_quarterly}"
        )
        return jsonify({"success": True, "message": "Successfully predicted sales."})
    except Exception as e:
        print("Error during prediction")
        return jsonify(
            {"success": False, "message": f"Error during prediction: {str(e)}"}
        )


@optimization_bp.route("/get_predictions", methods=["GET"])
@login_required
def get_predictions():
    prediction_weekly = session.get("prediction_weekly")
    prediction_monthly = session.get("prediction_monthly")
    prediction_quarterly = session.get("prediction_quarterly")
    print(f"predictions: {prediction_weekly,prediction_monthly,prediction_quarterly}")

    if (
        prediction_weekly is None
        or prediction_monthly is None
        or prediction_quarterly is None
    ):
        print("Predictions not yet available")
        return jsonify({"success": False, "message": "Predictions not yet available."})

    return jsonify(
        {
            "prediction_weekly": prediction_weekly,
            "prediction_monthly": prediction_monthly,
            "prediction_quarterly": prediction_quarterly,
        }
    )


@optimization_bp.route("/optimize_prices", methods=["GET"])
@login_required
def optimize_prices():
    try:
        df_weekly = pd.DataFrame(session.get("prediction_df_weekly"))
        df_monthly = pd.DataFrame(session.get("prediction_df_monthly"))
        df_quarterly = pd.DataFrame(session.get("prediction_df_quarterly"))

        optimized_sales, optimized_prices, current_prices = (
            OptimizationService.optimize_prices(df_weekly, df_monthly, df_quarterly)
        )

        session["optimized_sales"] = optimized_sales
        session["optimized_prices"] = optimized_prices
        session["current_prices"] = current_prices

        if not all(
            k in session
            for k in [
                "optimized_sales",
                "optimized_prices",
                "current_prices",
            ]
        ):
            print("Optimization data unavailable")
            return jsonify(
                {
                    "success": False,
                    "message": "Optimization data not available.",
                }
            )
        print(f"Succesfully completed optimization.")
        return jsonify(
            {"success": True, "message": "Successfully completed optimization."}
        )

    except Exception as e:
        print(f"Error during optimization: {str(e)}")
        return jsonify(
            {"success": False, "message": f"Error during optimization: {str(e)}"}
        )


@optimization_bp.route("/get_optimizations", methods=["GET"])
@login_required
def get_optimizations():
    optimized_sales = session.get("optimized_sales")
    optimized_prices = session.get("optimized_prices")
    current_prices = session.get("current_prices")
    print("Optimizations received from session.")

    if optimized_sales is None or optimized_prices is None or current_prices is None:
        print("Optimizations not yet available")
        return jsonify(
            {"success": False, "message": "Optimizations not yet available."}
        )

    return jsonify(
        {
            "optimized_sales": optimized_sales,
            "optimized_prices": optimized_prices,
            "current_prices": current_prices,
        }
    )


@optimization_bp.route("save_to_db", methods=["POST"])
@login_required
def save_optimization_to_db():
    """"""
    # Get the dataset file ID, chosen metric, cluster counts, and metric averages
    # dataset_file_id = session.get("dataset_file_id")
    # prediction_weekly = session.get("prediction_weekly")
    # prediction_monthly = session.get("prediction_monthly")
    # prediction_quarterly = session.get("prediction_quarterly")

    # try:
    #     # Save the data to the database
    #     PredictionService.save_to_db(
    #         dataset_file_id, prediction_weekly, prediction_monthly, prediction_quarterly
    #     )

    #     # Return a success response
    #     print("Prediction report saved successfully!")
    #     return jsonify(
    #         {"success": True, "message": "Prediction report saved successfully!"}
    #     )

    # except Exception as e:
    #     print("Error:", e)
    #     return jsonify({"success": False, "message": str(e)})
