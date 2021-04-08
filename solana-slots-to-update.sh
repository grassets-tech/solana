#!/bin/bash
BIN_FILE="/home/solana/.local/share/solana/install/active_release/bin/solana"
url="http://127.0.0.1:8899/"
minRange=2250 ###  15 minutes

identity=$($BIN_FILE address -k validator-keypair.json 2>/dev/null)
#identity=$($BIN_FILE address --url $url 2>/dev/null)
curSlot=$($BIN_FILE slot --url $url 2>/dev/null)
slots=$($BIN_FILE leader-schedule --url $url --output json 2>/dev/null | jq '.[]' | jq '.[]? | select(.leader == "'$identity'") | select(.slot >= '$curSlot') | .slot' 2>/dev/null)

prevSlot=$curSlot
maxRange=0
maxSlot=0
nearRange=0
nearSlot=0

for slot in ${slots}; do
	curRange=$((slot - prevSlot))
	if ((curRange > minRange)) && ((curRange > maxRange)); then
		maxRange=$curRange && maxSlot=$prevSlot
	fi
	if ((curRange > minRange)) && ((nearRange == 0)); then
		nearRange=$curRange && nearSlot=$prevSlot
	fi
	prevSlot=$slot
done

function slotsToMinutes () {
	bc -l <<< "scale=0; $1 * 0.4 / 60"
}

function echoRange () {
	local _slot=$1
	local _range=$2
	local _range_in_minutes=$(slotsToMinutes $_range)
	local _slots_before_this_range=$((_slot - curSlot))
	local _slots_before_this_range_in_minutes=$(slotsToMinutes $_slots_before_this_range)
	echo -ne "$_slot ($_range slots long = $_range_in_minutes minutes, will happen after $_slots_before_this_range slots = $_slots_before_this_range_in_minutes minutes)"
}


echo
echo "Current slot: $curSlot" && \
echo "Nearest update slot: $(echoRange $nearSlot $nearRange)"
echo "Longest update slot: $(echoRange $maxSlot $maxRange)"
