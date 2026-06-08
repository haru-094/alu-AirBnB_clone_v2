#!/usr/bin/python3
"""Unittest cases for BaseModel"""
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')


class test_basemodel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """Set up test environment"""
        pass

    def tearDown(self):
        """Clean up after each test"""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_default(self):
        """Test default instantiation"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Test instantiation with kwargs from to_dict"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """Test that integer key in kwargs raises TypeError"""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    @unittest.skipIf(storage_type == 'db', 'Not applicable for db storage')
    def test_save(self):
        """Testing save writes to file.json"""
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_save_updates_updated_at(self):
        """Test that save() updates the updated_at timestamp"""
        i = self.value()
        old_updated = i.updated_at
        i.save()
        self.assertGreaterEqual(i.updated_at, old_updated)

    def test_str(self):
        """Test string representation format"""
        i = self.value()
        s = str(i)
        self.assertIn('[{}]'.format(self.name), s)
        self.assertIn('({})'.format(i.id), s)

    def test_todict(self):
        """Test to_dict returns correct dict"""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_to_dict_contains_class_key(self):
        """Test that to_dict contains __class__ key"""
        i = self.value()
        d = i.to_dict()
        self.assertIn('__class__', d)
        self.assertEqual(d['__class__'], self.name)

    def test_to_dict_type(self):
        """Test that to_dict returns a dict"""
        i = self.value()
        self.assertIsInstance(i.to_dict(), dict)

    def test_to_dict_datetime_strings(self):
        """Test that created_at and updated_at are ISO strings in to_dict"""
        i = self.value()
        d = i.to_dict()
        self.assertIsInstance(d['created_at'], str)
        self.assertIsInstance(d['updated_at'], str)

    def test_kwargs_none(self):
        """Test that None key raises TypeError"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """Test instantiation with minimal kwargs (v2: no KeyError expected)"""
        n = {'Name': 'test'}
        new = self.value(**n)
        self.assertIsInstance(new, BaseModel)
        self.assertIsInstance(new.id, str)
        self.assertIsInstance(new.created_at, datetime.datetime)
        self.assertIsInstance(new.updated_at, datetime.datetime)

    def test_id(self):
        """Test that id is a string"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_id_is_unique(self):
        """Test that two instances have different ids"""
        a = self.value()
        b = self.value()
        self.assertNotEqual(a.id, b.id)

    def test_created_at(self):
        """Test created_at is a datetime object"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """Test updated_at is a datetime object"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new2 = BaseModel(**n)
        self.assertEqual(type(new2.updated_at), datetime.datetime)
        self.assertEqual(type(new2.created_at), datetime.datetime)

    def test_instantiation_no_args(self):
        """Test that BaseModel can be instantiated with no args"""
        obj = self.value()
        self.assertIsNotNone(obj)

    def test_is_instance(self):
        """Test that instance is of correct type"""
        obj = self.value()
        self.assertIsInstance(obj, BaseModel)

    def test_has_id(self):
        """Test that new instance has an id attribute"""
        obj = self.value()
        self.assertTrue(hasattr(obj, 'id'))

    def test_has_created_at(self):
        """Test that new instance has created_at attribute"""
        obj = self.value()
        self.assertTrue(hasattr(obj, 'created_at'))

    def test_has_updated_at(self):
        """Test that new instance has updated_at attribute"""
        obj = self.value()
        self.assertTrue(hasattr(obj, 'updated_at'))

    @unittest.skipIf(storage_type == 'db', 'Not applicable for db storage')
    def test_base_model_no_file_before_save(self):
        """Test that file.json is not created by instantiation alone"""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass
        obj = self.value()
        self.assertFalse(os.path.exists('file.json'))


    def test_str_format(self):
        """Test __str__ output format is correct"""
        obj = self.value()
        s = str(obj)
        self.assertIn('[', s)
        self.assertIn(']', s)
        self.assertIn(obj.id, s)
