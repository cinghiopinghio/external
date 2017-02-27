#!/bin/bash

case $ALBERT_OP in
  "METADATA")
    METADATA='{
      "iid":"org.albert.extension.external/v2.0",
      "name":"Buku",
      "version":"1.0",
      "author":"CP",
      "dependencies":["buku"],
      "trigger":"bk"
    }'
    echo -n "${METADATA}"
    exit 0
    ;;
  "INITIALIZE")
    exit 0
    ;;
  "FINALIZE")
    exit 0
    ;;
  "SETUPSESSION")
    exit 0
    ;;
  "TEARDOWNSESSION")
    exit 0
    ;;
  "QUERY")
    echo $ALBERT_QUERY >> ~/bk.log
    RESULTS=`buku -p -j | jq -r '[.[] | {"id": .index|tostring, "title": .title, "description": .uri,  "actions": [{"name": "open", "command": "notify-send", "arguments": [.title, .uri]}]}]'`
    RESULTS='{"items":'${RESULTS}'}'
    echo "${RESULTS}" >> ~/bk.log
    echo -n "${RESULTS}"
    exit 0
    ;;
esac
