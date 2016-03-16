# MetaParser
It is an easy web parser agregator to get any kind of information from any website.

# Purpose
I created many small web parser, one at a time and didn't use more complete tools like scrappy because it was still too complicated.
And at one time I merged all the code into a new one: **MetaParser**.
Now the each parser is meant to do only the essential, what you need !
All boring stuff like getting html, files and can be delegated to MetaParser.

# Example
Don't believe me and see how it works: you want to get every title from [Google News](https://news.google.com/).

```python
from metaParser import Parser
from lxml import html
from lxml import etree

class ChildParser(Parser):
    def parse(self, url):
        ans = self.dl.get_html(url, clean=True)
        tree = html.fromstring(ans)
        news = tree.xpath('//span[@class="titletext"]')
        print("Got", len(news), "news")
        for i in news:
            print(i.text)
```

Important things here:

We create a class with name ChildParser that *implement* Parser:

`
from metaParser import Parser
class ChildParser(Parser):
`

And in this class we have the function parse:

`
def parse(self, url):
`

The name of the class and function cannot be changed.

# How to launch
`
python3 metaParser.py https://news.google.com/
`

# How does it work and how to name new parser
When an url is given to metaParser it will search in the folder **hoster** the corresponding parser file.

The name of the parser in hoster is the website name without *.* or *-* and no *https* or *www*:

https://news.google.com -> newsgoogle.py

www.theguardian.com/stuff -> guardian.py

https://news.google.guardian-whynot.net/something.html -> newsgoogleguardianwhynot.py

# tl;dr

In hoster put a file named from the website you want without http,www,.,-

paste that inside:

```
from metaParser import Parser

class ChildParser(Parser):
    def parse(self, url):
        pass
```

replace pass by what you want and that's good.

# Details
By implementing Parser, you get an attribute called **dl**.

metaparser.py contain the original ouput_path where will be saved files or images or whatever.

What can do *self.dl*
```python
# Get html via requests, if clean, will force the conversion to utf8
self.dl.get_html(url, clean=False)

# Get file, if nothing other that url if given, it will guess name and output folder
self.dl.get_file(url, folder_name="default", file_name="", verbose=False)

# A good parser wait before another attempt, but we can be sneaky if needed (random: 0-1sec)
self.dl.wait(wait_time=1, random=False)
```
I put more setter, getter and some file management functions in **metaParserUtils.py**.

