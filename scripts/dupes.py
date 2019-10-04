#! /usr/bin/env python3
#
#  Copyright 2019 Rolf Michelsen
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

# Standard library modules
import glob
import hashlib
import io
import sys
from argparse import ArgumentParser
from pathlib import Path



verbose = False


class FileInfo:
    """
    Information about a single file.
    """

    Name = None
    Signature = None

    def __init__(self, path):
        """
        Initialize a file information object based on the provided path
        """
        self.Name = path
        self.Signature = self.__createDigest(path)
    


    def __createDigest(self, path):
        """
        Return the digest for the given file.
        """
        f = open(path, "rb", buffering=0)
        data = f.readall()
        digest = hashlib.md5()
        digest.update(data)
        return digest.digest()



def scanPath(path, recurse):
    """
    Scans all files under the specified path, represented by a Path object.  
    Returns a list of FileInfo objects.
    """
    try:
        files = []
        if recurse and path.is_dir():
            for p in path.iterdir():
                files.extend(scanPath(p, recurse))
        elif path.is_file():
            files.append(FileInfo(path))
        else:
            print("Ignoring special file {}".format(path), file=sys.stderr)
        return files
    except PermissionError:
        print("Access denied {}".format(path), file=sys.stderr)
    except:
        print("Unexpected error {}".format(path), file=sys.stderr)
    return []



def findDuplicates(files):
    """
    Find file duplicates.  Input is a list of FileInfo objects.  Returns a list where each element is a list of duplicate files.
    """
    # Build a dictionary where where the keys are file signatures and the values are corresponding FileInfo objects.
    dupes = {}
    for f in files:
        if f.Signature in dupes:
            dupes[f.Signature].append(f)
        else:
            dupes[f.Signature] = [f]

    # Take all dictionary values with more than one element and construct a new list of these values.
    result = []
    for d in dupes.values():
        if len(d) > 1:
            result.append(d)

    return result



def printReport(dupes):
    """
    Print a report of duplicate files.  The input is a list where each element is a list of duplicate files, each file
    represented by a FileInfo object.  This is the  same data structure as returned from findDuplicates().
    """
    for d in dupes:
        print(d[0].Name)
        for f in d[1:]:
            print("\t", f.Name)
        print()



def getArguments():
    """
    Get command line arguments.
    """
    description = "Find duplicate files"
    epilog = """
    This script uses file content to determine that two files are duplicates.  It calculates a hash of
    each candidate file and looks for equal hash values.  Other file attributes, such as name or
    timestamps, are not considered.
    """
    argParser = ArgumentParser(description=description, epilog=epilog, fromfile_prefix_chars="@")
    argParser.add_argument("path", action="store", nargs="+", help="path to include in scan")
    argParser.add_argument("-r", "--recurse", dest="recurse", action="store_true", help="recurse into subdirectories")
    argParser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="more verbose output")
    return argParser.parse_args()



def main():
    global verbose
    args = getArguments()
    verbose = args.verbose
    files = []

    for path in args.path:
        if verbose: print(path, file=sys.stderr)
        for p in glob.iglob(path):
            f = scanPath(Path(p), args.recurse)
            files.extend(f)
        
    if verbose: print("{} files scanned".format(len(files)), file=sys.stderr)

    if verbose: print("Scanning for duplicates... ", end="", file=sys.stderr)
    dupes = findDuplicates(files)
    if verbose: print("done", file=sys.stderr)

    printReport(dupes)



if __name__ == '__main__':
    main()
