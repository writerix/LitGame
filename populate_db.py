# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import nltk.data
import sqlite3
import os.path

INSERT_QUOTE = """INSERT INTO quote(author, work, sentence) VALUES(?, ?, ?)"""

def extract_sent(text):
    '''
    Input: string
    Output: List of sentences in string form
    '''
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    los = sent_detector.tokenize(text.strip())
    return los

def populate(db_file, author, work, sentences):
    '''
    Adds the sentences to the db table of quotes
    '''
    if(os.path.isfile(db_file)):
        conn = sqlite3.connect(db_file)
    else:
        print("Error " + db_file + " was not found.", file=sys.stderr)
        sys.exit(1)
    cursor = conn.cursor()
    for sent in sentences:
        cursor.execute(INSERT_QUOTE, (author, work, sent))
    conn.commit()
    conn.close()

def main():
    db_file = input("Enter name of database file: ")
    author_name = input("Enter author name: ")
    num_works = int(input("Enter the number of works by the author to populate " + db_file + " with: "))
    if num_works < 3:
        print("Warning: the literature game expects at least 3 works per author.")
    all_works = []
    all_sent = []
    for i in range(1, (num_works + 1)):
        if i == 1:
            work_name = input("Enter the name of the 1st work: ")
        elif i == 2:
            work_name = input("Enter the name of the 2nd work: ")
        elif i == 3:
            work_name = input("Enter the name of the 3rd work: ")
        else:
            work_name = input("Enter the name of the " + str(i) + "th work: ")
        fname = input("Enter the file name for " + work_name +": ")
        try:
            infile = open(fname, "r")
            intext = infile.read()
            infile.close()
        except FileNotFoundError:
            print("Error: file {0} not found. Please check name and path.".format(fname), file=sys.stderr)
            sys.exit(1)
        sentences = extract_sent(intext)
        print(str(len(sentences)) + " sentences extracted.")
        all_works.append(work_name)
        all_sent.append(sentences)
    unique_sent = all_sent.copy()
    for i in range(num_works):
        for j in range(num_works):
            if j == i:
                continue
            unique_sent[i] = list(filter(lambda x: x not in all_sent[j], unique_sent[i]))###
    for k in range(num_works):
        populate(db_file, author_name, all_works[k], unique_sent[k])
    print("Insertions completed.")
    
if __name__ == "__main__":
    main()