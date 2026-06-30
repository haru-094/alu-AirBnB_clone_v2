#!/usr/bin/python3
"""This module defines the entry point of the command interpreter."""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


CLASSES = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review,
}


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the AirBnB clone project."""

    prompt = "(hbnb) "

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        print()
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def do_create(self, line):
        """Create a new instance with optional key=value parameters.

        Usage: create <class name> [<key>=<value> ...]

        Value formats accepted:
          String : <key>="<value>"  (underscores become spaces)
          Float  : <key>=<unit>.<decimal>
          Integer: <key>=<number>

        Invalid parameters are silently skipped.
        """
        if not line:
            print("** class name missing **")
            return
        args = line.split()
        class_name = args[0]
        if class_name not in CLASSES:
            print("** class doesn't exist **")
            return

        kwargs = {}
        for param in args[1:]:
            if "=" not in param:
                continue
            key, _, raw = param.partition("=")
            if not key or not raw:
                continue

            if raw.startswith('"'):
                # String: must start AND end with a double-quote
                if not raw.endswith('"') or len(raw) < 2:
                    continue
                # Strip surrounding quotes
                value = raw[1:-1]
                # Replace escaped quotes with actual quotes
                value = value.replace('\\"', '"')
                # Replace underscores with spaces
                value = value.replace('_', ' ')
                kwargs[key] = value
            elif '.' in raw:
                # Float
                try:
                    kwargs[key] = float(raw)
                except ValueError:
                    continue
            else:
                # Integer
                try:
                    kwargs[key] = int(raw)
                except ValueError:
                    continue

        obj = CLASSES[class_name](**kwargs)
        obj.save()
        print(obj.id)

    def do_show(self, line):
        """Print string representation of an instance.

        Usage: show <class name> <id>
        """
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in CLASSES:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return
        print(obj)

    def do_destroy(self, line):
        """Delete an instance based on the class name and id.

        Usage: destroy <class name> <id>
        """
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in CLASSES:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return
        storage.delete(obj)
        storage.save()

    def do_all(self, line):
        """Print all string representations of all instances.

        Usage: all [class name]
        """
        if line and line not in CLASSES:
            print("** class doesn't exist **")
            return
        result = []
        for key, obj in storage.all().items():
            if not line or key.startswith(line + "."):
                result.append(str(obj))
        print(result)

    def do_update(self, line):
        """Update an instance by adding or updating an attribute.

        Usage: update <class name> <id> <attribute name> <attribute value>
        """
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in CLASSES:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr_name = args[2]
        attr_value = args[3]

        # Strip surrounding quotes from string values
        if attr_value.startswith('"'):
            joined = line.split(None, 3)
            if len(joined) >= 4:
                attr_value = joined[3]
            if attr_value.startswith('"'):
                attr_value = attr_value.lstrip('"')
                quote_end = attr_value.find('"')
                if quote_end != -1:
                    attr_value = attr_value[:quote_end]

        # Cast to existing attribute type if attribute already exists
        existing = getattr(obj, attr_name, None)
        if existing is not None:
            try:
                attr_value = type(existing)(attr_value)
            except (ValueError, TypeError):
                pass
        else:
            try:
                attr_value = int(attr_value)
            except ValueError:
                try:
                    attr_value = float(attr_value)
                except ValueError:
                    pass

        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
