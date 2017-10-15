#!/bin/bash
zcat $1 | awk -F "\"*,\"*" '{print $4}' | grep -v 'start station id' | sort -n | uniq >../data/start_station_ids.txt
zcat $1 | awk -F "\"*,\"*" '{print $8}' | grep -v 'end station id' | sort -n | uniq >../data/end_station_ids.txt
zcat $1 | awk -F "\"*,\"*" '{printf("%d,\"%s\",%s,%s\n", $4, $5, $6, $7)}' | grep -v 'start station' | sort -n | uniq >../data/station_lat_longs.csv
