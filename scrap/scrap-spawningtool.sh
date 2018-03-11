#!/bin/bash

mkdir -p replay/spawningtool && cd replay/spawningtool
LIST='curl -sL http://lotv.spawningtool.com/replays/?p={}&pro_only=on&query=&after_time=&before_time=&after_played_on=01%2F01%2F16&before_played_on=&order_by=play'
DL='curl -sL http://lotv.spawningtool.com/{}/download/ > {}.SC2Replay'
parallel -j0 -q $LIST ::: $(seq 0 1 100) | pup 'a[href*=download] attr{href}' | sed 's/\/\(.*\)\/download\//\1/' | parallel -j0 $DL
