#!/usr/bin/python3
"""Unit tests for the City class."""
import unittest
import os
from models.city import City
from models.base_model import BaseModel

IS_DB = os.getenv("HBNB_TYPE_STORAGE") == "db"


class TestCityInstantiation(unittest.TestCase):
    """Tests for City instantiation."""

    def test_is_basemodel_subclass(self):
        """Test that City is a subclass of BaseModel."""
        obj = City()
        self.assertIsInstance(obj, BaseModel)

    @unittest.skipIf(IS_DB, "City.state_id is a Column in DBStorage")
    def test_state_id_class_attr(self):
        """Test that state_id is a class attribute and empty string."""
        self.assertEqual(City.state_id, "")

    @unittest.skipIf(IS_DB, "City.name is a Column in DBStorage")
    def test_name_class_attr(self):
        """Test that name is a class attribute and empty string."""
        self.assertEqual(City.name, "")

    @unittest.skipIf(IS_DB, "City.state_id is a Column in DBStorage")
    def test_state_id_is_string(self):
        """Test that state_id attribute type is str."""
        self.assertIsInstance(City.state_id, str)

    @unittest.skipIf(IS_DB, "City.name is a Column in DBStorage")
    def test_name_is_string(self):
        """Test that name attribute type is str."""
        self.assertIsInstance(City.name, str)

    @unittest.skipIf(not IS_DB, "Only for DBStorage")
    def test_columns_are_sqlalchemy_columns(self):
        """Test that City attributes are SQLAlchemy Columns in DBStorage."""
        from sqlalchemy import Column
        self.assertIsInstance(City.name.property.columns[0], Column)
        self.assertIsInstance(City.state_id.property.columns[0], Column)

    def test_str_representation(self):
        """Test that str representation contains City."""
        obj = City()
        self.assertIn("City", str(obj))

    def test_to_dict_class_is_city(self):
        """Test that to_dict has __class__ equal to City."""
        obj = City()
        self.assertEqual(obj.to_dict()["__class__"], "City")

    def test_kwargs_instantiation(self):
        """Test instantiation from dictionary."""
        obj = City()
        obj_dict = obj.to_dict()
        new_obj = City(**obj_dict)
        self.assertEqual(obj.id, new_obj.id)

    def test_instance_attributes_settable(self):
        """Test that name and state_id can be set on City instances."""
        obj = City()
        obj.name = "Nairobi"
        obj.state_id = "some-state-id"
        self.assertEqual(obj.name, "Nairobi")
        self.assertEqual(obj.state_id, "some-state-id")


if __name__ == "__main__":
    unittest.main()
