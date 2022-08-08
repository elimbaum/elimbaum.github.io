#!/bin/zsh

ROOT=$(git rev-parse --show-toplevel)

# this is good enough
URL_REGEX='https\?:[^\)"\S]*'

for url in $(grep $URL_REGEX -ohIR $ROOT | sort | uniq)
do
    curl -sS $url > /dev/null
    if [[ $? -ne 0 ]]
    then
        echo $url
    fi
done