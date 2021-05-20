"""Utility functions for working with LSP Messages."""
from __future__ import annotations
import dataclasses
import json
from typing import Dict, Any, Optional


@dataclasses.dataclass
class LspRequest:
  """Describes a request RPC."""
  id: int
  method: str
  params: Optional[Dict[str, Any]]

  def __str__(self) -> str:
    """Writes the LspRequest as a string."""
    return f"{self.id} - {self.method} - {self.params}"

  def serialize(self) -> bytes:
    """Creates a LSP message with header and content components.

    Returns:
      A serialized LSP message, which contains a header and content
      section. The header describes the content, while the content itself is a
      utf-8 encoded json-rpc message.
    """
    content = json.dumps({
        "jsonrpc": "2.0",
        "id": self.id,
        "method": self.method,
        "params": self.params,
    }).encode("utf-8")
    # Each header parameter is terminated by \r\n, and the header itself is also
    # terminated by \r\n.
    header = (f"Content-Length: {len(content)}\r\n"
              "Content-Type: application/vscode-jsonrpc;charset=utf-8\r\n"
              "\r\n")
    return header.encode("utf-8") + content

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
