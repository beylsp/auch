from flask import jsonify
from flask import g
from flask import make_response
from flask import request
from flask import abort
from flask import url_for
from auchapp import app
from auchapp.database import db
from auchapp.models import user_schema
from auchapp.authentication import auth
from auchapp.models import User

@app.route('/api/login', methods=['GET'])
@auth.http_auth_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })


@app.route('/api/test', methods=['GET'])
@auth.auth_token_required
def get_test_resource():
    return make_response(jsonify({'result': 'success'}), 200)
     

@app.route('/api/users', methods=['POST'])
def new_user():
    if not request.get_json():
        abort(400) # no json body

    data, errors = user_schema.load(request.json)
    if errors:
        abort(400)

    user = User(username = data.get('username'))
    user.password = data.get('password')
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify({'id': user.id}), 201)


@app.route('/api/users/edit', methods=['PUT'])
@auth.auth_token_required
def edit_user():
    if not request.get_json():
        abort(400) # no json body

    data, errors = user_schema.load(request.json)
    if errors:
        abort(400)

    User.query.filter_by(username = g.user.username).update(data)
    db.session.commit()
    return make_response(jsonify({'id': g.user.id}), 200)


@app.route('/api/users/delete', methods=['DELETE'])
@auth.auth_token_required
def del_user():
    db.session.delete(g.user)
    db.session.commit()
    return make_response(jsonify({'id': g.user.id}), 200)
