#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser
import re
import sys


class configParser:
    result = {}

    @staticmethod
    def parse(config_file):
        if not configParser.result:
            ter_parser = SafeConfigParser()
            ter_parser.read(config_file)

            for section_name in ter_parser.sections():
                if section_name == "mail":
                    for name, value in ter_parser.items(section_name):
                        if name == "domain":
                            domain = value
                            configParser.result["domain"] = domain
                elif section_name == "smtp":
                    for name, value in ter_parser.items(section_name):
                        if name == "server":
                            server = value
                            configParser.result["server"] = value
                        elif name == "time":
                            wait_time = value
                            configParser.result["wait_time"] = value
                elif section_name == "log":
                    for name, value in ter_parser.items(section_name):
                        if name == "type":
                            mail_type = value
                            configParser.result["mail_type"] = value
                        elif name == "log_path":
                            mail_log = value
                            configParser.result["mail_log"] = value
                else:
                    print >> sys.stderr, bcolors.OKBLUE + "Error: " + bcolors.ENDC + bcolors.FAIL + \
                        "Wrong Parameter usage in the config: %s" % (
                            self.config_file) + bcolors.ENDC
                    sys.exit(1)
            return configParser.result
        else:
            return configParser.result
