#!/bin/sh
set -e
cd "$(dirname "$0")/.."
echo 'a b c' | ./fieldcut --fields 1,3 | grep -q $'^a\tc$'
echo 'a b c' | ./fieldcut --fields 2 --delimiter , | grep -q '^b$'
printf 'x y\np q r\n' > /tmp/fieldcut-sample.txt
./fieldcut --fields 1,3 /tmp/fieldcut-sample.txt | head -1 | grep -q '^x\t$'
rm -f /tmp/fieldcut-sample.txt
if echo 'a b c' | ./fieldcut --fields 0 2>/dev/null; then echo "expected exit 2"; exit 1; fi
echo "smoke OK"
