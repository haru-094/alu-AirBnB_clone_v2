#!/usr/bin/python3
"""Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage
import os


storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')


@unittest.skipIf(storage_type == 'db', 'FileStorage tests only')
class test_fileStorage(unittest.TestCase):
    """Class to test the file storage method"""

    def setUp(self):
        """Set up test environment"""
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """Remove storage file at end of tests"""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_obj_list_empty(self):
        """__objects is initially empty after setUp"""
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """New object is correctly added to __objects via storage.new()"""
        new = BaseModel()
        storage.new(new)
        found = False
        for obj in storage.all().values():
            if obj is new:
                found = True
        self.assertTrue(found)

    def test_all(self):
        """__objects is properly returned as dict"""
        new = BaseModel()
        new.save()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_all_returns_dict(self):
        """storage.all() always returns a dict"""
        self.assertIsInstance(storage.all(), dict)

    def test_base_model_instantiation(self):
        """File is not created on BaseModel instantiation (only on save)"""
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """Data is saved to file after save()"""
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """FileStorage save method creates file"""
        new = BaseModel()
        storage.new(new)
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """Storage file is successfully loaded to __objects"""
        new = BaseModel()
        new.save()
        storage.reload()
        found = False
        for obj in storage.all().values():
            if obj.to_dict()['id'] == new.to_dict()['id']:
                found = True
        self.assertTrue(found)

    def test_reload_from_nonexistent(self):
        """Nothing happens if file does not exist"""
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """BaseModel save() calls storage.new() and storage.save()"""
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """Confirm __file_path is string"""
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """Confirm __objects is a dict"""
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """Key is properly formatted as ClassName.id"""
        new = BaseModel()
        new.save()
        _id = new.id
        temp = None
        for key in storage.all().keys():
            if key.endswith(_id):
                temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """FileStorage object storage created"""
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(storage), FileStorage)

    def test_new_adds_to_objects(self):
        """storage.new() adds object to __objects"""
        new = BaseModel()
        storage.new(new)
        key = 'BaseModel.' + new.id
        self.assertIn(key, storage.all())

    def test_save_creates_file(self):
        """save() creates the JSON file"""
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.isfile('file.json'))

    def test_reload_restores_objects(self):
        """reload() restores objects from file"""
        new = BaseModel()
        new.save()
        storage._FileStorage__objects = {}
        storage.reload()
        self.assertGreater(len(storage.all()), 0)

    def test_save_and_reload_preserves_id(self):
        """Object id is preserved after save and reload"""
        new = BaseModel()
        orig_id = new.id
        new.save()
        storage._FileStorage__objects = {}
        storage.reload()
        key = 'BaseModel.' + orig_id
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].id, orig_id)

    def test_multiple_objects_stored(self):
        """Multiple objects can be stored and retrieved"""
        obj1 = BaseModel()
        obj2 = BaseModel()
        obj1.save()
        obj2.save()
        self.assertGreaterEqual(len(storage.all()), 2)

    def test_file_path_default(self):
        """Default file path is file.json"""
        self.assertEqual(storage._FileStorage__file_path, 'file.json')


class test_storage_general(unittest.TestCase):
    """Storage-agnostic tests that run with any storage engine"""

    def test_storage_has_all(self):
        """storage object has all() method"""
        self.assertTrue(hasattr(storage, 'all'))

    def test_storage_has_new(self):
        """storage object has new() method"""
        self.assertTrue(hasattr(storage, 'new'))

    def test_storage_has_save(self):
        """storage object has save() method"""
        self.assertTrue(hasattr(storage, 'save'))

    def test_storage_has_reload(self):
        """storage object has reload() method"""
        self.assertTrue(hasattr(storage, 'reload'))

    def test_storage_all_returns_dict(self):
        """storage.all() returns a dictionary"""
        result = storage.all()
        self.assertIsInstance(result, dict)
