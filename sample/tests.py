#! -*- coding: utf8 -*-
import json
import types

from _app import *

import unittest

class TodoTest(unittest.TestCase):
    def setUp(self):
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        self.app = app.test_client()

    def post(self, url, data):
        if type(data) == types.DictType:
            data = json.dumps(data)

        return json.loads(self.app.post(url, data=data).data)

    def get(self, url):
        return json.loads(self.app.get(url).data)

    def delete(self, url):
        return self.app.delete(url).data

    def put(self, url, data):
        if type(data) == types.DictType:
            data = json.dumps(data)

        return json.loads(self.app.put(url, data=data).data)

    def test_simple(self):
        # create
        resp = self.post('/todo/', {'task': 'sample test'})
        self.assertTrue(resp['todo']['id'])
        todo_id = resp['todo']['id']

        # list
        resp = self.get('/todo/')
        self.assertEquals(1, len(resp), resp)

        # read
        resp = self.get('/todo/%s' % todo_id)
        self.assertEquals(todo_id, resp['todo']['id'], str(resp))

        # update
        resp = self.put('/todo/%s' % todo_id, {'task': 'updated'})
        self.assertEquals('updated', resp['todo']['task'])

        # delete
        resp = self.delete('/todo/%s' % resp['todo']['id'])
        resp = self.get('/todo/%s' % todo_id)
        self.assertEquals(404, resp['status'])

if __name__ == '__main__':
    unittest.main()
