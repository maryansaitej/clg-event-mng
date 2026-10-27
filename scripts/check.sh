#!/usr/bin/env bash
source "$(dirname "$0")/environment.sh"
mvn -q -f backend/pom.xml spotless:check test
pnpm --dir frontend test
pnpm --dir frontend lint
pnpm --dir frontend exec prettier --check src e2e '*.ts' '*.js' '*.json'
pnpm --dir frontend build
mvn -q -f backend/pom.xml -DskipTests package
