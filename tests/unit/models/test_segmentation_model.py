from datetime import datetime
import pytest
from app.models.DatasetFile.model import DatasetFile
from app.models.Segmentation.model import Segmentation
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


def test_new_segmentation(new_datasetfile):
    """
    GIVEN a Segmentation model
    WHEN a new Segmentation is created
    THEN check the chosen_metric, num_of_clusters, dataset_file_id fields are defined correctly.
    """
    segmentation = Segmentation(
        chosen_metric="Total Quantity",
        num_of_clusters=4,
        dataset_file_id=new_datasetfile.id,
    )

    assert segmentation.chosen_metric == "Total Quantity"
    assert segmentation.num_of_clusters == 4
    assert segmentation.dataset_file_id == new_datasetfile.id
