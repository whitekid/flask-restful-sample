# -*- coding: utf-8 -*-
import os

from flask import Flask, Request
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

class MyRequest(Request):
    json_paths = []

    def __init__(self, environ, populate_request=True, shallow=False):
        # add_resource로 추가한 url을 넣으려고 생각했는데..
        # 이미 여기 들어온 것들은 add_resource가 실행되어서 들어온 것들이군.
        # api와 html을 동시에 서비스하지 않는다면 굳이 url에 따라서 분기할
        # 필요가 없군요.
        if not environ.get('CONTENT_TYPE', ''):
            environ['CONTENT_TYPE'] = 'application/json'
        super(self.__class__, self).__init__(environ, populate_request, shallow)


class MyApi(Api):
    def add_resource(self, resource, *urls, **kwargs):
        return super(self.__class__, self).add_resource(resource, *urls, **kwargs)

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)

app.request_class = MyRequest

# for route
import todos
