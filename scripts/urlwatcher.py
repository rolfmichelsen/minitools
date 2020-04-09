#! /usr/bin/env python3
#
#  Copyright 2020 Rolf Michelsen
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# ------------------------------------------------------------------------
#
#  This script depends on the requests package.  Install with
#
#      python -m pip install requests
#
#  For more information, see https://requests.readthedocs.io/en/master/.

import io
import requests
import sys
import time
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

verbose = False


def scheduler(url, period, count, extension):
    """
    Manages the scheduling of all resource downloads.
    """
    sequence = 0
    while sequence < count:
        downloadResource(url, sequence, extension)
        sequence = sequence + 1
        time.sleep(period)


def downloadResource(url, sequence, extension):
    """
    Downloads a resource identified by the url and stores it to a local file.  The
    sequence number is appended to the filename.
    """
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0;) Gecko/20100101 Firefox/75.0"
    }
    r = requests.get(url, headers=headers)
    filename = "{:05d}.{}".format(sequence, extension)
    if verbose: print("{3:.2f}: Retrieved {0} Status {1} : {2}".format(filename, r.status_code, r.reason, time.time()), file=sys.stderr)
    if r.status_code == 200:
        f = io.open(filename, "wb")
        f.write(r.content)
        f.close()


def getArguments():
    """
    Get command line arguments.
    """
    description = "Periodically download data from URL"
    epilog = None
    argParser = ArgumentParser(description=description, epilog=epilog, fromfile_prefix_chars="@")
    argParser.add_argument("url", action="store", help="url to download")
    argParser.add_argument("--count", dest="count", action="store", type=int, default=1, help="number of times to download url")
    argParser.add_argument("--delay", dest="delay", action="store", type=float, default=60, help="seconds to wait between each download of url")
    argParser.add_argument("--ext", dest="extension", action="store", default="dat", help="extension of stored files")
    argParser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="more verbose output")
    return argParser.parse_args()


def main():
    global verbose
    args = getArguments()
    verbose = args.verbose

    if verbose:
        print("Retrieving from {}, count={}, delay={}s".format(args.url, args.count, args.delay), file=sys.stderr)

    scheduler(args.url, args.delay, args.count, args.extension)


if __name__ == '__main__':
    main()
