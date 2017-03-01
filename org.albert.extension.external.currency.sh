#!/bin/bash

case $ALBERT_OP in
  "METADATA")
    METADATA='{
      "iid":"org.albert.extension.external/v2.0",
      "name":"Currency converter",
      "version":"1.0",
      "author":"Manuel Schneider",
      "dependencies":[],
      "trigger":"exch "
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
    amount=`echo ${ALBERT_QUERY:5} | cut -d ' ' -f1`
    from=`echo ${ALBERT_QUERY:5} | cut -sd ' ' -f2 | tr "[:lower:]" "[:upper:]"`
    to=`echo ${ALBERT_QUERY:5} | cut -sd ' ' -f3 | tr "[:lower:]" "[:upper:]"`
    if [[ -z $to ]];
    then 
      echo  \
'{
  "items":[{
    "name":"Currency Exchange",
    "description":"Usage: exch '${amount:=Amount}' '${from:=FROM}' '${to:=TO}'",
    "icon":"accessories-calculator",
    "actions":[]
  }]
}'
      exit 0
    fi

    conversion=`curl -s http://api.fixer.io/latest\?symbols=${to}\&base\=${from} | sed -e 's/[{}]/\n/g' | grep -i ${to} | sed -e 's/^.*://'`
    equation=`echo "$amount * $conversion" | bc`
    rhs="$amount $from = $equation $to"
    echo \
'{
  "items":[{
    "name":"'${rhs}'",
    "description":"Conversion '${conversion}'",
    "icon":"accessories-calculator",
    "actions":[{
      "name":"Copy to clipboard",
      "command":"sh",
      "arguments":["-c", "echo -n \"'"${rhs}"'\" | xclip -i; echo -n \"'"${rhs}"'\" | xclip -i -selection clipboard;"]
    }]
  }]
}'
    exit 0
    ;;
esac
