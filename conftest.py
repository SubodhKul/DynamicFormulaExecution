import pytest
import pandas as pd

@pytest.fixture
def test_dataframe():
    """Fixture to create a DataFrame with different data types."""
    data = {
        'number': [1, 2, 3],  
        'boolean': ['True', 'False', 'True'],  
        'currency': ['10$ ', '20 USD', '$30'],  
        'percentage': ['10%', '20%', '30%']
    }
    return pd.DataFrame(data)

@pytest.fixture
def config_dict():
    """Fixture to map column names to expected data types."""
    return {
            
        'number': 'number',
        'boolean': 'boolean', 
        'currency': 'currency',
        'percentage': 'percentage'
    }

@pytest.fixture
def expected_dataframe():
    """Fixture to create the expected DataFrame after processing."""
    data = {
        'number': [1, 2, 3], 
        'boolean': [True, False, True],  
        'currency': [10.0, 20.0, 30.0],  
        'percentage': [10.0, 20.0, 30.0]
    }
    return pd.DataFrame(data)
