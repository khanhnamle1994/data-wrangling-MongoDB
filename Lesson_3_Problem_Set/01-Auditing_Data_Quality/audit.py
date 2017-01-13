#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.
In the first exercise we want you to audit the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- 'NoneType' if the value is a string "NULL" or an empty string ""
- 'list', if the value starts with "{"
- 'int', if the value can be cast to int
- 'float', if the value can be cast to float, but is not an int
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and the datatypes that can be found in the field.
All the data initially is a string, so you have to do some checks on the values first.

"""
import codecs
import csv
import json
import pprint
import collections as col

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal", 
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long", 
          "areaLand", "areaMetro", "areaUrban"]

def is_int(item):
    try:
        int(item)
        return True
    except ValueError:
        return False

def is_float(item):
    try:
        float(item)
        return True
    except ValueError:
        return False

def is_list(item):
    try:
        item[0]
        return (item[0] == '{')
    except ValueError:
        return False

def is_noneType(item):
    if item in ["NULL",""]:
        return True
    return False

def audit_file(filename, fields):
    fieldtypes = col.defaultdict(set)
    noneType = type(None)
    intType = type(1)
    listType = type([])
    floatType = type(1.1)

    # YOUR CODE HERE
    with open(filename) as f:
        cities = csv.DictReader(f)
        for i, row in enumerate(cities):
            if i < 3:
                pass
            for key, item in row.iteritems():
                if is_int(item):
                    fieldtypes[key].add(intType)
                elif is_float(item):
                    fieldtypes[key].add(floatType)
                elif is_noneType(item):
                    fieldtypes[key].add(noneType)
                elif is_list(item):
                    fieldtypes[key].add(listType)
                else:
                    fieldtypes[key].add(type(item))

    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()
