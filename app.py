from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds


app = Flask(__name__)

@app.post('/api/painting')
def insert_painting():
    invalid = check_endpoint_info(request.json, ['painting_artist','painting_date_painted','painting_name','painting_image_url'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

    results = dbhelper.run_statment('CALL insert_painting(?,?,?,?)',
    [request.json.get('painting_artist'), request.json.get('painting_date_painted'), request.json.get('painting_name'), request.json.get('painting_image_url')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)


@app.get('/api/painting')
def get_artist():
    invalid = check_endpoint_info(request.args, ['artist'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

    results = dbhelper.run_statment('CALL specific_artist(?)', [request.args.get('artist')])
    if(type(results ) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)
        


if(dbcreds.production_mode == True):
    print("Running in Production Mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode!")
    app.run(debug=True)