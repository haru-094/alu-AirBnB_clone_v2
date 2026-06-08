#!/usr/bin/python3
"""Module for testing DBStorage"""
import unittest
import os

storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')


@unittest.skipIf(storage_type != 'db', 'DBStorage tests only')
class test_dbStorage(unittest.TestCase):
    """Class to test the DBStorage method"""

    def setUp(self):
        """Set up test environment"""
        from models import storage
        self.storage = storage

    def tearDown(self):
        """Clean up after each test"""
        pass

    def test_storage_type_is_db(self):
        """Confirm we are using DBStorage"""
        from models.engine.db_storage import DBStorage
        self.assertIsInstance(self.storage, DBStorage)

    def test_all_returns_dict(self):
        """storage.all() returns a dict"""
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    def test_all_with_class_arg(self):
        """storage.all(cls) returns dict filtered by class"""
        from models.state import State
        result = self.storage.all(State)
        self.assertIsInstance(result, dict)

    def test_new_obj(self):
        """New object is added via storage.new()"""
        from models.state import State
        s = State()
        s.name = "TestState"
        self.storage.new(s)
        self.storage.save()
        key = 'State.' + s.id
        self.assertIn(key, self.storage.all(State))
        self.storage.delete(s)
        self.storage.save()

    def test_save_obj(self):
        """storage.save() commits object to DB"""
        from models.state import State
        s = State()
        s.name = "SaveTestState"
        self.storage.new(s)
        self.storage.save()
        all_states = self.storage.all(State)
        key = 'State.' + s.id
        self.assertIn(key, all_states)
        self.storage.delete(s)
        self.storage.save()

    def test_delete_obj(self):
        """storage.delete() removes object from DB"""
        from models.state import State
        s = State()
        s.name = "DeleteState"
        self.storage.new(s)
        self.storage.save()
        self.storage.delete(s)
        self.storage.save()
        all_states = self.storage.all(State)
        key = 'State.' + s.id
        self.assertNotIn(key, all_states)

    def test_reload(self):
        """storage.reload() is callable without error"""
        try:
            self.storage.reload()
        except Exception as e:
            self.fail("reload() raised an exception: {}".format(e))

    def test_storage_has_all(self):
        """DBStorage has all() method"""
        self.assertTrue(hasattr(self.storage, 'all'))

    def test_storage_has_new(self):
        """DBStorage has new() method"""
        self.assertTrue(hasattr(self.storage, 'new'))

    def test_storage_has_save(self):
        """DBStorage has save() method"""
        self.assertTrue(hasattr(self.storage, 'save'))

    def test_storage_has_delete(self):
        """DBStorage has delete() method"""
        self.assertTrue(hasattr(self.storage, 'delete'))

    def test_storage_has_reload(self):
        """DBStorage has reload() method"""
        self.assertTrue(hasattr(self.storage, 'reload'))

    def test_key_format_in_all(self):
        """Keys in all() follow ClassName.id format"""
        from models.state import State
        s = State()
        s.name = "KeyFormatState"
        self.storage.new(s)
        self.storage.save()
        result = self.storage.all(State)
        for key in result.keys():
            parts = key.split('.')
            self.assertEqual(len(parts), 2)
            self.assertEqual(parts[0], 'State')
        self.storage.delete(s)
        self.storage.save()

    def test_state_creation_mysql(self):
        """Validate that creating a State adds a row to the DB (MySQLdb)"""
        import MySQLdb
        import subprocess

        db_user = os.getenv('HBNB_MYSQL_USER')
        db_pwd = os.getenv('HBNB_MYSQL_PWD')
        db_host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        db_name = os.getenv('HBNB_MYSQL_DB')

        conn = MySQLdb.connect(
            host=db_host, user=db_user, passwd=db_pwd, db=db_name
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        count_before = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        result = subprocess.run(
            ['python3', 'console.py'],
            input='create State name="California"\nquit\n',
            capture_output=True, text=True,
            env=dict(os.environ)
        )

        conn = MySQLdb.connect(
            host=db_host, user=db_user, passwd=db_pwd, db=db_name
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        count_after = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        self.assertEqual(count_after - count_before, 1)
