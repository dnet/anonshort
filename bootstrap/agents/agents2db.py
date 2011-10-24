#!/usr/bin/env python

from __future__ import with_statement, print_function
import sqlite3

CREATE_SQL = """
CREATE TABLE agents (id INT PRIMARY KEY, agent TEXT);
CREATE TABLE metadata (key TEXT PRIMARY KEY, value INT);
INSERT INTO metadata (key, value) VALUES ('version', 1);
"""

class AgentParser(object):
    def __init__(self):
        self.counter = 0

    def parse_agents(self, txtfile):
        for row in txtfile:
            count, agent = row.strip().split(' ', 1)
            self.counter += int(count)
            yield self.counter, agent

def convert(agents_file, db_file):
    parser = AgentParser()
    with sqlite3.connect(db_file) as sql:
        cursor = sql.cursor()
        cursor.executescript(CREATE_SQL)
        with file(agents_file, 'r') as txt:
            cursor.executemany('INSERT INTO agents (id, agent) VALUES (?, ?)',
                    parser.parse_agents(txt))
        cursor.execute('INSERT INTO metadata (key, value) VALUES (?, ?)',
                ('counter', parser.counter))

def main():
    import sys
    try:
        agents_file, db_file = sys.argv[1:3]
    except ValueError:
        print('Usage: {0} <agents.txt> <output.db>'.format(sys.argv[0]),
                file=sys.stderr)
    else:
        convert(agents_file, db_file)

if __name__ == '__main__':
    main()
