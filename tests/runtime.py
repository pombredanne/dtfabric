# -*- coding: utf-8 -*-
"""Tests for the run-time object."""

import unittest
import uuid

from dtfabric import data_types
from dtfabric import definitions
from dtfabric import errors
from dtfabric import runtime

from tests import test_lib


class EmptyDataTypeDefinition(data_types.DataTypeDefinition):
  """Empty data type definition for testing."""

  def GetAttributeNames(self):
    """Determines the attribute (or field) names of the data type definition.

    Returns:
      list[str]: attribute names.
    """
    return [u'empty']

  def GetByteSize(self):
    """Determines the byte size of the data type definition.

    Returns:
      int: data type size in bytes or None if size cannot be determined.
    """
    return

  def GetStructByteOrderString(self):
    """Retrieves the Python struct format string.

    Returns:
      str: format string as used by Python struct or None if format string
          cannot be determined.
    """
    return

  def GetStructFormatString(self):
    """Retrieves the Python struct format string.

    Returns:
      str: format string as used by Python struct or None if format string
          cannot be determined.
    """
    return


class StructOperationTest(test_lib.BaseTestCase):
  """Python struct-base byte stream operation tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    byte_stream_operation = runtime.StructOperation(u'b')
    self.assertIsNotNone(byte_stream_operation)

    with self.assertRaises(errors.FormatError):
      runtime.StructOperation(None)

    with self.assertRaises(errors.FormatError):
      runtime.StructOperation(u'z')

  def testReadFrom(self):
    """Tests the ReadFrom function."""
    byte_stream_operation = runtime.StructOperation(u'i')

    value = byte_stream_operation.ReadFrom(b'\x12\x34\x56\x78')
    self.assertEqual(value, (0x78563412, ))

    with self.assertRaises(IOError):
      byte_stream_operation.ReadFrom(None)

    with self.assertRaises(IOError):
      byte_stream_operation.ReadFrom(b'\x12\x34\x56')


class StructureValuesClassFactoryTest(test_lib.BaseTestCase):
  """Structure values class factory tests."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the __init__ function."""
    definitions_file = self._GetTestFilePath([u'integer.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)
    data_type_definition = definitions_registry.GetDefinitionByName(u'int32le')

    data_type_map = runtime.DataTypeMap(data_type_definition)
    self.assertIsNotNone(data_type_map)

  @test_lib.skipUnlessHasTestFile([u'structure.yaml'])
  def testCreateClassTemplate(self):
    """Tests the _CreateClassTemplate function."""
    definitions_file = self._GetTestFilePath([u'structure.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'point3d')

    class_template = runtime.StructureValuesClassFactory._CreateClassTemplate(
        data_type_definition)
    self.assertIsNotNone(class_template)

    # TODO: implement error conditions.

  def testIsIdentifier(self):
    """Tests the _IsIdentifier function."""
    result = runtime.StructureValuesClassFactory._IsIdentifier(u'valid')
    self.assertTrue(result)

    result = runtime.StructureValuesClassFactory._IsIdentifier(u'_valid')
    self.assertTrue(result)

    result = runtime.StructureValuesClassFactory._IsIdentifier(u'valid1')
    self.assertTrue(result)

    result = runtime.StructureValuesClassFactory._IsIdentifier(u'')
    self.assertFalse(result)

    result = runtime.StructureValuesClassFactory._IsIdentifier(u'0invalid')
    self.assertFalse(result)

    result = runtime.StructureValuesClassFactory._IsIdentifier(u'in-valid')
    self.assertFalse(result)

  def testValidateDataTypeDefinition(self):
    """Tests the _ValidateDataTypeDefinition function."""
    definitions_file = self._GetTestFilePath([u'structure.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'point3d')

    runtime.StructureValuesClassFactory._ValidateDataTypeDefinition(
        data_type_definition)

    # TODO: implement error conditions.

  def testCreateClass(self):
    """Tests the CreateClass function."""
    definitions_file = self._GetTestFilePath([u'structure.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'point3d')

    structure_values_class = runtime.StructureValuesClassFactory.CreateClass(
        data_type_definition)
    self.assertIsNotNone(structure_values_class)


class DataTypeMapContextTest(test_lib.BaseTestCase):
  """Data type map context tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    data_type_map_context = runtime.DataTypeMapContext()
    self.assertIsNotNone(data_type_map_context)


@test_lib.skipUnlessHasTestFile([u'integer.yaml'])
class DataTypeMapTest(test_lib.BaseTestCase):
  """Data type map tests."""

  # pylint: disable=protected-access

  def testGetByteStreamOperation(self):
    """Tests the _GetByteStreamOperation function."""
    definitions_file = self._GetTestFilePath([u'integer.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)
    data_type_definition = definitions_registry.GetDefinitionByName(u'int32le')

    data_type_map = runtime.DataTypeMap(data_type_definition)

    operation = data_type_map._GetByteStreamOperation(data_type_definition)
    self.assertIsInstance(operation, runtime.StructOperation)

    with self.assertRaises(errors.FormatError):
      data_type_map._GetByteStreamOperation(None)

    with self.assertRaises(errors.FormatError):
      data_type_definition = EmptyDataTypeDefinition(u'empty')
      data_type_map._GetByteStreamOperation(data_type_definition)

  def testGetStructByteOrderString(self):
    """Tests the _GetStructByteOrderString function."""
    definitions_file = self._GetTestFilePath([u'integer.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)
    data_type_definition = definitions_registry.GetDefinitionByName(u'int32le')

    data_type_map = runtime.DataTypeMap(data_type_definition)

    format_string = data_type_map._GetStructByteOrderString(
        data_type_definition)
    self.assertEqual(format_string, u'<')

    with self.assertRaises(errors.FormatError):
      data_type_map._GetStructByteOrderString(None)

    with self.assertRaises(errors.FormatError):
      data_type_definition = EmptyDataTypeDefinition(u'empty')
      data_type_map._GetStructByteOrderString(data_type_definition)

  def testGetStructFormatString(self):
    """Tests the _GetStructFormatString function."""
    definitions_file = self._GetTestFilePath([u'integer.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)
    data_type_definition = definitions_registry.GetDefinitionByName(u'int32le')

    data_type_map = runtime.DataTypeMap(data_type_definition)

    format_string = data_type_map._GetStructFormatString(data_type_definition)
    self.assertEqual(format_string, u'i')

    with self.assertRaises(errors.FormatError):
      data_type_map._GetStructFormatString(None)

    with self.assertRaises(errors.FormatError):
      data_type_definition = EmptyDataTypeDefinition(u'empty')
      data_type_map._GetStructFormatString(data_type_definition)

  def testGetByteSize(self):
    """Tests the GetByteSize function."""
    definitions_file = self._GetTestFilePath([u'integer.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)
    data_type_definition = definitions_registry.GetDefinitionByName(u'int32le')

    data_type_map = runtime.DataTypeMap(data_type_definition)

    byte_size = data_type_map.GetByteSize()
    self.assertEqual(byte_size, 4)


@test_lib.skipUnlessHasTestFile([u'integer.yaml'])
class PrimitiveDataTypeMapTest(test_lib.BaseTestCase):
  """Primitive data type map tests."""

  def testMapByteStream(self):
    """Tests the MapByteStream function."""
    definitions_file = self._GetTestFilePath([u'integer.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'int32le')
    data_type_map = runtime.PrimitiveDataTypeMap(data_type_definition)

    integer_value = data_type_map.MapByteStream(b'\x01\x00\x00\x00')
    self.assertEqual(integer_value, 1)

  def testMapValue(self):
    """Tests the MapValue function."""
    definitions_file = self._GetTestFilePath([u'integer.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'int32le')
    data_type_map = runtime.PrimitiveDataTypeMap(data_type_definition)

    integer_value = data_type_map.MapValue(1)
    self.assertEqual(integer_value, 1)


@test_lib.skipUnlessHasTestFile([u'definitions', u'booleans.yaml'])
class BooleanMapTest(test_lib.BaseTestCase):
  """Boolean map tests."""

  def testInitialize(self):
    """Tests the __init__ function."""
    definitions_file = self._GetTestFilePath([u'definitions', u'booleans.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)
    data_type_definition = definitions_registry.GetDefinitionByName(u'bool32')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN

    data_type_definition.false_value = None
    data_type_definition.true_value = None
    with self.assertRaises(errors.FormatError):
      runtime.BooleanMap(data_type_definition)

  def testMapByteStream(self):
    """Tests the MapByteStream function."""
    definitions_file = self._GetTestFilePath([u'definitions', u'booleans.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'bool8')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN
    data_type_map = runtime.BooleanMap(data_type_definition)
    data_type_definition.true_value = 1

    bool_value = data_type_map.MapByteStream(b'\x00')
    self.assertFalse(bool_value)

    bool_value = data_type_map.MapByteStream(b'\x01')
    self.assertTrue(bool_value)

    with self.assertRaises(errors.MappingError):
      data_type_map.MapByteStream(b'\xff')

    data_type_definition = definitions_registry.GetDefinitionByName(u'bool16')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN
    data_type_definition.false_value = None
    data_type_definition.true_value = 1
    data_type_map = runtime.BooleanMap(data_type_definition)

    bool_value = data_type_map.MapByteStream(b'\xff\xff')
    self.assertFalse(bool_value)

    bool_value = data_type_map.MapByteStream(b'\x01\x00')
    self.assertTrue(bool_value)

    data_type_definition = definitions_registry.GetDefinitionByName(u'bool32')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN
    data_type_definition.true_value = None
    data_type_map = runtime.BooleanMap(data_type_definition)

    bool_value = data_type_map.MapByteStream(b'\x00\x00\x00\x00')
    self.assertFalse(bool_value)

    bool_value = data_type_map.MapByteStream(b'\xff\xff\xff\xff')
    self.assertTrue(bool_value)

    with self.assertRaises(errors.MappingError):
      data_type_map.MapByteStream(b'\x01\x00')


@test_lib.skipUnlessHasTestFile([u'definitions', u'characters.yaml'])
class CharacterMapTest(test_lib.BaseTestCase):
  """Character map tests."""

  def testMapByteStream(self):
    """Tests the MapByteStream function."""
    definitions_file = self._GetTestFilePath([
        u'definitions', u'characters.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'char')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN
    data_type_map = runtime.CharacterMap(data_type_definition)

    string_value = data_type_map.MapByteStream(b'\x41')
    self.assertEqual(string_value, u'A')

    data_type_definition = definitions_registry.GetDefinitionByName(u'wchar16')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN
    data_type_map = runtime.CharacterMap(data_type_definition)

    string_value = data_type_map.MapByteStream(b'\xb6\x24')
    self.assertEqual(string_value, u'\u24b6')

    data_type_definition = definitions_registry.GetDefinitionByName(u'wchar32')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN
    data_type_map = runtime.CharacterMap(data_type_definition)

    string_value = data_type_map.MapByteStream(b'\xb6\x24\x00\x00')
    self.assertEqual(string_value, u'\u24b6')

    with self.assertRaises(errors.MappingError):
      data_type_map.MapByteStream(b'\xb6\x24')


@test_lib.skipUnlessHasTestFile([u'definitions', u'floating-points.yaml'])
class FloatingPointMapTest(test_lib.BaseTestCase):
  """Floating-point map tests."""

  def testMapByteStream(self):
    """Tests the MapByteStream function."""
    definitions_file = self._GetTestFilePath([
        u'definitions', u'floating-points.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'float32')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN
    data_type_map = runtime.FloatingPointMap(data_type_definition)

    float_value = data_type_map.MapByteStream(b'\xa4\x70\x45\x41')
    self.assertEqual(float_value, 12.34000015258789)

    data_type_definition = definitions_registry.GetDefinitionByName(u'float64')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN
    data_type_map = runtime.FloatingPointMap(data_type_definition)

    float_value = data_type_map.MapByteStream(
        b'\xae\x47\xe1\x7a\x14\xae\x28\x40')
    self.assertEqual(float_value, 12.34)

    with self.assertRaises(errors.MappingError):
      data_type_map.MapByteStream(b'\xa4\x70\x45\x41')


@test_lib.skipUnlessHasTestFile([u'definitions', u'integers.yaml'])
class IntegerMapTest(test_lib.BaseTestCase):
  """Integer map tests."""

  def testMapByteStream(self):
    """Tests the MapByteStream function."""
    definitions_file = self._GetTestFilePath([u'definitions', u'integers.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'uint8')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN
    data_type_map = runtime.IntegerMap(data_type_definition)

    integer_value = data_type_map.MapByteStream(b'\x12')
    self.assertEqual(integer_value, 0x12)

    data_type_definition = definitions_registry.GetDefinitionByName(u'uint16')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN
    data_type_map = runtime.IntegerMap(data_type_definition)

    integer_value = data_type_map.MapByteStream(b'\x12\x34')
    self.assertEqual(integer_value, 0x3412)

    data_type_definition = definitions_registry.GetDefinitionByName(u'uint32')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN
    data_type_map = runtime.IntegerMap(data_type_definition)

    integer_value = data_type_map.MapByteStream(b'\x12\x34\x56\x78')
    self.assertEqual(integer_value, 0x78563412)

    data_type_definition = definitions_registry.GetDefinitionByName(u'uint32')
    data_type_definition.byte_order = definitions.BYTE_ORDER_BIG_ENDIAN
    data_type_map = runtime.IntegerMap(data_type_definition)

    integer_value = data_type_map.MapByteStream(b'\x12\x34\x56\x78')
    self.assertEqual(integer_value, 0x12345678)

    data_type_definition = definitions_registry.GetDefinitionByName(u'uint64')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN
    data_type_map = runtime.IntegerMap(data_type_definition)

    integer_value = data_type_map.MapByteStream(
        b'\x12\x34\x56\x78\x9a\xbc\xde\xf0')
    self.assertEqual(integer_value, 0xf0debc9a78563412)

    with self.assertRaises(errors.MappingError):
      data_type_map.MapByteStream(b'\x12\x34\x56\x78')


@test_lib.skipUnlessHasTestFile([u'sequence.yaml'])
class SequenceMapTest(test_lib.BaseTestCase):
  """Sequence map tests."""

  # pylint: disable=protected-access

  def testInitialize(self):
    """Tests the __init__ function."""
    definitions_file = self._GetTestFilePath([u'sequence.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)
    data_type_definition = definitions_registry.GetDefinitionByName(u'vector4')

    data_type_map = runtime.SequenceMap(data_type_definition)
    self.assertIsNotNone(data_type_map)

  def testGetElementDataTypeDefinition(self):
    """Tests the _GetElementDataTypeDefinition function."""
    definitions_file = self._GetTestFilePath([u'sequence.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)
    data_type_definition = definitions_registry.GetDefinitionByName(u'vector4')

    data_type_map = runtime.SequenceMap(data_type_definition)

    element_data_type_definition = data_type_map._GetElementDataTypeDefinition(
        data_type_definition)
    self.assertIsNotNone(element_data_type_definition)

    with self.assertRaises(errors.FormatError):
      data_type_map._GetElementDataTypeDefinition(None)

    with self.assertRaises(errors.FormatError):
      data_type_definition = EmptyDataTypeDefinition(u'empty')
      data_type_map._GetElementDataTypeDefinition(data_type_definition)

  def testMapByteStream(self):
    """Tests the MapByteStream function."""
    definitions_file = self._GetTestFilePath([u'sequence.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)
    data_type_definition = definitions_registry.GetDefinitionByName(u'vector4')

    data_type_map = runtime.SequenceMap(data_type_definition)

    sequence_value = data_type_map.MapByteStream(
        b'\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00')
    self.assertEqual(sequence_value, (1, 2, 3, 4))

    with self.assertRaises(errors.MappingError):
      data_type_map.MapByteStream(None)

    with self.assertRaises(errors.MappingError):
      data_type_map.MapByteStream(b'\x12\x34\x56')


class StructureMapTest(test_lib.BaseTestCase):
  """Structure map tests."""

  # pylint: disable=protected-access

  @test_lib.skipUnlessHasTestFile([u'structure.yaml'])
  def testInitialize(self):
    """Tests the __init__ function."""
    definitions_file = self._GetTestFilePath([u'structure.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'point3d')
    data_type_map = runtime.StructureMap(data_type_definition)
    self.assertIsNotNone(data_type_map)

  @test_lib.skipUnlessHasTestFile([u'structure.yaml'])
  def testCheckCompositeMap(self):
    """Tests the _CheckCompositeMap function."""
    definitions_file = self._GetTestFilePath([u'structure.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'point3d')
    data_type_map = runtime.StructureMap(data_type_definition)

    result = data_type_map._CheckCompositeMap(data_type_definition)
    self.assertFalse(result)

    with self.assertRaises(errors.FormatError):
      data_type_map._CheckCompositeMap(None)

    with self.assertRaises(errors.FormatError):
      data_type_definition = EmptyDataTypeDefinition(u'empty')
      data_type_map._CheckCompositeMap(data_type_definition)

    data_type_definition = definitions_registry.GetDefinitionByName(
        u'triangle3d')
    data_type_map = runtime.StructureMap(data_type_definition)

    result = data_type_map._CheckCompositeMap(data_type_definition)
    self.assertTrue(result)

    data_type_definition = definitions_registry.GetDefinitionByName(u'box3d')
    data_type_map = runtime.StructureMap(data_type_definition)

    result = data_type_map._CheckCompositeMap(data_type_definition)
    self.assertTrue(result)

    data_type_definition = definitions_registry.GetDefinitionByName(
        u'sphere3d')
    data_type_map = runtime.StructureMap(data_type_definition)

    result = data_type_map._CheckCompositeMap(data_type_definition)
    self.assertTrue(result)

  @test_lib.skipUnlessHasTestFile([u'structure.yaml'])
  def testGetByteStreamOperation(self):
    """Tests the _GetByteStreamOperation function."""
    definitions_file = self._GetTestFilePath([u'structure.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)
    data_type_definition = definitions_registry.GetDefinitionByName(u'point3d')

    data_type_map = runtime.StructureMap(data_type_definition)

    operation = data_type_map._GetByteStreamOperation(data_type_definition)
    self.assertIsInstance(operation, runtime.StructOperation)

    with self.assertRaises(errors.FormatError):
      data_type_map._GetByteStreamOperation(None)

    with self.assertRaises(errors.FormatError):
      data_type_definition = EmptyDataTypeDefinition(u'empty')
      data_type_map._GetByteStreamOperation(data_type_definition)

  @test_lib.skipUnlessHasTestFile([u'structure.yaml'])
  def testGetMemberDataTypeMaps(self):
    """Tests the _GetMemberDataTypeMaps function."""
    definitions_file = self._GetTestFilePath([u'structure.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)
    data_type_definition = definitions_registry.GetDefinitionByName(u'point3d')

    data_type_map = runtime.StructureMap(data_type_definition)

    members_data_type_maps = data_type_map._GetMemberDataTypeMaps(
        data_type_definition, {})
    self.assertIsNotNone(members_data_type_maps)

    with self.assertRaises(errors.FormatError):
      data_type_map._GetMemberDataTypeMaps(None, {})

    with self.assertRaises(errors.FormatError):
      data_type_definition = EmptyDataTypeDefinition(u'empty')
      data_type_map._GetMemberDataTypeMaps(data_type_definition, {})

  @test_lib.skipUnlessHasTestFile([u'structure.yaml'])
  def testMapByteStream(self):
    """Tests the MapByteStream function."""
    definitions_file = self._GetTestFilePath([u'structure.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'point3d')
    data_type_map = runtime.StructureMap(data_type_definition)

    byte_values = []
    for value in range(1, 4):
      byte_value_upper, byte_value_lower = divmod(value, 256)
      byte_values.extend([byte_value_lower, byte_value_upper, 0, 0])

    byte_stream = bytes(bytearray(byte_values))

    named_tuple = data_type_map.MapByteStream(byte_stream)
    self.assertEqual(named_tuple.x, 1)
    self.assertEqual(named_tuple.y, 2)
    self.assertEqual(named_tuple.z, 3)

  @test_lib.skipUnlessHasTestFile([u'structure.yaml'])
  def testMapByteStreamWithSequence(self):
    """Tests the MapByteStream function with a sequence."""
    definitions_file = self._GetTestFilePath([u'structure.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'box3d')
    data_type_map = runtime.StructureMap(data_type_definition)

    byte_values = []
    for value in range(1, 433):
      byte_value_upper, byte_value_lower = divmod(value, 256)
      byte_values.extend([byte_value_lower, byte_value_upper, 0, 0])

    byte_stream = bytes(bytearray(byte_values))

    box = data_type_map.MapByteStream(byte_stream)
    self.assertEqual(box.triangles[0].a.x, 1)
    self.assertEqual(box.triangles[0].a.y, 2)
    self.assertEqual(box.triangles[0].a.z, 3)

  @test_lib.skipUnlessHasTestFile([u'structure.yaml'])
  def testMapByteStreamWithSequenceWithExpression(self):
    """Tests the MapByteStream function with a sequence with expression."""
    definitions_file = self._GetTestFilePath([u'structure.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'sphere3d')
    data_type_map = runtime.StructureMap(data_type_definition)

    byte_values = [3, 0, 0, 0]
    for value in range(1, 113):
      byte_value_upper, byte_value_lower = divmod(value, 256)
      byte_values.extend([byte_value_lower, byte_value_upper, 0, 0])

    byte_stream = bytes(bytearray(byte_values))

    sphere = data_type_map.MapByteStream(byte_stream)
    self.assertEqual(sphere.number_of_triangles, 3)
    self.assertEqual(sphere.triangles[0].a.x, 1)
    self.assertEqual(sphere.triangles[0].a.y, 2)
    self.assertEqual(sphere.triangles[0].a.z, 3)

    self.assertEqual(sphere.triangles[0].b.x, 4)
    self.assertEqual(sphere.triangles[0].b.y, 5)
    self.assertEqual(sphere.triangles[0].b.z, 6)

    self.assertEqual(sphere.triangles[0].c.x, 7)
    self.assertEqual(sphere.triangles[0].c.y, 8)
    self.assertEqual(sphere.triangles[0].c.z, 9)

  @test_lib.skipUnlessHasTestFile([u'structure2.yaml'])
  def testMapByteStreamWithSequenceWithExpression2(self):
    """Tests the MapByteStream function with a sequence with expression."""
    definitions_file = self._GetTestFilePath([u'structure2.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(
        u'extension_block')
    data_type_map = runtime.StructureMap(data_type_definition)

    byte_values = [4, 1, 0, 0]
    for byte_value in range(0, 256):
      byte_values.extend([byte_value])

    byte_stream = bytes(bytearray(byte_values))

    extension_block = data_type_map.MapByteStream(byte_stream)
    self.assertEqual(extension_block.size, 260)
    self.assertEqual(extension_block.data[0], 0)
    self.assertEqual(extension_block.data[-1], 255)

    byte_values = [3, 0, 0, 0]
    for byte_value in range(0, 256):
      byte_values.extend([byte_value])

    byte_stream = bytes(bytearray(byte_values))

    with self.assertRaises(errors.MappingError):
      data_type_map.MapByteStream(byte_stream)


@test_lib.skipUnlessHasTestFile([u'uuid.yaml'])
class UUIDMapTest(test_lib.BaseTestCase):
  """UUID map tests."""

  def testMapByteStream(self):
    """Tests the MapByteStream function."""
    definitions_file = self._GetTestFilePath([u'uuid.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'uuid')
    data_type_definition.byte_order = definitions.BYTE_ORDER_LITTLE_ENDIAN
    data_type_map = runtime.UUIDMap(data_type_definition)

    expected_uuid_value = uuid.UUID(u'{00021401-0000-0000-c000-000000000046}')
    uuid_value = data_type_map.MapByteStream(
        b'\x01\x14\x02\x00\x00\x00\x00\x00\xc0\x00\x00\x00\x00\x00\x00\x46')
    self.assertEqual(uuid_value, expected_uuid_value)


@test_lib.skipUnlessHasTestFile([u'integer.yaml'])
class DataTypeMapFactoryTest(test_lib.BaseTestCase):
  """Data type map factory tests."""

  def testCreateDataTypeMap(self):
    """Tests the CreateDataTypeMap function."""
    definitions_file = self._GetTestFilePath([u'integer.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = EmptyDataTypeDefinition(u'empty')
    definitions_registry.RegisterDefinition(data_type_definition)

    factory = runtime.DataTypeMapFactory(definitions_registry)

    data_type_map = factory.CreateDataTypeMap(u'int32le')
    self.assertIsNotNone(data_type_map)

    data_type_map = factory.CreateDataTypeMap(u'empty')
    self.assertIsNone(data_type_map)

    data_type_map = factory.CreateDataTypeMap(u'bogus')
    self.assertIsNone(data_type_map)

  def testCreateDataTypeMapByType(self):
    """Tests the CreateDataTypeMapByType function."""
    definitions_file = self._GetTestFilePath([u'integer.yaml'])
    definitions_registry = self._CreateDefinitionRegistryFromFile(
        definitions_file)

    data_type_definition = definitions_registry.GetDefinitionByName(u'int32le')
    data_type_map = runtime.DataTypeMapFactory.CreateDataTypeMapByType(
        data_type_definition)
    self.assertIsNotNone(data_type_map)

    data_type_definition = EmptyDataTypeDefinition(u'empty')
    data_type_map = runtime.DataTypeMapFactory.CreateDataTypeMapByType(
        data_type_definition)
    self.assertIsNone(data_type_map)


if __name__ == '__main__':
  unittest.main()
