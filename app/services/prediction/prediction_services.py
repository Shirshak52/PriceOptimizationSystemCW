from flask import session
import numpy as np

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from app import db
from app.models.Prediction.model import Prediction
from app.services.prediction.timeframe_specific_services.prediction_services_monthly import (
    PredictionServiceMonthly,
)
from app.services.prediction.timeframe_specific_services.prediction_services_quarterly import (
    PredictionServiceQuarterly,
)
from app.services.prediction.timeframe_specific_services.prediction_services_weekly import (
    PredictionServiceWeekly,
)


class PredictionService:

    @staticmethod
    def save_to_db(
        dataset_file_id, prediction_weekly, prediction_monthly, prediction_quarterly
    ):
        """Saves the predicted sales to the database."""
        try:
            prediction = Prediction(
                dataset_file_id=dataset_file_id,
                sales_next_week=prediction_weekly,
                sales_next_month=prediction_monthly,
                sales_next_quarter=prediction_quarterly,
            )
            db.session.add(prediction)
            db.session.commit()
        except Exception as e:
            print(f"Error: {str(e)}")

    @staticmethod
    def predict_sales(df_weekly, df_monthly, df_quarterly):
        """Returns the sales predicted for the next week, month, and quarter."""
        weekly_prediction = PredictionServiceWeekly.predict_weekly_sales(df_weekly)
        monthly_prediction = PredictionServiceMonthly.predict_monthly_sales(df_monthly)
        quarterly_prediction = PredictionServiceQuarterly.predict_quarterly_sales(
            df_quarterly
        )

        return (
            float(weekly_prediction),
            float(monthly_prediction),
            float(quarterly_prediction),
        )

    @staticmethod
    def scale_dataset(df):
        """Scales the dataset."""
        scaler = MinMaxScaler()
        df_scaled = df.copy()
        numcols = df.select_dtypes(include=[np.number]).columns.tolist()
        df_scaled[numcols] = scaler.fit_transform(df_scaled[numcols])

        return df_scaled

    @staticmethod
    def engineer_features(df):
        """Engineers weekly, monthly, and quarterly features  for prediction and combines them into a single dataset."""

        df_original = df[["Product ID", "Order Date", "Price", "Quantity", "Sales"]]
        # print(f"df_original: {df_original.head()}")

        # Engineer Year-Week, Year-Month, Year-Quarter columns
        df_timeframes = PredictionService.engineer_timeframes(df_original)
        # print(f"df_timeframes: {df_timeframes.head()}")

        # Engineer weekly, monthly, quarterly features
        df_weekly = PredictionServiceWeekly.engineer_features(df_timeframes)
        df_monthly = PredictionServiceMonthly.engineer_features(df_timeframes)
        df_quarterly = PredictionServiceQuarterly.engineer_features(df_timeframes)

        # Drop Product ID
        df_weekly = df_weekly.drop(columns=["Product ID"])
        df_monthly = df_monthly.drop(columns=["Product ID"])
        df_quarterly = df_quarterly.drop(columns=["Product ID"])

        # Save the dataframes to the session
        session["prediction_df_weekly"] = (
            df_weekly.copy().drop(columns={"Year-Week"}).to_dict()
        )
        session["prediction_df_monthly"] = (
            df_monthly.copy().drop(columns={"Year-Month"}).to_dict()
        )
        session["prediction_df_quarterly"] = (
            df_quarterly.copy().drop(columns={"Year-Quarter"}).to_dict()
        )

        # Vertically concatenate the datasets
        df_combined = pd.concat(
            [df_weekly, df_monthly, df_quarterly], axis=0, ignore_index=True
        )

        return df_combined

    @staticmethod
    def engineer_timeframes(df_original):
        """Engineers Year-Week, Year-Month, and Year-Quarter features."""
        df_timeframes = df_original.copy()

        # Year-Week
        df_timeframes["Year-Week"] = df_timeframes["Order Date"].dt.strftime("%Y-%U")

        # Year-Month
        df_timeframes["Year-Month"] = df_timeframes["Order Date"].dt.strftime("%Y-%m")

        # Year-Quarter
        df_timeframes["Year-Quarter"] = df_timeframes["Order Date"].dt.to_period("Q")

        return df_timeframes
