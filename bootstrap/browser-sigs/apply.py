#!/usr/bin/env python

from __future__ import print_function, with_statement
from contextlib import closing
import sqlite3, json, re

class TemplateMatcher(object):
    def __init__(self, apply_json):
        with file(apply_json, 'rb') as json_file:
            self.templates = json.load(json_file)
        for template in self.templates:
            template['compiled_rules'] = [compile_rule(rule(rule)) for rule in template['rules']]

    def match(self, agent):
        for template in self.templates:
            if all(r(agent) for r in template['compiled_rules']):
                return template['input']
        raise RuntimeError('No rule matches the agent "{0}"'.format(agent))


def compile_rule(rule):
    if rule['type'] == 'ua-contains':
        return lambda x: rule['value'] in x
    if rule['type'] == 'ua-matches':
        return lambda x: bool(re.search(rule['value'], x))
    raise ValueError('Unsupported rule type')

def apply_templates(db, apply_json):
    matcher = TemplateMatcher(apply_json)
    sql = sqlite3.connect(db)
    with closing(sql.cursor()) as cursor:
        cursor.execute('SELECT agent FROM agents')
        for (agent,) in cursor:
            matcher.match(agent)

def main():
    import sys
    try:
        db, apply_json = sys.argv[1:3]
    except ValueError:
        print('Usage: {0} <agents.db> <apply.json>'.format(
            sys.argv[0]), file=sys.stderr)
    else:
        apply_templates(db, apply_json)


if __name__ == '__main__':
    main()
