from flask import Flask, request, jsonify, redirect, make_response, render_template
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = 'IhrGeheimesSchluessel'

def generate_token(uuid):
    payload = {
        'uuid': uuid,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def validate_uuid(uuid):
    valid_uuids = ['uuid1', 'uuid2', 'uuid3']
    return uuid in valid_uuids

@app.route('/nfc', methods=['GET'])
def nfc():
    uuid = request.args.get('uuid')
    if validate_uuid(uuid):
        token = generate_token(uuid)
        response = make_response(redirect('/positive-message'))
        response.set_cookie('access_token', token)
        return response
    else:
        return jsonify(message='Ungültige UUID'), 403

@app.route('/positive-message', methods=['GET'])
def positive_message():
    token = request.cookies.get('access_token')
    if not token:
        return jsonify(message='Kein Token gefunden'), 403
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        uuid = payload['uuid']
        if validate_uuid(uuid):
            return render_template('index.html')
        else:
            return jsonify(message='Ungültige UUID'), 403
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token abgelaufen'), 403
    except jwt.InvalidTokenError:
        return jsonify(message='Ungültiges Token'), 403

if __name__ == '__main__':
    app.run()
