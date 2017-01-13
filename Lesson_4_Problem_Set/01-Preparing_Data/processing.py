#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it, 
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.
Your task in this exercise is to parse the file, process only the fields that are listed in the
FIELDS dictionary as keys, and return a dictionary of cleaned values. 

The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary
- trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)"
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'.
- if a value of a field is "NULL", convert it to None
- if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the cleanup is up to you,
  eg removing "*" prefixes etc
- strip leading and ending whitespace from all fields, if there is any
- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
                    'family': 'Orb-weaver spider',
                    'class': 'Arachnid',
                    'phylum': 'Arthropod',
                    'order': 'Spider',
                    'kingdom': 'Animal',
                    'genus': None
                    }
}
"""
import codecs
import csv
import json
import pprint
import re

DATAFILE = 'arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}


def process_file(filename, fields):

    process_fields = fields.keys()
    data = []
    
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i, line in enumerate(reader):
        
            myInnerDictionary ={}
            myInnerDictionary['classification'] = {}
        
            if i > 2:
            
                for key in line:
                    if key in  FIELDS:
                        myNewKey = FIELDS[key]
                     
                        if key == 'rdf-schema#label':
                            if line[key] != 'NULL' :
                                myNewValue = line['rdf-schema#label'].split()[0]
                                myInnerDictionary[myNewKey] = myNewValue
                            else:
                                myInnerDictionary[myNewKey] = None

                        elif key == 'name':
                            if line[key] != 'NULL':
                                if line[key].isalnum():
                                    myNewValue = line[key] 
                                    myInnerDictionary[myNewKey] = myNewValue                         
                                else:
                                    myInnerDictionary[myNewKey] = line['rdf-schema#label']
                            else:
                                myInnerDictionary[myNewKey] =  line['rdf-schema#label']
                 
                        elif key == 'synonym':
                            scrubbedSynonymList = []
                            cleanedSynonymList = parse_array(line[key])
                         
                            if line[key] != 'NULL':
                                for i, cleaned_synonym in enumerate(cleanedSynonymList):
                                    print("\ti - {}, cleaned_synonym - {}".format(i, cleaned_synonym))
                                    print("\tlen(cleaned_synonym) - {}".format(len(cleaned_synonym)))
                                
                                    if '* ' in cleaned_synonym:
                                        scrubbed_synonym = cleaned_synonym.replace("* ", "")
                                        scrubbedSynonymList.append(scrubbed_synonym)
                                        myInnerDictionary[myNewKey] = scrubbedSynonymList

                                    elif '*' in cleaned_synonym:
                                        scrubbed_synonym = cleaned_synonym.replace("*", "")
                                        scrubbedSynonymList.append(scrubbed_synonym)
                                        myInnerDictionary[myNewKey] = scrubbedSynonymList
                                    
                                    else:
                                        scrubbedSynonymList.append(cleaned_synonym)
                                        myInnerDictionary[myNewKey] = scrubbedSynonymList
                            else:
                                myInnerDictionary[myNewKey] = None
                        
                        elif key == 'URI':
                            if line[key] != 'NULL':
                                myInnerDictionary[myNewKey] = line[key]
                            else:
                                myInnerDictionary[myNewKey] = None
                        
                        elif key == 'rdf-schema#comment':
                            if line[key] != 'NULL':
                                myInnerDictionary[myNewKey] = line[key]
                            else:
                                myInnerDictionary[myNewKey] = None
                        
                        else:
                            if line[key] != 'NULL':
                                myInnerDictionary['classification'][myNewKey] = line[key] 
                            else:
                                myInnerDictionary['classification'][myNewKey] = None
                        
                data.append(myInnerDictionary)
    return data

def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]


def test():
    data = process_file(DATAFILE, FIELDS)

    pprint.pprint(data[0])
    assert data[0] == {
                        "synonym": None, 
                        "name": "Argiope", 
                        "classification": {
                            "kingdom": "Animal", 
                            "family": "Orb-weaver spider", 
                            "order": "Spider", 
                            "phylum": "Arthropod", 
                            "genus": None, 
                            "class": "Arachnid"
                        }, 
                        "uri": "http://dbpedia.org/resource/Argiope_(spider)", 
                        "label": "Argiope", 
                        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
                    }


if __name__ == "__main__":
    test()
