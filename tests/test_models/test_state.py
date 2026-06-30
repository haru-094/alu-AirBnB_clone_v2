#!/usr/bin/python3
"""Unit tests for the State class."""
import unittest
import os
from models.state import State
from models.base_model import BaseModel

IS_DB = os.getenv("HBNB_TYPE_STORAGE") == "db"


class TestStateInstantiation(unittest.TestCase):
    """Tests for State instantiation."""

    def test_is_basemodel_subclass(self):
        """Test that State is a subclass of BaseModel."""
        obj = State()
        self.assertIsInstance(obj, BaseModel)

    @unittest.skipIf(IS_DB, "State.name is a Column in DBStorage")
    def test_name_class_attr(self):
        """Test that name is a class attribute and empty string (FileStorage)."""
        self.assertEqual(State.name, "")

    @unittest.skipIf(IS_DB, "State.name is a Column in DBStorage")
    def test_name_is_string(self):
        """Test that name class attribute type is str (FileStorage)."""
        self.assertIsInstance(State.name, str)

    @unittest.skipIf(not IS_DB, "Only for DBStorage")
    def test_name_is_column(self):
        """Test that name is a SQLAlchemy Column in DBStorage."""
        from sqlalchemy import Column
        self.assertIsInstance(State.name.property.columns[0], Column)

    def test_str_representation(self):
        """Test that str representation contains State."""
        obj = State()
        self.assertIn("State", str(obj))

    def test_to_dict_class_is_state(self):
        """Test that to_dict has __class__ equal to State."""
        obj = State()
        self.assertEqual(obj.to_dict()["__class__"], "State")

    def test_kwargs_instantiation(self):
        """Test instantiation from dictionary."""
        obj = State()
        obj_dict = obj.to_dict()
        new_obj = State(**obj_dict)
        self.assertEqual(obj.id, new_obj.id)

    def test_instance_name_can_be_set(self):
        """Test that name can be set as instance attribute."""
        obj = State()
        obj.name = "Rwanda"
        self.assertEqual(obj.name, "Rwanda")

    @unittest.skipIf(IS_DB, "cities property only in FileStorage")
    def test_cities_property_filestorage(self):
        """Test that cities returns a list for FileStorage."""
        from models import storage
        from models.city import City
        obj = State()
        obj.name = "Kenya"
        storage.new(obj)
        city = City()
        city.name = "Nairobi"
        city.state_id = obj.id
        storage.new(city)
        self.assertIsInstance(obj.cities, list)
        self.assertIn(city, obj.cities)


if __name__ == "__main__":
    unittest.main()
