#!/bin/bash

# NOTE:
# http://offbytwo.com/2011/06/26/things-you-didnt-know-about-xargs.html
# https://www.gnu.org/software/parallel/parallel_tutorial.html
# > By default --jobs is the same as the number of CPU cores. --jobs 0 will run as many jobs in parallel as possible.
# https://jqplay.org/
# http://superuser.com/questions/644272/how-do-i-delete-all-files-smaller-than-a-certain-size-in-all-subfolders

mkdir -p replay/ggtracker && cd replay/ggtracker
LIST='curl -sL http://ggtracker.com:9292/api/v1/matches?average_league=6&page={}&paginate=false&replay=true'
DL='curl -sL http://ggtracker.com/matches/{}/replay > {}.SC2Replay'
parallel -j0 -q $LIST ::: $(seq 0 1 150) | jq '.collection[].id' | parallel -j0 $DL
