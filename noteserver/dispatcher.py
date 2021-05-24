"""The Dispatcher is responsible for sending inbound RPCs to the right place.

The server receives LspMessages and sends them to the dispatcher. The
dispatcher sends the RPCs to relevant hooks, or produces a "not implemented"
error response.  The dispatcher may also need to manage state for RPCs that are
sent from the server to the client and await a response.

"""

from typing import Iterable
from noteserver import lsp_message


def _produce_not_impl_error(
    client_message: lsp_message.LspMessage) -> Iterable[lsp_message.LspMessage]:
  """If the client_message is a request, responds with not impl error.

  Produces no response if the client_message is not an LspRequest.

  Args:
    client_message: An RPC sent from the client.

  Returns:
    At most one LspResponse. Describes the method that was called but is not
    implemented.
  """
  if not isinstance(client_message, lsp_message.LspRequest):
    return []
  return [
      lsp_message.LspResponse(
          id=client_message.id,
          error=lsp_message.LspError(
              code=lsp_message.INTERNAL_ERROR,
              message=f"{client_message.method} not implemented",
              data=client_message.params))
  ]


class Dispatcher:  # pylint: disable=too-few-public-methods
  """Responsible for maintaining state between processes.

  Some functions may need to send and receive RPCs to and from the client.
  """

  def __call__(
      self, client_message: lsp_message.LspMessage
  ) -> Iterable[lsp_message.LspMessage]:
    """Reads one message and routes it to the correct process.

    Args:
      client_message: A single RPC sent from the client.

    Returns:
      An iterable that produces RPCs that need to be sent from the server to
      the client.
    """
    return _produce_not_impl_error(client_message)
