#!/usr/bin/python3
# coding: UTF-8
import shutil
import requests
import os
import time
import random
import os.path
from lxml import html


class Downloader:
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/6.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/21.0.1084.52 Safari/546.5',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-EN,fr;q=0.8,en-US;q=0.6,en;q=0.4',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'identity',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    DEFAULT_WAIT = 1
    DEFAULT_NAME = "default"
    
    COOKIES = dict()

    def __init__(self, parent, output_path):
        self.parent = parent
        self.output_path = output_path
        self.folder_name = self.DEFAULT_NAME
        self.wait_time = self.DEFAULT_WAIT

    def get_html(self, url, clean=False):
        r = requests.get(url, headers=self.headers, cookies=self.COOKIES)
        if r.status_code == 200:
            if clean:
                if not r.encoding:
                    r.encoding = "utf8"
                return r.text.encode(r.encoding, "ignore")
            else:
                return r.text
        else:
            print("Invalid URL:",url)
            return ""

    def get_xpath(self, url, xpath=None):
        web_page = self.get_html(url, True)
        if web_page:
            tree = html.fromstring(web_page)
            if xpath is None:
                return tree
            else:
                return tree.xpath(xpath)
        return None

    def get_file(self, url, folder_name="", file_name="", verbose=False):
        if folder_name == "":
            folder_name = self.folder_name
        if file_name is "":
            file_name = url.split("/")[-1]
        if verbose:
            print("DOWNLOADING", folder_name, file_name)
        r = requests.get(url, headers=self.headers, stream=True, cookies=self.COOKIES)
        self.create_folder(self.output_path + folder_name)
        with open(self.output_path + folder_name + os.sep + file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    def file_exists(self, file_path):
        return os.path.isfile(file_path)

    def create_folder(self, path):
        try:
            os.makedirs(path)
        except OSError:
            pass

    def wait(self, wait_time=0, random=False):
        if wait_time == 0:
            wait_time = self.wait_time
        if random:
            time.sleep(wait_time + random.random())  # wait time +- 1sec
        else:
            time.sleep(wait_time)

    def add_cookie(self, k, v):
        self.COOKIES[k] = v
            
    def get_output_path(self):
        return self.output_path

    def set_wait_time(self, time):
        self.wait_time = time

    def set_folder_name(self, name):
        self.folder_name = name

    def reset(self):
        self.folder_name = "default"
        self.wait_time = self.DEFAULT_WAIT
        
    def parse(self, url):
        self.parent.execute([url])

    def debug(self):
        print("[DEBUG] Path: "+self.output_path+" time: "+str(self.wait_time))
