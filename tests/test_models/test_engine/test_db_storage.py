#!/usr/bin/python3
"""Unit tests for the DBStorage class."""
import unittest
import os
from models import storage
from models.state import State
from models.city import City
from models.user import User

IS_DB = os.getenv("HBNB_TYPE_STORAGE") == "db"


def get_mysql_count(table):
    """Return the row count of a MySQL table using MySQLdb.

    Args:
        table (str): The name of the table to count.

    Returns:
        int: Number of rows in the table.
    """
    import MySQLdb
    conn = MySQLdb.connect(
        host=os.getenv("HBNB_MYSQL_HOST", "localhost"),
        user=os.getenv("HBNB_MYSQL_USER"),
        passwd=os.getenv("HBNB_MYSQL_PWD"),
        db=os.getenv("HBNB_MYSQL_DB")
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM {}".format(table))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count


@unittest.skipIf(not IS_DB, "DBStorage tests only — set HBNB_TYPE_STORAGE=db")
class TestDBStorageInstantiation(unittest.TestCase):
    """Tests for DBStorage instantiation."""

    def test_storage_is_dbstorage(self):
        """Test that storage is a DBStorage instance."""
        from models.engine.db_storage import DBStorage
        self.assertIsInstance(storage, DBStorage)

    def test_all_returns_dict(self):
        """Test that all() returns a dictionary."""
        self.assertIsInstance(storage.all(), dict)


@unittest.skipIf(not IS_DB, "DBStorage tests only — set HBNB_TYPE_STORAGE=db")
class TestDBStorageAll(unittest.TestCase):
    """Tests for DBStorage all method."""

    def test_all_with_state_class(self):
        """Test that all(State) returns only State objects."""
        result = storage.all(State)
        for key in result:
            self.assertTrue(key.startswith("State."))

    def test_all_with_city_class(self):
        """Test that all(City) returns only City objects."""
        result = storage.all(City)
        for key in result:
            self.assertTrue(key.startswith("City."))

    def test_all_with_string_class_name(self):
        """Test that all('State') works with a string class name."""
        result = storage.all("State")
        for key in result:
            self.assertTrue(key.startswith("State."))

    def test_all_none_returns_multiple_types(self):
        """Test that all(None) can return objects of different types."""
        s = State(name="AllTestState")
        s.save()
        result = storage.all()
        self.assertIsInstance(result, dict)
        storage.delete(s)
        storage.save()


@unittest.skipIf(not IS_DB, "DBStorage tests only — set HBNB_TYPE_STORAGE=db")
class TestDBStorageNewAndSave(unittest.TestCase):
    """Tests for DBStorage new and save methods."""

    def test_create_state_adds_db_row(self):
        """Test that saving a State adds exactly one row to states table."""
        before = get_mysql_count("states")
        s = State(name="TestNewState")
        s.save()
        after = get_mysql_count("states")
        self.assertEqual(after - before, 1)
        storage.delete(s)
        storage.save()

    def test_create_user_adds_db_row(self):
        """Test that saving a User adds exactly one row to users table."""
        before = get_mysql_count("users")
        u = User(email="test@db.com", password="testpwd")
        u.save()
        after = get_mysql_count("users")
        self.assertEqual(after - before, 1)
        storage.delete(u)
        storage.save()


@unittest.skipIf(not IS_DB, "DBStorage tests only — set HBNB_TYPE_STORAGE=db")
class TestDBStorageDelete(unittest.TestCase):
    """Tests for DBStorage delete method."""

    def test_delete_state_removes_db_row(self):
        """Test that deleting a State removes one row from states table."""
        s = State(name="ToDeleteDB")
        s.save()
        before = get_mysql_count("states")
        storage.delete(s)
        storage.save()
        after = get_mysql_count("states")
        self.assertEqual(before - after, 1)

    def test_delete_none_does_nothing(self):
        """Test that delete(None) does not raise or affect the DB."""
        before = get_mysql_count("states")
        try:
            storage.delete(None)
            storage.save()
        except Exception as e:
            self.fail("delete(None) raised: {}".format(e))
        after = get_mysql_count("states")
        self.assertEqual(before, after)

    def test_deleted_object_not_in_all(self):
        """Test that a deleted object is no longer in storage.all()."""
        s = State(name="GoneState")
        s.save()
        key = "State.{}".format(s.id)
        self.assertIn(key, storage.all())
        storage.delete(s)
        storage.save()
        self.assertNotIn(key, storage.all())


if __name__ == "__main__":
    unittest.main()
