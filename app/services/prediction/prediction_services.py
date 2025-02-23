from flask import session
import numpy as np

# from sklearn.cluster import KMeans

# from sklearn.metrics import silhouette_score
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

        # Engineer Year-Week, Year-Month, Year-Quarter columns
        df_timeframes = PredictionService.engineer_timeframes(df_original)

        # Engineer weekly, monthly, quarterly features
        df_weekly = PredictionServiceWeekly.engineer_features(df_timeframes)
        df_monthly = PredictionServiceMonthly.engineer_features(df_timeframes)
        df_quarterly = PredictionServiceQuarterly.engineer_features(df_timeframes)

        # Drop Product ID
        df_weekly = df_weekly.drop(columns=["Product ID"])
        df_monthly = df_monthly.drop(columns=["Product ID"])
        df_quarterly = df_quarterly.drop(columns=["Product ID"])

        # Save the dataframes to the session
        session["prediction_df_weekly"] = df_weekly
        session["prediction_df_monthly"] = df_monthly
        session["prediction_df_quarterly"] = df_quarterly

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
