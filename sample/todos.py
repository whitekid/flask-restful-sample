#! -*- coding: utf8 -*-
import uuid

from flask import request
from flask_restful import Resource, fields, marshal_with
from werkzeug import exceptions

# see werkzeug.http.HTTP_STATUS_CODES
CREATED = 201
ACCEPTED = 202
NO_CONTENT = 204

# resource def
todos = {}

# reset fields
todo_fields = {
    'id': fields.String(attribute='id'),
    'task': fields.String
}

class Todo(object):
    def __init__(self, task):
        self.id = str(uuid.uuid1())
        self.task = task


class TodoResource(Resource):
    @marshal_with(todo_fields, envelope='todo')
    def get(self, todo_id):
        if todo_id not in todos:
            raise exceptions.NotFound

        return todos[todo_id]

    @marshal_with(todo_fields, envelope='todo')
    def put(self, todo_id):
        if todo_id not in todos:
            raise exceptions.NotFound

        data = request.json
        todo = todos[todo_id]
        todo.task = data['task']
        return todo, CREATED

    def delete(self, todo_id):
        if todo_id not in todos:
            raise exceptions.NotFound

        del todos[todo_id]

        return '', NO_CONTENT


class TodoList(Resource):
    @marshal_with(todo_fields)
    def get(self):
        return todos.values()

    @marshal_with(todo_fields, envelope='todo')
    def post(self):
        # request의 content-type이 application/json이여야 함
        todo = Todo(request.json['task'])
        todos[todo.id] = todo

        # response의 content_type은 application/json으로 설정됨
        return todo, CREATED


from _app import api

# get/put/delete는 Todo... post는 list resource해 했음
api.add_resource(TodoResource, '/todo/<string:todo_id>')
# 리소스에 추가는 List Action..
api.add_resource(TodoList, '/todo/')
