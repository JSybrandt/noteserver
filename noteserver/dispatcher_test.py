"""Tests for dispatcher.py"""

import unittest
from noteserver import dispatcher
from noteserver import lsp_message


class DispatcherTest(unittest.TestCase):
  """Tests the behavior of the dispatcher."""

  def test_not_implimented_error_on_bad_request(self):
    """Tests that an unimplimented request produces an error response."""
    test_dispatcher = dispatcher.Dispatcher()
    response = list(
        test_dispatcher(
            lsp_message.LspRequest(id=13,
                                   method="test/method",
                                   params={"foo": "bar"})))
    self.assertEqual(response, [
        lsp_message.LspResponse(id=13,
                                error=lsp_message.LspError(
                                    code=lsp_message.INTERNAL_ERROR,
                                    message="test/method not implemented",
                                    data={"foo": "bar"}))
    ])

  def test_not_implimented_error_on_bad_request_no_param(self):
    """Tests that a bad request with no params  produces an error."""
    test_dispatcher = dispatcher.Dispatcher()
    response = list(
        test_dispatcher(lsp_message.LspRequest(id=13, method="test/method")))
    self.assertEqual(response, [
        lsp_message.LspResponse(id=13,
                                error=lsp_message.LspError(
                                    code=lsp_message.INTERNAL_ERROR,
                                    message="test/method not implemented"))
    ])
