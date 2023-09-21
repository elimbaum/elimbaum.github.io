#!/bin/zsh

ROOT=$(git rev-parse --show-toplevel)

# this is good enough
URL_REGEX='https\?:[^\)"[:space:]]*'

for url in $(grep $URL_REGEX -ohIR $ROOT --exclude-dir _site | sort | uniq)
do
    curl -fsS $url > /dev/null
    if [[ $? -ne 0 ]]
    then
        echo "FAILED" $url
    else
        # echo "   ok $url"
    fi
done