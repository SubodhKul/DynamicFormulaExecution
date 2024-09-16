from flask import request
import pandas as pd
import json



def apply_formulas(df,formulas):
    """
    Apply formulas to the input dataframe.
    """
    for formula in formulas:
        df = apply_formula_to_df(df,formula)
    return df

def apply_formula_to_df(df,formula):
    try:
        output_var = formula.get("outputVar")
        expression = formula.get("expression")
        df[output_var] = df.eval(expression)
    except Exception as e:
        raise Exception("Exception occured while evaluating expression",e)

    return df

def data_to_dataframe():
    """
    Converts input Data to Dataframe.
    Creates Dataframe that is ready to apply formulas.
    """
    
    data_json = request.get_json()
    df = pd.DataFrame(data_json["data"])

    inputs_df = pd.DataFrame(data_json["formulas"][0].get("inputs"))
    type_dict = dict(zip(inputs_df['varName'],inputs_df['varType']))

    transformed_df = parse_input(df,type_dict)
    return transformed_df

def format_output(result_df):
    input_df = pd.DataFrame(request.get_json().get("data"))
    input_cols = set(input_df.columns)
    result_cols = set(result_df.columns)

    results = list(result_cols - input_cols)
    results_df = result_df[results]
    results_dict = {col: results_df[col].tolist() for col in results}
    results_dict["status"] = "success"
    results_dict["message"] = "The formulas were executed successfully." if len(results)  < 2 else "The formulas were executed successfully with variable-based chaining."
    # results_json = json.dumps({"results":results_dict},indent = 2)
    
    return results_dict



def parse_input(df,type_dict):
    """
    Converts inputs used in expression to numeric.
    """
    for col, dtype in type_dict.items():
        if col in df.columns:
            if dtype == "number":
                df[col] = pd.to_numeric(df[col], errors='coerce')
            elif dtype == "currency":
                df[col] = df[col].str.replace(r'[^\d.]', '', regex=True).astype(float)
            elif dtype == "percentage":
                df[col] = df[col].str.rstrip('%').astype(float)
            elif dtype == "datetime":
                df[col] = pd.to_datetime(df[col], errors = 'coerce')
            elif dtype == "boolean":
                def str_to_bool(val):
                    if isinstance(val, str):
                        if val.lower() == 'false':
                            return False
                        elif val.lower() == 'true':
                            return True
                    return val 
                df[col] = df[col].apply(str_to_bool)


    return df
