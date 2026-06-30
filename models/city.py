#!/usr/bin/python3
"""This module defines the City class."""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Represents a City.

    Attributes (DBStorage):
        __tablename__ (str): The MySQL table name.
        name (Column): The city name — max 128 chars, required.
        state_id (Column): Foreign key referencing states.id, required.
        places (relationship): One-to-many relationship to Place objects.
                               Deleting a City cascades to its Places.

    Attributes (FileStorage):
        state_id (str): The id of the parent State.
        name (str): The city name.
    """

    __tablename__ = "cities"

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        places = relationship(
            "Place",
            backref="city",
            cascade="all, delete-orphan"
        )
    else:
        state_id = ""
        name = ""
