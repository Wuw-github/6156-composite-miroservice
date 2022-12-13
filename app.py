from flask import Flask, request, g
import json
from flask_cors import CORS
import requests

app = Flask(__name__)
app.secret_key = "it-is-hard-to-guess"
CORS(app)


@app.route('/userinfo')
def get_user_info():
    token = request.headers.get('Authorization')
    if not token:
        return {'msg': 'Missing token'}, 401
    rsp = requests.get('http://carpoolcontact-env.eba-macduk5c.us-east-1.elasticbeanstalk.com/contacts/users/', headers={'Authorization': token})
    if rsp.status_code != 200:
        return rsp.json(), rsp.status_code
    userinfo = rsp.json()
    rsp = requests.get('http://54.204.232.23:5011/auth/userinfo', headers={'Authorization': token})
    if rsp.status_code != 200:
        return rsp.json(), rsp.status_code

    return {**userinfo, **rsp.json()}, 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)
