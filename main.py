#!/usr/bin/python3
from os import sys

from fileloader import FileLoader

if __name__ == "__main__":
    if len(sys.argv) == 2:  # Only one argument: yaml file path
        yaml_file = sys.argv[1]
        menu = FileLoader.load_yaml(yaml_file)
        print(menu.show_rofi())
    else:
        print("Nombre d'arguments incorrect: " + str(len(sys.argv)))
