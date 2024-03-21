#!/usr/bin/env bash
# for file in "./db"/*.sql; do
#     psql -f "${file}" > ${file%.sql}.txt
# done

for file in "./db"/*.sql; do
    psql -f "${file}"
done
