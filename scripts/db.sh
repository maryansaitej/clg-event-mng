#!/usr/bin/env bash
source "$(dirname "$0")/environment.sh"
for cmd in initdb pg_ctl createdb psql; do command -v "$cmd" >/dev/null || { echo "Install PostgreSQL 17 and add its bin directory to PATH."; exit 1; }; done
if [[ ! -f .data/postgres/PG_VERSION ]]; then
 initdb -D "$TASK_ROOT/.data/postgres" -A trust -U campus --no-instructions > .data/initdb.log
fi
if ! pg_ctl -D "$TASK_ROOT/.data/postgres" status >/dev/null 2>&1; then
 pg_ctl -D "$TASK_ROOT/.data/postgres" -l "$TASK_ROOT/.data/postgres.log" -o '-p 54329 -h 127.0.0.1 -k /tmp' start
fi
if [[ "$(psql -h 127.0.0.1 -p 54329 -U campus -d postgres -Atc "SELECT 1 FROM pg_database WHERE datname='campus_commons'")" != 1 ]]; then createdb -h 127.0.0.1 -p 54329 -U campus campus_commons; fi
printf '%s\n' 'Local development database: 127.0.0.1:54329/campus_commons (loopback only, development trust authentication).'
