#!/bin/sh

while read LINE; do
	if echo "$LINE" | egrep -q '^[^\w]$' ; then
		exit 0;
	fi
	echo "$LINE"
done
