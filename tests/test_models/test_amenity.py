#!/usr/bin/python3
"""Unittest cases for Amenity model"""
import os
import unittest
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity

storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')


class test_Amenity(test_basemodel):
    """Test cases for Amenity class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """Test name attribute type"""
        new = self.value()
        self.assertEqual(type(new.name), str)

    def test_is_subclass(self):
        """Test that Amenity is a subclass of BaseModel"""
        from models.base_model import BaseModel
        new = self.value()
        self.assertIsInstance(new, BaseModel)

    def test_has_name(self):
        """Test that Amenity has name attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'name'))

    def test_str_representation(self):
        """Test __str__ includes class name"""
        new = self.value()
        self.assertIn('Amenity', str(new))

    def test_to_dict_class_name(self):
        """Test that to_dict contains correct __class__ value"""
        new = self.value()
        d = new.to_dict()
        self.assertEqual(d['__class__'], 'Amenity')

    @unittest.skipIf(storage_type == 'db', 'FileStorage only')
    def test_name_default_file(self):
        """Test name defaults to empty string in file storage"""
        new = self.value()
        self.assertEqual(new.name, '')

    def test_instantiation(self):
        """Test that Amenity can be instantiated"""
        new = self.value()
        self.assertIsNotNone(new)

    def test_to_dict_has_id(self):
        """Test that to_dict contains id"""
        new = self.value()
        d = new.to_dict()
        self.assertIn('id', d)
