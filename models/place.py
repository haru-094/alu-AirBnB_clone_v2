#!/usr/bin/python3
"""This module defines the Place class."""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    # Association table for Place-Amenity Many-To-Many relationship
    place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column(
            "place_id",
            String(60),
            ForeignKey("places.id"),
            primary_key=True,
            nullable=False
        ),
        Column(
            "amenity_id",
            String(60),
            ForeignKey("amenities.id"),
            primary_key=True,
            nullable=False
        ),
        extend_existing=True
    )


class Place(BaseModel, Base):
    """Represents a Place.

    Attributes (DBStorage):
        __tablename__ (str): The MySQL table name.
        city_id (Column): FK to cities.id, required.
        user_id (Column): FK to users.id, required.
        name (Column): Place name — max 128 chars, required.
        description (Column): Place description — max 1024 chars, nullable.
        number_rooms (Column): Number of rooms, default 0, required.
        number_bathrooms (Column): Number of bathrooms, default 0, required.
        max_guest (Column): Max guest count, default 0, required.
        price_by_night (Column): Price per night, default 0, required.
        latitude (Column): Latitude coordinate, nullable.
        longitude (Column): Longitude coordinate, nullable.
        reviews (relationship): One-to-many to Review. Cascades on delete.
        amenities (relationship): Many-to-many to Amenity via place_amenity.

    Attributes (FileStorage):
        All of the above as plain Python class attributes with default values.
        amenity_ids (list): List of Amenity ids linked to this Place.
        amenities (property): Returns list of linked Amenity instances.
        amenities (setter): Appends an Amenity id to amenity_ids.
    """

    __tablename__ = "places"

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
            "Review",
            backref="place",
            cascade="all, delete-orphan"
        )
        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False,
            overlaps="place_amenities"
        )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Return list of Review instances linked to this Place."""
            from models import storage
            from models.review import Review
            return [
                r for r in storage.all(Review).values()
                if r.place_id == self.id
            ]

        @property
        def amenities(self):
            """Return list of Amenity instances linked to this Place."""
            from models import storage
            from models.amenity import Amenity
            return [
                a for a in storage.all(Amenity).values()
                if a.id in self.amenity_ids
            ]

        @amenities.setter
        def amenities(self, obj):
            """Append an Amenity id to amenity_ids if obj is an Amenity.

            Args:
                obj: An Amenity instance to link to this Place.
            """
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
