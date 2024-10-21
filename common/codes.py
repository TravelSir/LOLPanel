# coding: utf8
"""
Descriptive HTTP status codes, for code readability.
See RFC 2616 and RFC 6585.
RFC 2616: http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
RFC 6585: http://tools.ietf.org/html/rfc6585
"""
from __future__ import unicode_literals

from flask import request


def is_informational(code):
    return 100 <= code <= 199


def is_success(code):
    return 200 <= code <= 299


def is_redirect(code):
    return 300 <= code <= 399


def is_client_error(code):
    return 400 <= code <= 499


def is_server_error(code):
    return 500 <= code <= 599


class Codes(object):
    CONTINUE = 100
    SWITCHING_PROTOCOLS = 101
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    MULTIPLE_CHOICES = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    USE_PROXY = 305
    RESERVED = 306
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    REQUEST_ENTITY_TOO_LARGE = 413
    REQUEST_URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    REQUESTED_RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    IM_A_TEAPOT = 418
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    CONNECTION_CLOSED_WITHOUT_RESPONSE = 444
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    LOOP_DETECTED = 508
    NOT_EXTENDED = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511


def request_finish(code=None, data=None, headers=None, error_code=None, schema=None):
    """
    如果是0-99/499+的响应码，那么将直接返回response_data内容，不进行任何封装
    如果是3XX的响应，将进行重定向
    """
    if schema and is_success(code):
        result = schema().load(data)
        if result.errors:
            raise Exception('反序列化失败')
        data = result.data
    from flask import redirect
    if not isinstance(code, int):
        raise Exception("http code 必须是整形")

    if is_success(code):
        return data, code, headers
    elif is_redirect(code):
        return redirect(data)
    elif is_client_error(code) or is_server_error(code) or is_informational(code):
        _data = {'error_code': error_code or code, 'error_msg': str(data)}
        return _data, code, headers
    else:
        return data
