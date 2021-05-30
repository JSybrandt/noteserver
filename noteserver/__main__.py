"""Launches noteserver!

```
# Example Usage:
python -m noteserver
```

The noteserver reads messages from stdin and writes to stdout.
"""

import sys
from typing import Optional
import logging
import fire
from noteserver import server


def main(verbose: bool = False, log_path: Optional[str] = None):
  """Launches Noteserver.

  Noteserver is a LSP server that works with most editors in order to help make
  taking notes easier! This program expects to receive LSP RPCs from stdin and
  will produce LSP RPCs to stdout.

  Args:
    verbose: Include for additional logging.
    log_path: Set to write debug logs to a file.
  """
  logging.basicConfig(filename=log_path,
                      filemode="w",
                      level=logging.DEBUG if verbose else logging.WARNING)

  # Start server!
  while True:
    try:
      logging.info("Starting server!")
      server.Server(reader=sys.stdin.buffer, writer=sys.stdout.buffer).run()
    except ValueError as error:
      logging.error("Encountered server error and restarting: %s", error)


if __name__ == "__main__":
  fire.Fire(main)
