"""An example test. Presubmit will execute this."""

import unittest


class TestExample(unittest.TestCase):
  """An example test."""

  def test_always_true(self):
    """Always returns true."""
    self.assertEqual(1, 1)


if __name__ == "__main__":
  unittest.main()
