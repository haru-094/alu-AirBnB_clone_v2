#!/usr/bin/python3
"""This module defines the FileStorage class."""
import json


class FileStorage:
    """Serializes instances to a JSON file and deserializes back.

    Attributes:
        __file_path (str): Path to the JSON file.
        __objects (dict): Dictionary of all stored objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return stored objects, optionally filtered by class.

        Args:
            cls: Optional class (or class name string) to filter by.

        Returns:
            dict: All objects, or only those matching cls if provided.
        """
        if cls is None:
            return FileStorage.__objects
        result = {}
        for key, obj in FileStorage.__objects.items():
            cls_name = cls if isinstance(cls, str) else cls.__name__
            if type(obj).__name__ == cls_name:
                result[key] = obj
        return result

    def new(self, obj):
        """Set obj in __objects with key <class name>.id.

        Args:
            obj: The object to store.
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file."""
        data = {}
        for key, obj in FileStorage.__objects.items():
            data[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def reload(self):
        """Deserialize the JSON file to __objects if it exists."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
        }

        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key, value in data.items():
                class_name = value.get("__class__")
                if class_name in classes:
                    FileStorage.__objects[key] = classes[class_name](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it exists.

        Args:
            obj: The object to delete. Does nothing if obj is None.
        """
        if obj is None:
            return
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects.pop(key, None)

    def close(self):
        """Call reload() to deserialize the JSON file to objects."""
        self.reload()
