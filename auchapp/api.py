from auchapp import app
from auchapp.models import User
from flask import jsonify
from flask import g
from flask_httpauth import HTTPBasicAuth
from flask import make_response

#extensions
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@app.route('/api/users', methods=['POST'])
def new_user():
    return jsonify({})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Not allowed'}), 405)
