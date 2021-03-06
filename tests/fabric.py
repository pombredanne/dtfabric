# -*- coding: utf-8 -*-
"""Tests for the dtFabric helper objects."""

import os
import unittest

from dtfabric import fabric

from tests import test_lib


class DataTypeFabricTest(test_lib.BaseTestCase):
  """Data type fabric tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    definitions_file = os.path.join(u'data', u'definitions', u'core.yaml')

    with open(definitions_file, 'rb') as file_object:
      yaml_definition = file_object.read()

    factory = fabric.DataTypeFabric(yaml_definition=yaml_definition)
    self.assertIsNotNone(factory)


if __name__ == '__main__':
  unittest.main()
