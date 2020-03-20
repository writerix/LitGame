# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import json
import nltk
import sqlalchemy
import html
from models import Quote


def extract_sent(text):
    '''
    Input: string
    Output: List of sentences in string form
    '''
    los = nltk.sent_tokenize(text)
    return los

def populate_quote(author, work, sentence, session):
    new_quote = Quote(author = author, work = work, sentence = sentence)
    session.add(new_quote)
    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        db_connection = input("Enter database connection string: ")
        manifest = input("Enter name of manifest file: ")
    else:
        db_connection = sys.argv[1]
        manifest = sys.argv[2]

    engine = sqlalchemy.create_engine(db_connection, echo=True)
    engine.connect()
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    with open(manifest, 'r') as manifest_file:
        manifest_data = json.loads(manifest_file.read())
    manifest_file.closed

    authors = manifest_data['authors']
    for author in authors:
        author_all_works = []
        for work in author['works']:
            with open(work['filename'], 'r') as file:
                author_all_works.append(file.read())
            file.closed
        author_sentences = []
        for text in author_all_works:
            author_sentences.append(extract_sent(text))
        for i in range(len(author_sentences)):
            for j in range(len(author_sentences)):
                if j == i:
                    continue
                else:
                    author_sentences[i] = list(filter(lambda x: x not in author_all_works[j], author_sentences[i]))
        for i in range(len(author_sentences)):
            for sentence in author_sentences[i]:
                print(author['author'])
                print(html.escape(author['author']))
                populate_quote(html.escape(author['author']), html.escape(author['works'][i]['title']), html.escape(sentence), session)
        session.commit()
