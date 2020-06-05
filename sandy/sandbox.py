#!/usr/bin/env python3

class Sandbox:

    def __init__(self, command: str):
        self.command = command

    def enforce(self):
        """TODO"""
        pass

    def run(self):
        return eval()


if __name__ == "__main__":
    res = input(">> ")
    sandbox = Sandbox(str(res))
    print(sandbox.run())
