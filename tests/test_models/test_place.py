#!/usr/bin/python3
"""Unittest cases for Place model"""
import os
import unittest
from tests.test_models.test_base_model import test_basemodel
from models.place import Place

storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')


class test_Place(test_basemodel):
    """Test cases for Place class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """Test city_id attribute type"""
        new = self.value()
        self.assertEqual(type(new.city_id), str)

    def test_user_id(self):
        """Test user_id attribute type"""
        new = self.value()
        self.assertEqual(type(new.user_id), str)

    def test_name(self):
        """Test name attribute type"""
        new = self.value()
        self.assertEqual(type(new.name), str)

    def test_description(self):
        """Test description attribute type"""
        new = self.value()
        self.assertEqual(type(new.description), str)

    def test_number_rooms(self):
        """Test number_rooms attribute type"""
        new = self.value()
        self.assertEqual(type(new.number_rooms), int)

    def test_number_bathrooms(self):
        """Test number_bathrooms attribute type"""
        new = self.value()
        self.assertEqual(type(new.number_bathrooms), int)

    def test_max_guest(self):
        """Test max_guest attribute type"""
        new = self.value()
        self.assertEqual(type(new.max_guest), int)

    def test_price_by_night(self):
        """Test price_by_night attribute type"""
        new = self.value()
        self.assertEqual(type(new.price_by_night), int)

    def test_latitude(self):
        """Test latitude attribute type"""
        new = self.value()
        self.assertEqual(type(new.latitude), float)

    def test_longitude(self):
        """Test longitude attribute type"""
        new = self.value()
        self.assertEqual(type(new.latitude), float)

    @unittest.skipIf(storage_type == 'db', 'FileStorage only')
    def test_amenity_ids(self):
        """Test amenity_ids attribute type"""
        new = self.value()
        self.assertEqual(type(new.amenity_ids), list)

    def test_is_subclass(self):
        """Test that Place is a subclass of BaseModel"""
        from models.base_model import BaseModel
        new = self.value()
        self.assertIsInstance(new, BaseModel)

    def test_has_city_id(self):
        """Test that Place has city_id attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'city_id'))

    def test_has_user_id(self):
        """Test that Place has user_id attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'user_id'))

    def test_has_name(self):
        """Test that Place has name attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'name'))

    def test_str_representation(self):
        """Test __str__ includes class name"""
        new = self.value()
        self.assertIn('Place', str(new))

    def test_to_dict_class_name(self):
        """Test that to_dict contains correct __class__ value"""
        new = self.value()
        d = new.to_dict()
        self.assertEqual(d['__class__'], 'Place')

    @unittest.skipIf(storage_type == 'db', 'FileStorage only')
    def test_numeric_defaults_file(self):
        """Test numeric attributes default to 0 in file storage"""
        new = self.value()
        self.assertEqual(new.number_rooms, 0)
        self.assertEqual(new.number_bathrooms, 0)
        self.assertEqual(new.max_guest, 0)
        self.assertEqual(new.price_by_night, 0)

    @unittest.skipIf(storage_type == 'db', 'FileStorage only')
    def test_float_defaults_file(self):
        """Test float attributes default to 0.0 in file storage"""
        new = self.value()
        self.assertEqual(new.latitude, 0.0)
        self.assertEqual(new.longitude, 0.0)
