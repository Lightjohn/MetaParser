#!/usr/bin/python3
# coding: UTF-8
from metaParser import Parser
import time

class ChildParser(Parser):
    def parse(self, url):
        # If we don't want downloaded files to arrive in standard folder
        self.dl.set_folder_name("mydemo")
        # Print some informations about the parser
        self.dl.debug()
        # let's dl some google Logo
        self.dl.get_file("https://www.google.fr/images/branding/googleg/1x/googleg_standard_color_128dp.png")

