import ast
import os
import platform
import sys
import types

import pyash_stdlib


ALLOWED_TOKENS = {
    ast.Add,
    ast.BinOp,
    ast.Constant,
    ast.Dict,
    ast.Index,
    ast.Invert,
    ast.Name,
    ast.NameConstant,
    ast.Num,
    ast.Module,
    ast.Mult,
    ast.List,
    ast.Compare,
    ast.Gt,
    ast.Lt,
    ast.Set,
    ast.Str,
    ast.Tuple,
    ast.UnaryOp,
    ast.Subscript,
    ast.Expr,
    ast.Sub,
    ast.Div,
    ast.Mod,
    ast.Call,
    ast.Load,
    #    ast.Attribute  # Nice try
    #    ast.Assign,
    #    ast.Store,
}


def extract_runtime(module):
    runtime = {}

    for name in dir(module):
        attr = getattr(module, name)
        if not name.startswith("_") and not isinstance(attr, types.ModuleType):
            runtime[name] = attr
    return runtime


class BashMe(ast.NodeTransformer):
    def visit_Expr(self, node: ast.Expr):
        pass


class Pyash(object):
    def __init__(self, runtime: dict = None):
        self.runtime = runtime
        if runtime is None:
            self.runtime = extract_runtime(pyash_stdlib)

        def help():
            """ Show help """
            for name in self.runtime:
                print("%s:%s" % (name, self.runtime[name].__doc__))

        self.runtime["help"] = help

    def check_allowed_token(self, node) -> bool:
        for token in ALLOWED_TOKENS:
            if isinstance(node, token):
                return True
        return False

    def verify(self, src: str):
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if not self.check_allowed_token(node):
                token_name = node.__class__.__name__
                raise SyntaxError("Invalid token: '%s'" % (token_name))

    def evaluate(self, src: str):
        result = None
        self.verify(src)
        result = eval(src, {"__builtins__": None}, self.runtime)
        return result

    def print_motd(self):
        print(
            'Pyash %s on %s\nType "help()" for more information.'
            % (sys.version, platform.system())
        )

    def interactive(self):
        self.print_motd()
        while True:
            src = input(">>> ")
            result = self.evaluate(src)
            if result:
                print(result)


if __name__ == "__main__":
    shell = Pyash()
    shell.interactive()
