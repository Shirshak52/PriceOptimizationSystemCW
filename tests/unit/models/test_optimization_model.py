from datetime import datetime
import pytest
from app.models.DatasetFile.model import DatasetFile
from app.models.Optimization.model import Optimization
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


def test_new_optimization(new_datasetfile):
    """
    GIVEN an Optimization model
    WHEN a new Optimization is created
    THEN check the dataset_file_id field is defined correctly.
    """
    optimization = Optimization(
        dataset_file_id=new_datasetfile.id,
    )

    assert optimization.dataset_file_id == new_datasetfile.id
