#!/bin/sh
docker run \
    --rm \
    -i \
    --network=host \
    -v "$HOME":"$HOME":ro \
    -u $(id -u) \
    -w "$PWD" \
    $USER/ledserver:latest \
    python3.7 $@

exit $?