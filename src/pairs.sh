#!/bin/bash
zcat $1 | awk -F "\"*,\"*" '{printf("%d, %d\n", $4, $8)}' | grep -v '0, 0' | sort -n | uniq >all_pairs.csv
