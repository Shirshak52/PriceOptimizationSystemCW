import pandas as pd
from app.services.prediction.prediction_services import PredictionService
from app.services.prediction.timeframe_specific_services.prediction_services_monthly import (
    PredictionServiceMonthly,
)
from app.services.prediction.timeframe_specific_services.prediction_services_quarterly import (
    PredictionServiceQuarterly,
)
from app.services.prediction.timeframe_specific_services.prediction_services_weekly import (
    PredictionServiceWeekly,
)


def test_engineer_timeframes(app):

    test_df = pd.DataFrame(
        {
            "Order Date": pd.to_datetime(
                [
                    "2023-01-01",
                    "2023-03-15",
                    "2023-06-30",
                    "2023-09-10",
                    "2023-12-25",
                    "2024-01-05",
                    "2024-04-20",
                    "2024-07-07",
                    "2024-10-15",
                    "2024-12-31",
                ]
            )
        }
    )

    test_result = PredictionService.engineer_timeframes(test_df)

    for col in ["Year-Week", "Year-Month", "Year-Quarter"]:
        assert col in test_result.columns

    assert test_result["Year-Week"][1] == "2023-11"
    assert test_result["Year-Month"][1] == "2023-03"
    assert str(test_result["Year-Quarter"][2]) == "2023Q2"


def test_rename_columns(app):
    test_df = pd.DataFrame(
        {
            "Price": [1000, 2000, 3000],
            "Sales": [5000, 4000, 5000],
            "Quantity": [4, 7, 9],
        }
    )

    test_result = PredictionServiceMonthly.rename_columns(test_df)

    for col in ["Price This Month", "Sales This Month", "Quantity This Month"]:
        assert col in test_result.columns

    assert test_result["Price This Month"].tolist() == [1000, 2000, 3000]
    assert test_result["Sales This Month"].tolist() == [5000, 4000, 5000]
    assert test_result["Quantity This Month"].tolist() == [4, 7, 9]


def test_engineer_price_change_percent(app):
    test_df = pd.DataFrame(
        {
            "Price This Week": [110, 200, 300, 400],
            "Price Last Week": [100, 190, 290, 500],
        }
    )

    test_result = PredictionServiceWeekly.engineer_price_change_percent(test_df)
    required_col = "Price Change (%)"
    assert required_col in test_result.columns
    assert test_result[required_col][0] == (110 - 100) / 100
    assert test_result[required_col][1] == (200 - 190) / 190
    assert test_result[required_col][2] == (300 - 290) / 290
    assert test_result[required_col][3] == (400 - 500) / 500


def test_engineer_sales_growth_rate(app):
    test_df = pd.DataFrame(
        {
            "Sales This Quarter": [1200, 1500, 2000],
            "Sales Last Quarter": [1000, 1500, 2500],
        }
    )

    test_result = PredictionServiceQuarterly.engineer_sales_growth_rate(test_df)
    required_col = "Sales Growth Rate"
    assert required_col in test_result.columns
    assert test_result[required_col][0] == (1200 - 1000) / 1000
    assert test_result[required_col][1] == (1500 - 1500) / 1500
    assert test_result[required_col][2] == (2000 - 2500) / 2500
