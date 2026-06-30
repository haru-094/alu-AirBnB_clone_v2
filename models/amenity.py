#!/usr/bin/python3
"""This module defines the Amenity class."""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Represents an Amenity.

    Attributes (DBStorage):
        __tablename__ (str): The MySQL table name.
        name (Column): Amenity name — max 128 chars, required.
        place_amenities (relationship): Many-to-Many relationship to Place
                                        via the place_amenity association table.

    Attributes (FileStorage):
        name (str): The amenity name.
    """

    __tablename__ = "amenities"

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
            "Place",
            secondary="place_amenity",
            viewonly=False,
            overlaps="amenities"
        )
    else:
        name = ""
