"""
runner.py

    Executes the actual sandbox environment, and handles
    any segfaults that occur and return the flag
"""

import os
import subprocess

if __name__ == "__main__":
    res = subprocess.call(["python", "sandbox.py"])
    if res in [-11, 245]:
        with open("flag.txt", "r") as f:
            print(f.read().strip())
