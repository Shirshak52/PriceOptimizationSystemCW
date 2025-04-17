from datetime import datetime
import pytest
from app.models.Branch.model import Branch
from app.models.DatasetFile.model import DatasetFile
from tests.unit.models.test_branch_model import new_supermarket


@pytest.fixture
def new_branch(new_supermarket, db_session):

    branch = Branch(
        name="TestBranch",
        location="Kathmandu",
        phone_number="1234567890",
        email="testbranch@gmail.com",
        password="testpw",
        supermarket_id=new_supermarket.id,
    )

    db_session.add(branch)
    db_session.commit()

    yield branch

    db_session.delete(branch)
    db_session.commit()


def test_new_datasetfile(new_branch):
    """
    GIVEN a DatasetFile model
    WHEN a new DatasetFile is created
    THEN check the file_path, upload_datetime, branch_id fields are defined correctly.
    """
    dataset_file = DatasetFile(
        file_path="test_file_path",
        upload_datetime=datetime(2025, 4, 17, 12, 0, 0),
        branch_id=new_branch.id,
    )

    assert dataset_file.file_path == "test_file_path"
    assert dataset_file.upload_datetime == datetime(2025, 4, 17, 12, 0, 0)
    assert dataset_file.branch_id == new_branch.id
