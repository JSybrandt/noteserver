"""Utility functions for working with LSP Messages."""
from __future__ import annotations
import dataclasses
import json
from typing import Dict, Any, Optional, List, Union


def _serialize_content_with_header(content: Dict[str, Any]) -> bytes:
  """Writes serialized LSP message that includes a header and content."""
  serialized_content = json.dumps(content).encode("utf-8")
  # Each header parameter is terminated by \r\n, and the header itself is also
  # terminated by \r\n.
  header = (f"Content-Length: {len(serialized_content)}\r\n"
            "Content-Type: application/vscode-jsonrpc;charset=utf-8\r\n"
            "\r\n")
  return header.encode("utf-8") + serialized_content


@dataclasses.dataclass
class LspNotification:
  """Describes a notification RPC that doesn't require a response."""
  method: str
  params: Optional[Dict[str, Any]] = None

  def __str__(self) -> str:
    """Writes the LspNotification as a string."""
    res = f"Notification[{self.method}]"
    if self.params is not None:
      res += f" : {self.params}"
    return res

  def get_content(self) -> Dict[str, Any]:
    """Returns the content of this Lsp Message."""
    content = {
        "jsonrpc": "2.0",
        "method": self.method,
    }
    if self.params is not None:
      content["params"] = self.params
    return content

  def serialize(self) -> bytes:
    """Creates a LSP message with header and content components.

    Returns:
      A serialized LSP message, which contains a header and content
      section. The header describes the content, while the content itself is a
      utf-8 encoded json-rpc message.
    """
    return _serialize_content_with_header(self.get_content())

  @classmethod
  def from_content(cls, content: Dict[str, Any]) -> LspNotification:
    """Creates the LspNotification from a content dict.

    Returns:
      An LspNotification with values from 'content'

    Raises:
      ValueError: If the content does not contain the expected fields.
    """
    if "method" not in content:
      raise ValueError("Serialized LSP Notification does not contain method")
    notification = LspNotification(content["method"])
    if "params" in content:
      notification.params = content["params"]
    return notification

  @classmethod
  def parse(cls, message: bytes) -> LspNotification:
    """Extracts the method name and rpc parameters of a given LSP message.

    Args:
      message: A string containing an LSP header and content segment.

    Returns:
      An LspNotification object containing the content from `message`.

    Raises:
      ValueError: The message cannot be parsed.
    """
    tokens = message.decode("utf-8").split("\r\n\r\n")
    if len(tokens) != 2:
      raise ValueError(r"Serialized LSP Request does not contain \r\n\r\n.")
    content = json.loads(tokens[1])
    return LspNotification.from_content(content)


@dataclasses.dataclass
class LspRequest:
  """Describes a request RPC."""
  id: int
  method: str
  params: Optional[Dict[str, Any]] = None

  def __str__(self) -> str:
    """Writes the LspRequest as a string."""
    res = f"Request[{self.id}][{self.method}]"
    if self.params is not None:
      res += f" : {self.params}"
    return res

  def get_content(self) -> Dict[str, Any]:
    """Returns the content of this Lsp Message."""
    content = {
        "jsonrpc": "2.0",
        "id": self.id,
        "method": self.method,
    }
    if self.params is not None:
      content["params"] = self.params
    return content

  def serialize(self) -> bytes:
    """Creates a LSP message with header and content components.

    Returns:
      A serialized LSP message, which contains a header and content
      section. The header describes the content, while the content itself is a
      utf-8 encoded json-rpc message.
    """
    return _serialize_content_with_header(self.get_content())

  @classmethod
  def from_content(cls, content: Dict[str, Any]) -> LspRequest:
    """Creates the LspRequest from a content dict.

    Returns:
      An LspRequest with values from 'content'

    Raises:
      ValueError: If the content does not contain the expected fields.
    """
    for key in ["id", "method"]:
      if key not in content:
        raise ValueError(f"Serialized LSP Request does not contain {key}")
    request = LspRequest(content["id"], content["method"])
    if "params" in content:
      request.params = content["params"]
    return request

  @classmethod
  def parse(cls, message: bytes) -> LspRequest:
    """Extracts the method name and rpc parameters of a given LSP message.

    Args:
      message: A string containing an LSP header and content segment.

    Returns:
      An LspRequest object containing the content from `message`.

    Raises:
      ValueError: The message cannot be parsed.
    """
    tokens = message.decode("utf-8").split("\r\n\r\n")
    if len(tokens) != 2:
      raise ValueError(r"Serialized LSP Request does not contain \r\n\r\n.")
    content = json.loads(tokens[1])
    return LspRequest.from_content(content)


