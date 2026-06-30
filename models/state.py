#!/usr/bin/python3
"""This module defines the State class."""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Represents a State.

    Attributes (DBStorage):
        __tablename__ (str): The MySQL table name.
        name (Column): The state name — max 128 chars, required.
        cities (relationship): One-to-many relationship to City objects.
                               Deleting a State cascades to its Cities.

    Attributes (FileStorage):
        name (str): The state name.
        cities (property): List of City instances whose state_id matches
                           this State's id.
    """

    __tablename__ = "states"

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship(
            "City",
            backref="state",
            cascade="all, delete-orphan"
        )
    else:
        name = ""

        @property
        def cities(self):
            """Return list of City instances linked to this State."""
            from models import storage
            from models.city import City
            return [
                city for city in storage.all(City).values()
                if city.state_id == self.id
            ]
