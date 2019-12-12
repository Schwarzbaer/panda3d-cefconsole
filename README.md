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


Status a.k.a. TODO
------------------

This is just a few days work.

* The HTML templates are pretty atrocious in look, feel, and code quality.
* The code could use a thorough review.
* The subconsoles shipped with this package are lacking in number and functionality.
  * Python
    * This needs to be less of a basic test and moreofan IDE.
  * Panda3D
    * basics: toggling frame rate, base.mouse modes, oobe, render.analyze(), ...
    * scene graph explorer / manipulator
    * task manager
    * events (listening / creating)
    * insight into `ModelPool` and other `*Pools`.
    * Add subconsole to default console
  * Console theme
    * Editor for the console's style
* Documentation besides this README is non-existant.
* Tests are completely unheard of.

But technologically... it is done. And it works pretty well, too.


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

`cefconsole_demo` is a very rudimentary Panda3D application. Its code can be
found in `cefconsole/boilerplate.py` in the function `main()`, but the relevant
bits are these (edited for explanatory purposes):

    from cefconsole import add_console
    from cefconsole import DemoSubconsole
    from cefconsole import PythonSubconsole


    # This has to be done after ShowBase()

    add_console(
        size=[-1, 1, -0.33, 1], # Don't cover the whole window
        console_open=True, # Whether to show console initially; default False
	toggle='f9', # Panda3D event that toggles the console; default f9
	subconsoles=[DemoSubconsole()], # Subconsole to be added immediately
    )
    # There's also `render_immediately`; If True, the console is rendered at the
    # end of add_console, and no further subconsoles can be added.

    # Now there's a base.console, so let's another subconsole to it.
    base.console.add_subconsole(PythonSubconsole())

    # After all subconsoles have been added, the console can be rendered.
    base.console.render_console()

If `render_immediate` is set, but no subconsoles are given, the
`PythonSubconsole` is added by default. So in the end, all you would have needed
to start out is:

    from cefconsole import add_console

    add_console(render_immediately=True)


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

`base.console` is a `cefpanda.CEFPanda` object, so further information on it
can be found in the `cefpanda` repo.
