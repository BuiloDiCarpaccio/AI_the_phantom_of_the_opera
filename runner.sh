#! /usr/bin/env bash

LOOP_COUNT=$([ -z ${1+x} ] && echo -n 1 || echo -n $1)

echo "Running the simulation for ${LOOP_COUNT} times"
OUTPUT=$(mktemp)

run() {
	for (( i=1; i<=LOOP_COUNT; ++i ))
	do
		START=$(date +%s)
		echo -n "Run ${i}: "
		LAUNCHER_OUTPUT=$(sh launch.sh)
		echo "${LAUNCHER_OUTPUT}" >> $OUTPUT
		END=$(date +%s)
		RESULT=$([ $(echo -n ${LAUNCHER_OUTPUT} | tr ';' '\n' | sed -n '1p') == "inspector" ] && echo -ne "\e[32mwin\e[0m" || echo -ne "\e[31mloose\e[0m")
		RESULT=$([ $(echo -n ${LAUNCHER_OUTPUT} | tr ';' '\n' | sed -n '1p') == "timeout" ] && echo -ne "\e[31mtimeout\e[0m" || echo -ne "${RESULT}")
		echo "${RESULT} in $(( ${END} - ${START} )) sec"
	done
}

exec 3>&1 4>&2
TIME=$(TIMEFORMAT="%R"; { time run 1>&3 2>&4; } 2>&1)
exec 3>&- 4>&-

WINS=$(grep inspector ${OUTPUT} | wc -l)
WINS_CALC=$(( ${WINS} * 100 ))
TIMEOUTS=$(grep timeout ${OUTPUT} | wc -l)
WINRATE=$(( ${WINS_CALC} / ${LOOP_COUNT} ))

echo "${LOOP_COUNT} runs finished in ${TIME} sec"
echo "Results:"
echo "	Winrate: ${WINRATE}%"
echo "	Wins: ${WINS}/${LOOP_COUNT}"
echo "	Timeouts: ${TIMEOUTS}"