#!/bin/sh

cd isutest/gitback

pwd

python3 -m gitback -o MitraInnovationRepo -d git_backup -t cat .'token.txt' --shallow
