#!/usr/bin/python3
"""This module defines the User class."""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Represents a User.

    Attributes (DBStorage):
        __tablename__ (str): The MySQL table name.
        email (Column): User email address — max 128 chars, required.
        password (Column): User password — max 128 chars, required.
        first_name (Column): User first name — max 128 chars, nullable.
        last_name (Column): User last name — max 128 chars, nullable.
        places (relationship): One-to-many to Place. Cascades on delete.
        reviews (relationship): One-to-many to Review. Cascades on delete.

    Attributes (FileStorage):
        email (str): User email address.
        password (str): User password.
        first_name (str): User first name.
        last_name (str): User last name.
    """

    __tablename__ = "users"

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship(
            "Place",
            backref="user",
            cascade="all, delete-orphan"
        )
        reviews = relationship(
            "Review",
            backref="user",
            cascade="all, delete-orphan"
        )
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
