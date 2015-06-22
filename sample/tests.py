#! -*- coding: utf8 -*-
import json
import types

from _app import *

import unittest

class TodoTest(unittest.TestCase):
    def setUp(self):
        # 서버 코드 안에까지 traceback 출력하는군.
        # app.config['DEBUG'] = True
        self.app = app.test_client()

    def post(self, url, data):
        if type(data) == types.DictType:
            data = json.dumps(data)

        return json.loads(self.app.post(url, data=data).data)

    def get(self, url):
        return json.loads(self.app.get(url).data)

    def delete(self, url):
        return json.loads(self.app.delete(url).data)

    def put(self, url, data):
        if type(data) == types.DictType:
            data = json.dumps(data)

        return json.loads(self.app.put(url, data=data).data)

    def test_simple(self):
        # create
        resp = self.post('/todo/', {'task': 'sample test'})
        self.assertTrue(resp['id'])

        # read
        todo_id = resp['id']
        resp = self.get('/todo/%s' % todo_id)
        self.assertEquals(todo_id, resp['id'], str(resp))

        # update
        resp = self.put('/todo/%s' % todo_id, {'task': 'updated'})
        self.assertEquals('updated', resp['task'])

        # delete
        resp = self.delete('/todo/%s' % resp['id'])
        resp = self.get('/todo/%s' % todo_id)
        self.assertEquals(404, resp['status'])

if __name__ == '__main__':
    unittest.main()
