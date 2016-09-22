# -*- coding: utf-8 -*-
import csv
import pudb
import string
import requests
import json

from bs4 import BeautifulSoup

# class JsonHelpers:
#     @classmethod
#     def pp(cls, my_dict):
#         """
#         takes a dict
#         and prints it pretty
#         """
#         print json.dumps(my_dict, sort_keys=True, indent=4)

class StringHelpers:

    @classmethod
    def strip_nonalnum(cls, word):
        """
        strips non alnums from beginning and end of a str
        leaves them in the middle
        """
        for start, c in enumerate(word):
            if c.isalnum():
                break
        for end, c in enumerate(word[::-1]):
            if c.isalnum():
                break
        return word[start:len(word) - end]

    @classmethod
    def percent_upper(cls, word):
        """
        returns the number of uppercase chars in a str
        """
        total = len(word)
        uppers = [c for c in word if c.upper() == c]
        return len(uppers) / float(total)

    @classmethod
    def trim_nums_from_str(cls, _str):
        """
        takes a str like '637 Symposium: Industry-Academia Collaborative'
        returns 'Symposium: Industry-Academia Collaborative''
        """
        l = _str.split(" ")
        try:
            foo = int(l[0])
            l.pop(0)
            return " ".join(l)
        except ValueError:
            return _str

    @classmethod
    def remove_html_tags(cls, _str_with_tags):
        """
        takes str with random html tags
        and returns just the text
        """
        soup = BeautifulSoup(_str_with_tags)
        return soup.get_text()

    @classmethod
    def make_printable(cls, _str):
        """
        takes string with weird chars
        and kills them
        """
        printable = set(string.printable)
        return "".join([filter(lambda x: x in printable, word) for word in _str])

printable = set(string.printable)

# get urls
with open('files/urls.txt') as f:
    urls = f.readlines()

urls = [u.strip() for u in urls]

# get json reponses
jsons = []
for url in urls:
    print url
    json = requests.get(url).json()
    jsons.append(json)

entries = []
for j in jsons:
    entry = j['entries']
    entries.append(entry)

peeps = []
for entry in entries:
    for e in entry:
        lname = e['last_name']
        fname = e['first_name']
        email = e['email']
        p_id = e['oid']
        peeps.append( [lname, fname, email, p_id] )

more_info_for_peep_url_1 = 'https://event.crowdcompass.com/e/8GpPc6n8Sz/lookup?_release=2014112800&lookup={"0":{"collection":{"name":"person","scope":"with_assets"},"project":[{"presentation":{"purpose":"speaker"}}],"filter":{"byField":{"name":"oid","matchValue":"'
more_info_for_peep_url_2 = '"}}}}&_=1474570619394'

all_peep_data = []
for peep in peeps:
    url = more_info_for_peep_url_1 + peep[3] + more_info_for_peep_url_2
    info = requests.get(url).json()
    activities = info['0']['results'][0]['presenting_activities']
    if len(activities) > 0:
        a_title = activities[0]['activity']['name']
        a_desc = StringHelpers.make_printable(StringHelpers.remove_html_tags(activities[0]['activity']['description']))
    else:
        a_title = ""
        a_desc = ""

    peep.extend([a_title, a_desc])

    out = [filter(lambda x: x in printable, word) for word in peep]

    all_peep_data.append(out)
    print out

with open('files/spsp.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile)
    for el in all_peep_data:
        thedatawriter.writerow(el) 
