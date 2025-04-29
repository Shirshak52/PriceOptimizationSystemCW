import os
from flask import current_app
from joblib import load


class PredictionServiceMonthly:

    @classmethod
    def load_model(cls):
        model_dir = current_app.config["MODELS_FOLDER_PREDICTION"]
        monthly_pred_model = load(os.path.join(model_dir, "xgboost_monthly.joblib"))
        return monthly_pred_model

    monthly_X_cols = [
        "Price This Month",
        # "Price Last Month",
        # "Sales This Month",
        # "Sales Last Month",
        # "Quantity This Month",
        # "Quantity Last Month",
        "Price Change (%)",
        # "Sales Growth Rate",
        "Stock to Sales Ratio",
        # "Momentum",
        "Rolling Average Sales",
        # "Price-to-Sales Ratio",
    ]

    @staticmethod
    def predict_monthly_sales(df_monthly):
        """Predicts the sales next month from the given dataset."""
        prediction_X_monthly = df_monthly[PredictionServiceMonthly.monthly_X_cols]

        monthly_predictions = PredictionServiceMonthly.load_model().predict(
            prediction_X_monthly
        )

        df_monthly_predictions = df_monthly.copy()
        df_monthly_predictions["Predictions"] = monthly_predictions

        # Sort by Product ID (ascending) and Year-Month (descending)
        df_monthly_predictions = df_monthly_predictions.sort_values(
            by=["Product ID", "Year-Month"], ascending=[True, False]
        )

        latest_monthly_predictions = df_monthly_predictions.groupby("Product ID")[
            "Predictions"
        ].first()

        total_monthly_prediction = latest_monthly_predictions.sum()

        return total_monthly_prediction

    @staticmethod
    def engineer_features(df_timeframes):

        df_monthly = df_timeframes.copy().drop(columns=["Year-Week", "Year-Quarter"])

        # Aggregate data by Product ID and Year-Month
        df_monthly = (
            df_monthly.groupby(["Product ID", "Year-Month"])
            .agg({"Price": "mean", "Quantity": "sum", "Sales": "sum"})
            .reset_index()
        )

        # Sort data by Product ID and Year-Month for proper time sequence
        df_monthly = df_monthly.sort_values(by=["Product ID", "Year-Month"])

        # Rename Price, Sales, and Quantity columns to reflect that they are of the current month
        df_monthly = PredictionServiceMonthly.rename_columns(df_monthly)

        # Engineer lag features
        df_monthly = PredictionServiceMonthly.engineer_lag_features(df_monthly)

        # Calculate Price Change (%) (Change from Price Last Month to This Month)
        df_monthly = PredictionServiceMonthly.engineer_price_change_percent(df_monthly)

        # Calculate Sales Growth Rate (Growth from Sales Last Month to This Month)
        df_monthly = PredictionServiceMonthly.engineer_sales_growth_rate(df_monthly)

        # Calculate Stock to Sales Ratio (Quantity This Month / Sales This Month)
        df_monthly = PredictionServiceMonthly.engineer_stock_sales_ratio(df_monthly)

        # Calculate Momentum (Sales This Month - Sales Last Month)
        df_monthly = PredictionServiceMonthly.engineer_momentum(df_monthly)

        # Calculate Rolling Average Sales (Mean of Sales This Month and Last Month)
        df_monthly = PredictionServiceMonthly.engineer_rolling_average_sales(df_monthly)

        # Calculate Price-to-Sales Ratio (Price This Month / Sales This Month)
        df_monthly = PredictionServiceMonthly.engineer_price_sales_ratio(df_monthly)

        df_monthly["Timeframe"] = "Weekly"

        return df_monthly

    @staticmethod
    def rename_columns(df_monthly):
        df_renamed_cols = df_monthly.copy()

        df_renamed_cols.rename(
            columns={
                "Price": "Price This Month",
                "Sales": "Sales This Month",
                "Quantity": "Quantity This Month",
            },
            inplace=True,
        )

        return df_renamed_cols

    @staticmethod
    def engineer_lag_features(df_monthly):
        """Engineers lag features of quantity, sales, and price from the monthly dataset."""
        df_lag_features = df_monthly.copy()

        # Calculate quantity last month
        df_lag_features["Quantity Last Month"] = df_lag_features.groupby("Product ID")[
            "Quantity This Month"
        ].shift(1)
        df_lag_features = df_lag_features.dropna(subset=["Quantity Last Month"])

        # Calculate sales last month
        df_lag_features["Sales Last Month"] = df_lag_features.groupby("Product ID")[
            "Sales This Month"
        ].shift(1)
        df_lag_features = df_lag_features.dropna(subset=["Sales Last Month"])

        # Calculate price last month
        df_lag_features["Price Last Month"] = df_lag_features.groupby("Product ID")[
            "Price This Month"
        ].shift(1)
        df_lag_features = df_lag_features.dropna(subset=["Price Last Month"])

        return df_lag_features

    @staticmethod
    def engineer_price_change_percent(df_monthly):
        df_price_change_percent = df_monthly.copy()

        df_price_change_percent["Price Change (%)"] = (
            df_price_change_percent["Price This Month"]
            - df_price_change_percent["Price Last Month"]
        ) / df_price_change_percent["Price Last Month"]
        df_price_change_percent = df_price_change_percent.dropna(
            subset=["Price Change (%)"]
        )

        return df_price_change_percent

    @staticmethod
    def engineer_sales_growth_rate(df_monthly):
        df_sales_growth_rate = df_monthly.copy()

        df_sales_growth_rate["Sales Growth Rate"] = (
            df_sales_growth_rate["Sales This Month"]
            - df_sales_growth_rate["Sales Last Month"]
        ) / df_sales_growth_rate["Sales Last Month"]

        df_sales_growth_rate = df_sales_growth_rate.dropna(subset=["Sales Growth Rate"])

        return df_sales_growth_rate

    @staticmethod
    def engineer_stock_sales_ratio(df_monthly):
        df_stock_sales_ratio = df_monthly.copy()

        df_stock_sales_ratio["Stock to Sales Ratio"] = df_stock_sales_ratio[
            "Quantity This Month"
        ] / (df_stock_sales_ratio["Sales This Month"] + 1)

        df_stock_sales_ratio = df_stock_sales_ratio.dropna(
            subset=["Stock to Sales Ratio"]
        )

        return df_stock_sales_ratio

    @staticmethod
    def engineer_momentum(df_monthly):
        df_monthly_momentum = df_monthly.copy()

        df_monthly_momentum["Momentum"] = (
            df_monthly_momentum["Sales This Month"]
            - df_monthly_momentum["Sales Last Month"]
        )

        df_monthly_momentum = df_monthly_momentum.dropna(subset=["Momentum"])

        return df_monthly_momentum

    @staticmethod
    def engineer_rolling_average_sales(df_monthly):
        df_monthly_rolling_average_sales = df_monthly.copy()

        df_monthly_rolling_average_sales["Rolling Average Sales"] = (
            df_monthly_rolling_average_sales[
                ["Sales Last Month", "Sales This Month"]
            ].mean(axis=1)
        )

        df_monthly_rolling_average_sales = df_monthly_rolling_average_sales.dropna(
            subset=["Rolling Average Sales"]
        )

        return df_monthly_rolling_average_sales

    @staticmethod
    def engineer_price_sales_ratio(df_monthly):
        df_monthly_price_sales_ratio = df_monthly.copy()

        df_monthly_price_sales_ratio["Price-to-Sales Ratio"] = (
            df_monthly_price_sales_ratio["Price This Month"]
            / (df_monthly_price_sales_ratio["Sales This Month"] + 1)
        )

        df_monthly_price_sales_ratio = df_monthly_price_sales_ratio.dropna(
            subset=["Price-to-Sales Ratio"]
        )

        return df_monthly_price_sales_ratio
