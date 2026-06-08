#!/usr/bin/python3
"""Unittest cases for User model"""
import os
import unittest
from tests.test_models.test_base_model import test_basemodel
from models.user import User

storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')


class test_User(test_basemodel):
    """Test cases for User class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """Test first_name attribute type"""
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """Test last_name attribute type"""
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """Test email attribute type"""
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """Test password attribute type"""
        new = self.value()
        self.assertEqual(type(new.password), str)

    def test_is_subclass(self):
        """Test that User is a subclass of BaseModel"""
        from models.base_model import BaseModel
        new = self.value()
        self.assertIsInstance(new, BaseModel)

    def test_has_email(self):
        """Test that User has email attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'email'))

    def test_has_password(self):
        """Test that User has password attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'password'))

    def test_has_first_name(self):
        """Test that User has first_name attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'first_name'))

    def test_has_last_name(self):
        """Test that User has last_name attribute"""
        new = self.value()
        self.assertTrue(hasattr(new, 'last_name'))

    def test_str_representation(self):
        """Test __str__ includes class name"""
        new = self.value()
        self.assertIn('User', str(new))

    def test_to_dict_class_name(self):
        """Test that to_dict contains correct __class__ value"""
        new = self.value()
        d = new.to_dict()
        self.assertEqual(d['__class__'], 'User')
