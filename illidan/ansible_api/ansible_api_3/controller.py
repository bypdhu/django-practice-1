import json

from flask import Flask, request, abort, jsonify

from api import Api

VERSION = '1.0.0'
app = Flask(__name__)


@app.route("/adhoc", methods=['POST'])
def handle_request():
    if request.headers.get('Content-Type') != "application/json":
        abort(400)

    user_data = json.loads(request.get_data())
    print(user_data)
    try:
        api = Api(**user_data)
        result = api.run_cmd()
        return jsonify(result), 200

    except Exception as e:
        resp = {"error": True, "msg": str(e)}
        return jsonify(resp), 444


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5566)
