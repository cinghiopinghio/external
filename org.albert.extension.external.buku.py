#!/usr/bin/env python

import os
import sys
import json
import subprocess

albert_op = os.environ.get("ALBERT_OP")

if albert_op == "METADATA":
    metadata = """{
      "iid":"org.albert.extension.external/v2.0",
      "name":"Bookmarks",
      "version":"1.0",
      "author":"Cinghio Pinghio",
      "dependencies":["buku"],
      "trigger":"b "
    }"""
    print(metadata)
    sys.exit(0)

elif albert_op == "NAME":
    print("NAME")
    sys.exit(0)

elif albert_op == "INITIALIZE":
    sys.exit(0)

elif albert_op == "FINALIZE":
    sys.exit(0)

elif albert_op == "SETUPSESSION":
    sys.exit(0)

elif albert_op == "SETUPSESSION":
    sys.exit(0)

elif albert_op == "TEARDOWNSESSION":
    sys.exit(0)

elif albert_op == "QUERY":

    albert_query = os.environ.get("ALBERT_QUERY", '')[2:]

    items = []

    if albert_query != '':
        command = ['/usr/bin/buku', '--sreg', albert_query, '-j']
    else:
        command = ['/usr/bin/buku', '-p', '1', '-j']
    output = subprocess.check_output(command).decode().strip()
    if output[0] != '[':
        output = '['+output+']'
    for bm in json.loads(output):
        item = {
            'id': 'buku' + str(bm['index']),
            'name': bm['title'],
            'description': bm['uri'],
            'icon': "accessories-calculator",
            'actions': []
        }

        action = {
            'command': '/usr/bin/buku',
            'arguments': ['-o', str(bm['index'])],
            'name': 'Open on Browser'
        }

        item['actions'].append(action)
        items.append(item)

    res = {
        'items': items[:1]
    }
    print(json.dumps(res), end='')
    sys.exit(0)

elif albert_op == "COPYTOCLIPBOARD":
    # clipboard.copy(sys.argv[1])
    pass

sys.exit(0)
