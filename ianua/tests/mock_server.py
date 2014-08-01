from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
"""
As small as possible web server that returns 200 and requested path
"""

@Request.application
def application(request):
    return Response('requested:{}'.format(request.path))


if __name__ == '__main__':
    run_simple('localhost', 4000, application)
