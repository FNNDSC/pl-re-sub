#!/bin/bash -ex
# Simple test for pl-re-sub.
# Creates some data in /tmp and uses Docker or Podman to run the code.
#
# Clean-up instructions:
#     docker rmi pl-re-sub:test
#     rm -rvf /tmp/resub-test.???

ws=$(mktemp -p /tmp -d resub-test.XXX)

mkdir $ws/incoming $ws/outgoing

cat > $ws/incoming/data.csv << EOF
name,dob,food
Ron,08/02/00,mochi
Ben,01/23/02,sashimi
Becky,12/20/01,onigiri
EOF

cat > $ws/expected.csv << EOF
name,dob,food
Ron,2000.08.02,mochi
Ben,2002.01.23,sashimi
Becky,2001.12.20,onigiri
EOF

docker=docker
which docker > /dev/null || docker=podman

$docker build -t pl-re-sub:test .
$docker run --rm  \
    --userns=host \
    -v $ws/incoming:/incoming:ro  \
    -v $ws/outgoing:/outgoing:rw  \
    pl-re-sub:test resub  \
    --expression '(\d\d/\d\d)/(\d\d) (\d\d)/(\d\d)/(\d\d\d\d)' \
    --replacement '\1/20\2 \3.\1.\2' \
    --ifs ' ' \
    --inputPathFilter data.csv  /incoming /outgoing

diff -q $ws/expected.csv $ws/outgoing/data.csv
