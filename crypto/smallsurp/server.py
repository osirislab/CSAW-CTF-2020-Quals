#!/usr/bin/env python3
import os
import base64
import hashlib
import random

import flask
import flask_socketio as sio

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(12)

# read flag from file
with open("flag.txt", "r") as fd:
    FLAG = list(fd.read())

with open("database.txt", "r") as fd:
    lines = fd.readlines()

# instantiate database from incomplete database and portions of the flag
DATABASE = {}
for line in lines:
    DATABASE[line.split(":")[0]] = base64.b64encode(bytes("".join(FLAG[0:3]), "utf-8")).decode("ascii")
    FLAG = FLAG[3:]

# NIST compliant prime number
N = int("00ab76f585834c3c2b7b7b2c8a04c66571539fa660d39762e338cd8160589f08e3d223744cb7894ea6b424ebab899983ff61136c8315d9d03aef12bd7c0486184945998ff80c8d3d59dcb0196fb2c37c43d9cbff751a0745b9d796bcc155cfd186a3bb4ff6c43be833ff1322693d8f76418a48a51f43d598d78a642072e9fff533", 16)

# agreed upon parameters by both client and server
g = 2
k = 3

# we generate our own pseudorandom `b`
b = random.randint(0, N - 1)

# generate a salt to be used for hashing
salt = str(random.randint(0, 2**32 - 1))

# HMAC we want to use to compare with client
SERVER_HMAC = None

def gen_seed():
    return random.randint(0, N - 1)

def xor_data(binary_data_1, binary_data_2):
    return bytes([b1 ^ b2 for b1, b2 in zip(binary_data_1, binary_data_2)])

def modular_pow(base, exponent, modulus):
    if modulus == -1:
        return 0

    result = 1
    base %= modulus

    while exponent > 0:
        if exponent % 2:
            result = (result * base) % modulus
        exponent >>= 1
        base = (base * base) % modulus

    return result


def hmac_sha256(key, message):
    if len(key) > 64:
        key = sha256(key).digest()
    if len(key) < 64:
        key += b'\x00' * (64 - len(key))

    o_key_pad = xor_data(b'\x5c' * 64, key)
    i_key_pad = xor_data(b'\x36' * 64, key)
    return hashlib.sha256(o_key_pad + hashlib.sha256(i_key_pad + message).digest()).hexdigest()


def hasher(data):
    return int(hashlib.sha256(data.encode()).hexdigest(), 16)


# reuse methods and constants across HTML templates
app.jinja_env.globals.update(
    gen_seed=gen_seed,
    modular_pow=modular_pow,
    N=N,
)


@app.route("/", methods=["GET", "POST"])
def home():
    global SERVER_HMAC
    print(DATABASE)
    if flask.request.method == "POST":

        # get username to identify entry in "database"
        username = flask.request.form.get("username")
        if username is None:
            flask.flash("Error encountered on server-side.")
            return flask.redirect(flask.url_for("home"))


        # find entry given the username on our server-side
        try:
            pwd = DATABASE[username]
        except KeyError:
            flask.flash("Cannot find password for username in database")
            return flask.redirect(flask.url_for("home"))

        # if HMAC parameter is set, check instead and redirect
        hmac = flask.request.form.get("hmac")
        if (hmac is not None) and (SERVER_HMAC is not None):

            print(hmac, SERVER_HMAC)

            # success! authenticated without the need for sending password
            if hmac == SERVER_HMAC:
                #return flask.redirect(flask.url_for("dash"))
                return "Noice"
            else:
                flask.flash("Incorrect password.")
                return flask.redirect(flask.url_for("home"))

        # client side should generate `A = g**a % N` and send instead of pwd
        A = flask.request.form.get("a")
        if A is None:
            flask.flash("Error encountered on server-side.")
            return flask.redirect(flask.url_for("home"))

        # block certain values of A to make it harder
        if A in [str(N)]:
            flask.flash("Cannot find password for username in database")
            return flask.redirect(flask.url_for("home"))

        # xH = sha256(salt + pwd)
        xH = hasher(salt + str(pwd))

        # v = g**x % N
        v = modular_pow(g, xH, N)

        # create B value to return back to client
        B = (k * v + modular_pow(g, b, N)) % N
        u = hasher(str(A) + str(B))

        # compute S and K
        S = modular_pow(float(A) * modular_pow(v, u, N), b, N)
        K = hashlib.sha256(str(S).encode()).digest()

        # compute the HM on the server end for comparison
        SERVER_HMAC = hmac_sha256(K, salt.encode())

        # send back salt and B for client to use to compute HMAC
        return flask.jsonify(salt=salt, B=B)
    else:
        return flask.render_template("home.html")


@app.route("/dash/<user>", methods=["POST"])
def dashboard(user):
    pwd = DATABASE[user]
    encoded = base64.b64encode(bytes(pwd, "utf-8")).encode()
    return flask.render_template("home.html", encoded=encoded)


if __name__ == "__main__":
    app.run()
