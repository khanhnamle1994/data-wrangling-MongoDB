#!/usr/bin/env python
# -*- coding: utf-8 -*-
# So, the problem is that the gigantic file is actually not a valid XML, because
# it has several root elements, and XML declarations.
# It is, a matter of fact, a collection of a lot of concatenated XML documents.
# So, one solution would be to split the file into separate documents,
# so that you can process the resulting files as valid XML documents.

import xml.etree.ElementTree as ET
PATENTS = 'patent.data'

def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def split_file(filename):
    # we want you to split the input file into separate files
    # each containing a single patent.
    # As a hint - each patent declaration starts with the same line that was causing the error
    # The new files should be saved with filename in the following format:
    # "{}-{}".format(filename, n) where n is a counter, starting from 0.

    # File counter
    n = 0
    # Open the large file
    with open(filename, "r") as largefile:
        # Loop large file line by line
        for line in largefile:
            if line.startswith('<?xml'):
                # New file will be written now
                newfile = "{}-{}".format(filename, n)
                print "Writing new file: {}".format(newfile)

                if n == 0:
                    fout = open(newfile, 'w')
                else:
                    # Close the old file first
                    fout.close()
                    # Open again
                    fout = open(newfile, "w")

                # Update counter
                n += 1

            # Write file
            try:
                fout.write(line)
            except NameError:
                continue


def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            f.close()
        except:
            print "Could not find file {}. Check if the filename is correct!".format(fname)


test()
