#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import logging
logfile = os.path.expanduser('~/bk.log')
logging.basicConfig(filename=logfile, level=logging.DEBUG)

albert_op = os.environ.get("ALBERT_OP")
trigger = "bb "

if albert_op == "METADATA":
    metadata = {
        "iid": "org.albert.extension.external/v2.0",
        "name": "Bookmarks",
        "version": "0.1",
        "author": "Cinghio Pinghio",
        "dependencies": ["buku"],
        "trigger": trigger
    }
    print(json.dumps(metadata))
    sys.exit(0)

elif albert_op == "NAME":
    print("BuKu")
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
    albert_query = os.environ.get("ALBERT_QUERY", '')
    albert_query = albert_query[len(trigger):].strip()

    # logging.debug(json.dumps(dict(os.environ), indent=4))

    logging.debug('query: ' + albert_query)
    items = []

    if albert_query == '':
        albert_query = 'news'
    command = ['buku', '--deep', albert_query, '-j', '--np']
    command += ['-z']
    logging.debug('running ' + ' '.join(command))
    # command = ' '.join(command) + '; exit 0'

    proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            )
    try:
        output, perr = proc.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        output, perr = proc.communicate()
    output = output.decode()
    perr = perr.decode()
    logging.debug('STDERR' + perr)
    logging.debug('STDOUT' + output)
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
        'items': items[:]
    }
    print(json.dumps(res))
    sys.exit(0)

elif albert_op == "COPYTOCLIPBOARD":
    # clipboard.copy(sys.argv[1])
    pass

sys.exit(0)
