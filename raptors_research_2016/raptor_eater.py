# -*- coding: utf-8 -*-
from docx import Document
import csv
import pudb
import string

class StringHelpers:

    @classmethod
    def strip_nonalnum(cls, word):
        for start, c in enumerate(word):
            if c.isalnum():
                break
        for end, c in enumerate(word[::-1]):
            if c.isalnum():
                break
        return word[start:len(word) - end]

    @classmethod
    def percent_upper(cls, word):
        total = len(word)
        uppers = [c for c in word if c.upper() == c]
        return len(uppers) / float(total)

# class RaptorHelpers:

#     @classmethod
#     def get_inst(cls, j, text_list):
#         # get institution
#         while True:
#             # 1 - get next paragraph
#             next = ps[j+1].text
#             #2 - check % of upper case letters
#             per = StringHelpers.percent_upper(next)
#             if per > 0.4:
#                 institution = next
#                 return institution
#             j += 1

doc = Document('files/raptorresearchconference-alltalksandposters.docx')

printable = set(string.printable)

email_title_institution_fname_lname_abstract = []

ps = doc.paragraphs

for i, p in enumerate(ps):

    # get email 
    if '@' in p.text:
        text = p.text
        text_list = text.split(" ")
        for j, word in enumerate(text_list):
            if '@' in word:
                email = StringHelpers.strip_nonalnum(word)

        # get Name 
        for x, word in enumerate(text_list):
            if "*" in word:
                fname = StringHelpers.strip_nonalnum(word).title()
                if len(fname) < 2:
                    fname = StringHelpers.strip_nonalnum(text_list[x+1]).title()

        # get title
        title = ps[i - 1].text
            
        # get email
        text_list = text.split(",")
        for k, el in enumerate(text_list):
            if "@" in el:
                email_index = k + 1
                break

        # if email == "binothman.albara@sdstate.edu":
        #     pu.db
        
        # get institution
        count = 0
        while True and count < 10:
            words = text_list[email_index]
            per = StringHelpers.percent_upper(words)
            if per < 0.4:
                institution = words
                z = email_index + 1
                o_count = 0
                while True and o_count < 3:
                    if StringHelpers.percent_upper(text_list[z]) < 0.4:
                        institution += " "
                        institution += text_list[z]
                    else:
                        break
                    o_count += 1
                    z += 1
                break
            email_index += 1
            count += 1

        # get abstract
        abstract = ps[i+1].text

        out = [email, title, institution, fname, abstract]
        out = [filter(lambda x: x in printable, word) for word in out]

        email_title_institution_fname_lname_abstract.append(out)

with open('files/raptors.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile)
    for el in email_title_institution_fname_lname_abstract:
        thedatawriter.writerow(el)
        


        
            


    
