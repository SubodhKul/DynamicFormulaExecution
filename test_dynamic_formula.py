import pytest
from lib.utils import parse_input
from lib.validations import extract_variables, invalid_formulas_dataframe
import pandas as pd
import re

@pytest.mark.parse_input_function
def test_parse_input(test_dataframe,config_dict,expected_dataframe):
    parsed = parse_input(test_dataframe,config_dict)
    pd.testing.assert_frame_equal(parsed,expected_dataframe)


@pytest.mark.extract_variables_from_expression
@pytest.mark.parametrize(
    "expression,expected_set",
    [
        ("fieldA + 10",{'fieldA'}),
        ("((unitPrice * quantity) - (unitPrice * quantity * (discount / 100)))",{'unitPrice','quantity','discount'}),
        ("sumResult * 2 + fieldA",{'sumResult','fieldA'})
    ]
)
def test_extract_variables(expression,expected_set):
    res = set(extract_variables(expression)[0])
    assert res == expected_set

@pytest.mark.validate_expression
@pytest.mark.parametrize(
    "inputs,expression,expected_output",
    [
        (({"varName": "sumResult", "varType": "number"}, {"varName": "fieldA", "varType": "number"}),
         "sumResult * 2 + fieldA",False),
    ]
)
def test_invalid_formulas_dataframe(inputs,expression,expected_output):
    res = invalid_formulas_dataframe(inputs,expression)
    assert expected_output == res
