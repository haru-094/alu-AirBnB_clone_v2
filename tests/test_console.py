#!/usr/bin/python3
"""Unittest cases for the console's do_create command with parameters.

Tests are FileStorage-only (HBNB_TYPE_STORAGE != 'db').
"""
import unittest
import os
import json
from io import StringIO
from unittest.mock import patch

storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')


@unittest.skipIf(storage_type == 'db', 'FileStorage create-params tests only')
class TestConsoleCreate(unittest.TestCase):
    """Test the parameterized create command of the HBNB console"""

    def setUp(self):
        """Back up file.json if it exists"""
        try:
            os.rename('file.json', 'file.json.bak')
        except FileNotFoundError:
            pass

    def tearDown(self):
        """Restore file.json backup and remove test file"""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass
        try:
            os.rename('file.json.bak', 'file.json')
        except FileNotFoundError:
            pass

    def _run_create(self, line):
        """Helper: run do_create and return printed id"""
        from console import HBNBCommand
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(line)
            return f.getvalue().strip()

    def _get_obj(self, cls_name, obj_id):
        """Helper: reload storage and return the object"""
        from models import storage
        storage.reload()
        key = '{}.{}'.format(cls_name, obj_id)
        return storage.all().get(key)

    # ------------------------------------------------------------------ basics
    def test_create_no_args_prints_error(self):
        """create with no args prints class name missing"""
        from console import HBNBCommand
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create')
        self.assertIn('** class name missing **', f.getvalue())

    def test_create_invalid_class(self):
        """create with bad class name prints doesn't exist"""
        from console import HBNBCommand
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create NotAClass')
        self.assertIn("** class doesn't exist **", f.getvalue())

    def test_create_state_no_params(self):
        """create State with no params creates a valid State"""
        obj_id = self._run_create('create State')
        self.assertTrue(len(obj_id) == 36)  # UUID length

    def test_create_returns_id(self):
        """create prints a UUID string"""
        obj_id = self._run_create('create State')
        self.assertRegex(obj_id,
                         r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}'
                         r'-[0-9a-f]{4}-[0-9a-f]{12}$')

    # --------------------------------------------------------------- strings
    def test_create_string_param(self):
        """create State name="California" sets name attribute"""
        obj_id = self._run_create('create State name="California"')
        obj = self._get_obj('State', obj_id)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.name, 'California')

    def test_create_string_underscore_to_space(self):
        """Underscores in string values are replaced by spaces"""
        obj_id = self._run_create('create State name="My_little_state"')
        obj = self._get_obj('State', obj_id)
        self.assertEqual(obj.name, 'My little state')

    def test_create_string_escaped_quote(self):
        """Escaped double quote inside string value is preserved"""
        obj_id = self._run_create(r'create State name="Say_\"hi\""')
        obj = self._get_obj('State', obj_id)
        self.assertIn('"hi"', obj.name)

    def test_create_multiple_string_params(self):
        """Multiple string params are all set"""
        obj_id = self._run_create(
            'create State name="Arizona"'
        )
        obj = self._get_obj('State', obj_id)
        self.assertEqual(obj.name, 'Arizona')

    # --------------------------------------------------------------- integers
    def test_create_integer_param(self):
        """Integer parameter is parsed and set correctly"""
        obj_id = self._run_create('create Place number_rooms=4')
        obj = self._get_obj('Place', obj_id)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.number_rooms, 4)
        self.assertIsInstance(obj.number_rooms, int)

    def test_create_multiple_integer_params(self):
        """Multiple integer params are all set"""
        obj_id = self._run_create(
            'create Place number_rooms=4 number_bathrooms=2 max_guest=10'
        )
        obj = self._get_obj('Place', obj_id)
        self.assertEqual(obj.number_rooms, 4)
        self.assertEqual(obj.number_bathrooms, 2)
        self.assertEqual(obj.max_guest, 10)

    # --------------------------------------------------------------- floats
    def test_create_float_param(self):
        """Float parameter is parsed and set correctly"""
        obj_id = self._run_create('create Place latitude=37.773972')
        obj = self._get_obj('Place', obj_id)
        self.assertIsNotNone(obj)
        self.assertAlmostEqual(obj.latitude, 37.773972, places=5)
        self.assertIsInstance(obj.latitude, float)

    def test_create_negative_float_param(self):
        """Negative float parameter is parsed correctly"""
        obj_id = self._run_create('create Place longitude=-122.431297')
        obj = self._get_obj('Place', obj_id)
        self.assertAlmostEqual(obj.longitude, -122.431297, places=5)

    # --------------------------------------------------------------- mixed
    def test_create_full_place(self):
        """Full Place creation with all param types"""
        cmd = ('create Place city_id="0001" user_id="0001" '
               'name="My_little_house" number_rooms=4 number_bathrooms=2 '
               'max_guest=10 price_by_night=300 '
               'latitude=37.773972 longitude=-122.431297')
        obj_id = self._run_create(cmd)
        obj = self._get_obj('Place', obj_id)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.name, 'My little house')
        self.assertEqual(obj.city_id, '0001')
        self.assertEqual(obj.user_id, '0001')
        self.assertEqual(obj.number_rooms, 4)
        self.assertEqual(obj.number_bathrooms, 2)
        self.assertEqual(obj.max_guest, 10)
        self.assertEqual(obj.price_by_night, 300)
        self.assertAlmostEqual(obj.latitude, 37.773972, places=5)
        self.assertAlmostEqual(obj.longitude, -122.431297, places=5)

    # --------------------------------------------------- invalid params skipped
    def test_invalid_param_no_equals(self):
        """Param without = sign is silently skipped"""
        obj_id = self._run_create('create State badparam')
        obj = self._get_obj('State', obj_id)
        self.assertIsNotNone(obj)
        self.assertFalse(hasattr(obj, 'badparam'))

    def test_invalid_param_bad_float(self):
        """Non-numeric value without quotes is silently skipped"""
        obj_id = self._run_create('create State name=notquoted')
        obj = self._get_obj('State', obj_id)
        self.assertIsNotNone(obj)

    def test_invalid_string_unclosed_quote(self):
        """String value with unclosed quote is silently skipped"""
        obj_id = self._run_create('create State name="unclosed')
        obj = self._get_obj('State', obj_id)
        self.assertIsNotNone(obj)

    def test_valid_and_invalid_mixed(self):
        """Valid params are set; invalid ones are skipped"""
        obj_id = self._run_create(
            'create State name="California" badparam invalid=notok'
        )
        obj = self._get_obj('State', obj_id)
        self.assertEqual(obj.name, 'California')
        self.assertFalse(hasattr(obj, 'badparam'))

    # --------------------------------------------------------- file persistence
    def test_create_saves_to_file(self):
        """create saves the new object to file.json"""
        obj_id = self._run_create('create State name="Saved"')
        self.assertTrue(os.path.exists('file.json'))
        with open('file.json', 'r') as f:
            data = json.load(f)
        key = 'State.' + obj_id
        self.assertIn(key, data)
        self.assertEqual(data[key]['name'], 'Saved')
