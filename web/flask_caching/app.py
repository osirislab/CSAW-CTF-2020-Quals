#!/usr/bin/env python2

from flask import Flask
from flask import request, redirect
from flask_caching import Cache
from redis import Redis
import jinja2
import os

app = Flask(__name__)
app.config['CACHE_REDIS_HOST'] = 'redis'
app.config['DEBUG'] = True

cache = Cache(app, config={'CACHE_TYPE': 'redis'})
redis = Redis('redis')
jinja_env = jinja2.Environment(autoescape=['html', 'xml'])


def python3_actual_decode(a):
    return b''.join(bytes([ord(i)]) for i in a)


@app.route('/', methods=['GET', 'POST'])
def notes_post():
    if request.method == 'GET':
        return '''
        <h4>Post a note</h4>
        <form method=POST enctype=multipart/form-data>
        <input name=title placeholder=title>
        <input type=file name=content placeholder=content>
        <input type=submit>
        </form>
        '''

    print(request.form, flush=True)
    print(request.files, flush=True)
    title = request.form.get('title', default=None)
    content = request.files.get('content', default=None)

    if title is None or content is None:
        return 'Missing fields', 400

    content = content.stream.read()
    if len(title) > 100 or len(content) > 256:
        return 'Too long', 400

    redis.set(name=title, value=content)

    return redirect(os.path.join('/view/', title))


@app.route('/view/<path:title>')
@cache.memoize(timeout=30)
def notes_view(title):
    content = redis.get(title)

    return jinja_env.from_string('''
    <h4>{{ title }}</h4>
    <p>{{ content }}</h4>
    ''').render(title=title, content=content)


@cache.cached(timeout=3)
def _test():
    return 'test'
@cache.cached(timeout=3)
def _ping():
    return 'ping'
@cache.cached(timeout=3)
def _pong():
    return 'pong'
@cache.cached(timeout=3)
def _hello_there():
    return '...General Kenobi!'


@app.route('/test')
def test():
    _test()
    return 'test'
@app.route('/ping')
def ping():
    _ping()
    return 'pong'
@app.route('/pong')
def pong():
    _pong()
    return 'ping'
@app.route('/hello_there')
def hello_there():
    _hello_there()
    return '...General Kenobi!'

if __name__ == "__main__":
    app.run('0.0.0.0', 5000)
