'''
Created on 10.05.2017

@author: sebastian
'''

import unittest
from requests.exceptions import ConnectionError

from butler_offline.viewcore.context import generate_redirect_context
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.test.RequestStubs import PostRequest, GetRequest
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.core import file_system


class TesteRequestHandler(unittest.TestCase):

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        persisted_state.database_instance()
        request_handler.stub_me_theme()

    def test_manual_redirect(self):
        self.set_up()
        result = request_handler.handle_request(GetRequest(), lambda x: generate_redirect_context('to_url'), 'nothing')
        assert result == 'to_url'

    def test_extra_page(self):
        self.set_up()
        result = request_handler.handle_request(PostRequest({}), lambda x: {'special_page': 'something_special'}, 'something_normal')
        assert result['content'] == 'something_special'

    def test_default_page(self):
        self.set_up()
        result = request_handler.handle_request(PostRequest({}), lambda x: {}, 'something_normal')
        assert result['content'] == 'something_normal'

    def raise_http_error(self):
        raise ConnectionError()

    def raise_error(self):
        raise Exception()

    def test_http_exception(self):
        self.set_up()
        request_handler.stub_me()

        result = request_handler.handle_request(PostRequest({}), lambda x: self.raise_http_error(), 'something_normal')
        assert result['message']
        assert result['message_type'] == 'error'
        assert result['message_content'] == 'Verbindung zum Server konnte nicht aufgebaut werden.'

    def test_exception(self):
        self.set_up()
        request_handler.stub_me()

        result = request_handler.handle_request(PostRequest({}), lambda x: self.raise_error(), 'something_normal')
        print(result['message_content'])
        assert result['message']
        assert result['message_type'] == 'error'
        assert result['message_content'] == 'Ein Fehler ist aufgetreten: <br>\n '
