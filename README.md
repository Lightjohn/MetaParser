# MetaParser
It is an easy web parser agregator to get any kind of information from any website

# Purpose
I created many small web parser, one at a time and didn't use more complete tools like scrappy because it was still too complicated.
And at one time I merged all the code into a new one: **MetaParser**.
Now the each parser is meant to do only the essential, what you need !
All boring stuff like getting html, files and can be delegated to MetaParser

# Example
Don't believe me and see how it works: you want to get every title from [Google News](https://news.google.com/)

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

We create a class with name ChildParser that *implement* Parser

`
from metaParser import Parser
class ChildParser(Parser):
`

And in this class we have the function parse

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

The name of the parser in hoster is the website name without *.* or *-* and no *https* or *www*

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
