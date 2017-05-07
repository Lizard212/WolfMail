#!/usr/bin/env python
# -*- coding: utf-8 -*-


class wolfException(Exception):
    def __init__(self, errMess):
        self.err = errMess

    def __str__(self):
        return self.err
