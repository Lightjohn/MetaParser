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

sys.path.insert(0, 'hoster')  # adding local path hoster for futur import
output_path = expanduser("~")+os.sep+"metaParser/"


class Parser:
    '''
    Every parser should implement this class and overload parser
    Contains:
        dl (downloader tool wrapping requests)
    '''

    def __init__(self, dl_util):

        if isinstance(dl_util, metaParserUtils.Downloader):
            self.dl = dl_util
        else:
            raise TypeError

    def parse(self, url):
        pass


class MetaParser:

    THREADS = 4

    def fix_object_name(self, obj_name):
        for a in ['.', '-']:
            obj_name = obj_name.replace(a, '')
        return obj_name

    def fix_url(self, url):
        # In the case where we have a simple url with no / at the end
        if "/" not in url.replace("://", ""):
            url += "/"
        return url

    def execute(self, argv):
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
                        traceback.print_exc()
                except ImportError as e:
                    print(
                        "Cannot load module: " + module_name + " : NOT IMPLEMENTED YET (or missing import or module dependency not installed on the system)")
                    traceback.print_exc()
            else:
                print("Invalid URL found: " + url)
        dl_utils.close_and_join()

    def execute_main(self, argv):
        parser = argparse.ArgumentParser(
            description='Handle url and will git them to the good module')
        parser.add_argument('-n',  type=int, default=4,help='Number of downloads in parallel')
        parser.add_argument('urls', metavar='N', nargs='+', help='an infinite numbers of URLS')
        input_args = parser.parse_args()
        self.THREADS = input_args.n
        self.execute(input_args.urls)


if __name__ == "__main__":
    a = MetaParser()
    a.execute_main(sys.argv)
