"""
server.py

    Implements the API that implements a "secure" note-sharing service with your friendly authoritarian
    government.
"""

import ast
import json
import base64
import hashlib

import flask
import pickledb

# flag that is to be returned once authenticated
FLAG = "flag{h4ck_th3_h4sh}"

# secret used to generate HMAC with
SECRET = "br4nd_n3w_ap1"

app = flask.Flask(__name__)

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
        :password: helps protect the ID hash you get back with AES-CBC (does not encrypt your note, we do it for you)

    RETURN PARAMS:
        :id: an ID protected by password  that you can use to retrieve and decrypt the note.
        :integrity: make sure you give this to validate your ID, Fraud is a high-level offense!


/view
    DESCRIPTION:
        View and decrypt the contents of a note stored on our government-sponsored AWS knockoff

    GET PARAMS:
        :id: an ID that you can use to retrieve and decrypt the note.
        :integrity: make sure you give this to validate your ID, Fraud is a high-level offense!

    RETURN PARAMS:
        :message: the original unadultered message you stored on our service.

RULES
- We will be very upset if you send unwarranted API parameters >:(
- we will also be very upset if you attempt to impersonate our glorious admin >:(
- And we will most be upset if you are trying to read files you have no business reading >:(
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

        # generate an encoded ID from the payload
        identifier = base64.b64encode(bytes(str(info), "utf-8"))

        # TODO: encrypt the identifier with AES-CBC

        print(str(info))

        # instantiate a hasher and generate a vulnerable MAC
        hasher = hashlib.sha1()
        hasher.update((SECRET + str(info)).encode('utf-8'))
        checksum = hasher.hexdigest()
        return "Successfully added {}:{}\n".format(identifier, checksum)


@app.route("/view", methods=["POST"])
def view():

    # TODO: decrypt the identifier with AES-CBC

    # retrieve the note to recover from user input
    info = flask.request.form.to_dict()
    if "id" not in info.keys():
        return ">:(\n"
    if "integrity" not in info.keys():
        return ">:(\n"

    identifier = info["id"]
    checksum = info["integrity"]

    # rederive identifier dict
    note_dict = ast.literal_eval(str(base64.b64decode(identifier).decode("ascii")))

    # check integrity
    hasher = hashlib.sha1()
    hasher.update((SECRET + str(note_dict)).encode('utf-8'))
    gen_checksum = hasher.hexdigest()

    # return if failed integrity check
    if checksum != gen_checksum:
        return ">:(\n>:(\n>:(\n"

    # iterate over the note_dict.
    # Deny if admin = False and access_sensitive = False and
    # it wants any entrynum in the range of 0 - 10
    try:
        entrynum = int(note_dict["entrynum"])
        if 0 <= entrynum <= 10:
            if (note_dict["admin"] != True) and (note_dict["access_sensitive"] != True):
                return ">:(\n"

            if (entrynum == 7):
                return FLAG

    # IndexError, ...
    except Exception:
        return ">:(\n"

app.run()
