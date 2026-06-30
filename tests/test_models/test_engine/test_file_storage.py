#!/usr/bin/python3
"""Unit tests for the FileStorage class."""
import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage

IS_DB = os.getenv("HBNB_TYPE_STORAGE") == "db"


@unittest.skipIf(IS_DB, "FileStorage tests not applicable for DBStorage")
class TestFileStorageInstantiation(unittest.TestCase):
    """Tests for FileStorage instantiation."""

    def test_no_args(self):
        """Test that FileStorage can be instantiated without args."""
        self.assertIsInstance(FileStorage(), FileStorage)

    def test_storage_is_filestorage(self):
        """Test that the storage variable is a FileStorage instance."""
        self.assertIsInstance(storage, FileStorage)

    def test_file_path_is_private(self):
        """Test that __file_path is a private class attribute."""
        self.assertFalse(hasattr(FileStorage(), "__file_path"))

    def test_objects_is_private(self):
        """Test that __objects is a private class attribute."""
        self.assertFalse(hasattr(FileStorage(), "__objects"))


@unittest.skipIf(IS_DB, "FileStorage tests not applicable for DBStorage")
class TestFileStorageAll(unittest.TestCase):
    """Tests for FileStorage all method."""

    def test_all_returns_dict(self):
        """Test that all() returns a dictionary."""
        self.assertIsInstance(storage.all(), dict)

    def test_all_returns_same_dict(self):
        """Test that all() returns the same dict object consistently."""
        self.assertIs(storage.all(), storage.all())

    def test_all_with_class_filter(self):
        """Test that all(State) returns only State objects."""
        s = State()
        s.name = "FilterTest"
        storage.new(s)
        result = storage.all(State)
        for key in result:
            self.assertTrue(key.startswith("State."))

    def test_all_with_class_string_filter(self):
        """Test that all('State') filters correctly using string class name."""
        s = State()
        s.name = "StringFilter"
        storage.new(s)
        result = storage.all("State")
        for key in result:
            self.assertTrue(key.startswith("State."))

    def test_all_with_none_returns_all(self):
        """Test that all(None) returns all objects."""
        result_none = storage.all(None)
        result_plain = storage.all()
        self.assertEqual(result_none, result_plain)


@unittest.skipIf(IS_DB, "FileStorage tests not applicable for DBStorage")
class TestFileStorageNew(unittest.TestCase):
    """Tests for FileStorage new method."""

    def test_new_adds_object(self):
        """Test that new() adds an object to __objects."""
        obj = BaseModel()
        storage.new(obj)
        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, storage.all())

    def test_new_adds_user(self):
        """Test that new() adds a User object."""
        obj = User()
        storage.new(obj)
        key = "User.{}".format(obj.id)
        self.assertIn(key, storage.all())


