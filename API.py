from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

def check_login(username):
    if not os.path.isfile('logged_in_user'):
        return False
    with open('logged_in_user', 'r') as logged:
        creds = json.load(logged)
        if username != creds['username']:
            return False
        return True

@app.route('/normalize', methods=['POST'])
def normalize():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    req = request.json
    username = request.headers.get('username', None)
    if not username:
        return jsonify({"msg": "Missing username in request headers"}), 400
    if not check_login(username):
        return jsonify({"msg": "you're not logged in"}), 401

    resp = {k['name']:{k[value] for value in k.keys() if 'val' in value.lower()}.pop() for k in req}
    return json.dumps(resp), 200

@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({'msg': 'Missing JSON in request'}), 400
    req = request.json
    if "username" not in req or "password" not in req:
        resp =  app.response_class(status=400, mimetype='application/json', response=json.dumps({'reason': 'request must have username and password fields'}))
        return resp
    #perform some really important password validation
    with open('logged_in_user', 'w') as f:
        json.dump({'username':req['username']}, f)
    return jsonify({'msg':'logged in'}), 200



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)