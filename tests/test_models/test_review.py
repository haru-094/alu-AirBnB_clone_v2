#!/usr/bin/python3
"""Unit tests for the Review class."""
import unittest
import os
from models.review import Review
from models.base_model import BaseModel

IS_DB = os.getenv("HBNB_TYPE_STORAGE") == "db"


class TestReviewInstantiation(unittest.TestCase):
    """Tests for Review instantiation."""

    def test_is_basemodel_subclass(self):
        """Test that Review is a subclass of BaseModel."""
        obj = Review()
        self.assertIsInstance(obj, BaseModel)

    @unittest.skipIf(IS_DB, "Review.place_id is a Column in DBStorage")
    def test_place_id_class_attr(self):
        """Test that place_id is a class attribute and empty string."""
        self.assertEqual(Review.place_id, "")

    @unittest.skipIf(IS_DB, "Review.user_id is a Column in DBStorage")
    def test_user_id_class_attr(self):
        """Test that user_id is a class attribute and empty string."""
        self.assertEqual(Review.user_id, "")

    @unittest.skipIf(IS_DB, "Review.text is a Column in DBStorage")
    def test_text_class_attr(self):
        """Test that text is a class attribute and empty string."""
        self.assertEqual(Review.text, "")

    @unittest.skipIf(IS_DB, "Review.place_id is a Column in DBStorage")
    def test_place_id_is_string(self):
        """Test that place_id attribute type is str."""
        self.assertIsInstance(Review.place_id, str)

    @unittest.skipIf(IS_DB, "Review.user_id is a Column in DBStorage")
    def test_user_id_is_string(self):
        """Test that user_id attribute type is str."""
        self.assertIsInstance(Review.user_id, str)

    @unittest.skipIf(IS_DB, "Review.text is a Column in DBStorage")
    def test_text_is_string(self):
        """Test that text attribute type is str."""
        self.assertIsInstance(Review.text, str)

    @unittest.skipIf(not IS_DB, "Only for DBStorage")
    def test_columns_are_sqlalchemy_columns(self):
        """Test that Review attributes are SQLAlchemy Columns in DBStorage."""
        from sqlalchemy import Column
        self.assertIsInstance(Review.text.property.columns[0], Column)
        self.assertIsInstance(Review.place_id.property.columns[0], Column)
        self.assertIsInstance(Review.user_id.property.columns[0], Column)

    def test_str_representation(self):
        """Test that str representation contains Review."""
        obj = Review()
        self.assertIn("Review", str(obj))

    def test_to_dict_class_is_review(self):
        """Test that to_dict has __class__ equal to Review."""
        obj = Review()
        self.assertEqual(obj.to_dict()["__class__"], "Review")

    def test_kwargs_instantiation(self):
        """Test instantiation from dictionary."""
        obj = Review()
        obj_dict = obj.to_dict()
        new_obj = Review(**obj_dict)
        self.assertEqual(obj.id, new_obj.id)

    def test_instance_attributes_settable(self):
        """Test that attributes can be set on Review instances."""
        obj = Review()
        obj.text = "Great place!"
        obj.place_id = "some-place-id"
        obj.user_id = "some-user-id"
        self.assertEqual(obj.text, "Great place!")
        self.assertEqual(obj.place_id, "some-place-id")
        self.assertEqual(obj.user_id, "some-user-id")


if __name__ == "__main__":
    unittest.main()
