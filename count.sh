#!/bin/bash
i=0
while true;
do
  echo hello $i $*
  i=$((i+1))
  sleep 1
done
