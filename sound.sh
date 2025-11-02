#!/bin/bash

# Original source: https://gist.github.com/urcadox/5453502
# Author: Alexandre Berthaud
# Date: as of 2025-11-02
# This is based on the script linked above with some minor changes (different volume increases and now uses a shuffled playlist)

echo "Set playlist and initial volume"
mpc clear
mpc load test-playlist
mpc shuffle
mpc volume 5 > /dev/null
# sleep for a bit to make sure the volume change above takes place before playing
sleep 5 > /dev/null
echo "Start music"
mpc play > /dev/null
mpcfade.sh 5 20 2
mpcfade.sh 20 30 3
mpcfade.sh 30 45 4
sleep 180 > /dev/null
mpc stop
echo "Alarm cycle finished! Have a good day!"
