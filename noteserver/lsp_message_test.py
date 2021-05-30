"""Tests the utility functions for lsp messages."""
import unittest
import json
from noteserver import lsp_message


class LSPMessageTest(unittest.TestCase):
  """Tests the creation and parsing of LSP RPCs."""

  def test_serialize_and_parse_lsp_notification(self):
    """Tests that an encoded message can be decoded."""
    expected = lsp_message.LspNotification(method="test/method",
                                           params={
                                               "str_param": "foo",
                                               "int_param": 1,
                                               "float_param": 2.1,
                                           })
    actual = lsp_message.LspNotification.parse(expected.serialize())
    self.assertEqual(actual, expected)

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

  def test_serialize_and_parse_lsp_request_no_params(self):
    """Tests that an encoded message without params can be decoded."""
    expected = lsp_message.LspRequest(id=1, method="test/method")
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

  def test_serialize_and_parse_lsp_response(self):
    """Tests that a serialized response can deserialized."""
    expected = lsp_message.LspResponse(id=1,
                                       result="test_result",
                                       error=lsp_message.LspError(
                                           code=2,
                                           message="msg",
                                           data="test_data"))
    actual = lsp_message.LspResponse.parse(expected.serialize())
    self.assertEqual(actual, expected)

  def test_serialize_and_parse_lsp_response_no_error(self):
    """Tests that a serialized response without an error can deserialized."""
    expected = lsp_message.LspResponse(id=1, result="test_result")
    actual = lsp_message.LspResponse.parse(expected.serialize())
    self.assertEqual(actual, expected)

  def test_serialize_and_parse_lsp_response_no_result(self):
    """Tests that a serialized response without result can deserialized."""
    expected = lsp_message.LspResponse(id=1,
                                       error=lsp_message.LspError(
                                           code=2,
                                           message="msg",
                                           data="test_data"))
    actual = lsp_message.LspResponse.parse(expected.serialize())
    self.assertEqual(actual, expected)

  def test_serialize_and_parse_lsp_response_only_id(self):
    """Tests that a serialized response without result can deserialized."""
    expected = lsp_message.LspResponse(id=1)
    actual = lsp_message.LspResponse.parse(expected.serialize())
    self.assertEqual(actual, expected)

  def test_serialize_lsp_response_header(self):
    """Tests that a serialized response matches the LSP protocol."""
    message = lsp_message.LspResponse(id=1,
                                      result="test_result",
                                      error=lsp_message.LspError(
                                          code=2,
                                          message="msg",
                                          data="test_data")).serialize()
    # Message should contain "\r\n\r\n" that splits the header from content.
    tokens = message.decode("utf-8").split("\r\n\r\n")
    self.assertEqual(len(tokens), 2)
    header, content = tokens
    # The header should describe the content.
    expected_header = ("Content-Length: 113\r\n"
                       "Content-Type: application/vscode-jsonrpc;charset=utf-8")
    self.assertEqual(header, expected_header)
    # The content should be a json string that contains the LspRequest.
    self.assertEqual(
        json.loads(content), {
            "jsonrpc": "2.0",
            "id": 1,
            "result": "test_result",
            "error": {
                "code": 2,
                "message": "msg",
                "data": "test_data",
            }
        })

  def test_lsp_request_str_no_param(self):
    """LspRequest.__str__ matches the expected format without params."""
    request = lsp_message.LspRequest(id=1, method="test/method")
    self.assertEqual(str(request), "Request[1][test/method]")

  def test_lsp_request_str_with_param(self):
    """LspRequest.__str__ matches the expected format with params."""
    request = lsp_message.LspRequest(id=1,
                                     method="test/method",
                                     params={"param": "val"})
    self.assertEqual(str(request), "Request[1][test/method] : {'param': 'val'}")

  def test_lsp_response_str_only_id(self):
    """LspResponse.__str__ with only id matches the expected format."""
    response = lsp_message.LspResponse(id=1)
    self.assertEqual(str(response), "Response[1]")

  def test_lsp_response_str_id_and_result(self):
    """LspResponse.__str__ with id and result matches the expected format."""
    # Int result
    response = lsp_message.LspResponse(id=1, result=10)
    self.assertEqual(str(response), "Response[1] : 10")
    # Str result
    response = lsp_message.LspResponse(id=1, result="foo")
    self.assertEqual(str(response), "Response[1] : foo")
    # Dict result
    response = lsp_message.LspResponse(id=1, result={"foo": "bar"})
    self.assertEqual(str(response), "Response[1] : {'foo': 'bar'}")

  def test_lsp_response_str_id_and_error(self):
    """LspResponse.__str__ with id and error matches the format."""
    response = lsp_message.LspResponse(id=1,
                                       error=lsp_message.LspError(
                                           code=2, message="msg"))
    self.assertEqual(str(response), "Response[1] : < Error[2] : msg >")

  def test_lsp_response_str_id_result_error(self):
    """LspResponse.__str__ with id, result, and error matches the format."""
    response = lsp_message.LspResponse(id=1,
                                       result=2,
                                       error=lsp_message.LspError(
                                           code=3, message="msg"))
    self.assertEqual(str(response), "Response[1] : < Error[3] : msg > : 2")
