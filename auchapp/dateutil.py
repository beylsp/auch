from flask import request
from flask import make_response
from functools import wraps

import werkzeug


def _check_http_date():
    header_key = 'If-Modified-Since'
    modified_since = request.headers.get(header_key, None)
    return werkzeug.http.parse_date(modified_since)
    

def _http_date_error_callback():
    res = make_response()
    res.status_code = 400
    return res


def modified_since_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        date = _check_http_date()
        if date:
            return f(date, *args, **kwargs)
        else:
            return _http_date_error_callback()
    return decorated

