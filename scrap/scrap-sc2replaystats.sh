#!/bin/bash

# NOTE:
# https://github.com/ericchiang/pup
# bash ${i//\//-} replace / by - in var i
# GNU parallel can protect against evaluation by the sub shell by using -q
# https://www.biostars.org/p/63816/

mkdir -p replay/sc2replaystats && cd replay/sc2replaystats

LIST='curl -sL http://sc2replaystats.com{}'
DL='curl -sL http://sc2replaystats.com/download/{} > {}.SC2Replay'
LINK='../sc2replaystats-links.txt'
LADDER='curl -sL http://sc2replaystats.com/ladder/index?server={}&seasons_id=30&grandmaster=1'
curl http://sc2replaystats.com/events | pup 'a[href^="/events/details"] attr{href}' > $LINK
parallel -j0 -q $LIST ::: eu kr us | pup 'a[href^="/player"] attr{href}' >> $LINK
parallel -j0 $LIST :::: $LINK | pup 'a[href^="/download"] attr{href}' | sed 's/\/download\///' | parallel -j0 $DL
