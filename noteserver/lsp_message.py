"""Utility functions for working with LSP Messages."""
from __future__ import annotations
import dataclasses
import json
from typing import Dict, Any, Optional, List


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

  def serialize(self) -> bytes:
    """Creates a LSP message with header and content components.

    Returns:
      A serialized LSP message, which contains a header and content
      section. The header describes the content, while the content itself is a
      utf-8 encoded json-rpc message.
    """
    content = {
        "jsonrpc": "2.0",
        "id": self.id,
        "method": self.method,
    }
    if self.params is not None:
      content["params"] = self.params
    return _serialize_content_with_header(content)

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
    for key in ["id", "method", "params"]:
      if key not in content:
        raise ValueError(f"Serialized LSP Request does not contain {key}")
    return LspRequest(content["id"], content["method"], content["params"])


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
