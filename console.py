#!/usr/bin/python3
"""Module for the entry point of the command interpreter."""

import cmd
from models.base_model import BaseModel
from models import storage
import re
import json

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
                    if key in models.storage.all():
                        print(models.storage.all()[key])
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
                    if key in models.storage.all():
                        del models.storage.all()[key]
                        models.storage.save()
                    else:
                        print("** no instance found **")
            except NameError:
                print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        args = arg.split()
        obj_list = []
        if not args:
            for value in models.storage.all().values():
                obj_list.append(str(value))
            print(obj_list)
        else:
            try:
                class_name = args[0]
                if class_name in models.storage.all():
                    for key, value in models.storage.all().items():
                        if class_name in key:
                            obj_list.append(str(value))
                    print(obj_list)
                else:
                    print("** class doesn't exist **")
            except NameError:
                print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        else:
            try:
                class_name = args[0]
                if class_name not in models.storage.all():
                    print("** class doesn't exist **")
                    return
                if len(args) == 1:
                    print("** instance id missing **")
                else:
                    obj_id = args[1]
                    key = "{}.{}".format(class_name, obj_id)
                    if key not in models.storage.all():
                        print("** no instance found **")
                        return
                    if len(args) == 2:
                        print("** attribute name missing **")
                    else:
                        attribute_name = args[2]
                        if len(args) == 3:
                            print("** value missing **")
                        else:
                            attribute_value = args[3]
                            setattr(models.storage.all()[key], attribute_name,
                                    attribute_value)
                            models.storage.all()[key].save()
            except NameError:
                print("** class doesn't exist **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()