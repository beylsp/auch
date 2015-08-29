from auchapp import app
from flask_httpauth import HTTPBasicAuth
from flask import jsonify

#extensions
auth = HTTPBasicAuth()

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    return jsonify({'data': 'hello'})

if __name__ == '__main__':
    app.run(debug=True)
