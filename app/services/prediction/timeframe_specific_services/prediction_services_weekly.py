import os
from flask import current_app
from joblib import load


class PredictionServiceWeekly:

    model_dir = current_app.config["MODELS_FOLDER_PREDICTION"]
    weekly_pred_model = load(os.path.join(model_dir, "xgboost_weekly.joblib"))

    weekly_X_cols = [
        "Price This Week",
        "Price Last Week",
        # "Sales This Week",
        # "Sales Last Week",
        # "Quantity This Week",
        # "Quantity Last Week",
        # "Price Change (%)",
        # "Sales Growth Rate",
        # "Stock to Sales Ratio",
        # "Momentum",
        "Rolling Average Sales",
        # "Price-to-Sales Ratio",
    ]

    @staticmethod
    def predict_weekly_sales(df_weekly):
        """Predicts the sales next week from the given dataset."""
        prediction_X_weekly = df_weekly[PredictionServiceWeekly.weekly_X_cols]

        weekly_predictions = PredictionServiceWeekly.weekly_pred_model.predict(
            prediction_X_weekly
        )

        total_weekly_prediction = weekly_predictions.sum()

        return total_weekly_prediction

    @staticmethod
    def engineer_features(df_timeframes):
        df_weekly = df_timeframes.copy().drop(columns=["Year-Month", "Year-Quarter"])

        # Aggregate data by Product ID and Year-Week
        df_weekly = (
            df_weekly.groupby(["Product ID", "Year-Week"])
            .agg({"Price": "mean", "Quantity": "sum", "Sales": "sum"})
            .reset_index()
        )

        # Sort data by Product ID and Year-Week for proper time sequence
        df_weekly = df_weekly.sort_values(by=["Product ID", "Year-Week"])

        # Rename Price, Sales, and Quantity columns to reflect that they are of the current week
        df_weekly = PredictionServiceWeekly.rename_columns(df_weekly)

        # Engineer lag features
        df_weekly = PredictionServiceWeekly.engineer_lag_features(df_weekly)

        # Calculate Price Change (%) (Change from Price Last Week to This Week)
        df_weekly = PredictionServiceWeekly.engineer_price_change_percent(df_weekly)

        # Calculate Sales Growth Rate (Growth from Sales Last Week to This Week)
        df_weekly = PredictionServiceWeekly.engineer_sales_growth_rate(df_weekly)

        # Calculate Stock to Sales Ratio (Quantity This Week / Sales This Week)
        df_weekly = PredictionServiceWeekly.engineer_stock_sales_ratio(df_weekly)

        # Calculate Momentum (Sales This Week - Sales Last Week)
        df_weekly = PredictionServiceWeekly.engineer_momentum(df_weekly)

        # Calculate Rolling Average Sales (Mean of Sales This Week and Last Week)
        df_weekly = PredictionServiceWeekly.engineer_rolling_average_sales(df_weekly)

        # Calculate Price-to-Sales Ratio (Price This Week / Sales This Week)
        df_weekly = PredictionServiceWeekly.engineer_price_sales_ratio(df_weekly)

        df_weekly["Timeframe"] = "Weekly"

        return df_weekly

    @staticmethod
    def rename_columns(df_weekly):
        df_renamed_cols = df_weekly.copy()

        df_renamed_cols.rename(
            columns={
                "Price": "Price This Week",
                "Sales": "Sales This Week",
                "Quantity": "Quantity This Week",
            },
            inplace=True,
        )

        return df_renamed_cols

    @staticmethod
    def engineer_lag_features(df_weekly):
        """Engineers lag features of quantity, sales, and price from the weekly dataset."""
        df_lag_features = df_weekly.copy()

        # Calculate quantity last week
        df_lag_features["Quantity Last Week"] = df_lag_features.groupby("Product ID")[
            "Quantity This Week"
        ].shift(1)
        df_lag_features = df_lag_features.dropna(subset=["Quantity Last Week"])

        # Calculate sales last week
        df_lag_features["Sales Last Week"] = df_lag_features.groupby("Product ID")[
            "Sales This Week"
        ].shift(1)
        df_lag_features = df_lag_features.dropna(subset=["Sales Last Week"])

        # Calculate price last week
        df_lag_features["Price Last Week"] = df_lag_features.groupby("Product ID")[
            "Price This Week"
        ].shift(1)
        df_lag_features = df_lag_features.dropna(subset=["Price Last Week"])

        return df_lag_features

    @staticmethod
    def engineer_price_change_percent(df_weekly):
        df_price_change_percent = df_weekly.copy()

        df_price_change_percent["Price Change (%)"] = (
            df_price_change_percent["Price This Week"]
            - df_price_change_percent["Price Last Week"]
        ) / df_price_change_percent["Price Last Week"]
        df_price_change_percent = df_price_change_percent.dropna(
            subset=["Price Change (%)"]
        )

        return df_price_change_percent

    @staticmethod
    def engineer_sales_growth_rate(df_weekly):
        df_sales_growth_rate = df_weekly.copy()

        df_sales_growth_rate["Sales Growth Rate"] = (
            df_sales_growth_rate["Sales This Week"]
            - df_sales_growth_rate["Sales Last Week"]
        ) / df_sales_growth_rate["Sales Last Week"]

        df_sales_growth_rate = df_sales_growth_rate.dropna(subset=["Sales Growth Rate"])

        return df_sales_growth_rate

    @staticmethod
    def engineer_stock_sales_ratio(df_weekly):
        df_stock_sales_ratio = df_weekly.copy()

        df_stock_sales_ratio["Stock to Sales Ratio"] = df_stock_sales_ratio[
            "Quantity This Week"
        ] / (df_stock_sales_ratio["Sales This Week"] + 1)

        df_stock_sales_ratio = df_stock_sales_ratio.dropna(
            subset=["Stock to Sales Ratio"]
        )

        return df_stock_sales_ratio

    @staticmethod
    def engineer_momentum(df_weekly):
        df_weekly_momentum = df_weekly.copy()

        df_weekly_momentum["Momentum"] = (
            df_weekly_momentum["Sales This Week"]
            - df_weekly_momentum["Sales Last Week"]
        )

        df_weekly_momentum = df_weekly_momentum.dropna(subset=["Momentum"])

        return df_weekly_momentum

    @staticmethod
    def engineer_rolling_average_sales(df_weekly):
        df_weekly_rolling_average_sales = df_weekly.copy()

        df_weekly_rolling_average_sales["Rolling Average Sales"] = (
            df_weekly_rolling_average_sales[
                ["Sales Last Week", "Sales This Week"]
            ].mean(axis=1)
        )

        df_weekly_rolling_average_sales = df_weekly_rolling_average_sales.dropna(
            subset=["Rolling Average Sales"]
        )

        return df_weekly_rolling_average_sales

    @staticmethod
    def engineer_price_sales_ratio(df_weekly):
        df_weekly_price_sales_ratio = df_weekly.copy()

        df_weekly_price_sales_ratio["Price-to-Sales Ratio"] = (
            df_weekly_price_sales_ratio["Price This Week"]
            / (df_weekly_price_sales_ratio["Sales This Week"] + 1)
        )

        df_weekly_price_sales_ratio = df_weekly_price_sales_ratio.dropna(
            subset=["Price-to-Sales Ratio"]
        )

        return df_weekly_price_sales_ratio
