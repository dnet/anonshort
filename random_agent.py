#!/usr/bin/env python

from __future__ import print_function, with_statement
from contextlib import closing
import sqlite3, random

class RandomAgent(object):
    def __init__(self, db):
        random.seed()
        self.sql = sqlite3.connect(db)
        self.counter = self.query_db("SELECT value FROM metadata WHERE key = 'counter'")

    def get_agent(self):
        return self.query_db("SELECT agent FROM agents WHERE id > ? LIMIT 1",
                (random.randrange(self.counter),))

    def query_db(self, query, params=[]):
        with closing(self.sql.cursor()) as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()[0]

def main():
    import sys
    try:
        db = sys.argv[1]
    except IndexError:
        print('Usage: {0} <agents.db>'.format(sys.argv[0]), file=sys.stderr)
    else:
        print(RandomAgent(db).get_agent())

if __name__ == '__main__':
    main()
