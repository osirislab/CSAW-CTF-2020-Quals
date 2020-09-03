#!/usr/bin/env python3
"""
server.py

    Implements the API that implements a "secure" note-sharing service with your friendly authoritarian
    government.
"""

import struct
import base64
import flask

# flag that is to be returned once authenticated
FLAG = "flag{h4ck_th3_h4sh}"

# secret used to generate HMAC with
SECRET = "br4nd_n3w_ap1".encode()

app = flask.Flask(__name__)

def left_rotate(value, shift):
    return ((value << shift) & 0xffffffff) | (value >> (32 - shift))


def sha1(message, ml=None, h0=0x67452301, h1=0xEFCDAB89, h2=0x98BADCFE, h3=0x10325476, h4=0xC3D2E1F0):
    # Pre-processing:
    if ml is None:
        ml = len(message) * 8

    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'

    message += struct.pack('>Q', ml)

    # Process the message in successive 512-bit chunks:
    for i in range(0, len(message), 64):

        # Break chunk into sixteen 32-bit big-endian integers w[i]
        w = [0] * 80
        for j in range(16):
            w[j] = struct.unpack('>I', message[i + j * 4:i + j * 4 + 4])[0]

        # Extend the sixteen 32-bit integers into eighty 32-bit integers:
        for j in range(16, 80):
            w[j] = left_rotate(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16], 1)

        # Initialize hash value for this chunk:
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        # Main loop
        for j in range(80):
            if j <= 19:
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (d & (b | c))
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = left_rotate(a, 5) + f + e + k + w[j] & 0xffffffff
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp

        # Add this chunk's hash to result so far:
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff

    # Produce the final hash value (big-endian) as a 160 bit number, hex formatted:
    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)


@app.route("/", methods=["GET", "POST"])
def home():
    return """
This is a secure and private note-taking app sponsored by your favorite Nation-State.
For citizens' convenience, we offer to encrypt your notes with OUR own password! How awesome is that?
Just give us the ID that we give you back and we'll happily decrypt it back for you!

Unfortunately we have prohibited the use of frontend design in our intranet, so the only way you can interact with it is our API.

/new

    DESCRIPTION:
        Adds a new note and uses our Super Secure Cryptography to encrypt it.

    POST PARAMS:
        :author: your full government-issued legal name
        :note: the message body you want to include. We won't read it :)

    RETURN PARAMS:
        :id: an ID protected by password  that you can use to retrieve and decrypt the note.
        :integrity: make sure you give this to validate your ID, Fraud is a high-level offense!


/view
    DESCRIPTION:
        View and decrypt the contents of a note stored on our government-sponsored servers.

    GET PARAMS:
        :id: an ID that you can use to retrieve and decrypt the note.
        :integrity: make sure you give this to validate your ID, Fraud is a high-level offense!

    RETURN PARAMS:
        :message: the original unadultered message you stored on our service.

RULES
- Please do not set unwarranted API parameters >:(
"""

@app.route("/new", methods=["POST"])
def new():
    if flask.request.method == "POST":

        # check content provided
        payload = flask.request.form.to_dict()
        if "author" not in payload.keys():
            return ">:(\n"
        if "note" not in payload.keys():
            return ">:(\n"

        # user should not set `admin` or `access_sensitive` here, we set it for them, and they
        # override it when pinging back `/view`
        if "admin" in payload.keys():
            return ">:(\n>:(\n"
        if "access_sensitive" in payload.keys():
            return ">:(\n>:(\n"

        # sanitize payload with our stuff
        # - set `admin` and `access_sensitive` as False, user will need to append overrides
        # - set an entry number given the entry in the kv database, user will need to override as 7
        info = {"admin": False, "access_sensitive": False }
        info.update(payload)
        info["entrynum"] = 783

        # turn it back into a param string
        infostr = ""
        for pos, (key, val) in enumerate(info.items()):
            infostr += "{}={}".format(key, val)
            if pos != (len(info) - 1):
                infostr += "&"

	# convert to bytes for consumption
        infostr = infostr.encode()
        print(infostr)

        # generate an encoded ID from the payload
        identifier = base64.b64encode(infostr).decode("ascii")

        # instantiate a hasher and generate a vulnerable MAC
        checksum = sha1(SECRET + infostr)
        return "Encrypting with secret of size {}...\nSuccessfully added {}:{}\n".format(len(SECRET), identifier, checksum)


@app.route("/view", methods=["POST"])
def view():

    # retrieve the note to recover from user input
    info = flask.request.form.to_dict()
    if "id" not in info.keys():
        return ">:(\n"
    if "integrity" not in info.keys():
        return ">:(\n"

    identifier = base64.b64decode(info["id"]).decode()
    checksum = info["integrity"]

    # rederive identifier dict
    params = identifier.replace("&", " ").split(" ")
    note_dict = { param.split("=")[0]: param.split("=")[1]  for param in params }

    # check integrity
    print(identifier.encode())
    gen_checksum = sha1(SECRET + identifier.encode())

    # return if failed integrity check
    print(checksum, gen_checksum)
    if checksum != gen_checksum:
        return ">:(\n>:(\n>:(\n"

    # iterate over the note_dict.
    # Deny if admin = False and access_sensitive = False and
    # it wants any entrynum in the range of 0 - 10
    try:
        entrynum = int(note_dict["entrynum"])
        if 0 <= entrynum <= 10:
            print("We getting sensitive...")

            # both params must be set true to continue
            if (note_dict["admin"] not in [True, "True"]):
                return ">:(\n"
            if (note_dict["access_sensitive"] not in [True, "True"]):
                return ">:(\n"

            # our entrynum == 7, and the two necessary params are set
            if (entrynum == 7):
                return "You disobeyed our rules, but here's the note: " + FLAG + "\n"
            else:
                return "Hmmmmm...."

        # the entrynum is static, so just return the note stored on the ID
        else:
            return """Author: {}
Note: {}\n""".format(note_dict["author"], note_dict["note"])


    # IndexError, and other stuff that might break when iterating the dict
    except Exception:
        return ">:(\n"

app.run()
