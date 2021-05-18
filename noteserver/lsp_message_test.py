"""Tests the utility functions for lsp messages."""
import unittest
import json
from noteserver import lsp_message


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
    actual_method, actual_params = lsp_message.parseRequest(
        lsp_message.serializeRequest(expected_method, expected_params))
    self.assertEqual(actual_method, expected_method)
    self.assertEqual(actual_params, expected_params)

  def test_encode_lsp_message(self):
    """Tests that an encoded message matches an expected format."""
    lsp_msg = lsp_message.serializeRequest("test_method", {"param": "val"})
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
