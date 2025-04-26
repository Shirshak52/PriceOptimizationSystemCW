import pytest
import pandas as pd
from app.services.datasetfile_services import DatasetFileService


def test_validate_numcols():
    test_df = pd.DataFrame(
        {
            "Product ID": ["p001", "p002"],
            "Customer ID": ["c001", "c002"],
            "Order Date": [pd.to_datetime("2025-01-01"), pd.to_datetime("2025-02-02")],
            "Price": ["500", "600"],
            "Quantity": ["5", "6"],
            "Sales": ["2600", "3600"],
        }
    )

    test_result = DatasetFileService.validate_numcols(test_df)
    assert test_result is False


def test_has_missing_cols():
    test_df = pd.DataFrame(
        {
            "Product ID": ["p001", "p002"],
            "Customer ID": ["c001", "c002"],
            "Order Date": [pd.to_datetime("2025-01-01"), pd.to_datetime("2025-02-02")],
            "Price": [500, 600],
            "Quantity": [5, 6],
        }
    )

    test_result = DatasetFileService.has_missing_cols(test_df)
    assert test_result is True
