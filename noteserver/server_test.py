"""Tests for the flask server."""

import unittest
from noteserver import server
from noteserver import lsp_message


class FlaskServerTest(unittest.TestCase):
  """Test for the flask server."""

  def setUp(self):
    """Creates the flask server and client in test mode."""
    self.flask_app = server.create_flask_server(name="test_server",
                                                is_testing=True)

  def test_lsp_responds_with_error(self):
    """The LSP server isn't built, it should return a message saying so."""
    # We will remove this test once we actually build something.
    with self.flask_app.test_client() as client:
      request = lsp_message.LspRequest(id=0,
                                       method="test/method",
                                       params={"param": "val"})
      actual = lsp_message.LspResponse.parse(
          client.post("/lsp", data=request.serialize()).data)
      expected = lsp_message.LspResponse(
          id=0,
          error=lsp_message.LspError(lsp_message.INTERNAL_ERROR,
                                     "'test/method' is not implemented yet.",
                                     data=request.get_content()))
      self.assertEqual(actual, expected)
