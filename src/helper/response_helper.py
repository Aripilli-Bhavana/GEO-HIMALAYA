from helper import database_helper
from flask import jsonify

def get_result_from_db(llm_response : str, aoi : str) :
    result = database_helper.run_query(llm_response, aoi)
    if result[0] : 
        return True, result[1]
    else :
        error_str = f"{result[1]}"
        response = jsonify({
           "error" : error_str
        })
        return False, response
