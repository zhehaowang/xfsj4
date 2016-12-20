#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re

from string_parser import StringParse

#def lianhua_recipe():

class JnSpecific():
    def __init__(self):
        self.script_file_path = "../src/disaster4script.j"
        self.string_parser = StringParse()
        self.item_class_order = ["S+", "S", "A+", "A", "B+", "B", "C+", "C", "D+", "D", "E+", "E", "F+", "F", "G+", "G"]
        
        self.item_magic_stone = []
        self.item_regular = []
        self.item_misc = []

        self.html_template_start = "<div id=\"main_content_wrap\" class=\"outer\">\n<section id=\"main_content\" class=\"inner\">\n"
        self.html_template_end = "\n</section>\n</div>"

        return

    def parse_string(self):
        self.string_parser.parse()
        return

    def classify_items(self):
        classified_cnt = 0
        stone_cnt = 0
        item_dict = self.string_parser.item_id_dict
        for item in item_dict:
            item_dict[item]["item_id"] = item
            if not "description" in item_dict[item]:
                print "item " + item_dict[item]["name"] + "(" + item + ") does not have a description"
                continue

            description = item_dict[item]["description"]

            # magic stones
            if "魔石" in description:
                item_dict[item]["jn_type"] = "stone"
                self.item_magic_stone.append(item_dict[item])
                stone_cnt += 1
            else:
                # TODO: add specific type association Trig_item_wuqiActions, item types (weapon / armor) are done via item health
                item_dict[item]["jn_type"] = "regular"
                groups = re.search(r"等级：([A-Z]\+?)", description)
                if groups:
                    this_class = groups.group(1)
                    item_dict[item]["jn_class"] = this_class
                    self.item_regular.append(item_dict[item])
                    classified_cnt += 1
                else:
                    print "item " + item_dict[item]["name"] + "(" + item + ") does not have a class"
                    self.item_misc.append(item_dict[item])
        print "found " + str(stone_cnt) + " magic stones"
        print "classified " + str(classified_cnt) + " items"
        print "unable to process " + str(len(item_dict) - stone_cnt - classified_cnt) + " items"

    def sort_order(self, v):
        if 'jn_class' in v:
            return self.item_class_order.index(v['jn_class'])
        else:
            raise ValueError("Regular item does not have classification: " + str(v))

    def sort_items(self):
        self.item_regular.sort(key = self.sort_order)

    def beautify_escaped_string_html(self, s):
        s = re.sub(r"\|n", "<br>", s)
        #s = re.sub(r"\|cff([0-9a-zA-z]{6})([^\|]*)\|r", r"<font color=#\1>\2</font>", s)
        
        len_front = len(re.findall(r"\|cff([0-9a-zA-z]{6})", s))
        len_back = len(re.findall(r"\|r", s))

        s = re.sub(r"\|cff([0-9a-zA-z]{6})", r"<font color=#\1>", s)
        s = re.sub(r"\|r", r"</font>", s)

        for i in range(len_back, len_front):
            s += "</font>"
        return s

    def regular_items_to_html(self):
        html_string = ""
        for item in self.item_regular:
            html_string += "<h3 id=\"it-" + item["item_id"] + "\">" + self.beautify_escaped_string_html(item["name"]) + "</h3>\n"
            # html_string += "<p><b>等级 </b>" + self.beautify_escaped_string_html(item["jn_class"]) + "</p>\n"
            html_string += "<p><b>" + self.beautify_escaped_string_html(item["description"]) + "</b></p>\n<br>\n"
            # html_string += "<p><b>掉落/相关触发</b>" + item["class"] + "</p>\n"
        return html_string

    def write_html_to_file(self, html_string, file_name):
        html_string = self.html_template_start + html_string + self.html_template_end
        f = open(file_name,'w')
        f.write(html_string)
        f.close()

if __name__ == "__main__":
    jn = JnSpecific()
    jn.parse_string()
    jn.classify_items()
    jn.sort_items()
    jn.write_html_to_file(jn.regular_items_to_html(), "../docs/items-content.html")
