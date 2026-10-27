#!/usr/bin/env bash
# Sourced by project scripts. Prefer installed runtimes; the Codex bundle is a local fallback.
set -euo pipefail
TASK_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$TASK_ROOT"
TASK_BUNDLE="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies"
if ! command -v node >/dev/null && [[ -x "$TASK_BUNDLE/node/bin/node" ]]; then export PATH="$TASK_BUNDLE/node/bin:$PATH"; fi
if ! command -v pnpm >/dev/null && [[ -x "$TASK_BUNDLE/bin/fallback/pnpm" ]]; then export PATH="$TASK_BUNDLE/bin/fallback:$PATH"; fi
if [[ -d /opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home ]]; then export JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home; fi
if [[ -n "${JAVA_HOME:-}" ]]; then export PATH="$JAVA_HOME/bin:$PATH"; fi
if [[ -d /opt/homebrew/opt/postgresql@17/bin ]]; then export PATH="/opt/homebrew/opt/postgresql@17/bin:/opt/homebrew/bin:$PATH"; fi
if [[ -f .env ]]; then set -a; source .env; set +a; fi
mkdir -p .data
