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

  def test_lsp_echos_calls(self):
    """Sends a special RPC that causes the LSP to echo the request."""
    with self.flask_app.test_client() as client:
      request = lsp_message.LspRequest(id=0,
                                       method="test/method",
                                       params={"param": "val"})
      response = client.post("/lsp", data=request.serialize())
      self.assertEqual(request, lsp_message.LspRequest.parse(response.data))
