#!/usr/bin/python3
"""Unittest cases for State model"""
import os
import unittest
from tests.test_models.test_base_model import test_basemodel
from models.state import State

storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')


class test_state(test_basemodel):
    """Test cases for State class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """Test name attribute type"""
        new = self.value()
        self.assertEqual(type(new.name), str)

    def test_is_subclass(self):
        """Test that State is a subclass of BaseModel"""
        from models.base_model import BaseModel
        new = self.value()
        self.assertIsInstance(new, BaseModel)

    def test_has_name(self):
        """Test that State has name attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'name'))

    def test_str_representation(self):
        """Test __str__ includes class name"""
        new = self.value()
        self.assertIn('State', str(new))

    def test_to_dict_class_name(self):
        """Test that to_dict contains correct __class__ value"""
        new = self.value()
        d = new.to_dict()
        self.assertEqual(d['__class__'], 'State')

    @unittest.skipIf(storage_type == 'db', 'FileStorage only')
    def test_cities_property_file(self):
        """Test that cities property returns a list (FileStorage)"""
        new = self.value()
        self.assertIsInstance(new.cities, list)

    def test_name_default_empty_string(self):
        """Test that name default is empty string (file storage)"""
        if storage_type != 'db':
            new = self.value()
            self.assertEqual(new.name, '')
