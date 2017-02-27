#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import logging
logfile = os.path.expanduser('~/bk.log')
logging.basicConfig(filename=logfile, level=logging.DEBUG)

albert_op = os.environ.get("ALBERT_OP")
trigger = "nm "

if albert_op == "METADATA":
    metadata = {
        "iid": "org.albert.extension.external/v2.0",
        "name": "Emails",
        "version": "0.1",
        "author": "Cinghio Pinghio",
        "dependencies": ["notmuch"],
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

    logging.debug('query: ' + albert_query)
    items = []

    # if albert_query != '':
    #     command = ['buku', '--sreg', albert_query, '-j']
    # else:
    command = ['notmuch', 'count', 'tag:unread']
    logging.debug('running ' + ' '.join(command))

    proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                            )
    output, perr = proc.communicate()
    output = output.decode().strip()
    perr = perr.decode()

    logging.debug('STDERR ' + perr)
    logging.debug('STDOUT ' + output)

    item = {
        'id': 'notmuch',
        'name': 'You have {} unread emails'.format(output),
        'description': 'You have {} unread emails'.format(output),
        'icon': "new-mail",
        'actions': []
    }

    action = {
        'command': 'notify-send',
        'arguments': ['Happy', output],
        'name': 'Notify'
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
