node index.js

# Drop duplicate lines
for csv in data/* ; do
  awk '!seen[$0]++' $csv >> $csv.tmp && mv $csv.tmp $csv
done
