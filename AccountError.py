#!/usr/bin/env python3

class NegativeError(Exception):
    def __init__(self, msg):
        super().__init__("Negative Value: " + msg)
