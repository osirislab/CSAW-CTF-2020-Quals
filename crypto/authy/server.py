"""
server.py

    Implements the API that implements a "secure" note-sharing service with your friendly authoritarian
    government.
"""

import base64
import flask

# flag that is to be returned once authenticated
FLAG = "flag{h4ck_th3_h4sh}"

# secret used to generate HMAC with
SECRET = "br4nd_n3w_ap1"

app = flask.Flask(__name__)


def sha1(data):
    bytes = ""

    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    for n in range(len(data)):
        bytes+='{0:08b}'.format(ord(data[n]))
    bits = bytes+"1"
    pBits = bits
    #pad until length equals 448 mod 512
    while len(pBits)%512 != 448:
        pBits+="0"
    #append the original length
    pBits+='{0:064b}'.format(len(bits)-1)

    def chunks(l, n):
        return [l[i:i+n] for i in range(0, len(l), n)]

    def rol(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xffffffff

    for c in chunks(pBits, 512):
        words = chunks(c, 32)
        w = [0]*80
        for n in range(0, 16):
            w[n] = int(words[n], 2)
        for i in range(16, 80):
            w[i] = rol((w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]), 1)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(0, 80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = rol(a, 5) + f + e + k + w[i] & 0xffffffff
            e = d
            d = c
            c = rol(b, 30)
            b = a
            a = temp

        h0 = h0 + a & 0xffffffff
        h1 = h1 + b & 0xffffffff
        h2 = h2 + c & 0xffffffff
        h3 = h3 + d & 0xffffffff
        h4 = h4 + e & 0xffffffff

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

        # TODO: encrypt infostr with AES-CBC

        # generate an encoded ID from the payload
        identifier = str(base64.b64encode(infostr.encode("ascii")))

        # instantiate a hasher and generate a vulnerable MAC
        #hasher = hashlib.sha1()
        #hasher.update((SECRET + infostr).encode('utf-8'))
        #checksum = hasher.hexdigest()
        checksum = sha1(SECRET + infostr)
        return "Encrypting with secret of size {}...\nSuccessfully added {}:{}\n".format(len(SECRET), identifier, checksum)


@app.route("/view", methods=["POST"])
def view():

    # TODO: decrypt the identifier with AES-CBC

    # retrieve the note to recover from user input
    info = flask.request.form.to_dict()
    if "id" not in info.keys():
        return ">:(\n"
    if "integrity" not in info.keys():
        return ">:(\n"
    #if "password" not in info.keys():
    #    return ">:(\n"

    identifier = str(base64.b64decode(info["id"]).decode("ascii"))
    checksum = info["integrity"]

    print(SECRET + identifier)

    # rederive identifier dict
    params = identifier.replace("&", " ").split(" ")
    note_dict = { param.split("=")[0]: param.split("=")[1]  for param in params }

    # check integrity
    #hasher = hashlib.sha1()
    #hasher.update((SECRET + identifier).encode('utf-8'))
    #gen_checksum = hasher.hexdigest()
    gen_checksum = sha1(SECRET + identifier)

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
