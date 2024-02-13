#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""

    prompt = "(hbnb) "

    def emptyline(self):
        """Called when an empty line is entered"""
        pass

    def do_create(self, arg):
        """Create a new instance, save it, and print the id"""
        if not arg:
            print("** class name missing **")
        else:
            try:
                new_instance = eval(arg)()
                new_instance.save()
                print(new_instance.id)
            except NameError:
                print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        else:
            try:
                class_name = args[0]
                if len(args) == 1:
                    print("** instance id missing **")
                else:
                    obj_id = args[1]
                    key = "{}.{}".format(class_name, obj_id)
                    obj = storage.all().get(key)
                    if obj:
                        print(obj)
                    else:
                        print("** no instance found **")
            except NameError:
                print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        else:
            try:
                class_name = args[0]
                if len(args) == 1:
                    print("** instance id missing **")
                else:
                    obj_id = args[1]
                    key = "{}.{}".format(class_name, obj_id)
                    obj = storage.all().get(key)
                    if obj:
                        del storage.all()[key]
                        storage.save()
                    else:
                        print("** no instance found **")
            except NameError:
                print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        if not arg:
            print([str(obj) for obj in storage.all().values()])
        else:
            try:
                class_name = arg.split()[0]
                if class_name not in storage.classes():
                    print("** class doesn't exist **")
                else:
                    print([str(obj) for obj in storage.all().values() if type(obj).__name__ == class_name])
            except IndexError:
                print("** class name missing **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(class_name, args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attribute = args[2]
        value = args[3]
        try:
            value = eval(value)
        except (NameError, SyntaxError):
            pass
        setattr(storage.all()[key], attribute, value)
        storage.all()[key].save()

    def do_count(self, arg):
        """Counts the number of instances of a class"""
        if not arg:
            print("** class name missing **")
            return
        class_name = arg.split()[0]
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return
        count = sum(1 for obj in storage.all().values() if type(obj).__name__ == class_name)
        print(count)

    def do_show_instance(self, arg):
        """Retrieves an instance based on its ID"""
        args = arg.split()
        if len(args) < 2:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy_instance(self, arg):
        """Destroys an instance based on its ID"""
        args = arg.split()
        if len(args) < 2:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_EOF(self, line):
        """Handles EOF"""
        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

if __name__ == '__main__':
    HBNBCommand().cmdloop()