@unittest.skipIf(IS_DB, "FileStorage tests not applicable for DBStorage")
class TestFileStorageSave(unittest.TestCase):
    """Tests for FileStorage save method."""

    def test_save_creates_file(self):
        """Test that save() creates file.json."""
        obj = BaseModel()
        storage.new(obj)
        storage.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_file_is_valid_json(self):
        """Test that the saved file contains valid JSON."""
        obj = BaseModel()
        storage.new(obj)
        storage.save()
        with open("file.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)

    def test_save_includes_basemodel(self):
        """Test that saved file includes BaseModel object."""
        obj = BaseModel()
        storage.new(obj)
        storage.save()
        with open("file.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, data)


@unittest.skipIf(IS_DB, "FileStorage tests not applicable for DBStorage")
class TestFileStorageReload(unittest.TestCase):
    """Tests for FileStorage reload method."""

    def test_reload_does_not_raise_if_no_file(self):
        """Test that reload does not raise if file.json doesn't exist."""
        if os.path.exists("file.json"):
            os.rename("file.json", "file.json.bak")
        try:
            storage.reload()
        except Exception as e:
            self.fail("reload raised an exception: {}".format(e))
        finally:
            if os.path.exists("file.json.bak"):
                os.rename("file.json.bak", "file.json")

    def test_reload_restores_objects(self):
        """Test that reload restores previously saved objects."""
        obj = BaseModel()
        storage.new(obj)
        storage.save()
        old_id = obj.id
        storage.reload()
        key = "BaseModel.{}".format(old_id)
        self.assertIn(key, storage.all())

    def test_reload_restores_user(self):
        """Test that reload restores User objects."""
        obj = User()
        obj.email = "test@test.com"
        storage.new(obj)
        storage.save()
        old_id = obj.id
        storage.reload()
        key = "User.{}".format(old_id)
        self.assertIn(key, storage.all())

    def test_reload_all_classes(self):
        """Test that reload handles all supported classes."""
        classes = [State, City, Amenity, Place, Review]
        ids = []
        for cls in classes:
            obj = cls()
            storage.new(obj)
            ids.append((cls.__name__, obj.id))
        storage.save()
        storage.reload()
        for class_name, obj_id in ids:
            key = "{}.{}".format(class_name, obj_id)
            self.assertIn(key, storage.all())


@unittest.skipIf(IS_DB, "FileStorage tests not applicable for DBStorage")
class TestFileStorageDelete(unittest.TestCase):
    """Tests for FileStorage delete method."""

    def test_delete_removes_object(self):
        """Test that delete() removes an object from __objects."""
        obj = State()
        obj.name = "DeleteMe"
        storage.new(obj)
        key = "State.{}".format(obj.id)
        self.assertIn(key, storage.all())
        storage.delete(obj)
        self.assertNotIn(key, storage.all())

    def test_delete_none_does_nothing(self):
        """Test that delete(None) does not raise or change anything."""
        before = len(storage.all())
        try:
            storage.delete(None)
        except Exception as e:
            self.fail("delete(None) raised: {}".format(e))
        after = len(storage.all())
        self.assertEqual(before, after)

    def test_delete_nonexistent_object_is_safe(self):
        """Test that deleting an object not in __objects is safe."""
        obj = State()
        obj.name = "Ghost"
        # Do not call storage.new(obj) — obj is not tracked
        try:
            storage.delete(obj)
        except Exception as e:
            self.fail("delete of untracked object raised: {}".format(e))


@unittest.skipIf(not IS_DB, "DBStorage tests only")
class TestDBStorage(unittest.TestCase):
    """Tests for DBStorage using MySQLdb for direct verification."""

    def _get_count(self, table):
        """Return the row count of a MySQL table using MySQLdb."""
        import MySQLdb
        conn = MySQLdb.connect(
            host=os.getenv("HBNB_MYSQL_HOST", "localhost"),
            user=os.getenv("HBNB_MYSQL_USER"),
            passwd=os.getenv("HBNB_MYSQL_PWD"),
            db=os.getenv("HBNB_MYSQL_DB")
        )
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM {}".format(table))
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count

    def test_all_returns_dict(self):
        """Test that DBStorage.all() returns a dict."""
        self.assertIsInstance(storage.all(), dict)

    def test_all_with_state_class(self):
        """Test that DBStorage.all(State) returns only State objects."""
        result = storage.all(State)
        for key in result:
            self.assertTrue(key.startswith("State."))

    def test_new_and_save_state(self):
        """Test that saving a State adds one row to the states table."""
        before = self._get_count("states")
        s = State(name="DBTestState")
        s.save()
        after = self._get_count("states")
        self.assertEqual(after - before, 1)
        storage.delete(s)
        storage.save()

    def test_delete_state(self):
        """Test that deleting a State removes one row from the states table."""
        s = State(name="ToDeleteDB")
        s.save()
        before = self._get_count("states")
        storage.delete(s)
        storage.save()
        after = self._get_count("states")
        self.assertEqual(before - after, 1)

    def test_storage_is_dbstorage(self):
        """Test that storage is a DBStorage instance."""
        from models.engine.db_storage import DBStorage
        self.assertIsInstance(storage, DBStorage)


if __name__ == "__main__":
    unittest.main()
