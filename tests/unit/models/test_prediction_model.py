from datetime import datetime
import pytest
from app.models.DatasetFile.model import DatasetFile
from app.models.Prediction.model import Prediction
from tests.unit.models.test_datasetfile_model import new_branch
from tests.unit.models.test_branch_model import new_supermarket


@pytest.fixture
def new_datasetfile(new_branch, db_session):

    dataset_file = DatasetFile(
        file_path="test_file_path",
        upload_datetime=datetime(2025, 4, 17, 12, 0, 0),
        branch_id=new_branch.id,
    )

    db_session.add(dataset_file)
    db_session.commit()

    yield dataset_file

    db_session.delete(dataset_file)
    db_session.commit()


def test_new_prediction(new_datasetfile):
    """
    GIVEN a Prediction model
    WHEN a new Prediction is created
    THEN check the sales_next_week, sales_next_month, sales_next_quarter, dataset_file_id fields are defined correctly.
    """
    prediction = Prediction(
        sales_next_week=500.00,
        sales_next_month=600.00,
        sales_next_quarter=700.00,
        dataset_file_id=new_datasetfile.id,
    )

    assert prediction.sales_next_week == 500.00
    assert prediction.sales_next_month == 600.00
    assert prediction.sales_next_quarter == 700.00
    assert prediction.dataset_file_id == new_datasetfile.id
