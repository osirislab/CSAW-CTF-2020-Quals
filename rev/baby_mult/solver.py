#!/usr/bin/env python3
"""
solver.py

    Recovers program using capstone, which must then be manually reversed :(
"""
import binascii
from capstone import *

def main():
    with open("program.txt", "r") as fd:
        contents = fd.read().replace(",", "").strip().split(" ")

    print(contents)

    # parse out ints into hex string
    code = "".join([str(hex(int(b))).replace("0x", "") for b in contents])
    print(len(code))

    # raw binary for consumption
    bincode = binascii.a2b_hex(code)
    print(bincode)

    # print instructions
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    for i in md.disasm(code, 0x1000):
        print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))


if __name__ == "__main__":
    exit(main())
