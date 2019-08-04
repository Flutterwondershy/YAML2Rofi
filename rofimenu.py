import os
from typing import Union

class RofiMenu:
    """Represent a rofi menu"""

    def __init__(self, menu={}):
        self.menu = menu
        self.rofi_cmd = "rofi -dmenu -show run"

    def __getitem__(self, key: str):
        """Get a menu item"""
        if key in self.menu:
            return self.menu[key]

    def __delitem__(self, key: str):
        """Delete a menu item"""
        del self.menu[key]

    def __setitem__(self, key: str, value):
        """Set a menu item"""
        self.menu[key] = value

    def __str__(self):
        """Return the command line used to display the menu"""
        return 'echo -e "{items}" | {cmd}'.format(
                    items='\\n'.join(self.menu.keys()),
                    cmd=self.rofi_cmd)

    def __repr__(self):
        return str(self.menu)

    def __iter__(self):
        """Iterate each menu item"""
        if isinstance(self.menu, dict):
            yield from self.menu.items()

        # Simulate a dict
        elif isinstance(self.menu, list):
            for i in range(len(self.menu)):
                yield i, self.menu[i]

    def show_rofi(self) -> Union[str, None]:
        """Run the menu command line and manage the return"""

        # The root can be a list or a simple menu
        menus = self.menu if isinstance(self.menu, list) else [self]
        result = ""

        # For each menu
        for menu in menus:
            # Firstly, menu can be a simple command
            if isinstance(menu, str):
                result += RofiMenu.exec(menu)
                continue

            key = RofiMenu.exec(menu)
            if len(key) == 0:
                continue

            key = key.splitlines()[0] # Remove \n if exist
            if key in menu and isinstance(menu[key], list):
                for cmd in menu[key]:
                    result += RofiMenu.launch(cmd)
            else:
                result += RofiMenu.launch(menu[key])
        return result

    @staticmethod
    def launch(cmd: Union[str, object]) -> str:
        """Execute a command and return stdout output"""
        if isinstance(cmd, RofiMenu):
            return cmd.show_rofi()
        else:
            return RofiMenu.exec(cmd)

    @staticmethod
    def exec(cmd: Union[str, object]) -> str:
        # Execute only string (RofiMenu has __str__ method)
        save_context = """
set > /tmp/pre
touch /tmp/vars
eval $(cat /tmp/vars)
{}
set > /tmp/post
grep -v -F -f/tmp/pre /tmp/post > /tmp/vars
"""
        command = save_context.format(str(cmd))
        return os.popen(command).read()
