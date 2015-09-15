from flask import request
from flask import make_response
from functools import wraps
from auchapp import err

import werkzeug


def _check_http_date():
    header_key = 'If-Modified-Since'
    modified_since = request.headers.get(header_key, None)
    return werkzeug.http.parse_date(modified_since)
    

def modified_since_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        date = _check_http_date()
        if date:
            return f(date, *args, **kwargs)
        else:
            return err.make_error(400, "Missing HTTP header key If-Modified-Since")
    return decorated

