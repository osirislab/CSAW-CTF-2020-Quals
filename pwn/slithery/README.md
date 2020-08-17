## slithery

* __Category:__ - reversing
* __Point Value__ - 100-200 range

Python sandbox that restricts commonly used payloads for escape. User must instead figure out from obfuscated source what dependency is being used (numpy), and use that in order to craft a specialized payload to cause a segmentation fault, which returns the flag.

## Usage

`sandbox.py` is given to the user.

```
$ python runner.py
```
