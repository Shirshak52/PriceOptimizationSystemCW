import pytest
from app.models.Cluster.model import Cluster
from app.models.Segmentation.model import Segmentation
from tests.unit.models.test_datasetfile_model import new_branch
from tests.unit.models.test_branch_model import new_supermarket
from tests.unit.models.test_segmentation_model import new_datasetfile


@pytest.fixture
def new_segmentation(new_datasetfile, db_session):

    segmentation = Segmentation(
        chosen_metric="Total Quantity",
        num_of_clusters=4,
        dataset_file_id=new_datasetfile.id,
    )

    db_session.add(segmentation)
    db_session.commit()

    yield segmentation

    db_session.delete(segmentation)
    db_session.commit()


def test_new_cluster(new_segmentation):
    """
    GIVEN a Cluster model
    WHEN a new Cluster is created
    THEN check the segmentation_id, cluster_id, cluster_count, metric_avg fields are defined correctly.
    """
    cluster = Cluster(
        segmentation_id=new_segmentation.id,
        cluster_id=1,
        cluster_count=500,
        metric_avg=700.55,
    )

    assert cluster.segmentation_id == new_segmentation.id
    assert cluster.cluster_id == 1
    assert cluster.cluster_count == 500
    assert cluster.metric_avg == 700.55
