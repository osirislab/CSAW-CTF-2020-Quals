import os
import requests
import time


def default_callable(func):
    class Callable(object):
        def __init__(self, func):
            self.func = func

        def __repr__(self):
            return str(self)

        def __str__(self):
            return self()

        def __call__(self):
            return self.func()

    return Callable(func)


@default_callable
def ls():
    """ List directory contents """
    return os.system("ls")


class Service(object):
    """ Connect to a service """

    def __init__(self, host, default_args={}):
        self.host = host
        self.default_args = default_args

        self.cached = None
        self.last_cached = 0

    def __gt__(self, other):
        if not isinstance(other, Service):
            raise TypeError(
                "'>' is not supported between instances of '%s' and '%s'"
                % (type(self).__name__, type(other).__name__)
            )

        data = self()
        other(data)

    def __call__(self, args=None):
        if args is None:
            args = self.default_args

        if self.cached is not None and time.time() - last_cached <= 60:
            return self.cached

        try:
            r = requests.get(self.host, params=args)
            self.cached = r.text
            last_cached = time.time()
        except Exception as e:
            self.cached = ""
            print("Error: %s" % (e))

        return self.cached


def Import(fname: str):
    """ Import other Pyash files """
    if fname.endswith(".py"):
        __import__(fname)
    else:
        raise FileNotFoundError()
