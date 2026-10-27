#!/usr/bin/env bash
source "$(dirname "$0")/environment.sh"
./scripts/db.sh
if [[ "$(psql -h 127.0.0.1 -p 54329 -U campus -d postgres -Atc "SELECT 1 FROM pg_database WHERE datname='campus_commons_test'")" != 1 ]]; then createdb -h 127.0.0.1 -p 54329 -U campus campus_commons_test; fi
TEST_DATABASE_URL=jdbc:postgresql://127.0.0.1:54329/campus_commons_test TEST_DATABASE_USERNAME=campus mvn -q -f backend/pom.xml test
