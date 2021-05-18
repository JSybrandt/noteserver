"""Tests for the flask server."""

import unittest
import json
from noteserver import server


class LSPMessageTest(unittest.TestCase):
  """Tests the creation and parsing of LSP RPCs."""

  def test_encode_decode(self):
    """Tests that an encoded message can be decoded."""
    expected_method = "test/method"
    expected_params = {
        "str_param": "foo",
        "int_param": 1,
        "float_param": 2.1,
    }
    actual_method, actual_params = server.parseLspMessage(
        server.getLspMessage(expected_method, expected_params))
    self.assertEqual(actual_method, expected_method)
    self.assertEqual(actual_params, expected_params)

  def test_encode_lsp_message(self):
    """Tests that an encoded message matches an expected format."""
    lsp_msg = server.getLspMessage("test_method", {"param": "val"})
    tokens = lsp_msg.decode("utf-8").split("\r\n\r\n")
    self.assertEqual(len(tokens), 2)
    header, content = tokens
    expected_header = ("Content-Length: 80\r\n"
                       "Content-Type: application/vscode-jsonrpc;charset=utf-8")
    self.assertEqual(header, expected_header)
    self.assertEqual(
        json.loads(content), {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "test_method",
            "params": {
                "param": "val"
            }
        })


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
      request = server.getLspMessage(method, params)
      response = client.post("/lsp", data=request)
      actual_method, actual_params = server.parseLspMessage(response.data)
      self.assertEqual(actual_method, method)
      self.assertEqual(actual_params, params)
