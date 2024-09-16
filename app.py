from flask import Flask, request, jsonify
from lib.validations import validate_input
from lib.utils import data_to_dataframe,apply_formulas,format_output
app = Flask(__name__)



@app.post("/api/execute-formula")
@validate_input
def execute_formula():

    data = request.get_json()

    input_data_df = data_to_dataframe()
    
    result_df = apply_formulas(input_data_df,data["formulas"])

    result = format_output(result_df)
    
    return jsonify(result),200

if __name__ == '__main__':
    app.run(port=5000,debug = True)
