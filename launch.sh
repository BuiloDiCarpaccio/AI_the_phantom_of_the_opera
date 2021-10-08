#!/usr/bin/env bash

# Creating serv output temp file
SERV_OUTPUT=$(mktemp)

# Launching server
( python3 server.py ) &> "${SERV_OUTPUT}" &

# Getting the server PID
PID_SERV=$!

# Waiting for the server to init
sleep 2

# launching run.py
( python3 run.py ) &

sleep 1

# launching random fantom
python3 random_fantom.py &> /dev/null &

# Waiting for the game to end
wait $PID_SERV

# Parsing of SERV_OUTPUT
WINNER=`cat $SERV_OUTPUT | grep wins | tr ' ' '\n' | sed -n '2p'`
FANTOM=`cat $SERV_OUTPUT | grep wins | tr ' ' '\n' | tail -1`
FINAL_SCORE=`cat $SERV_OUTPUT | grep score | tr ' ' '\n' | tail -1`
FANTOM=$([ $FANTOM == "wins" ] && echo -n "" || echo -n "$FANTOM" )

echo "${WINNER};${FANTOM};${FINAL_SCORE}"