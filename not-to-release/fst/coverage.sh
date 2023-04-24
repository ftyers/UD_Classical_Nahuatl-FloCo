#!/bin/bash

cat ../conllu/*.conllu | grep 'Norm' | sed 's/Norm=/\t&/g'| cut -f11 | cut -f1 -d'|' | cut -f2 -d'=' | apertium-destxt | hfst-proc -w nci.mor.hfstol | apertium-cleanstream -n | grep -v '^$' > /tmp/nci.analysed

unknown=$(cat /tmp/nci.analysed | grep '*' | wc -l)
total=$(cat /tmp/nci.analysed | wc -l)
known=$(echo "${total} - ${unknown}" | bc -l)
coverage=$(echo "${known}/${total}*100" | bc -l | head -c 6)

#echo "Tokens: ${known}/${total} (${coverage}%)"

d=`date`
z=`date +%s`
stems=0
#`cd ~/source/apertium/incubator/apertium-$code/dev; bash countstems.sh 2>/dev/null; cd - >/dev/null`;
lex=0
#`cat ~/source/apertium/incubator/apertium-$code/apertium-$code.$code.lexc | grep 'LEXICON' | wc -l`;

cat /tmp/nci.analysed | cut -f2 -d'^' | cut -f1 -d'/' | sort -f | uniq -c | sort -gr > nci.freq

total_types=$(cat nci.freq | wc -l)
known_types=$(cat nci.freq | sed -E 's/[[:digit:]]+ //g' | hfst-proc nci.mor.hfstol   | grep '<' | wc -l)
coverage_types=$(echo "${known_types}/${total_types}*100" | bc -l | head -c 6)
#echo "Types:  ${known}/${total} (${coverage}%)" 

echo -e "${d}\t${z}\t${stems}/${lex}\t${known}/${total}\t${coverage}\t${known_types}/${total_types}\t${coverage_types}" >> history.log
tail -1 history.log

cat /tmp/nci.analysed | grep '*' | sort | uniq -c | sort -nr | head -n25
