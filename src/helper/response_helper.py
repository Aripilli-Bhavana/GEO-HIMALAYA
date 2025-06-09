from helper import database_helper
from flask import jsonify

def get_result_from_db(llm_response : str, aoi : str) :
    result = database_helper.run_query(llm_response, aoi)
    if result[0] : 
        response = jsonify({
            "sql_query" : llm_response,
            "data" : result[1]
        })
        return True, response
    else :
        error_str = f"{result[1]}"
        response = jsonify({
            "sql_query" : llm_response,
           "error" : error_str
        })
        return False, response
