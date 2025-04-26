import pandas as pd
from app.services.segmentation.segmentation_services import SegmentationService


def test_scale_dataset():
    test_df = pd.DataFrame(
        {
            "Product ID": ["p001", "p002"],
            "Customer ID": ["c001", "c002"],
            "Order Date": [pd.to_datetime("2025-01-01"), pd.to_datetime("2025-02-02")],
            "Price": [500, 600],
            "Quantity": [5, 6],
            "Sales": [100, 200],
        }
    )

    test_result = SegmentationService.scale_dataset(test_df)
    numcols = ["Price", "Quantity", "Sales"]
    for col in numcols:
        assert test_result[col].min() >= 0
        assert test_result[col].max() <= 1


def test_get_cluster_profiles():
    test_df = pd.DataFrame(
        {
            "Cluster": [0, 1, 0, 0, 1],
            "Total Sales": [100, 400, 200, 150, 420],
        }
    )

    test_cluster_counts, test_metric_averages = (
        SegmentationService.get_cluster_profiles(test_df, "Total Sales")
    )

    assert test_cluster_counts == {0: 3, 1: 2}
    assert test_metric_averages == {0: 150.0, 1: 410.0}
