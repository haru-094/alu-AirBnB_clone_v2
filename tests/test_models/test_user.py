#!/usr/bin/python3
"""Unit tests for the User class."""
import unittest
import os
import time
from models.user import User
from models.base_model import BaseModel

IS_DB = os.getenv("HBNB_TYPE_STORAGE") == "db"


class TestUserInstantiation(unittest.TestCase):
    """Tests for User instantiation."""

    def test_is_basemodel_subclass(self):
        """Test that User is a subclass of BaseModel."""
        obj = User()
        self.assertIsInstance(obj, BaseModel)

    @unittest.skipIf(IS_DB, "User.email is a Column in DBStorage")
    def test_email_class_attr(self):
        """Test that email is a class attribute and empty string."""
        self.assertEqual(User.email, "")

    @unittest.skipIf(IS_DB, "User.password is a Column in DBStorage")
    def test_password_class_attr(self):
        """Test that password is a class attribute and empty string."""
        self.assertEqual(User.password, "")

    @unittest.skipIf(IS_DB, "User.first_name is a Column in DBStorage")
    def test_first_name_class_attr(self):
        """Test that first_name is a class attribute and empty string."""
        self.assertEqual(User.first_name, "")

    @unittest.skipIf(IS_DB, "User.last_name is a Column in DBStorage")
    def test_last_name_class_attr(self):
        """Test that last_name is a class attribute and empty string."""
        self.assertEqual(User.last_name, "")

    @unittest.skipIf(IS_DB, "User.email is a Column in DBStorage")
    def test_email_is_string(self):
        """Test that email attribute type is str."""
        self.assertIsInstance(User.email, str)

    @unittest.skipIf(IS_DB, "User.password is a Column in DBStorage")
    def test_password_is_string(self):
        """Test that password attribute type is str."""
        self.assertIsInstance(User.password, str)

    @unittest.skipIf(IS_DB, "User.first_name is a Column in DBStorage")
    def test_first_name_is_string(self):
        """Test that first_name attribute type is str."""
        self.assertIsInstance(User.first_name, str)

    @unittest.skipIf(IS_DB, "User.last_name is a Column in DBStorage")
    def test_last_name_is_string(self):
        """Test that last_name attribute type is str."""
        self.assertIsInstance(User.last_name, str)

    @unittest.skipIf(not IS_DB, "Only for DBStorage")
    def test_columns_are_sqlalchemy_columns(self):
        """Test that User attributes are SQLAlchemy Columns in DBStorage."""
        from sqlalchemy import Column
        self.assertIsInstance(User.email.property.columns[0], Column)
        self.assertIsInstance(User.password.property.columns[0], Column)

    def test_str_representation(self):
        """Test that str representation contains User."""
        obj = User()
        self.assertIn("User", str(obj))

    def test_to_dict_class_is_user(self):
        """Test that to_dict has __class__ equal to User."""
        obj = User()
        self.assertEqual(obj.to_dict()["__class__"], "User")

    def test_kwargs_instantiation(self):
        """Test instantiation with keyword arguments."""
        obj = User()
        obj.email = "test@test.com"
        obj_dict = obj.to_dict()
        new_obj = User(**obj_dict)
        self.assertEqual(new_obj.email, "test@test.com")

    def test_instance_attributes_settable(self):
        """Test that instance attributes can be set on User."""
        obj = User()
        obj.email = "gania@alu.com"
        obj.password = "secret"
        self.assertEqual(obj.email, "gania@alu.com")
        self.assertEqual(obj.password, "secret")


class TestUserSave(unittest.TestCase):
    """Tests for User save method."""

    @unittest.skipIf(IS_DB, "Use test_save_updates_updated_at_db for DB")
    def test_save_updates_updated_at(self):
        """Test that save updates updated_at (FileStorage)."""
        obj = User()
        old = obj.updated_at
        time.sleep(0.05)
        obj.save()
        self.assertGreater(obj.updated_at, old)

    @unittest.skipIf(not IS_DB, "DBStorage version — requires valid fields")
    def test_save_updates_updated_at_db(self):
        """Test that save updates updated_at (DBStorage)."""
        from models import storage
        obj = User(email="savetest@db.com", password="testpwd123")
        old = obj.updated_at
        time.sleep(0.05)
        obj.save()
        self.assertGreater(obj.updated_at, old)
        storage.delete(obj)
        storage.save()


if __name__ == "__main__":
    unittest.main()
