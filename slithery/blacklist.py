"""
blacklist.py

    Module that is seperated and kept secret, as it contains all the banned keywords
    that cannot be executed in the sandbox.
"""

BLACKLIST = [
    "__builtins__",
    "__import__",
    "eval",
    "exec",
    "import",
    "from",
    "os",
    "sys",
    "system",
    "timeit",
    "base64"
    "commands",
    "subprocess",
    "pty",
    "platform",
    "open",
    "read",
    "write",
    "dir",
    "type",
]
