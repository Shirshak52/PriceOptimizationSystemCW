import pytest
from app.models.Optimization.model import Optimization
from app.models.OptimizedPrices.model import OptimizedPrices
from tests.unit.models.test_optimization_model import new_datasetfile
from tests.unit.models.test_datasetfile_model import new_branch
from tests.unit.models.test_branch_model import new_supermarket


@pytest.fixture
def new_optimization(new_datasetfile, db_session):

    optimization = Optimization(
        dataset_file_id=new_datasetfile.id,
    )

    db_session.add(optimization)
    db_session.commit()

    yield optimization

    db_session.delete(optimization)
    db_session.commit()


def test_new_optimizedprices(new_optimization):
    """
    GIVEN an OptimizedPrices model
    WHEN a new OptimizedPrices is created
    THEN check the optimization_id, timeframe, product_id, current_price, optimized_price fields are defined correctly.
    """
    optimized_prices = OptimizedPrices(
        optimization_id=new_optimization.id,
        timeframe="Next Month",
        product_id="P-001",
        current_price=50.00,
        optimized_price=70.00,
    )

    assert optimized_prices.optimization_id == new_optimization.id
    assert optimized_prices.timeframe == "Next Month"
    assert optimized_prices.product_id == "P-001"
    assert optimized_prices.current_price == 50.00
    assert optimized_prices.optimized_price == 70.00
