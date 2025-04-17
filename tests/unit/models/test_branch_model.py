import pytest
from app.models.Branch.model import Branch
from app.models.Supermarket.model import Supermarket


@pytest.fixture
def new_supermarket(db_session):
    supermarket = Supermarket(
        name="TestSupermarket",
        phone_number="9876543210",
        email="testsupermarket@gmail.com",
        password="testsupermarketpw",
    )
    db_session.add(supermarket)
    db_session.commit()

    yield supermarket

    db_session.delete(supermarket)
    db_session.commit()


def test_new_branch(new_supermarket):
    """
    GIVEN a Branch model
    WHEN a new Branch is created
    THEN check the name, location, phone_number, email, password, supermarket_id fields are defined correctly.
    """
    branch = Branch(
        name="TestBranch",
        location="Kathmandu",
        phone_number="1234567890",
        email="testbranch@gmail.com",
        password="testpw",
        supermarket_id=new_supermarket.id,
    )

    assert branch.name == "TestBranch"
    assert branch.location == "Kathmandu"
    assert branch.phone_number == "1234567890"
    assert branch.email == "testbranch@gmail.com"
    assert branch.password == "testpw"
    assert branch.supermarket_id == new_supermarket.id
