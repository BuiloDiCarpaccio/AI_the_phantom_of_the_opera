#!/usr/bin/env bash

# Creating serv output temp file
SERV_OUTPUT=$(mktemp)

# Launching server
( python3 bui_src/server.py ) &> "${SERV_OUTPUT}" &

# Getting the server PID
PID_SERV=$!

# Waiting for the server to init
sleep 1s

# launching inspector
( python3 $1 ) &> /dev/null &

sleep 0.5s

# launching fantom
( python3 $2 ) &> /dev/null &

# Waiting for the game to end
wait $PID_SERV

validate() {
	# Checking for timeout
	if grep -Fq timeout ${SERV_OUTPUT}
	then
		echo "timeout;;"
		return 2
	fi

	# Parsing of SERV_OUTPUT
	WINNER=$(cat $SERV_OUTPUT | grep wins | tr ' ' '\n' | sed -n '2p')
	PHANTOM=$(cat $SERV_OUTPUT | grep wins | tr ' ' '\n' | tail -1)
	FINAL_SCORE=$(cat $SERV_OUTPUT | grep score | tr ' ' '\n' | tail -1)
	PHANTOM=$([ $PHANTOM == "wins" ] && echo -n "" || echo -n "$PHANTOM" )

	echo "${WINNER};${PHANTOM};${FINAL_SCORE}"
}

validate