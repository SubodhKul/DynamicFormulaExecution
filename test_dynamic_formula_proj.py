import pytest
from lib.utils import apply_all_formulas, apply_formula



@pytest.mark.simple_addition
@pytest.mark.parametrize(
        "Data,Output",
        [
            ({"id": 1,"fieldA": 10},20),
            ({"id": 2,"fieldA": 20},30),
            ({"id": 2,"fieldA": -10},0),
            ({"id": 2,"fieldA": 0},10),
            ({"id": 2,"fieldA": 1},11)
        ]
)
def test_apply_formula(simple_addition_formula,Data,Output):
    result = apply_formula(Data,simple_addition_formula)
    assert result["result"] == Output


@pytest.mark.formula_chaining
@pytest.mark.parametrize(
    "data,output",
    [
        ({'id': 1, 'fieldA': 10, 'fieldB': 2},{'id': 1, 'fieldA': 10, 'fieldB': 2,'sumResult':12,'finalResult':34}),
        ({'id': 2, 'fieldA': 20, 'fieldB': 3},{'id': 2, 'fieldA': 20, 'fieldB': 3,'sumResult':23,'finalResult':66})
    ]
)
def test_formula_chaining(formula_chaining,data,output):
    result = apply_all_formulas(data,formula_chaining)

    assert result == output
