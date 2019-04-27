#!/bin/sh
docker run \
    --rm \
    -i \
    --network=host \
    -v "$HOME":"$HOME":ro \
    -u $(id -u) \
    -w "$PWD" \
    clburlison/pylint:py3-alpine \
    pylint $@
    
exit $?