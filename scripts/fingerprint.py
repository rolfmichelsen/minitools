#! /usr/bin/env python3
#
#   Copyright 2020 Rolf Michelsen
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import sys
from argparse import ArgumentParser

verbose = False


class Fingerprint:
    """
    File fingerprint.
    """

    filename = None
    digest = None

    def __init__(self, filename):
        self.filename = filename

    def Pack(self):
        """
        Returns a dictionary representing the file fingerprint.
        """
        return {
            "filename": self.filename,
            "digest": self.digest
        }


def getArguments():
    description = "Fingerprint files"
    epilog = """
    Fingerprint selected files.
    """
    argParser = ArgumentParser(description=description, epilog=epilog, fromfile_prefix_chars="@")
    argParser.add_argument("path", action="store", nargs="+", help="path to include in scan")
    argParser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="more verbose output")
    return argParser.parse_args()


def main():
    global verbose
    args = getArguments()
    verbose = args.verbose


if __name__ == '__main__':
    main()
