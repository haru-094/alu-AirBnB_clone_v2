#!/usr/bin/python3
"""Unit tests for the BaseModel class."""
import unittest
import os
import time
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModelInstantiation(unittest.TestCase):
    """Tests for BaseModel instantiation."""

    def test_no_args(self):
        """Test that BaseModel can be instantiated without arguments."""
        obj = BaseModel()
        self.assertIsInstance(obj, BaseModel)

    def test_id_is_string(self):
        """Test that id is a string."""
        obj = BaseModel()
        self.assertIsInstance(obj.id, str)

    def test_id_is_unique(self):
        """Test that two instances have different ids."""
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.assertNotEqual(obj1.id, obj2.id)

    def test_created_at_is_datetime(self):
        """Test that created_at is a datetime object."""
        obj = BaseModel()
        self.assertIsInstance(obj.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """Test that updated_at is a datetime object."""
        obj = BaseModel()
        self.assertIsInstance(obj.updated_at, datetime)

    def test_created_updated_at_equal_on_creation(self):
        """Test that created_at and updated_at are close on creation."""
        obj = BaseModel()
        self.assertAlmostEqual(
            obj.created_at.timestamp(),
            obj.updated_at.timestamp(),
            delta=0.1
        )

    def test_kwargs_instantiation(self):
        """Test instantiation with keyword arguments."""
        obj = BaseModel()
        obj_dict = obj.to_dict()
        new_obj = BaseModel(**obj_dict)
        self.assertEqual(obj.id, new_obj.id)
        self.assertEqual(obj.created_at, new_obj.created_at)
        self.assertEqual(obj.updated_at, new_obj.updated_at)

    def test_kwargs_does_not_add_class_key(self):
        """Test that __class__ key is not added as attribute."""
        obj = BaseModel()
        obj_dict = obj.to_dict()
        new_obj = BaseModel(**obj_dict)
        self.assertNotIn("__class__", new_obj.__dict__)

    def test_kwargs_datetime_converted(self):
        """Test that datetime strings are converted back to datetime."""
        obj = BaseModel()
        obj_dict = obj.to_dict()
        new_obj = BaseModel(**obj_dict)
        self.assertIsInstance(new_obj.created_at, datetime)
        self.assertIsInstance(new_obj.updated_at, datetime)

    def test_kwargs_not_same_object(self):
        """Test that the new object is not the same as the original."""
        obj = BaseModel()
        obj_dict = obj.to_dict()
        new_obj = BaseModel(**obj_dict)
        self.assertIsNot(obj, new_obj)

    def test_args_not_used(self):
        """Test that positional args are not used."""
        obj = BaseModel("arg1", "arg2")
        self.assertIsInstance(obj, BaseModel)

    def test_partial_kwargs_sets_id(self):
        """Test that partial kwargs still generates an id."""
        obj = BaseModel(name="Test")
        self.assertIsNotNone(obj.id)
        self.assertIsInstance(obj.id, str)

    def test_partial_kwargs_sets_created_at(self):
        """Test that partial kwargs still sets created_at."""
        obj = BaseModel(name="Test")
        self.assertIsInstance(obj.created_at, datetime)


class TestBaseModelSave(unittest.TestCase):
    """Tests for the BaseModel save method."""

    def test_save_updates_updated_at(self):
        """Test that save updates the updated_at attribute."""
        obj = BaseModel()
        old_updated = obj.updated_at
        time.sleep(0.05)
        obj.save()
        self.assertGreater(obj.updated_at, old_updated)

    def test_save_does_not_change_created_at(self):
        """Test that save does not change created_at."""
        obj = BaseModel()
        old_created = obj.created_at
        obj.save()
        self.assertEqual(obj.created_at, old_created)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db",
        "file.json not used in DBStorage"
    )
    def test_save_creates_file(self):
        """Test that save creates the JSON file (FileStorage only)."""
        obj = BaseModel()
        obj.save()
        self.assertTrue(os.path.exists("file.json"))

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") != "db",
        "Only applicable for DBStorage"
    )
    def test_save_persists_to_db(self):
        """Test that save commits the object (DBStorage only)."""
        from models import storage
        from models.state import State
        s = State(name="TestPersist")
        s.save()
        key = "State.{}".format(s.id)
        self.assertIn(key, storage.all())
        storage.delete(s)
        storage.save()


class TestBaseModelToDict(unittest.TestCase):
    """Tests for the BaseModel to_dict method."""

    def test_to_dict_returns_dict(self):
        """Test that to_dict returns a dictionary."""
        obj = BaseModel()
        self.assertIsInstance(obj.to_dict(), dict)

    def test_to_dict_has_class_key(self):
        """Test that to_dict result has __class__ key."""
        obj = BaseModel()
        self.assertIn("__class__", obj.to_dict())

    def test_to_dict_class_value(self):
        """Test that __class__ value is 'BaseModel'."""
        obj = BaseModel()
        self.assertEqual(obj.to_dict()["__class__"], "BaseModel")

    def test_to_dict_has_id(self):
        """Test that to_dict result has id key."""
        obj = BaseModel()
        self.assertIn("id", obj.to_dict())

    def test_to_dict_has_created_at(self):
        """Test that to_dict result has created_at key."""
        obj = BaseModel()
        self.assertIn("created_at", obj.to_dict())

    def test_to_dict_has_updated_at(self):
        """Test that to_dict result has updated_at key."""
        obj = BaseModel()
        self.assertIn("updated_at", obj.to_dict())

    def test_to_dict_created_at_is_string(self):
        """Test that created_at in to_dict is a string."""
        obj = BaseModel()
        self.assertIsInstance(obj.to_dict()["created_at"], str)

    def test_to_dict_updated_at_is_string(self):
        """Test that updated_at in to_dict is a string."""
        obj = BaseModel()
        self.assertIsInstance(obj.to_dict()["updated_at"], str)

    def test_to_dict_datetime_format(self):
        """Test that datetime strings use ISO format."""
        obj = BaseModel()
        d = obj.to_dict()
        fmt = "%Y-%m-%dT%H:%M:%S.%f"
        try:
            datetime.strptime(d["created_at"], fmt)
            datetime.strptime(d["updated_at"], fmt)
        except ValueError:
            self.fail("Datetime strings are not in ISO format")

    def test_to_dict_contains_custom_attributes(self):
        """Test that custom attributes appear in to_dict."""
        obj = BaseModel()
        obj.name = "Test"
        obj.number = 42
        d = obj.to_dict()
        self.assertEqual(d["name"], "Test")
        self.assertEqual(d["number"], 42)

    def test_to_dict_not_same_as_instance_dict(self):
        """Test that to_dict result is not the instance __dict__."""
        obj = BaseModel()
        self.assertIsNot(obj.to_dict(), obj.__dict__)

    def test_to_dict_no_sa_instance_state(self):
        """Test that _sa_instance_state is not in to_dict output."""
        obj = BaseModel()
        self.assertNotIn("_sa_instance_state", obj.to_dict())


class TestBaseModelDelete(unittest.TestCase):
    """Tests for the BaseModel delete method."""

    def test_delete_method_exists(self):
        """Test that delete method exists on BaseModel instances."""
        obj = BaseModel()
        self.assertTrue(hasattr(obj, "delete"))
        self.assertTrue(callable(obj.delete))


if __name__ == "__main__":
    unittest.main()
