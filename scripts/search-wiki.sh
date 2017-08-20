#!/bin/bash

lang=$(echo $1 | cut -f1 -d '-')
text=$2
query=${text// /_}
#curl -sS "https://$lang.wikipedia.org/wiki/$query?action=raw"
json=$(curl -sS "https://$lang.wikipedia.org/w/api.php?action=opensearch&search=$query&limit=1&namespace=0&format=json")
descrquote=$(echo $json | sed -r 's/([^,]*,){2}//' | cut -f1 -d ']')
descr=${descrquote//\"/}
echo "Msg:"${descr//[/}
#/usr/bin/printf "Msg:${descr//[/}"

