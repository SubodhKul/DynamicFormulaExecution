from flask import Flask, request, jsonify
from lib.utils import validate_input,apply_all_formulas
from usingPandas import convert_to_dataframe
app = Flask(__name__)



@app.post("/api/execute-formula")
@validate_input
def execute_formula():

    app_data = request.get_json()
    results = convert_to_dataframe(app_data)
    # results = []
    # for data in app_data["data"]:
    #     result = apply_all_formulas(data,app_data["formulas"])
    #     results.append(result)
    return results.to_json()

if __name__ == '__main__':
    app.run(port=5000,debug = True)









