unknown=$(cat ../../scripts/lexicon.tsv  | cut -f1 | hfst-lookup nci.mor.hfst 2>/dev/null | grep '+?' | wc -l)
total=$(cat ../../scripts/lexicon.tsv  | cut -f1 | hfst-lookup nci.mor.hfst 2>/dev/null | grep '^$' | wc -l)
known=$(echo "${total} - ${unknown}" | bc -l)
coverage=$(echo "${known}/${total}*100" | bc -l | head -c 6)

echo "${known}/${total} (${coverage}%)"
