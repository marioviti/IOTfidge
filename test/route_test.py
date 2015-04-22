from bottle import route, run, template, response
from json import dumps
response.content_type = 'application/json'

@route('/hello/<name>')
def index(name):
    return dumps([{ "id": 1, "name": name }, { "id": 2, "name": "Test Item 2" }])

run(host='localhost', port=8080)