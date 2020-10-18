"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback


def index(*args):
    return """
            <h1>WSGI Calculator</h1>
            <h2>All requests must be URLs in the form "domain/function/x/y/z"</h2>
            <h2>Legal values for function are listed in the table below with number of arguments</h2>
            <br>
           <table border="1"><tr><th>Math Function</th><th>Arguments</th></tr>
           <tr><td>add</td><td>As Many As You Like</td></tr>
           <tr><td>multiply</td><td>As Many As You Like</td></tr>
           <tr><td>subtract</td><td>Must Have 2</td></tr>
           <tr><td>divide</td><td>Must Have 2</td></tr>
           </table>"
           """



def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    addends = args
    sum = 0
    for x in addends:
        sum += float(x)

    return str(sum)

# TODO: Add functions for handling more arithmetic operations.


def multiply(*args):
    multiplicands = args
    if len(multiplicands) == 0:
        return "No Arguments Given"

    product = 1
    for x in multiplicands:
        product *= float(x)
    return str(product)


def divide(*args):
    if len(args) != 2:
        return "Improper Number of Arguments"
    return str(float(args[0]) / float(args[1]))


def subtract(*args):
    if len(args) != 2:
        return "Improper Number of Arguments"
    return str(float(args[0]) - float(args[1]))


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {
        '': index,
        'add': add,
        'multiply': multiply,
        'divide': divide,
        'subtract': subtract
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Data"
        body = "<h1>Unable to Divide by Zero</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    pass


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
