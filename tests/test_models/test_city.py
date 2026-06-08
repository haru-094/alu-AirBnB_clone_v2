#!/usr/bin/python3
"""Unittest cases for City model"""
import os
import unittest
from tests.test_models.test_base_model import test_basemodel
from models.city import City

storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')


class test_City(test_basemodel):
    """Test cases for City class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """Test state_id attribute type"""
        new = self.value()
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """Test name attribute type"""
        new = self.value()
        self.assertEqual(type(new.name), str)

    def test_is_subclass(self):
        """Test that City is a subclass of BaseModel"""
        from models.base_model import BaseModel
        new = self.value()
        self.assertIsInstance(new, BaseModel)

    def test_has_name(self):
        """Test that City has name attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'name'))

    def test_has_state_id(self):
        """Test that City has state_id attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'state_id'))

    def test_str_representation(self):
        """Test __str__ includes class name"""
        new = self.value()
        self.assertIn('City', str(new))

    def test_to_dict_class_name(self):
        """Test that to_dict contains correct __class__ value"""
        new = self.value()
        d = new.to_dict()
        self.assertEqual(d['__class__'], 'City')

    @unittest.skipIf(storage_type == 'db', 'FileStorage only')
    def test_state_id_default_file(self):
        """Test state_id defaults to empty string in file storage"""
        new = self.value()
        self.assertEqual(new.state_id, '')

    @unittest.skipIf(storage_type == 'db', 'FileStorage only')
    def test_name_default_file(self):
        """Test name defaults to empty string in file storage"""
        new = self.value()
        self.assertEqual(new.name, '')
