"""Tests for the flask server."""

import unittest
from noteserver import server
from noteserver import lsp_message


class FlaskServerTest(unittest.TestCase):
  """Test for the flask server."""

  def setUp(self):
    """Creates the flask server and client in test mode."""
    self.flask_app = server.createFlaskServer(name="test_server",
                                              is_testing=True)

  def test_lsp_echos_calls(self):
    """Sends a special RPC that causes the LSP to echo the request."""
    with self.flask_app.test_client() as client:
      method = "test/method"
      params = {"test_param": "val"}
      request = lsp_message.serializeRequest(method, params)
      response = client.post("/lsp", data=request)
      actual_method, actual_params = lsp_message.parseRequest(response.data)
      self.assertEqual(actual_method, method)
      self.assertEqual(actual_params, params)
