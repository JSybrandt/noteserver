"""Tests the Lsp Server and IO routines."""

import io
import unittest
from noteserver import server
from noteserver import lsp_message


class ServerTest(unittest.TestCase):
  """Behavior of server.py"""

  def test_unimplimented_error(self):
    """Tests that an unimplimented request produces an error response."""
    reader = io.BytesIO(
        lsp_message.LspRequest(id=1, method="test/method").serialize())
    writer = io.BytesIO()
    test_server = server.Server(reader, writer)
    test_server.run()
    actual = lsp_message.LspResponse.parse(writer.getvalue())
    expected = lsp_message.LspResponse(
        id=1,
        error=lsp_message.LspError(code=lsp_message.INTERNAL_ERROR,
                                   message="test/method not implemented"))
    self.assertEqual(actual, expected)


class LspMessageSourceTest(unittest.TestCase):
  """Tests the message IO behavior of server.py"""

  def test_read_request_and_response(self):
    """Multiple messages of different types can be read."""
    request = lsp_message.LspRequest(id=1,
                                     method="request",
                                     params={"foo": "bar"})
    response = lsp_message.LspResponse(id=2,
                                       result="response",
                                       error=lsp_message.LspError(
                                           code=3, message="err"))
    # A bytes file with two messages.
    bytes_file = io.BytesIO(request.serialize() + response.serialize())
    actual = list(server.lsp_message_source(bytes_file))
    self.assertEqual(actual, [request, response])

  def test_empty_file(self):
    """Tests that an empty buffer file doesn't cause errors."""
    # A bytes file with two messages.
    bytes_file = io.BytesIO(b"")
    actual = list(server.lsp_message_source(bytes_file))
    self.assertEqual(actual, [])

  def test_malformed_header(self):
    """Tests that a source with a bad header results in a ValueError."""
    # A bytes file with two messages.
    bytes_file = io.BytesIO(b"garbage header")
    with self.assertRaises(ValueError):
      list(server.lsp_message_source(bytes_file))

  def test_content_length_too_large(self):
    """Raises a ValueError if the content length exceeds the size of the msg."""
    message = (
        # This content length is much too high for the message.
        b"Content-Length: 80\r\n"
        b"Content-Type: application/vscode-jsonrpc;charset=utf-8\r\n"
        b"\r\n"
        # This is a correct LspRequest with Content-Length: 52
        b'{"jsonrpc": "2.0", "id": 1, "method": "test/method"}')
    with self.assertRaises(ValueError):
      list(server.lsp_message_source(io.BytesIO(message)))

  def test_content_length_too_small(self):
    """Raises a ValueError if the content length is too low."""
    message = (
        # This content length is much too low for the message.
        b"Content-Length: 10\r\n"
        b"Content-Type: application/vscode-jsonrpc;charset=utf-8\r\n"
        b"\r\n"
        # This is a correct LspRequest with Content-Length: 52
        b'{"jsonrpc": "2.0", "id": 1, "method": "test/method"}')
    with self.assertRaises(ValueError):
      list(server.lsp_message_source(io.BytesIO(message)))

  def test_content_doesnt_match_schema(self):
    """Raises a ValueError if the content isn't an expected LspMessage."""
    message = (
        # This content-length is correct.
        b"Content-Length: 18\r\n"
        b"Content-Type: application/vscode-jsonrpc;charset=utf-8\r\n"
        b"\r\n"
        # This message is missing the "method" field.
        b'{"jsonrpc": "2.0"}')
    with self.assertRaises(ValueError):
      list(server.lsp_message_source(io.BytesIO(message)))
