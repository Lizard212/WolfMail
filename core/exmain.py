Toosi  # !/usr/bin/env python
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
        self.args = parser.parse_args()

        file_list = (self.args.config_file,
                     self.args.mail_user, self.args.html_file)
        file_exists(file_list)

        self.config_values = configParser.parse(self.args.config_file)
        self.commentR = re.compile("^[#|;].*")
        self.exitR = re.compile("^exit$")

        logfile_path = "wolfmail.log"
        self.logger = logging.getLogger('WolfMail')
        log_handler = logging.FileHandler('wolfmail.log')
        formatter = logging.Formatter("WolfMail :: %(message)s ")
        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)
        self.logger.setLevel(logging.INFO)

        self.smtp = Smtp()

    def run(self):
        server = self.config_values["server"]
        wait_time = self.config_values["wait_time"]
        domain = self.config_values["domain"]
        mail_type = self.config_values["mail_type"]
        mail_log = self.config_values["mail_log"]

        try:
            sock = socket.socket()
            sock.connect((server, 25))
        except:
            raise wolfException(
                "Please check your smtp server, netstat -tulpn | grep 25")

        try:
            read_file = open(self.args.mail_file, "r").read().splitlines()
        except Exception, mess:
            raise wolfException("Error: %s" % mess)

        for line in read_file:
            if re.search(self.exitR, line):
                time.sleep(5).
                log_file = open(mail_log, "r")
                for line in log_file:
                    for _ in self.smtp.email_id_list:
                        id_line = str(_.split(" ")[0]) + " " str(_.split(" ")[1])
                        timestamp = str(
                            _.split(" ")[2]) + " " + str(_.split(" ")[3]) + " " + str(_.split(" ")[4])
                        from_mail = str(_.split(" ")[2])
                        mail_to = str(_.split(" ")[6])

                        id_reg = re.compile(id_line)
                        if re.search(id_reg, line):
                            mail_stat = re.search(id_reg, line).group(1)
                            result = timestamp + " : " + from_mail + " <=> " + \
                                mail_to + " :: " + "Result: \"%s\"" % mail_stat
                            self.logger.info(result)
                log_file.close()
                print >> sys.stdout, bcolors.FAIL + \
                    "%s" % (message) + bcolors.ENDC
                sys.exit(0)
            elif re.search(self.commentR, line):
                continue

            else:
                if not len(line.split(":")) == 4:
                    print >> sys.stderr, bcolors.OKBLUE + "Warning: " + bcolors.ENDC + bcolors.FAIL + "Line must be \":X:X:X:X\" format, " + \
                        bcolors.OKBLUE + "But line is " + bcolors.ENDC + \
                        bcolors.FAIL + "%s" % (line) + bcolors.ENDC
                else:
                    from_mail_header = line.split(":")[0]
                    from_mail_gecos = line.split(":")[1]
                    subject = line.split(":")[2]
                    mail_to = line.split(":")[3]

                    time_interval = wait_time.split(",")
                    if len(time_interval) == 2:
                        wait = random.randrange(
                            int(time_interval[0]), int(time_interval[1]))
                    else:
                        wait = int(wait_time.split(",")[0])
                    try:
                        self.smtp.main(self.args.attach,
                                       from_mail_header, from_mail_gecos, mail_to, subject, server, domain, self.args.html_file, self.args.verbose, mail_type, mail_log, self.args.options)
                    except Exception, mess:
                        raise wolfException("Error: %s" % mess)
                    time.sleep(float(wait))
