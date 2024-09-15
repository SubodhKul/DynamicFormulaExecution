import pytest
import json

@pytest.fixture
def simple_addition_formula():
    with open('./Data/simple_addition.json','r') as _f:
        data = json.load(_f)

    return data["formulas"][0]

@pytest.fixture
def formula_chaining():
    with open('./Data/formula_chaining.json','r') as _f:
        data = json.load(_f)

    return data["formulas"]