"""
Homework this week, wsgi application of.
Online calculator that can perform several operations.
"""

import re
import traceback
import math


def add(*args):
    """
    Returns a STRING with the sum of the arguments
    A call to /add/a/b yields a + b
    """
    body = []
    total=0
    try:
        total = sum(map(int, args))
        body.append("Result is: {}".format(total))
    except (ValueError, TypeError) as err:
        body = "Unable to calculate a sum: please provide int values" + str(err)
    return str(body)


def subtract(*args):
    """
    Returns a STRING with the subtract of the arguments
    A call to /subtruct/a/b yields a + b
    """
    body = []
    total = 0
    try:
        total = int(args[0]) - int(args[1])
        body.append("Result is: {}".format(total))
    except (ValueError, TypeError) as err:
        body = "Unable to calculate a subtract: please provide int values" + str(err)
    return body

def multiply(*args):
    """
    Returns a STRING with the multiply of the arguments
    A call to /multiply/a/b yields a + b
    """
    body = []
    total = 0
    try:
        total = int(args[0]) * int(args[1])
        body.append("Result is: {}".format(total))
    except (ValueError, TypeError) as err:
        body = "Unable to calculate a multiply: please provide int values" + str(err)
    return body


def divide(*args):
    """
    Returns a STRING with the divide of the arguments
    A call to /divide/a/b yields a + b
    """
    body = []
    total = 0
    try:
        total = int(args[0]) // int(args[1])
        body.append("Result is: {}".format(total))
    except (ValueError, TypeError) as err:
        body = "Unable to calculate a divide: please provide int values" + str(err)
    return body


def root_path(*args):
    """
    The index page at the root of the server shall include instructions
    on how to use the page.
    """
    body = """
    <p>Instructions on how to use the page.</p>
        <ul>
        <li>A call to: /add/a/b yields a + b </li>
        <li>A call to: /subtract/a/b yields a - b </li>
        <li>A call to: /multiply/a/b yields a * b </li>
        <li>A call to: /divide/a/b yields a / b </li>
        <li>A call to: / yields instruction index page </li>
        </ul>
    """
    try:
        print("Instruction page", body)
    except (ValueError, TypeError) as err:
        body = "Unable to calculate a divide: please provide int values" + str(err)
    return body

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        '': root_path,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    path = path.strip('/').split('/')
    # print("after strip:", path)
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
        print ("func: ", func);
    except KeyError:
        raise NameError
    return func, args

def application(environ, start_response):
    # application will invoke start_response(status, headers) and
    # Param: environ and start_response
    # return the body of the response in BYTE encoding.
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError as e:
        print("got name error", e)
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        body = str(body);
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # wsgiref simple server creation
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
