#!/usr/bin/python3
"""This module defines the DBStorage class for MySQL database storage."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """Manages persistent storage of hbnb models using SQLAlchemy and MySQL.

    Attributes:
        __engine: The SQLAlchemy engine connected to MySQL.
        __session: The current database session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Create the SQLAlchemy engine linked to the MySQL database.

        Reads connection parameters from environment variables:
            HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB.
        Drops all tables if HBNB_ENV equals 'test'.
        """
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST", "localhost")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db),
            pool_pre_ping=True
        )

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of the given class from the current session.

        Args:
            cls: Optional class or class name string to filter by.
                 If None, all supported model types are queried.

        Returns:
            dict: Dictionary of objects with keys in format <ClassName>.<id>.
        """
        from models.user import User
        from models.state import State
        from models.city import City
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review

        all_classes = [User, State, City, Amenity, Place, Review]
        result = {}

        if cls:
            if isinstance(cls, str):
                cls = next((c for c in all_classes if c.__name__ == cls), None)
            if cls:
                for obj in self.__session.query(cls).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    result[key] = obj
        else:
            for klass in all_classes:
                for obj in self.__session.query(klass).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    result[key] = obj

        return result

    def new(self, obj):
        """Add the object to the current database session.

        Only adds the object if it is a mapped SQLAlchemy model (i.e. has a
        __tablename__). Plain BaseModel instances (used only in FileStorage
        tests) are silently ignored to avoid UnmappedInstanceError.

        Args:
            obj: The model instance to add to the session.
        """
        if obj is not None and hasattr(obj, "__tablename__"):
            self.__session.add(obj)

    def save(self):
        """Commit all pending changes in the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if it is not None.

        Args:
            obj: The model instance to delete. Does nothing if None.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all database tables and initialise a new scoped session.

        Imports all models so SQLAlchemy can register their table mappings
        before calling create_all. Uses a scoped session for thread safety.
        """
        from models.user import User
        from models.state import State
        from models.city import City
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the current session."""
        self.__session.close()
