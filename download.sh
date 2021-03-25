#!/bin/bash

cd data
for x in `cat ../urls.txt`; do
    echo downloading $x
    wget $x
done
