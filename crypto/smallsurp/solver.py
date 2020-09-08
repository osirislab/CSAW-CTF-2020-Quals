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
import server

N = server.N
g = 2
k = 3

def main():

    # username and password combo
    username = "joe"
    password = "i have no idea"

    # manually regenerate A value
    a = server.gen_seed()
    #A = server.modular_pow(g, a, N)
    A = server.N

    # get salt and B value
    resp = requests.post("http://127.0.0.1:5000", data={"username": username, "a": A}).json()
    salt = resp.get("salt")
    B = resp.get("B")

    # generate u
    u = server.hasher(str(A) + str(B))
    x = server.hasher(salt + password)

    # compute S and K
    #S = server.modular_pow(B - k * server.modular_pow(g, x, N), a + u * x, N)
    S = hex(0)[2:]
    K = hashlib.sha256(S.encode()).digest()

    # Compute HMAC
    hm = server.hmac_sha256(K, salt.encode())

    resp = requests.post("http://127.0.0.1:5000", data={"username": username, "hmac": hm}).text
    print(resp)


if __name__ == "__main__":
    exit(main())
