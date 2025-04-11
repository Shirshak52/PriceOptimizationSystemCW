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

                optimization_df_original = OptimizationService.get_original_dataset(
                    file
                )
                session["optimization_df_original"] = optimization_df_original

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
                    "message": validation_message,
                }
            )

    else:
        print("Form val failed")
        message = DatasetFileService.validate_datasetfile(form.file.data)[1]
        return jsonify(
            {
                "success": False,
                "message": form.file.errors,
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
        df_original = pd.DataFrame(session.get("optimization_df_original"))

        optimized_sales, price_list = OptimizationService.optimize_prices(
            df_weekly, df_monthly, df_quarterly, df_original
        )

        session["optimized_sales"] = optimized_sales
        session["price_list"] = price_list

        if not all(
            k in session
            for k in [
                "optimized_sales",
                "price_list",
            ]
        ):
            print("Optimization data unavailable")
            return jsonify(
                {
                    "success": False,
                    "message": "Optimization data not available.",
                }
            )
        print(f"Succesfully completed optimization, optimized sales: {optimized_sales}")
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
    price_list = session.get("price_list")
    print(f"Optimizations received from session, optimized sales: {optimized_sales}")

    if optimized_sales is None or price_list is None:
        print("Optimizations not yet available")
        return jsonify(
            {"success": False, "message": "Optimizations not yet available."}
        )

    return jsonify(
        {
            "optimized_sales": optimized_sales,
            "price_list": price_list,
        }
    )


@optimization_bp.route("save_to_db", methods=["GET"])
@login_required
def save_optimization_to_db():
    """Saves the optimization data to the database"""
    dataset_file_id = session.get("dataset_file_id")
    price_list = session.get("price_list")
    optimized_sales = session.get("optimized_sales")

    prediction_weekly = session.get("prediction_weekly")
    prediction_monthly = session.get("prediction_monthly")
    prediction_quarterly = session.get("prediction_quarterly")

    predicted_sales = [prediction_weekly, prediction_monthly, prediction_quarterly]

    try:
        # Save the data to the database
        OptimizationService.save_to_db(
            dataset_file_id, price_list, optimized_sales, predicted_sales
        )

        # Return a success response
        print("Optimization report saved successfully!")
        return jsonify(
            {"success": True, "message": "Optimization report saved successfully!"}
        )

    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": str(e)})
