"""Functions to construct the noteserver flask server.

This module contains create_flask_server, which is used to produce a flask app
capable of responding to all required LSP and browser requests.
"""

import json
from typing import Dict, Any, Tuple
import flask
from flask import logging

# Represents the RPC parameters of a json rpc message.
Parameters = Dict[str, Any]


def getLspMessage(method: str, params: Parameters) -> bytes:
  """Creates a LSP message with header and content components.

  Args:
    method: The RPC method to call.
    params: The parameters of the specified RPC message.

  Returns:
    A serialized LSP message, which contains a header and content
    section. The header describes the content, while the content itself is a
    utf-8 encoded json-rpc message.
  """
  content = json.dumps({
      "jsonrpc": "2.0",
      "id": 1,
      "method": method,
      "params": params,
  }).encode("utf-8")
  # Each header parameter is terminated by \r\n, and the header itself is also
  # terminated by \r\n.
  header = (f"Content-Length: {len(content)}\r\n"
            "Content-Type: application/vscode-jsonrpc;charset=utf-8\r\n"
            "\r\n")
  return header.encode("utf-8") + content


def parseLspMessage(message: bytes) -> Tuple[str, Parameters]:
  """Extracts the method name and rpc parameters of a given LSP message.

  Args:
    message: A string containing an LSP header and content segment.

  Returns:
    A tuple of [method, parameters], that describes the RPC.

  Raises:
    ValueError: The message cannot be parsed.
  """
  tokens = message.decode("utf-8").split("\r\n\r\n")
  if len(tokens) != 2:
    raise ValueError(r"Serialized LSP Message does not contain \r\n\r\n.")
  content = json.loads(tokens[1])
  if "method" not in content:
    raise ValueError("LSP Message does not contain 'method' key.")
  if "params" not in content:
    raise ValueError("LSP Message does not contain 'params' key.")
  return content["method"], content["params"]


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
    method, params = parseLspMessage(msg)
    logger.info("%s: %s", method, params)
    return getLspMessage(method, params)

  return app
