#!/usr/bin/env python3
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
    password = "Zmxh"

    # manually regenerate A value
    a = server.gen_seed()
    A = server.modular_pow(g, a, N)

    # get salt and B value
    resp = requests.post("http://127.0.0.1:5000", data={"username": username, "a": A}).json()
    salt = resp.get("salt")
    B = resp.get("B")

    # generate u
    u = server.hasher(str(A) + str(B))
    x = server.hasher(salt + password)

    # compute S and K
    S = server.modular_pow(B - k * server.modular_pow(g, x, N), a + u * x, N)
    K = hashlib.sha256(str(S).encode()).digest()

    # Compute HMAC
    hm = server.hmac_sha256(K, salt.encode())

    resp = requests.post("http://127.0.0.1:5000", data={"username": username, "hmac": hm}).text
    print(resp)


if __name__ == "__main__":
    exit(main())
