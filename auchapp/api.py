from flask import jsonify
from flask import g
from flask import make_response
from flask import request
from flask import url_for
from auchapp import app
from auchapp import err
from auchapp import dateutil
from auchapp.database import db
from auchapp.store import store
from auchapp.authentication import auth
from auchapp.models.users import User
from auchapp.models.users import user_schema


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
        return err.make_error(400, "Missing json body")

    data, errors = user_schema.load(request.json)
    if errors:
        return err.make_error(400, "Invalid json body")

    user = User(username = data.get('username'))
    user.password = data.get('password')
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify({'id': user.id}), 201)


@app.route('/api/users/edit', methods=['PUT'])
@auth.auth_token_required
def edit_user():
    if not request.get_json():
        return err.make_error(400, "Missing json body")

    data, errors = user_schema.load(request.json)
    if errors:
        return err.make_error(400, "Invalid json body")

    User.query.filter_by(username = g.user.username).update(data)
    db.session.commit()
    return make_response(jsonify({'id': g.user.id}), 200)


@app.route('/api/users/delete', methods=['DELETE'])
@auth.auth_token_required
def del_user():
    db.session.delete(g.user)
    db.session.commit()
    return make_response(jsonify({'id': g.user.id}), 200)


@app.route('/api/sync', methods=['GET'])
@dateutil.modified_since_required
@auth.auth_token_required
def sync_data(modified_since):
    last_update = store.last_update
    if modified_since == last_update:
        return err.make_error(304, "Not modified")
    elif modified_since < last_update:
        return make_response(jsonify(
            {'format': 'auch-json-v1',
             'product_files': store.product_files(g.user) }),
            200)
    else:
        return err.make_error(400, "Invalid modified date")


@app.route('/api/sync/<product>_v<version>.json', methods=['GET'])
@auth.auth_token_required
def sync_product(product, version):
    if not store.contains(g.user, product):
        return err.make_error(404, "Invalid product")
    if not store.is_latest(product, version):
        return err.make_error(404, "Not latest product version")
    return make_response(jsonify({'product': store.get_product(product)}), 200)


@app.errorhandler(404)
def not_found(e):
    return err.make_error(e.code, e.name)
 
 
@app.errorhandler(405)
def not_allowed(e):
    return err.make_error(e.code, e.name)
