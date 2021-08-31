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
Ron,08/02/1999,mochi
Ben,01/23/2002,sashimi
Becky,12/20/2001,onigiri
EOF

cat > $ws/expected.csv << EOF
name,dob,food
Ron,1999.08.02,mochi
Ben,2002.01.23,sashimi
Becky,2001.12.20,onigiri
EOF

docker=docker
which docker > /dev/null || docker=podman

$docker build -t pl-re-sub:test .
$docker run --rm  \
    -v $ws/incoming:/incoming:ro  \
    -v $ws/outgoing:/outgoing:rw  \
    pl-re-sub:test resub  \
    --expression '(\d\d)/(\d\d)/(\d\d\d\d)' \
    --replacement '\3.\1.\2' \
    --inputPathFilter data.csv  /incoming /outgoing

diff -q $ws/expected.csv $ws/outgoing/data.csv
