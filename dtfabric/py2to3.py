# -*- coding: utf-8 -*-
"""The Python 2 and 3 compatible definitions."""

import sys


if sys.version_info[0] < 3:
  BYTES_TYPE = str
  INTEGER_TYPES = (int, long)
  STRING_TYPES = (basestring, )
  UNICHR = unichr
  UNICODE_TYPE = unicode
else:
  BYTES_TYPE = bytes
  INTEGER_TYPES = (int, )
  STRING_TYPES = (str, )
  UNICHR = chr
  UNICODE_TYPE = str
