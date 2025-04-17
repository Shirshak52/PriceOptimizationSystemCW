import pytest
from app.models.Branch.model import Branch
from app.models.Supermarket.model import Supermarket


def test_new_supermarket(db_session):
    """
    GIVEN a Supermarket model
    WHEN a new Supermarket is created
    THEN check the name, phone_number, email, password fields are defined correctly.
    """
    supermarket = Supermarket(
        name="TestSupermarket",
        phone_number="9876543210",
        email="testsupermarket@gmail.com",
        password="testsupermarketpw",
    )

    assert supermarket.name == "TestSupermarket"
    assert supermarket.phone_number == "9876543210"
    assert supermarket.email == "testsupermarket@gmail.com"
    assert supermarket.password == "testsupermarketpw"
