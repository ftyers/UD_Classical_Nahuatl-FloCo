#!/bin/bash

cat ../conllu/*.conllu | grep 'Norm' | sed 's/Norm=/\t&/g'| cut -f11 | cut -f1 -d'|' | cut -f2 -d'=' | apertium-destxt | hfst-proc -w nci.mor.hfstol | apertium-retxt > /tmp/nci.analysed

unknown=$(cat /tmp/nci.analysed | grep '*' | wc -l)
total=$(cat /tmp/nci.analysed | wc -l)
known=$(echo "${total} - ${unknown}" | bc -l)
coverage=$(echo "${known}/${total}*100" | bc -l | head -c 6)

echo "Tokens: ${known}/${total} (${coverage}%)"

cat /tmp/nci.analysed | cut -f2 -d'^' | cut -f1 -d'/' | sort -f | uniq -c | sort -gr > nci.freq

total=$(cat nci.freq | apertium-destxt | hfst-proc nci.mor.hfstol   | wc -l)
known=$(cat nci.freq | apertium-destxt | hfst-proc nci.mor.hfstol   | grep '<' | wc -l)
coverage=$(echo "${known}/${total}*100" | bc -l | head -c 6)
echo "Types:  ${known}/${total} (${coverage}%)" 
