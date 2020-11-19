from pathlib import Path
from bottle import route, run as b_run, template

www = Path(__file__).parents[0] / 'www'


@route('/')
@route('/index.html')
def index():
    with open(www / "index.j2") as f:
        return template(f.read(), client_key=None)


@route('/<name>')
def other(name):
    with open(www / name, 'rb') as f:
        return f.read()


def run():
    b_run(host='', port=8000)
