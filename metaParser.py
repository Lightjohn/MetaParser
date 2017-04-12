#!/usr/bin/python3
# coding: UTF-8
from os.path import expanduser
import requests
import sys
import os
import importlib
import re
import types
import metaParserUtils
import traceback
import socket
import argparse

# adding local path hoster for futur import, taken from the location of this file
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))+os.sep+"hoster")
output_path = expanduser("~")+os.sep+"metaParser"+os.sep


class Parser:
    """
    Every parser should implement this class and overload parser
    Contains:
        dl (downloader tool wrapping requests)
    """

    def __init__(self, dl_util):

        if isinstance(dl_util, metaParserUtils.Downloader):
            self.dl = dl_util
        else:
            raise TypeError

    def parse(self, url):
        pass


class MetaParser:
    """
        Metaparser is the main class that will read the input and will find and launch the module linked to the url.
    """
    THREADS = 4
    DEBUG = False

    def fix_object_name(self, obj_name):
        """
        Function that will remove every forbidden character in an url.

        :param obj_name:
        :return:
        """
        for a in ['.', '-']:
            obj_name = obj_name.replace(a, '')
        return obj_name

    def fix_url(self, url):
        """
        In the case where we have a simple url with no / at the end.

        :param url:
        :return:
        """
        if "/" not in url.replace("://", ""):
            url += "/"
        return url

    def execute(self, argv):
        """
        For every url:
            We purify the url, then we extract the core name of the url
            we try to load a module according to the core name
            Then we launch the module if everything is good

        :param argv:
        :return:
        """
        dl_utils = metaParserUtils.Downloader(self, output_path, nb_downloads=self.THREADS)
        loaded_module = dict()
        for url in argv:
            # extract the name from the url
            url = self.fix_url(url)
            name = re.match('(https?:\/\/)?(www\.)?(?P<website>.*?)\.[a-z]{2,3}\/', url)
            name = name.groupdict()
            module_name = name["website"]
            if module_name is not "":
                # When we have the name of the site, we load the file of the same name
                dl_utils.reset()
                try:
                    # importing module from hoster file
                    module_name = self.fix_object_name(module_name)
                    if module_name in loaded_module:
                        new_module = loaded_module[module_name]
                        importlib.reload(new_module)
                    else:
                        new_module = importlib.import_module(module_name)
                        loaded_module[module_name] = new_module
                    # getting class from the module
                    module = getattr(new_module, "ChildParser")
                    # initiating the module and parsing the url
                    m = module(dl_utils)
                    print("Module:", module_name)
                    try:
                        m.parse(url)
                    except Exception as e:
                        print("Exception occur in", module_name, e)
                        if self.DEBUG:
                            traceback.print_exc()
                except ImportError:
                    print(
                        "Cannot load module: " + module_name +
                        " : NOT IMPLEMENTED YET (or missing import or module dependency "
                        "not installed on the system)")
                    if self.DEBUG:
                        traceback.print_exc()
            else:
                print("Invalid URL found: " + url)
        dl_utils.close_and_join()

    def execute_main(self):
        parser = argparse.ArgumentParser(
            description='Handle url and will git them to the good module')
        parser.add_argument('-n', type=int, default=4, help='Number of downloads in parallel')
        parser.add_argument('-d', action='store_true', default=False, help='Enable debug output')
        parser.add_argument('urls', metavar='N', nargs='+', help='an infinite numbers of URLS')
        input_args = parser.parse_args()
        self.DEBUG = input_args.d
        self.THREADS = input_args.n
        self.execute(input_args.urls)


if __name__ == "__main__":
    a = MetaParser()
    a.execute_main()
