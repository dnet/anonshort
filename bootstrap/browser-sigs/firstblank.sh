#!/bin/sh

while read LINE; do
	echo "$LINE" | grep '^[A-Z]' || exit 0
done
