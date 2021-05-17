"""Tests for the flask server."""

from noteserver import server

import json
import unittest
from typing import *


class FlaskServerTest(unittest.TestCase):
  """Test for the flask server."""

  def setUp(self):
    self.flask_app = server.create_flask_server(name="test_server", is_testing=True)
    self.client = self.flask_app.test_client()


  def test_hello_world(self):
    self.client.post("/", data=self.RE)