# Lsp Error codes defined in the specification.
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603
SERVER_ERROR_START = JSON_RPC_RESERVED_ERROR_RANGE_START = -32099
SERVER_NOT_INITIALIZED = -32002
UNKNOWN_ERROR_CODE = -32001
JSON_RPC_RESERVED_ERROR_RANGE_END = -32000
SERVER_ERROR_END = JSON_RPC_RESERVED_ERROR_RANGE_END = -32800
LSP_RESERVED_ERROR_RANGE_START = -32899
CONTENT_MODIFIED = -32801
REQUEST_CANCELLED = -32800


@dataclasses.dataclass
class LspError:
  """Describes an error to be transmitted over the LSP protocol."""
  code: int
  message: str
  data: Optional[Any] = None

  def __str__(self) -> str:
    """Writes the LspError to a string."""
    res = f"Error[{self.code}] : {self.message}"
    if self.data is not None:
      res += f" : {self.data}"
    return res

  def get_content(self) -> Dict[str, Any]:
    """Returns the content of this Lsp Message."""
    content = {"code": self.code, "message": self.message}
    if self.data is not None:
      content["data"] = self.data
    return content

  @classmethod
  def from_content(cls, content: Dict[str, Any]) -> LspError:
    """Creates the LspError from a content dict.

    Returns:
      An LspError with values from 'content'

    Raises:
      ValueError: If the content does not contain the expected fields.
    """
    for key in ["code", "message"]:
      if key not in content:
        raise ValueError(f"Serialized LSP Error does not contain {key}")
    error = LspError(content["code"], content["message"])
    if "data" in content:
      error.data = content["data"]
    return error


@dataclasses.dataclass
class LspResponse:
  """Describes a response RPC."""
  id: int
  result: Optional[Any] = None
  error: Optional[LspError] = None

  def __str__(self) -> str:
    """Writes the LspResponse as a string."""
    tokens: List[str] = [f"Response[{self.id}]"]
    if self.error is not None:
      tokens.append(f"< {self.error} >")
    if self.result is not None:
      tokens.append(str(self.result))
    return " : ".join(tokens)

  def get_content(self) -> Dict[str, Any]:
    """Returns the content of this Lsp Message."""
    content = {"jsonrpc": "2.0", "id": self.id}
    if self.result is not None:
      content["result"] = self.result
    if self.error is not None:
      content["error"] = self.error.get_content()
    return content

  def serialize(self) -> bytes:
    """Creates a LSP message with header and content components.

    Returns:
      A serialized LSP message, which contains a header and content
      section. The header describes the content, while the content itself is a
      utf-8 encoded json-rpc message.
    """
    return _serialize_content_with_header(self.get_content())

  @classmethod
  def from_content(cls, content: Dict[str, Any]) -> LspResponse:
    """Creates the LspResponse from a content dict.

    Returns:
      An LspError with values from 'content'

    Raises:
      ValueError: If the content does not contain the expected fields.
    """
    if "id" not in content:
      raise ValueError("Serialized LSP Error does not contain id")
    response = LspResponse(content["id"])
    if "result" in content:
      response.result = content["result"]
    if "error" in content:
      response.error = LspError.from_content(content["error"])
    return response

  @classmethod
  def parse(cls, message: bytes) -> LspResponse:
    """Extracts the method name and rpc parameters of a given LSP message.

    Args:
      message: A string containing an LSP header and content segment.

    Returns:
      An LspResponse object containing the content from `message`.

    Raises:
      ValueError: The message cannot be parsed.
    """
    tokens = message.decode("utf-8").split("\r\n\r\n")
    if len(tokens) != 2:
      raise ValueError(r"Serialized LSP Response does not contain \r\n\r\n.")
    content = json.loads(tokens[1])
    return LspResponse.from_content(content)


# A type hint for specifying any of the LSP messages.
LspMessage = Union[LspResponse, LspRequest, LspNotification]


def parse(message: bytes) -> LspMessage:
  """Returns the correct LspMessage parsed from `message`.

  Args:
    message: A serialized LspMessage.

  Returns:
    An LspMessage. The type depends on the fields present in the content
    section of `message`.

  Raises:
    ValueError: If `message` cannot be parsed by any LspMessage type.
  """
  try:
    return LspNotification.parse(message)
  except ValueError:
    pass
  try:
    return LspRequest.parse(message)
  except ValueError:
    pass
  try:
    return LspResponse.parse(message)
  except ValueError:
    pass
  raise ValueError(f"Could not parse `message` as any LspMessage: {message}")
