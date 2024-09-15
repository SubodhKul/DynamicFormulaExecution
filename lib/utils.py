from flask import request

#read json

def parse_var(value,varType):
    if varType == "number":
        return float(value)
    if varType == "currency":
        return float(value.split(" ")[0])
    if varType == "percentage":
        return float(value[:-1])
    
    return 

def apply_formula(data_unit,formula):
    """
    Apply a single formula to single unit of data and return the outputVar/new variable

    """

    output_var = formula.get("outputVar") # string result of formula applied to single data unit.
    expression = formula.get("expression") # string expr should be passed to eval
    inputs = formula.get('inputs') # list of vars required in expr

    var_dict = data_unit.copy()
    
    for input in inputs:
        key = input.get("varName")
        value = parse_var(str(var_dict[key]),input.get("varType"))
        var_dict[key] = value

    #apply formula to single data unit
    try:
        result = eval(expression,var_dict) # need to use dataframe..
        data_unit[output_var] = result
    except Exception as e:
        raise Exception("Exception occured: ",e)


    return data_unit

def apply_all_formulas(data, formulas):
    """
    Applies formula chainig on data.
    """
    
    for formula in formulas:
        data = apply_formula(data,formula)
    return data

def validate_input(func):
    """
    This decorator validates request format.
    Ensures input request has required schema(json) with correct data schema and formula schema. 
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
                    #formula validation pending...
                    x=validate_formula(formula)
                else:
                    raise Exception(f"Invalid Formula {formula}. Formula should have outputVar,expression and inputs")
                
        except Exception as e:
            return {"Error": str(e)}
        return func(*args,**kwargs)
    return wrapper

def validate_formula(formula):

    """
    This function validates feasibility of formula.It should have all the variables required in expression.
    """
    pass



# for d in data["data"]:
#     print(apply_all_formulas(d,data["formulas"]))