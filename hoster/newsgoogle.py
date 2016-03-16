#!/usr/bin/python3
# coding: UTF-8
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
