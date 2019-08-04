import yaml
from jinja2 import Environment

from rofimenu import RofiMenu


class FileLoader:
    @staticmethod
    def load_yaml(file: str) -> RofiMenu:
        """Load a YAML file and return the corresponding menu"""
        loaded_menu = None
        with open(file, 'r') as stream:
            try:
                stream = Environment().from_string(stream.read()).render()
                loaded_menu = RofiMenu(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                print(exc)

        def submenus(menu: RofiMenu) -> None:
            """Recursive function that manages the submenus"""
            if menu is None:
                return

            for key, value in menu:
                # Convert dict to RofiMenu
                if isinstance(value, dict):
                    menu[key] = RofiMenu(value)
                    submenus(menu[key])

                if isinstance(value, list):
                    for i in range(len(value)): # For each item on the list
                        if isinstance(value[i], dict):
                            menu[key][i] = RofiMenu(menu[key][i])
                            submenus(menu[key][i])

        submenus(loaded_menu) # Call local function

        return loaded_menu
