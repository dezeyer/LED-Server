#!/bin/sh
docker run \
    --rm \
    -i \
    --network="host" \
    -v "$HOME":"$HOME":ro \
    -u $(id -u) \
    -w "$PWD" \
    devel:latest \
    python3.7 -u $@

exit $?