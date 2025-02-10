#!/usr/bin/bash
while read p; do
  "$p"
#  echo "$p" | sed 's/\\/\\\\/g'
  break
done <audit.log
