#!/usr/bin/python3
"""This module defines the BaseModel class and SQLAlchemy Base."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """Defines all common attributes and methods for other classes.

    All models inherit from this class to get id, created_at, and updated_at.
    Models that use DBStorage also inherit from Base to enable SQLAlchemy
    table mapping.
    """

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance.

        Args:
            *args: Unused positional arguments.
            **kwargs: Key/value pairs to set as instance attributes.
                      Supports both JSON-reloaded dicts and direct param dicts
                      like {'name': 'California'}.
        """
        fmt = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in ("created_at", "updated_at"):
                    if isinstance(value, str):
                        value = datetime.strptime(value, fmt)
                setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """Return string representation of the BaseModel instance."""
        d = {k: v for k, v in self.__dict__.items()
             if k != '_sa_instance_state'}
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)

    def save(self):
        """Update updated_at to now, register with storage, and save."""
        self.updated_at = datetime.utcnow()
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance.

        Returns:
            dict: All instance attributes including __class__, with
                  created_at and updated_at as ISO-format strings.
                  The SQLAlchemy internal key _sa_instance_state is excluded.
        """
        result = self.__dict__.copy()
        result.pop("_sa_instance_state", None)
        result["__class__"] = type(self).__name__
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        return result

    def delete(self):
        """Delete the current instance from storage."""
        from models import storage
        storage.delete(self)
