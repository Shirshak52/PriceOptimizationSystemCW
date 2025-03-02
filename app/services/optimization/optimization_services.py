from flask import session
import numpy as np

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from app import db
from app.models.Optimization.model import Optimization
from app.models.OptimizedPrices.model import OptimizedPrices
from app.models.OptimizedSales.model import OptimizedSales
from app.models.Prediction.model import Prediction
from app.services.optimization.timeframe_specific_services.optimization_services_monthly import (
    OptimizationServiceMonthly,
)
from app.services.optimization.timeframe_specific_services.optimization_services_quarterly import (
    OptimizationServiceQuarterly,
)
from app.services.optimization.timeframe_specific_services.optimization_services_weekly import (
    OptimizationServiceWeekly,
)


class OptimizationService:

    @staticmethod
    def optimize_prices(df_weekly, df_monthly, df_quarterly, df_original):
        """"""
        optimized_sales_weekly, optimized_prices_weekly, prices_this_week = (
            OptimizationServiceWeekly.maximize_weekly_sales(df_weekly, df_original)
        )
        optimized_sales_monthly, optimized_prices_monthly, prices_this_month = (
            OptimizationServiceMonthly.maximize_monthly_sales(df_monthly, df_original)
        )
        optimized_sales_quarterly, optimized_prices_quarterly, prices_this_quarter = (
            OptimizationServiceQuarterly.maximize_quarterly_sales(
                df_quarterly, df_original
            )
        )

        optimized_sales = [
            float(optimized_sales_weekly),
            float(optimized_sales_monthly),
            float(optimized_sales_quarterly),
        ]

        optimized_prices = [
            optimized_prices_weekly,
            optimized_prices_monthly,
            optimized_prices_quarterly,
        ]

        current_prices = [prices_this_week, prices_this_month, prices_this_quarter]

        price_list = {
            "weekly": [
                {
                    "product_id": product_id,
                    "current_price": float(current_prices[0].get(product_id)),
                    "optimized_price": float(optimized_prices[0].get(product_id)),
                }
                for product_id in current_prices[0]
            ],
            "monthly": [
                {
                    "product_id": product_id,
                    "current_price": float(current_prices[1].get(product_id)),
                    "optimized_price": float(optimized_prices[1].get(product_id)),
                }
                for product_id in current_prices[1]
            ],
            "quarterly": [
                {
                    "product_id": product_id,
                    "current_price": float(current_prices[2].get(product_id)),
                    "optimized_price": float(optimized_prices[2].get(product_id)),
                }
                for product_id in current_prices[2]
            ],
        }

        # print(price_list)
        # print(f"Optimized sales from service fn: {optimized_sales}")

        return (
            optimized_sales,
            price_list,
        )

    @staticmethod
    def get_original_dataset(file):
        try:
            file.seek(0)
            # Excel
            if file.filename.endswith((".xls", ".xlsx")):
                df = pd.read_excel(file)

            # CSV
            elif file.filename.endswith(".csv"):
                df = pd.read_csv(file, encoding="utf-8")

            df_original = df.copy()
            df_original["Order Date"] = pd.to_datetime(
                df_original["Order Date"], errors="coerce"
            )
            df_original.dropna(inplace=True)
            df_original.drop_duplicates(inplace=True)

        except Exception as e:
            print(f"Error while getting original dataset: {str(e)}")

        return df_original

    @staticmethod
    def save_to_db(dataset_file_id, price_list, optimized_sales, predicted_sales):
        """Saves the predicted sales to the database."""
        try:
            optimization = Optimization(dataset_file_id=dataset_file_id)
            db.session.add(optimization)
            db.session.commit()

            optimization_id = optimization.id

            timeframes = ["Next Week", "Next Month", "Next Quarter"]
            for timeframe, predicted, optimized in zip(
                timeframes, predicted_sales, optimized_sales
            ):
                optimized_sales_record = OptimizedSales(
                    optimization_id=optimization_id,
                    timeframe=timeframe,
                    predicted_sales=predicted,
                    optimized_sales=optimized,
                )
                db.session.add(optimized_sales_record)

            for i, (key, products) in enumerate(price_list.items()):
                timeframe = timeframes[i]
                for product in products:
                    optimized_prices_record = OptimizedPrices(
                        optimization_id=optimization_id,
                        timeframe=timeframe,
                        product_id=product["product_id"],
                        current_price=product["current_price"],
                        optimized_price=product["optimized_price"],
                    )
                    db.session.add(optimized_prices_record)

            db.session.commit()
        except Exception as e:
            print(f"Error: {str(e)}")

    @staticmethod
    def predict_sales(df_weekly, df_monthly, df_quarterly):
        """Returns the sales predicted for the next week, month, and quarter."""
        weekly_prediction = OptimizationServiceWeekly.predict_weekly_sales(df_weekly)
        monthly_prediction = OptimizationServiceMonthly.predict_monthly_sales(
            df_monthly
        )
        quarterly_prediction = OptimizationServiceQuarterly.predict_quarterly_sales(
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
        df_timeframes = OptimizationService.engineer_timeframes(df_original)
        # print(f"df_timeframes: {df_timeframes.head()}")

        # Engineer weekly, monthly, quarterly features
        df_weekly = OptimizationServiceWeekly.engineer_features(df_timeframes)
        df_monthly = OptimizationServiceMonthly.engineer_features(df_timeframes)
        df_quarterly = OptimizationServiceQuarterly.engineer_features(df_timeframes)

        # # Drop Product ID
        # df_weekly = df_weekly.drop(columns=["Product ID"])
        # df_monthly = df_monthly.drop(columns=["Product ID"])
        # df_quarterly = df_quarterly.drop(columns=["Product ID"])

        # Save the dataframes to the session
        session["prediction_df_weekly"] = df_weekly.copy().to_dict()
        session["prediction_df_monthly"] = df_monthly.copy().to_dict()
        session["prediction_df_quarterly"] = df_quarterly.copy().to_dict()

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
