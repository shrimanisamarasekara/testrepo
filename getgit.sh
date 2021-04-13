#!/bin/sh

cd gitback

pwd

python3 -m gitback -o MitraInnovationRepo -d git_backup -f ./key.txt --shallow
