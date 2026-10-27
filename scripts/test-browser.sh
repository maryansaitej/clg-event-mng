#!/usr/bin/env bash
source "$(dirname "$0")/environment.sh"
./scripts/db.sh
if [[ "$(psql -h 127.0.0.1 -p 54329 -U campus -d postgres -Atc "SELECT 1 FROM pg_database WHERE datname='campus_commons_e2e'")" != 1 ]]; then createdb -h 127.0.0.1 -p 54329 -U campus campus_commons_e2e; fi
if [[ ! -f backend/target/campus-commons-1.0.0.jar ]]; then echo 'Run ./scripts/check.sh first to build the tested backend.'; exit 1; fi
if curl -fsS http://127.0.0.1:8082/api/health >/dev/null 2>&1 || curl -fsS http://127.0.0.1:5174 >/dev/null 2>&1; then echo 'Test ports 8082 or 5174 are in use.'; exit 1; fi
cp backend/target/campus-commons-1.0.0.jar .data/campus-e2e.jar
SPRING_PROFILES_ACTIVE=dev APP_SEED=true APP_ADMIN_EMAIL='' APP_ADMIN_PASSWORD='' APP_PAYMENT_PROVIDER=mock APP_BASE_URL=http://127.0.0.1:5174 PORT=8082 DATABASE_URL=jdbc:postgresql://127.0.0.1:54329/campus_commons_e2e DATABASE_USERNAME=campus DATABASE_PASSWORD='' java -Xmx384m -jar .data/campus-e2e.jar > .data/e2e-backend.log 2>&1 & TASK_API_PID=$!
(cd frontend; export API_PROXY_TARGET=http://127.0.0.1:8082; exec node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5174) > .data/e2e-frontend.log 2>&1 & TASK_WEB_PID=$!
trap 'kill "$TASK_API_PID" "$TASK_WEB_PID" 2>/dev/null || true' EXIT INT TERM
for ((i=0;i<60;i++)); do
 if curl -fsS http://127.0.0.1:8082/api/health >/dev/null 2>&1 && curl -fsS http://127.0.0.1:5174 >/dev/null 2>&1; then
  pnpm --dir frontend exec playwright install chromium
  BASE_URL=http://127.0.0.1:5174 pnpm --dir frontend test:e2e
  exit 0
 fi
 if ! kill -0 "$TASK_API_PID" "$TASK_WEB_PID" 2>/dev/null; then tail -30 .data/e2e-backend.log .data/e2e-frontend.log; exit 1; fi
 sleep 1
done
echo 'Browser test server startup timed out.'; exit 1
