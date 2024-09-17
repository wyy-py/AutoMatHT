#!/bin/bash

for i
do
    [ ! -s $i/OUTCAR ] && continue
    EFIELD="${i%%/*}"
    DATA="$(BTE-EpsilonBorn.sh $i/OUTCAR | grep epsilon)"
    X="$(echo "$DATA" | head -1 | cut -d = -f 2 | cut -d ' ' -f 1)"
    Y="$(echo "$DATA" | head -2 | tail -1 | cut -d = -f 2 | cut -d ' ' -f 2)"
    Z="$(echo "$DATA" | head -3 | tail -1 | cut -d = -f 2 | cut -d ' ' -f 3)"
    echo "${EFIELD#ori-e} $X $Y $Z"
done
