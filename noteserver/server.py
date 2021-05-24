"""Implements the IO for noteserver.

Language servers typically use stdin and stdout to communicate with editors. We
also want to be able to use custom files for unit and integration tests.

This module exposes a Server class that buffers messages from its input, sends
messages to its dispatcher callback, and forwards responses to its output.
"""

import io
from typing import Iterable
from noteserver import lsp_message


def lsp_message_source(
    buffered_reader: io.BufferedIOBase) -> Iterable[lsp_message.LspMessage]:
  """Yields LspMessages present in the buffered_reader.

  The full LspMessage format is described in lsp_message.py

  Args:
    buffered_reader: An open source of bytes that another source will write
    serialized LspMessages to. Generation ends when this source is closed.

  Yields:
    LspMessages parsed from the buffered_reader as they arrive.

  Raises:
    ValueError: The bytes stream encounters an error or bytes that cannot be
    parsed.
  """
  # This buffer will fill until we can parse a full LspMessage.
  lsp_buffer = bytearray()
  while not buffered_reader.closed:
    next_byte: bytes = buffered_reader.read(1)
    if not next_byte:
      break
    lsp_buffer.extend(next_byte)
    if lsp_buffer[-4:] != b"\r\n\r\n":
      continue

    # Now that we have the header, we need to know how much content to expect.
    # The header starts with this pattern: 'Content-Length: [0-9]+\r\n'
    first_space: int = lsp_buffer.find(b" ")
    if first_space < 0:
      raise ValueError(f"Failed to find the first space in: {lsp_buffer}")
    first_separator: int = lsp_buffer.find(b"\r\n")
    if first_separator < 0:
      raise ValueError(f"Failed to find the first separator in: {lsp_buffer}")
    if first_space > first_separator:
      raise ValueError(
          f"Space index {first_space} > Separator index {first_separator}")
    content_length = int(lsp_buffer[first_space:first_separator])
    content = buffered_reader.read(content_length)
    if len(content) != content_length:
      raise ValueError(
          f"Expected to read {content_length} bytes. Read {len(content)}")
    lsp_buffer.extend(content)
    yield lsp_message.parse(lsp_buffer)
    lsp_buffer.clear()
  # By the time we reach this, the buffer should be empty.
  if lsp_buffer:
    raise ValueError(f"Invalid input. Remaining buffer: {lsp_buffer}")
