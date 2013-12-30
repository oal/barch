## Barch

Barch is a simple backup tool for Seafile.

### Setup

    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt

    python barch.py

Then you should be asked to fill in your Seafile server address, library etc.

You have to create a library, and put a file called "config.json" in its root. The file should look something like this:

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
