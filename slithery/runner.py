"""
runner.py

    Executes the actual sandbox environment, and handles
    any segfaults that occur and return the flag
"""

import os
import subprocess

if __name__ == "__main__":
    try:
        res = subprocess.run(["python", "sandbox.py"])
        if res in [-11, 245]:
            print("flag")
    except Exception:
        pass
