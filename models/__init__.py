#!/usr/bin/python3
"""This module creates a storage instance based on the HBNB_TYPE_STORAGE
environment variable. Use 'db' for DBStorage (MySQL) or leave unset / set
to anything else for FileStorage (JSON file)."""
import os

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
