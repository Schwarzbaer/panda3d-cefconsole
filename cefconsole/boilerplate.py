import sys

from direct.showbase.ShowBase import ShowBase 

from cefconsole import add_console
from cefconsole import DemoSubconsole
from cefconsole import PythonSubconsole


def main():
    # Application Basics
    ShowBase()
    base.disable_mouse()
    base.accept('escape', sys.exit)

    # Adding a console
    add_console(
        size=[-1, 1, -0.33, 1],
        render_immediately=False,
        console_open=True,
    )
    base.console.add_subconsole(DemoSubconsole())
    base.console.add_subconsole(PythonSubconsole())
    base.console.render_console()

    # And here we go...
    base.run()
