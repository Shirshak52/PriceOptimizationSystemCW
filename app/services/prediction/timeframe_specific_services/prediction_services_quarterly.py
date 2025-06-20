import os
from flask import current_app
from joblib import load


class PredictionServiceQuarterly:

    @classmethod
    def load_model(cls):
        model_dir = current_app.config["MODELS_FOLDER_PREDICTION"]
        quarterly_pred_model = load(os.path.join(model_dir, "xgboost_quarterly.joblib"))
        return quarterly_pred_model

    quarterly_X_cols = [
        "Price This Quarter",
        # "Price Last Quarter",
        # "Sales This Quarter",
        # "Sales Last Quarter",
        # "Quantity This Quarter",
        # "Quantity Last Quarter",
        "Price Change (%)",
        # "Sales Growth Rate",
        "Stock to Sales Ratio",
        # "Momentum",
        "Rolling Average Sales",
        # "Price-to-Sales Ratio",
    ]

    @staticmethod
    def predict_quarterly_sales(df_quarterly):
        """Predicts the sales next quarter from the given dataset."""
        prediction_X_quarterly = df_quarterly[
            PredictionServiceQuarterly.quarterly_X_cols
        ]

        quarterly_predictions = PredictionServiceQuarterly.load_model().predict(
            prediction_X_quarterly
        )

        df_quarterly_predictions = df_quarterly.copy()
        df_quarterly_predictions["Predictions"] = quarterly_predictions

        # Sort by Product ID (ascending) and Year-Quarter (descending)
        df_quarterly_predictions = df_quarterly_predictions.sort_values(
            by=["Product ID", "Year-Quarter"], ascending=[True, False]
        )

        latest_quarterly_predictions = df_quarterly_predictions.groupby("Product ID")[
            "Predictions"
        ].first()

        total_quarterly_prediction = latest_quarterly_predictions.sum()

        return total_quarterly_prediction

    @staticmethod
    def engineer_features(df_timeframes):
        df_quarterly = df_timeframes.copy().drop(columns=["Year-Month", "Year-Week"])

        # Aggregate data by Product ID and Year-Quarter
        df_quarterly = (
            df_quarterly.groupby(["Product ID", "Year-Quarter"])
            .agg({"Price": "mean", "Quantity": "sum", "Sales": "sum"})
            .reset_index()
        )

        # Sort data by Product ID and Year-Week for proper time sequence
        df_quarterly = df_quarterly.sort_values(by=["Product ID", "Year-Quarter"])

        # Rename Price, Sales, and Quantity columns to reflect that they are of the current week
        df_quarterly = PredictionServiceQuarterly.rename_columns(df_quarterly)

        # Engineer lag features
        df_quarterly = PredictionServiceQuarterly.engineer_lag_features(df_quarterly)

        # Calculate Price Change (%) (Change from Price Last Week to This Week)
        df_quarterly = PredictionServiceQuarterly.engineer_price_change_percent(
            df_quarterly
        )

        # Calculate Sales Growth Rate (Growth from Sales Last Week to This Week)
        df_quarterly = PredictionServiceQuarterly.engineer_sales_growth_rate(
            df_quarterly
        )

        # Calculate Stock to Sales Ratio (Quantity This Week / Sales This Week)
        df_quarterly = PredictionServiceQuarterly.engineer_stock_sales_ratio(
            df_quarterly
        )

        # Calculate Momentum (Sales This Week - Sales Last Week)
        df_quarterly = PredictionServiceQuarterly.engineer_momentum(df_quarterly)

        # Calculate Rolling Average Sales (Mean of Sales This Week and Last Week)
        df_quarterly = PredictionServiceQuarterly.engineer_rolling_average_sales(
            df_quarterly
        )

        # Calculate Price-to-Sales Ratio (Price This Week / Sales This Week)
        df_quarterly = PredictionServiceQuarterly.engineer_price_sales_ratio(
            df_quarterly
        )

        df_quarterly["Timeframe"] = "Quarterly"

        return df_quarterly

    @staticmethod
    def rename_columns(df_quarterly):
        df_renamed_cols = df_quarterly.copy()

        df_renamed_cols.rename(
            columns={
                "Price": "Price This Quarter",
                "Sales": "Sales This Quarter",
                "Quantity": "Quantity This Quarter",
            },
            inplace=True,
        )

        return df_renamed_cols

    @staticmethod
    def engineer_lag_features(df_quarterly):
        """Engineers lag features of quantity, sales, and price from the quarterly dataset."""
        df_lag_features = df_quarterly.copy()

        # Calculate quantity last quarter
        df_lag_features["Quantity Last Quarter"] = df_lag_features.groupby(
            "Product ID"
        )["Quantity This Quarter"].shift(1)
        df_lag_features = df_lag_features.dropna(subset=["Quantity Last Quarter"])

        # Calculate sales last quarter
        df_lag_features["Sales Last Quarter"] = df_lag_features.groupby("Product ID")[
            "Sales This Quarter"
        ].shift(1)
        df_lag_features = df_lag_features.dropna(subset=["Sales Last Quarter"])

        # Calculate price last quarter
        df_lag_features["Price Last Quarter"] = df_lag_features.groupby("Product ID")[
            "Price This Quarter"
        ].shift(1)
        df_lag_features = df_lag_features.dropna(subset=["Price Last Quarter"])

        return df_lag_features

    @staticmethod
    def engineer_price_change_percent(df_quarterly):
        df_price_change_percent = df_quarterly.copy()

        df_price_change_percent["Price Change (%)"] = (
            df_price_change_percent["Price This Quarter"]
            - df_price_change_percent["Price Last Quarter"]
        ) / df_price_change_percent["Price Last Quarter"]
        df_price_change_percent = df_price_change_percent.dropna(
            subset=["Price Change (%)"]
        )

        return df_price_change_percent

    @staticmethod
    def engineer_sales_growth_rate(df_quarterly):
        df_sales_growth_rate = df_quarterly.copy()

        df_sales_growth_rate["Sales Growth Rate"] = (
            df_sales_growth_rate["Sales This Quarter"]
            - df_sales_growth_rate["Sales Last Quarter"]
        ) / df_sales_growth_rate["Sales Last Quarter"]

        df_sales_growth_rate = df_sales_growth_rate.dropna(subset=["Sales Growth Rate"])

        return df_sales_growth_rate

    @staticmethod
    def engineer_stock_sales_ratio(df_quarterly):
        df_stock_sales_ratio = df_quarterly.copy()

        df_stock_sales_ratio["Stock to Sales Ratio"] = df_stock_sales_ratio[
            "Quantity This Quarter"
        ] / (df_stock_sales_ratio["Sales This Quarter"] + 1)

        df_stock_sales_ratio = df_stock_sales_ratio.dropna(
            subset=["Stock to Sales Ratio"]
        )

        return df_stock_sales_ratio

    @staticmethod
    def engineer_momentum(df_quarterly):
        df_quarterly_momentum = df_quarterly.copy()

        df_quarterly_momentum["Momentum"] = (
            df_quarterly_momentum["Sales This Quarter"]
            - df_quarterly_momentum["Sales Last Quarter"]
        )

        df_quarterly_momentum = df_quarterly_momentum.dropna(subset=["Momentum"])

        return df_quarterly_momentum

    @staticmethod
    def engineer_rolling_average_sales(df_quarterly):
        df_quarterly_rolling_average_sales = df_quarterly.copy()

        df_quarterly_rolling_average_sales["Rolling Average Sales"] = (
            df_quarterly_rolling_average_sales[
                ["Sales Last Quarter", "Sales This Quarter"]
            ].mean(axis=1)
        )

        df_quarterly_rolling_average_sales = df_quarterly_rolling_average_sales.dropna(
            subset=["Rolling Average Sales"]
        )

        return df_quarterly_rolling_average_sales

    @staticmethod
    def engineer_price_sales_ratio(df_quarterly):
        df_quarterly_price_sales_ratio = df_quarterly.copy()

        df_quarterly_price_sales_ratio["Price-to-Sales Ratio"] = (
            df_quarterly_price_sales_ratio["Price This Quarter"]
            / (df_quarterly_price_sales_ratio["Sales This Quarter"] + 1)
        )

        df_quarterly_price_sales_ratio = df_quarterly_price_sales_ratio.dropna(
            subset=["Price-to-Sales Ratio"]
        )

        return df_quarterly_price_sales_ratio
