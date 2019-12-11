import cefpanda

from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import select_autoescape

from cefconsole.repl import Interpreter


class Console(cefpanda.CEFPanda):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subconsoles = []
        self.env = Environment(
            loader=PackageLoader('cefconsole', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def add_subconsole(self, subconsole):
        self.subconsoles.append(subconsole)

    def render_console(self):
        for subconsole in self.subconsoles:
            subconsole.hook_js_funcs(self)
        template = self.env.get_template('console.html')
        content = template.render(subconsoles=self.subconsoles)
        self.load_string(content)


class Subconsole:
    name = ""
    funcs = {}

    def hook_js_funcs(self, console):
        self.console = console
        for js_func, py_func_name in self.funcs.items():
            console.set_js_function(js_func, getattr(self, py_func_name))


class DemoSubconsole(Subconsole):
    name = "Demo"
    html = "demo.html"
    funcs = {'call_python': 'test_hook'}

    def test_hook(self):
        print("Python handler `test_hook` for JavaScript hook `call_python` has been called.")
        self.console.exec_js_func('color_text', 'red')


class PythonSubconsole(Subconsole):
    name = "Python"
    html = "python.html"
    funcs = {'read_eval': 'read_and_eval'}
    interpreter = Interpreter()

    def read_and_eval(self, input):
        self.interpreter.runline(input)
        out = self.interpreter.output_string
        prompt = self.interpreter.prompt
        self.console.exec_js_func("print_output", out, prompt)


def add_console(*args, console_open=False, render_immediately=False, **kwargs):
    base.console_open = console_open
    base.console = Console(*args, **kwargs)
    if not base.console_open:
        base.console.node().hide()

    def toggle_console():
        base.console_open = not base.console_open
        if base.console_open:
            base.console.node().show()
        else:
            base.console.node().hide()
    base.accept('f9', toggle_console)

    if render_immediately:
        base.console.render_console()
