#!/bin/bash
chmod 755 /testfiles
cd /testfiles
adduser --disabled-password  --home "/home" --no-create-home  jsmith
chmod 000 cantreadme
chown jsmith cantreadme
chmod 0444 a/.hidden
chown jsmith a/notmine.sh
chown jsmith a/normal.sh
chown jsmith a/sgid.sh
chown jsmith a/suid.sh
chmod 2755 a/sgid.sh
chmod 4755 a/suid.sh
chmod 700 a/notmine.sh
chmod 070 a/group.sh
chmod 700 a/mine.sh
chmod 007 a/all.sh
chmod 111 b/c/111.txt
chmod 777 b/c/777.txt
chmod 555 b/c/test.txt