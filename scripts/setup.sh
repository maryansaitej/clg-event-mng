#!/usr/bin/env bash
source "$(dirname "$0")/environment.sh"
for cmd in node pnpm java mvn; do command -v "$cmd" >/dev/null || { echo "Missing $cmd. See README prerequisites."; exit 1; }; done
pnpm --dir frontend install --frozen-lockfile
./scripts/db.sh
mvn -q -f backend/pom.xml -DskipTests package
printf '%s\n' 'Setup complete. Start the application with ./scripts/dev.sh'
