#!/usr/bin/python3
"""This module defines the Review class."""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Represents a Review.

    Attributes (DBStorage):
        __tablename__ (str): The MySQL table name.
        text (Column): Review text — max 1024 chars, required.
        place_id (Column): FK to places.id, required.
        user_id (Column): FK to users.id, required.
        Back-reference from a Review to its Place is named 'place'.
        Back-reference from a Review to its User is named 'user'.

    Attributes (FileStorage):
        place_id (str): The id of the linked Place.
        user_id (str): The id of the linked User.
        text (str): The review text.
    """

    __tablename__ = "reviews"

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""
