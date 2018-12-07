# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sqlite3

#sqlite_file = "quote_db.sqlite"

def init_db(name):
	conn = sqlite3.connect(name)
	cursor = conn.cursor()
	cursor.execute("PRAGMA foreign_keys = 1")
	cursor.execute("CREATE TABLE quote(qid INTEGER PRIMARY KEY, author TEXT NOT NULL, work text NOT NULL, sentence text NOT NULL)")
	cursor.execute("CREATE TABLE user(uid INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, email TEXT NOT NULL UNIQUE, account_type INTEGER NOT NULL, joined INTEGER NOT NULL, latest_login INTEGER NOT NULL, pwd_hash TEXT NOT NULL)")
	cursor.execute("CREATE TABLE quiz(quiz_id INTEGER PRIMARY KEY, uid INTEGER NOT NULL, is_solved INTEGER NOT NULL, quotes TEXT NOT NULL, score INTEGER NOT NULL, FOREIGN KEY (uid) REFERENCES user(uid) ON DELETE CASCADE)")
	conn.commit()
	conn.close()

if __name__ == "__main__":
	init_db("quote_db.sqlite")