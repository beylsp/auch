from auchapp import app
from auchapp import db
from auchapp.models import User
from flask import jsonify
from flask import g
from flask_httpauth import HTTPBasicAuth
from flask import make_response
from flask import request
from flask import abort
from flask import url_for

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
    if not request.json:
        abort(400) # no json body
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        abort(400) # missing or empty argument
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # user already exists

    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify({'id': user.id}), 201)


@app.route('/api/users/delete', methods=['DELETE'])
@auth.login_required
def del_user():
    db.session.delete(g.user)
    db.session.commit()
    return make_response(jsonify({'id': g.user.id}), 200)


@app.route('/api/users/edit', methods=['PUT'])
@auth.login_required
def edit_user():
    if not request.json:
        abort(400) # no json body

    user = User.query.filter_by(username = g.user.username).first()

    username = request.json.get('username')
    if username is not None:
        if not username:
            abort(400) # empty username
        if g.user.username != username:
            if User.query.filter_by(username = username).first() is not None:
                abort(400) # new user already exists
            user.username = username                        
        
    password = request.json.get('password')
    if password is not None:
        if not password:
            abort(400) # empty username
        user.hash_password(password)
        
    db.session.commit()
    return make_response(jsonify({'id': user.id}), 200)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Not allowed'}), 405)
