import json
from django.http import HttpResponse
from django.views.generic import View

from webargs import Arg
from webargs.djangoparser import DjangoParser

parser = DjangoParser()
hello_args = {
    'name': Arg(str, default='World')
}
hello_multi = {
    'name': Arg(multiple=True)
}

def render_json_response(data):
    return HttpResponse(
        json.dumps(data),
        content_type='application/json'
    )


class SimpleCBVWithParam(View):

    @parser.use_args(hello_args)
    def get(self, args, request, pid):
        return render_json_response(args)

class SimpleCBV(View):

    def get(self, request):
        args = parser.parse(hello_args, self.request)
        return render_json_response(args)

    def post(self, request):
        args = parser.parse(hello_args, self.request)
        return render_json_response(args)

class SimpleCBVMulti(View):

    def get(self, request):
        args = parser.parse(hello_multi, self.request)
        return render_json_response(args)

    def post(self, request):
        args = parser.parse(hello_multi, self.request)
        return render_json_response(args)

class SimpleDecoratedCBV(View):

    @parser.use_args(hello_args)
    def get(self, args, request):
        return render_json_response(args)

    @parser.use_args(hello_args)
    def post(self, args, request):
        return render_json_response(args)


def simpleview(request):
    args = parser.parse(hello_args, request)
    return render_json_response(args)

required_args = {
    'name': Arg(str, required=True)
}
def simpleview_with_required_arg(request):
    args = parser.parse(required_args, request)
    return render_json_response(args)

def simpleview_multi(request):
    args = parser.parse(hello_multi, request)
    return render_json_response(args)

def cookieview(request):
    request.COOKIES['name'] = 'Joe'
    args = parser.parse(hello_args, request, locations=('cookies',))
    return render_json_response(args)

@parser.use_args(hello_args)
def simpleview_with_param(request, args, pid):
    return render_json_response(args)

@parser.use_args(hello_args)
def decoratedview(request, args):
    return render_json_response(args)

@parser.use_args({'validated': Arg(validate=lambda n: False)})
def validatedview(request, args):
    return render_json_response(args)
