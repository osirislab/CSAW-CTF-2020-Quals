#!/usr/bin/env python3
"""
solver.py

    Serves as both solver and client. Sends a zero key for A in order to
    break SRP and bypass authentication.

"""
import requests
import json
import hashlib
import random
import binascii

import server
import gen_db

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Protocol.SecretSharing import Shamir

N = server.N
g = 2
k = 3

# anything is fine, we are doing an auth bypass
password = "i have no idea"

def main():

    # manually regenerate A value
    a = server.gen_seed()
    #A = server.modular_pow(g, a, N)
    A = server.N * 2

    # get salt and B value
    shares = []
    for username in gen_db.NAMES:
        resp = requests.post("http://127.0.0.1:5000", data={"username": username, "token1": A}).json()
        salt = resp.get("nacl")
        B = resp.get("token2")

        # generate u
        u = server.hasher(str(A) + str(B))
        x = server.hasher(salt + password)

        # compute S and K
        #S = server.modular_pow(B - k * server.modular_pow(g, x, N), a + u * x, N)
        S = hex(0)[2:]
        K = hashlib.sha256(S.encode()).digest()

        # Compute HMAC
        hm = server.hmac_sha256(K, salt.encode())

        # validate and retrieve the share
        resp = requests.post("http://127.0.0.1:5000", data={"username": username, "computed": hm}).text

        # parse out share
        share = resp.splitlines()[-7].replace(" ", "").replace("<td>", "").replace("</td>", "")
        share = share.split(":")
        shares += [(int(share[0]), binascii.unhexlify(share[1]))]

    # reconstruct secret to file with shares
    key = Shamir.combine(shares)

    print(key)

    # decrypt encrypted file with reconstructed secret
    with open("encrypted.txt", "rb") as fd:
        ctstr = str(fd.read().decode()).split(":")

        iv = binascii.unhexlify(ctstr[1])
        ct = binascii.unhexlify(ctstr[2])

        cipher = AES.new(key, AES.MODE_CBC, iv)
        result = cipher.decrypt(ct)

    print(str(result))


if __name__ == "__main__":
    exit(main())
