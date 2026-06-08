#!/usr/bin/python3
"""Unittest cases for Review model"""
import os
import unittest
from tests.test_models.test_base_model import test_basemodel
from models.review import Review

storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')


class test_review(test_basemodel):
    """Test cases for Review class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """Test place_id attribute type"""
        new = self.value()
        self.assertEqual(type(new.place_id), str)

    def test_user_id(self):
        """Test user_id attribute type"""
        new = self.value()
        self.assertEqual(type(new.user_id), str)

    def test_text(self):
        """Test text attribute type"""
        new = self.value()
        self.assertEqual(type(new.text), str)

    def test_is_subclass(self):
        """Test that Review is a subclass of BaseModel"""
        from models.base_model import BaseModel
        new = self.value()
        self.assertIsInstance(new, BaseModel)

    def test_has_place_id(self):
        """Test that Review has place_id attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'place_id'))

    def test_has_user_id(self):
        """Test that Review has user_id attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'user_id'))

    def test_has_text(self):
        """Test that Review has text attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'text'))

    def test_str_representation(self):
        """Test __str__ includes class name"""
        new = self.value()
        self.assertIn('Review', str(new))

    def test_to_dict_class_name(self):
        """Test that to_dict contains correct __class__ value"""
        new = self.value()
        d = new.to_dict()
        self.assertEqual(d['__class__'], 'Review')

    @unittest.skipIf(storage_type == 'db', 'FileStorage only')
    def test_defaults_file(self):
        """Test attribute defaults are empty strings in file storage"""
        new = self.value()
        self.assertEqual(new.place_id, '')
        self.assertEqual(new.user_id, '')
        self.assertEqual(new.text, '')
