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

import glob
import hashlib
import io
import json
import sys
from argparse import ArgumentParser
from pathlib import Path

verbose = False


class Fingerprint:
    """
    File fingerprint.
    """

    Filename = None
    Digest = None

    def __init__(self, filename):
        self.Filename = filename
        self.Digest = self.__createDigest(filename)


    def Pack(self):
        """
        Returns a dictionary representing the file fingerprint.
        """
        hexdigest = "".join(format(x, "02x") for x in self.Digest)
        return {
            "filename": str(self.Filename),
            "digest": hexdigest
        }


    def __createDigest(self, path):
        """
        Return the digest for the given file.
        """
        f = open(path, "rb", buffering=0)
        data = f.readall()
        digest = hashlib.md5()
        digest.update(data)
        return digest.digest()


def processFiles(path, recurse):
    """
    Scans all files under the specified path, represented by a Path object.  
    Returns a list of Fingerprint objects.
    """
    try:
        files = []
        if recurse and path.is_dir():
            for p in path.iterdir():
                files.extend(processFiles(p, recurse))
        elif path.is_file():
            files.append(Fingerprint(path))
        else:
            print("Ignoring special file {}".format(path), file=sys.stderr)
        return files
    except PermissionError:
        print("Access denied {}".format(path), file=sys.stderr)
    return []



def processPaths(path, recurse):
    fingerprints = []
    if verbose: print("Processing {}".format(path), file=sys.stderr)
    for p in glob.iglob(path):
        f = processFiles(Path(p), recurse)
        fingerprints.extend(f)
    return fingerprints


def outputReportJson(fingerprints):
    report = []
    for fingerprint in fingerprints:
        report.append(fingerprint.Pack())
    return json.dumps(report, sort_keys=True, indent=4)


def getArguments():
    description = "Fingerprint files"
    epilog = """
    Fingerprint selected files.
    """
    argParser = ArgumentParser(description=description, epilog=epilog, fromfile_prefix_chars="@")
    argParser.add_argument("path", action="store", nargs="+", help="path to include in scan")
    argParser.add_argument("--recurse", dest="recurse", action="store_true", help="recurse into directories")
    argParser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="more verbose output")
    return argParser.parse_args()


def main():
    global verbose
    args = getArguments()
    verbose = args.verbose

    fingerprints = []
    for path in args.path:
        fingerprints.extend(processPaths(path, args.recurse))
    print(outputReportJson(fingerprints))


if __name__ == '__main__':
    main()
