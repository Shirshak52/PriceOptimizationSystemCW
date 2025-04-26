import pandas as pd
import pytest

from app.services.optimization.timeframe_specific_services.optimization_services_monthly import (
    OptimizationServiceMonthly,
)
from app.services.optimization.timeframe_specific_services.optimization_services_weekly import (
    OptimizationServiceWeekly,
)


def test_engineer_stock_sales_ratio(app):
    test_df = pd.DataFrame(
        {
            "Quantity This Week": [8, 10, 12],
            "Sales This Week": [1000, 1500, 2500],
        }
    )

    test_result = OptimizationServiceWeekly.engineer_stock_sales_ratio(test_df)
    required_col = "Stock to Sales Ratio"
    assert required_col in test_result.columns
    assert test_result[required_col][0] == pytest.approx(8 / 1000, rel=1e-3)
    assert test_result[required_col][1] == pytest.approx(10 / 1500, rel=1e-3)
    assert test_result[required_col][2] == pytest.approx(12 / 2500, rel=1e-3)


def test_engineer_momentum(app):
    test_df = pd.DataFrame(
        {
            "Sales This Month": [200, 300, 500],
            "Sales Last Month": [180, 250, 400],
        }
    )

    test_result = OptimizationServiceMonthly.engineer_momentum(test_df)
    required_col = "Momentum"
    assert required_col in test_result.columns
    assert test_result[required_col][0] == 200 - 180
    assert test_result[required_col][1] == 300 - 250
    assert test_result[required_col][2] == 500 - 400
