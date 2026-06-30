#!/usr/bin/python3
"""Unit tests for the Amenity class."""
import unittest
import os
from models.amenity import Amenity
from models.base_model import BaseModel

IS_DB = os.getenv("HBNB_TYPE_STORAGE") == "db"


class TestAmenityInstantiation(unittest.TestCase):
    """Tests for Amenity instantiation."""

    def test_is_basemodel_subclass(self):
        """Test that Amenity is a subclass of BaseModel."""
        obj = Amenity()
        self.assertIsInstance(obj, BaseModel)

    @unittest.skipIf(IS_DB, "Amenity.name is a Column in DBStorage")
    def test_name_class_attr(self):
        """Test that name is a class attribute and empty string."""
        self.assertEqual(Amenity.name, "")

    @unittest.skipIf(IS_DB, "Amenity.name is a Column in DBStorage")
    def test_name_is_string(self):
        """Test that name attribute type is str."""
        self.assertIsInstance(Amenity.name, str)

    @unittest.skipIf(not IS_DB, "Only for DBStorage")
    def test_name_is_column(self):
        """Test that name is a SQLAlchemy Column in DBStorage."""
        from sqlalchemy import Column
        self.assertIsInstance(Amenity.name.property.columns[0], Column)

    def test_str_representation(self):
        """Test that str representation contains Amenity."""
        obj = Amenity()
        self.assertIn("Amenity", str(obj))

    def test_to_dict_class_is_amenity(self):
        """Test that to_dict has __class__ equal to Amenity."""
        obj = Amenity()
        self.assertEqual(obj.to_dict()["__class__"], "Amenity")

    def test_kwargs_instantiation(self):
        """Test instantiation from dictionary."""
        obj = Amenity()
        obj_dict = obj.to_dict()
        new_obj = Amenity(**obj_dict)
        self.assertEqual(obj.id, new_obj.id)

    def test_instance_name_can_be_set(self):
        """Test that name can be set as an instance attribute."""
        obj = Amenity()
        obj.name = "WiFi"
        self.assertEqual(obj.name, "WiFi")


if __name__ == "__main__":
    unittest.main()
