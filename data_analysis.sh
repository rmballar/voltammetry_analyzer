#!/bin/bash
# Requires: python, gnumeric
cp ~/school/bme129/titration/voltammetry_analyzer.py .  # Path to python .tsv converter
mkdir out-files in-files
ls|grep .txt|python voltammetry_analyzer.py>np-num; NP=$(cat np-num)
ssconvert --merge-to=$NP *.tsv 2> err-log.err
rm np-num
gnuplot -e "load 'np_titration.gp' ; pause 5"
mv *.tsv out-files
mv *.txt in-files