#!/bin/bash

# If thy OS canst not find "dot", 
# thou must execute "sudo apt install graphviz".

for filename in .profiles/*.prof; do
    gprof2dot -f pstats $filename | dot -Tpng -o $filename.png && eog $filename.png
done

