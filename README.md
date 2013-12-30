## Barch

Barch is a simple backup tool for Seafile.

### Setup

    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt

    python barch.py

Then you should be asked to fill in your Seafile server address, library etc.

In your library, create a file called "config.json" in the library root. The file should look something like this:

```json
{
   "mysql": [
       {
           "username": "username",
           "password": "password",
           "databases": ["one", "or", "more", "databases"]
       }
   ],
   "git": [
       {
           "directory": "/home/git/repositories/",
           "recursive": true
       }
   ],
   "sqlite": [
       "/home/user/my.db"
   ],
   "postgres": [
       "db1",
       "db2"
   ]
}
```

Then when you run `python barch.py` on your server, it will read the `config.json` file that was created the first time `barch.py` was run, and connect to the library on your Seafile server. It'll download `config.json` from the library, and from the information you've added to that file, know what it should back up. Backups will be added to `library_root/git/repo.tar.gz`, and similar for the other backup procedures.

To sum things up: There are two `config.json` files. One is created on the server (contains login information to Seafile), and you create one in your library (containing database logins etc).

Feel free to add more backup procedures, or improve upon the existing ones.


I use this on two servers, and it works well. Just set it up to run with a cronjob every night (or more often if you want). Also, I put this on Github in a hurry, so let me know if you find any bugs or other issues.

You can find me in #seafile on Freenode as oal.

### License
The MIT License (MIT)

Copyright (c) 2013 Olav Lindekleiv

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
