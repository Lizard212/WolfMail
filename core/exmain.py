#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.com import *
from common.ver import *
from common.config import configParser
from common.exceptions import wolfException
import re
import os
import sys
import time
import random
import socket
import logging
import argparse
import subprocess


def file_exists(file_list):
    for file in file_list:
        if not os.path.exists(file):
            raise wolfException(
                "The file \"%s\" doesn't Exists on the system!!!" % (file))


class AddressAction(argparse.Action):
    def __call__(self, parser, args, values, option=None):
        args.options = values

        if args.attach:
            if not args.options:
                parser.error("Usage --attach <file1 file2 file3>")
            else:
                file_exists(args.options)


class exMain:
    def __init__(self):
        parser = argparse.ArgumentParser()
        group_parser = parser.add_mutually_exclusive_group(required=True)
        group_parser.add_argument(
            '--attach', dest='attach', action='store_const', const='attach', help="Attach Email")
        group_parser.add_argument(
            '--text', dest='text', action='store_const', const='text', help="Text Email")
        parser.add_argument('options', nargs='*', action=AddressAction)
        parser.add_argument('--config_file', '-c', action='store', dest='config_file',
                            help="Configuration file", metavar="FILE", required=True)
        parser.add_argument('--mail_user', '-m', action='store',
                            dest='mail_file', help="Mail File", metavar="FILE", required=True)
        parser.add_argument('--html_file', '-f', action='store',
                            dest='html_file', help="HTML file", metavar="FILE", required=True)
        parser.add_argument('--verbose', '-v', action='store_true',
                            help="Verbose for ending email", default=False)
        parser.add_argument('--warning', '-w', action='store_true',
                            help="Warning massage", default=False)
