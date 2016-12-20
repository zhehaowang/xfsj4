#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re

class StringParse():
    def __init__(self):
        self.string_file_path = "../src/disaster4strings.wts"
        self.item_id_dict = dict()
        self.unit_id_dict = dict()
        self.spell_id_dict = dict()
        self.spell_effect_id_dict = dict()
        self.tech_id_dict = dict()
        self.destructable_id_dict = dict()
        self.untyped_string_dict = dict()
        self.module = "string_parsing"

    def log_error(self, line_number, content):
        print self.module + ":" + str(line_number) + " " + content

    def dict_insertion(self, dst_dict, this_id, key, value, line_number = 0, expand_duplicate = False):
        if this_id in dst_dict:
            if key in dst_dict[this_id]:
                if not expand_duplicate:
                    self.log_error(str(line_number), "key already exists: " + key + " in " + this_id)
                else:
                    if not isinstance(dst_dict[this_id][key], list):
                        dst_dict[this_id][key] = [dst_dict[this_id][key]]
                    dst_dict[this_id][key].append(value)
            else:
                dst_dict[this_id][key] = value
        else:
            dst_dict[this_id] = {}
            dst_dict[this_id][key] = value

    def parse(self):
        with open(self.string_file_path, "r") as jn_strings:
            idx = -1
            line_number = 0
            in_brackets = False

            this_id = ""
            this_type = ""
            this_descriptor = ""
            this_name = ""
            this_description = ""
            this_level = ""
            str_id = ""

            for line in jn_strings:
                line_number += 1
                idx += 1
                if (not in_brackets) and re.match(r"\s", line):
                    idx = -1
                    this_id = ""
                    this_type = ""
                    this_descriptor = ""
                    this_name = ""
                    this_description = ""
                    this_level = ""
                    str_id = ""
                else:
                    if idx == 0:
                        groups = re.match(r"STRING ([0-9]+)\s", line)
                        if groups:
                            str_id = groups.group(1)
                        else:
                            self.log_error(line_number, "cannot match string ID pattern: " + line)
                    elif idx == 1:
                        if re.match("{\s", line):
                            in_brackets = True
                            continue
                        else:
                            groups = re.match(r"// (.*): ([a-zA-Z0-9]{4}) (\(.*\)), (.*) \(", line)
                            this_type = ""
                            if groups:
                                this_type = groups.group(1)
                                this_id = groups.group(2)
                                this_name = groups.group(3)
                                this_descriptor = groups.group(4)
                                idx -= 1
                            else:
                                self.log_error(line_number, "unexpected string: " + line)
                    elif idx == 2:
                        this_description = line
                    else:
                        if re.match("}\s", line):
                            if this_type == "单位":
                                self.dict_insertion(self.unit_id_dict, this_id, this_descriptor.lower(), this_description.strip(), line_number)
                            elif this_type == "物品":
                                self.dict_insertion(self.item_id_dict, this_id, this_descriptor.lower(), this_description.strip(), line_number)
                            elif this_type == "技能":
                                self.dict_insertion(self.spell_id_dict, this_id, this_descriptor.lower(), this_description.strip(), line_number, True)
                            elif this_type == "可破坏物":
                                self.dict_insertion(self.destructable_id_dict, this_id, this_descriptor.lower(), this_description.strip(), line_number)
                            elif this_type == "魔法效果":
                                self.dict_insertion(self.spell_effect_id_dict, this_id, this_descriptor.lower(), this_description.strip(), line_number)
                            elif this_type == "科技":
                                self.dict_insertion(self.tech_id_dict, this_id, this_descriptor.lower(), this_description.strip(), line_number, True)
                            elif this_type == "":
                                self.dict_insertion(self.untyped_string_dict, str_id, "content", this_description.strip(), line_number)
                            else:
                                self.log_error(line_number, "untyped: " + this_description)
                            in_brackets = False
                        else:
                            this_description += line
            print "processed: " + str(len(self.unit_id_dict)) + " units"
            print "processed: " + str(len(self.item_id_dict)) + " items"            
            print "processed: " + str(len(self.spell_id_dict)) + " spells"
            print "processed: " + str(len(self.spell_effect_id_dict)) + " spell effects"
            print "processed: " + str(len(self.tech_id_dict)) + " techs"
            print "processed: " + str(len(self.destructable_id_dict)) + " destructables"
            print "processed: " + str(len(self.untyped_string_dict)) + " untyped strings"

def pretty_print(this_dict):
    for key in this_dict:
        print "id: " + key
        for subkey in this_dict[key]:
            if isinstance(this_dict[key][subkey], list):
                print "  * " + subkey
                for i in range(0, len(this_dict[key][subkey])):
                    print "    * lv" + str(i + 1) + " : " + str(this_dict[key][subkey][i])
            else:
                print "  * " + subkey + " : " + this_dict[key][subkey]

if __name__ == "__main__":
    string_parser = StringParse()
    string_parser.parse()
    #pretty_print(string_parser.item_id_dict)
    #pretty_print(string_parser.unit_id_dict)
    #pretty_print(string_parser.spell_id_dict)
    #pretty_print(string_parser.tech_id_dict)

    

