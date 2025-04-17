import pytest
from app.models.Optimization.model import Optimization
from app.models.OptimizedSales.model import OptimizedSales
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


def test_new_optimizedsales(new_optimization):
    """
    GIVEN an OptimizedSales model
    WHEN a new OptimizedSales is created
    THEN check the optimization_id, timeframe, predicted_sales, optimized_sales fields are defined correctly.
    """
    optimized_sales = OptimizedSales(
        optimization_id=new_optimization.id,
        timeframe="Next Month",
        predicted_sales=500.00,
        optimized_sales=700.00,
    )

    assert optimized_sales.optimization_id == new_optimization.id
    assert optimized_sales.timeframe == "Next Month"
    assert optimized_sales.predicted_sales == 500.00
    assert optimized_sales.optimized_sales == 700.00
