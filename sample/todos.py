#! -*- coding: utf8 -*-
import uuid

from flask import request, abort
from flask_restful import Resource, fields, marshal_with

# resource def
todos = {}

class Todo(object):
    def __init__(self, task):
        self.id = str(uuid.uuid1())
        self.task = task

    def __iter__(self):
        for k in ('id', 'task'):
            yield k, getattr(self, k)


class TodoResource(Resource):
    fields = {
        'id': fields.String(attribute='id'),
        'task': fields.String
    }
    @marshal_with(fields)
    def get(self, todo_id):
        try:
            todo = todos[todo_id]
            # dict로 리턴하면 바로 json으로
            # 객체로 리턴하면 marshal_with로..
            # dict(todo)와 같음
            return todo
        except KeyError:
            abort(404)

    def put(self, todo_id):
        # reqjest.json은 application/json인 경우만..
        # 아닌 경우는 request.get_json(force=True)로 처리...
        try:
            data = request.get_json(force=True)
            todo = todos[todo_id]
            todo.task = data['task']
            return dict(todo)
        except KeyError:
            abort(404)

    def delete(self, todo_id):
        try:
            del todos[todo_id]

            return '{}'
        except KeyError:
            abort(404)


class TodoList(Resource):
    def post(self):
        # request의 content-type이 application/json이여야 함
        todo = Todo(request.json['task'])
        todos[todo.id] = todo

        # response의 content_type은 application/json으로 설정됨
        return dict(todo)


from _app import api

# get/put/delete는 Todo... post는 list resource해 했음
api.add_resource(TodoResource, '/todo/<string:todo_id>')
# 리소스에 추가는 List Action..
api.add_resource(TodoList, '/todo/')
