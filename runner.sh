#! /usr/bin/env bash

LOOP_COUNT=$([ -z ${1+x} ] && echo -n 1 || echo -n $1)
INSPECTOR=$([ -z ${2+x} ] && echo -n "random_inspector.py" || echo -n $2)
PHANTOM=$([ -z ${3+x} ] && echo -n "random_fantom.py" || echo -n $3)

echo "Running the simulation for ${LOOP_COUNT} times"
OUTPUT=$(mktemp)

run() {
	for (( i=1; i<=LOOP_COUNT; ++i ))
	do
		START=$(date +%s)
		echo -n "Run ${i}: "
		LAUNCHER_OUTPUT=$(sh launch.sh $INSPECTOR $PHANTOM)
		echo "${LAUNCHER_OUTPUT}" >> $OUTPUT
		END=$(date +%s)
		RESULT=$([ $(echo -n ${LAUNCHER_OUTPUT} | tr ';' '\n' | sed -n '1p') == "inspector" ] && echo -ne "\033[32minspector\033[0m | \033[31mphantom\033[0m " || echo -ne "\033[31minspector\033[0m | \033[32mphantom\033[0m")
		RESULT=$([ $(echo -n ${LAUNCHER_OUTPUT} | tr ';' '\n' | sed -n '1p') == "timeout" ] && echo -ne "\033[31mtimeout\033[0m" || echo -ne "${RESULT}")
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
echo "	Inspector winrate: ${WINRATE}%"
echo "	Inspector wins: ${WINS}/${LOOP_COUNT}"
echo "	Phantom winrate: $(( 100 - ${WINRATE} ))%"
echo "	Phantom wins: $(( ${LOOP_COUNT} - ${WINS} ))/${LOOP_COUNT}"
echo "	Timeouts: ${TIMEOUTS}"