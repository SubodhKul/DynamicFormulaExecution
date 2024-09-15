from flask import request
import pandas as pd
import re


def validate_input(func):
    """
    Validates inputs.
    """
    def wrapper(*args,**kwargs):
        request_body = request.get_json()
        try:
            if request_body.get("data"):
                data = request_body.get("data")
                if type(data) != list:
                    raise Exception("Data should be list")
                is_invalid = any([False if isinstance(item, dict) and item else True for item in data])
                if is_invalid:
                    raise Exception("Invalid data. Data should be non-empty list of dictionaries.")
            else:
                raise Exception("Empty field 'Data'.")

            if request_body.get("formulas",[]):
                formulas = request_body.get("formulas")
                if type(formulas) != list:
                    raise Exception("formula should be list.")
            else:
                raise Exception("Empty field 'formula'.")
            
            # create another function here..
            for formula in formulas:
                if formula.get("outputVar") and formula.get("expression") and formula.get("inputs"):
                    missing_values = invalid_formulas_dataframe(formula.get("inputs"),formula.get("expression"))
                    if missing_values:
                        raise Exception(f"Missing Values {missing_values}")
                else:
                    raise Exception(f"Invalid Formula {formula}. Formula should have outputVar,expression and inputs")
                
        except Exception as e:
            return {"Error": str(e)}
        return func(*args,**kwargs)
    return wrapper
    

def invalid_formulas_dataframe(inputs,expression):
    """
    validates formulas; checks that inputs have all the variables present in formulas.
    """
    data = request.get_json()
    df = pd.DataFrame(inputs)
    values_in_input = set(df['varName'].dropna())
    values_in_expression = set(extract_variables(expression))

    if not values_in_expression.issubset(values_in_input):
        missing_values = values_in_expression - values_in_input
        return missing_values
    else:
        return False

def extract_variables(expression):
     exp_df = pd.DataFrame(re.findall(r'\bw+\b', expression))
     return exp_df

    
    
