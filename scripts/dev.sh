#!/usr/bin/env bash
source "$(dirname "$0")/environment.sh"
export SPRING_PROFILES_ACTIVE="${SPRING_PROFILES_ACTIVE:-dev}"
export DATABASE_URL="${DATABASE_URL:-jdbc:postgresql://127.0.0.1:54329/campus_commons}"
export DATABASE_USERNAME="${DATABASE_USERNAME:-campus}"
if [[ "$DATABASE_URL" == 'jdbc:postgresql://127.0.0.1:54329/campus_commons' ]]; then ./scripts/db.sh; fi
if curl -fsS http://127.0.0.1:8080/api/health >/dev/null 2>&1 || curl -fsS http://127.0.0.1:5173 >/dev/null 2>&1; then echo 'Port 8080 or 5173 is already in use. Stop the existing development server first.'; exit 1; fi
mvn -q -f backend/pom.xml -DskipTests package
cp backend/target/campus-commons-1.0.0.jar .data/campus-dev.jar
java -Xmx384m -jar .data/campus-dev.jar > .data/backend.log 2>&1 & TASK_API_PID=$!
(cd frontend; exec node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5173) > .data/frontend.log 2>&1 & TASK_WEB_PID=$!
trap 'kill "$TASK_API_PID" "$TASK_WEB_PID" 2>/dev/null || true' EXIT INT TERM
for ((i=0;i<60;i++)); do
 if curl -fsS http://127.0.0.1:8080/api/health >/dev/null 2>&1 && curl -fsS http://127.0.0.1:5173 >/dev/null 2>&1; then printf '%s\n' 'Campus Commons is ready: http://127.0.0.1:5173' 'Logs: .data/backend.log and .data/frontend.log. Press Ctrl+C to stop.'; wait "$TASK_API_PID" "$TASK_WEB_PID"; exit 0; fi
 if ! kill -0 "$TASK_API_PID" "$TASK_WEB_PID" 2>/dev/null; then tail -30 .data/backend.log .data/frontend.log; exit 1; fi
 sleep 1
done
echo 'Startup timed out. Check .data/backend.log and .data/frontend.log.'; exit 1
