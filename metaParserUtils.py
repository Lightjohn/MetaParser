#!/usr/bin/python3
# coding: UTF-8
import shutil
import requests
import os
import time
import random
import os.path
from multiprocessing.pool import ThreadPool as Pool
from lxml import html


class Downloader:
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/7.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/21.0.1084.52 Safari/546.5',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-EN,fr;q=0.8,en-US;q=0.6,en;q=0.4',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'identity',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    DEFAULT_WAIT = 1
    DEFAULT_NAME = ""

    COOKIES = dict()
    AUTH = ()

    def __init__(self, parent=None, output_path="", nb_downloads=4):
        self.parent = parent
        self.output_path = output_path
        self.folder_name = self.DEFAULT_NAME
        self.wait_time = self.DEFAULT_WAIT
        self.pool = Pool(processes=nb_downloads)

    def __del__(self):
        pass

    def get_html(self, url, clean=False):
        """
        Return the content if the url given.

        :param url:
        :param clean: force the output to be converted to utf-8
        :return:
        """
        r = requests.get(url, headers=self.headers, auth=self.AUTH, cookies=self.COOKIES)
        if r.status_code == 200:
            if clean:
                if not r.encoding:
                    r.encoding = "utf8"
                return r.text.encode(r.encoding, "ignore")
            else:
                return r.text
        else:
            print("Invalid URL:", url)
            return ""

    def get_xpath(self, url, xpath=None):
        """
        Return a xpath on the url given in put
        Use get_html(url, True) to get html.

        :param url:
        :param xpath:
        :return:
        """
        web_page = self.get_html(url, True)
        if web_page:
            tree = html.fromstring(web_page)
            if xpath is None:
                return tree
            else:
                return tree.xpath(xpath)
        return None

    def create_folder(self, path):
        """
        A small utility function to encapsulate os.makedirs

        :param path:
        :return:
        """
        try:
            os.makedirs(path)
        except OSError:
            pass

    def download(self, url, folder_name, file_name):
        """
        This function will download as a file the url.
        Maybe the function you really want is get_file

        :param url:
        :param folder_name: the folder in wich we download the file
        :param file_name: the name of the file
        :return:
        """
        r = requests.get(url, headers=self.headers, stream=True, auth=self.AUTH, cookies=self.COOKIES)
        self.create_folder(self.output_path + folder_name)
        with open(self.output_path + folder_name + os.sep + file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    def get_file(self, url, folder_name="", file_name="", async=False, verbose=False):
        """
        High level function to encapsulate download.
        If no folder name or file name given the function will use global parameters or guess the values.

        :param url:
        :param folder_name:
        :param file_name:
        :param async: To use the thread pool to go faster
        :param verbose: Debug mode
        :return:
        """
        if folder_name == "":
            folder_name = self.folder_name
        elif self.folder_name != self.DEFAULT_NAME:
            folder_name = self.folder_name + os.sep + folder_name
        if file_name is "":
            file_name = url.split("/")[-1]
        if verbose:
            print("DOWNLOADING", folder_name, file_name)
        if async:
            self.pool.apply_async(self.download, (url, folder_name, file_name,))
        else:
            self.download(url, folder_name, file_name)

    def launch_async(self, func, args):
        """
        Debug function that will launch given function in threadpool.
        :param func:
        :param args: args of func
        :return:
        """
        return self.pool.apply_async(func, args)

    def file_exists(self, file_path):
        """
        Utility function because it's shorter to use this function.

        :param file_path:
        :return:
        """
        return os.path.isfile(file_path)

    def wait(self, wait_time=0, random=False):
        """
        To avoid saturate a website you should wait.
        If called without argument it will wait 1s. If random is true it will add a time between 0-1 sec.

        :param wait_time:
        :param random:
        :return:
        """
        if wait_time == 0:
            wait_time = self.wait_time
        if random:
            time.sleep(wait_time + random.random())  # wait time +- 1sec
        else:
            time.sleep(wait_time)

    def add_cookie(self, k, v):
        self.COOKIES[k] = v

    def add_auth(self, tuple):
        self.AUTH = tuple

    def get_output_path(self):
        """
        Return the concatenation of the output path and the current folder.

        :return:
        """
        return self.output_path + self.folder_name

    def set_wait_time(self, time):
        self.wait_time = time

    def set_folder_name(self, name):
        """
        Set the folder in which we will store the downloads.
        Note: This folder and output path are different.
        this folder will be appended to output path and for your own sake you should not override output path.

        :param name:
        :return:
        """
        self.folder_name = name

    def reset(self):
        """
        Reset the folder name, wait time.

        :return:
        """
        self.folder_name = "default"
        self.wait_time = self.DEFAULT_WAIT

    def parse(self, url):
        """
        If we want to add a new url to the parser we will call the parent
        :param url:
        :return:
        """
        if self.parent:
            self.parent.execute([url])
        else:
            print("No parent was given so the nothing will be done")

    def debug(self):
        print("[DEBUG] Path: " + self.output_path + " time: " + str(self.wait_time))

    def close_and_join(self):
        """
        Utility function, should never be call by anyone other than me. Why are you reading that ?

        :return:
        """
        self.pool.close()
        print("Finishing DL")
        self.pool.join()
        print("Done")
