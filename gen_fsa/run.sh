#!/usr/bin/sh
python topic2fsa.py -o rap.fsa -t $1 -m 0 -ln 4 -wn 9 -al 0 -d 0
carmel rap.fsa -Ok 10
