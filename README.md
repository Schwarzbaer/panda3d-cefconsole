panda3d-cefconsole
==================

This is a package for people who

* want to try out Panda3D *now*
* debug Panda3D applications, and would like to get a look at their innards in
  real time
* develop Panda3D applications, and would like to add application-specific
  consoles

It provides a console akin to those found in many modern games by adding a
CEFPanda node to the scene graph. The console can contain multiple subconsoles
between which the user can switch around. A Python console is also provided.


Status
------

This is just a few days work. The HTML templates are pretty atrocious. The code
could use a thorough review. But it works pretty well actually.


Installation
------------

`pip install panda3d-cefconsole`

...or clone the code from GitHub. I'm a README.md, not a cop.


Trying out the Python subconsole
--------------------------------

* `cefconsole_demo`
* F9 toggles the console
* In the Demo subconsole, you can click the text. This demonstrates a full
  JavaScript -> Python -> JavaScript roundtrip.
* In the Python console, add a Smiley ball:

      model = base.loader.load_model("models/smiley")
      model.reparent_to(base.render)
      base.cam.set_pos(0, -10, 0)


Using cefconsole
----------------

    from cefconsole import add_console
    from cefconsole import DemoSubconsole
    from cefconsole import PythonSubconsole


    # This has to be done after ShowBase()

    add_console(
        size=[-1, 1, -0.33, 1], # Don't cover the whole window
        console_open=True, # Whether to show console initially
    )
    # There's also `render_immediately`; If True, the console is rendered at the
    # end of add_console, and no further subconsoles can be added.

    # Now there's a base.console, so let's add subconsoles to it.
    base.console.add_subconsole(DemoSubconsole())
    base.console.add_subconsole(PythonSubconsole())

    # After all subconsoles have been added, the console can be rendered.
    base.console.render_console()


Adding Subconsoles
------------------

    from cefconsole import Subconsole


    class DemoSubconsole(Subconsole):
        name = "Demo"
        package = 'cefconsole'
        template_dir = 'templates'
        html = "demo.html"
        funcs = {'call_python': 'test_hook'}

    def test_hook(self):
        print("Python handler `test_hook` for JavaScript hook `call_python` has been called.")
        self.console.exec_js_func('color_text', 'red')

* `name` is used for the text in the header where you switch between
   subconsoles, as ID for the subconsole's HTML `div` container's id, and as
   prefix for the jinja2 `PrefixLoader`, so you'll have to add it to paths in
   HTML templates.
* `package` is the name of the module in which your templates are stored
  (usually the same as the subconsole itself, because why wouldn't you?)
* `template_dir` is the path from the module to the templates.
* `html` is the subconsole's actual template, which gets included in the
  console's template.
* `funcs` is a mapping from JavaScript function names to Python method names.
  These JS hooks will be added automatically. For example, here's `test_hook`,
  which is called by a JS function, and is calling one in turn.

The corresponding HTML code:

    <script>
      function color_text(color) {
          document.getElementById("colorable_text").style.color = color;
      }
    </script>
    <h1>A little demo subconsole</h1>
    <p id="colorable_text" onclick="call_python();">
      Click this text to color it red.
    </p>

As you see, when you click on the text, JS' `call_python` is called, which
means that Python's `DemoSubconsole.test_hook` is called, which calls JS'
`color_text`, and that's how you write `Subconsole`s.


TODO
====

* One-line creation
  * Add arg for a list of subconsoles to add immediately.
  * If `render_immediately` is set, but no subconsole list is given, add
    PythonSubconsole
* Make toggle button configurable
* Subconsoles
  * Panda3D
    * basics: toggling frame rate, base.mouse modes, oobe, render.analyze(), ...
    * scene graph explorer
    * task manager
    * events (listening / creating)
    * Add subconsole to default console
  * Console theme
    * Editor for the console's style
