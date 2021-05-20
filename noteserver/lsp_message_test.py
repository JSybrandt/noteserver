"""Tests the utility functions for lsp messages."""
import unittest
import json
from noteserver import lsp_message


class LSPMessageTest(unittest.TestCase):
  """Tests the creation and parsing of LSP RPCs."""

  def test_serialize_and_parse_lsp_request(self):
    """Tests that an encoded message can be decoded."""
    expected = lsp_message.LspRequest(id=1,
                                      method="test/method",
                                      params={
                                          "str_param": "foo",
                                          "int_param": 1,
                                          "float_param": 2.1,
                                      })
    actual = lsp_message.LspRequest.parse(expected.serialize())
    self.assertEqual(actual, expected)

  def test_serialize_lsp_request(self):
    """Tests that an encoded message matches an expected format."""
    request = lsp_message.LspRequest(id=1,
                                     method="test/method",
                                     params={"param": "val"})
    message = request.serialize()
    # Message should contain "\r\n\r\n" that splits the header from content.
    tokens = message.decode("utf-8").split("\r\n\r\n")
    self.assertEqual(len(tokens), 2)
    header, content = tokens
    # The header should describe the content.
    expected_header = ("Content-Length: 80\r\n"
                       "Content-Type: application/vscode-jsonrpc;charset=utf-8")
    self.assertEqual(header, expected_header)
    # The content should be a json string that contains the LspRequest.
    self.assertEqual(
        json.loads(content), {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "test/method",
            "params": {
                "param": "val"
            }
        })
