# -*- coding: utf-8 -*-
from docx import Document
import csv
import pudb
import string

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

printable = set(string.printable)

# get X's categories
with open('files/cats.txt') as f:
    content = f.readlines()

content = [StringHelpers.trim_nums_from_str(c).strip() for c in content]
content = [filter(lambda x: x in printable, word) for word in content]


# init ps
doc = Document('files/entomological_society_of_america_2016_names_emails_abstracts.docx')

email_title_institution_fname_lname_abstract = []

ps = doc.paragraphs

for i, p in enumerate(ps):


    text = p.text.strip()

    # get most recent category
    if text in content:
        category = text

    # get email
    if "@" in text:

        text_list = text.split(" ")
        for j, word in enumerate(text_list):
            if '@' in word:
                email = StringHelpers.strip_nonalnum(word)
                email_index = j

        for k, c in enumerate(list(text)):

            if '@' == c:
                try:
                    l = k
                    while text[l] != "(":
                        l -= 1
                    m = k
                    while text[m] != ")":
                        m += 1
                    email = text[l:m+1]
                    email = "".join(email.split(" "))
                except:
                    email = email

        email = StringHelpers.strip_nonalnum(email)
        print email

        # get title
        bolds = [run.text for run in p.runs if run.bold]
        for b in bolds:
            try:
                b = b.strip()
                int(b)
                num_index = text_list.index(b)
            except:
                continue
        
        title = text_list[num_index:email_index]

        print title

    

