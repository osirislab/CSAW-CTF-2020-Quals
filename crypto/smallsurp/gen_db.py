#!/usr/bin/env python3
"""
gen_db.py

    Given a secret (the flag), create a
"""
import os
from base64 import b64encode
from binascii import hexlify

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Protocol.SecretSharing import Shamir

# the field we are using is Gf(2^8)
POLYFIELD = 128

# represents password for admin we will use to encrypt the flag
SECRET = b"_z3r0_kn0wl3dg3_"

# names of all administrators
NAMES = [
   "Jere",
   "Lakisha",
   "Loraine",
   "Ingrid",
   "Orlando",
   "Berry",
   "Alton",
   "Bryan",
   "Kathryn",
   "Brigitte",
   "Dannie",
   "Jo",
   "Leslie",
   "Adrian",
   "Autumn",
   "Kellie",
   "Alphonso",
   "Joel",
   "Alissa",
   "Rubin"
]


DATABASE = {}

# first, write an incomplete db "breach" for handout
if not os.path.exists("database.txt"):
    with open("database.txt", "w") as fd:
        for name in NAMES:
            fd.write(name.lower() + ":\n")

shares = Shamir.split(18, 20, SECRET)

# initialize database with a share for each user
for name, share in zip(NAMES, shares):
    idx, content = share
    DATABASE[name] = "{}:{}:{}".format(idx, hexlify(content).decode(), POLYFIELD)

# create a encrypted.txt given the secret now
if not os.path.exists("encrypted.txt"):
    with open("encrypted.txt", "w") as fd, open("flag.txt", "rb") as flfd:

        flag = flfd.read()
        flag = flag + (AES.block_size - (len(flag) % AES.block_size)) * b'\x00'

        cipher = AES.new(SECRET, AES.MODE_CBC)
        ct = cipher.encrypt(flag)
        iv = cipher.iv

        fd.write("cbc:" + iv.hex() + ":" + ct.hex())
