"""Functions to construct the noteserver flask server.

This module contains create_flask_server, which is used to produce a flask app
capable of responding to all required LSP and browser requests.
"""

import flask
from flask import logging
from noteserver import lsp_message


def createFlaskServer(name: str = __name__,
                      is_testing: bool = False) -> flask.Flask:
  """Creates the Flask webserver.

  Args:
    name: The applications module or package. Defaults to __name__.
    is_testing: Sets the value on the returned Flask apps config["TESTING"]
      parameter.
  Returns:
    A flask app that specifies endpoints for the LSP protocol, as well as for
    generating webpages.
  """
  app = flask.Flask(name)
  app.config["TESTING"] = is_testing
  logger = logging.create_logger(app)

  @app.route("/lsp", methods=["POST"])
  def lsp() -> bytes:
    """Provides an endpoint for sending LSP requests.

    Clients can send POST requests to this endpoint in order to communicate
    with the language server. The data of these POST requests should conform to
    the LSP.

    Returns:
      A serialized LspMessage.
    """
    msg: bytes = flask.request.data
    method, params = lsp_message.parseLspMessage(msg)
    logger.info("%s: %s", method, params)
    return lsp_message.getLspMessage(method, params)

  return app
