#!/usr/bin/env bash

pids=()

cleanup() {
  trap - INT TERM EXIT
  for pid in "${pids[@]}"; do
    pkill -TERM -P "$pid" 2>/dev/null
    kill -TERM "$pid" 2>/dev/null
  done
  wait 2>/dev/null
  exit 0
}
trap cleanup INT TERM EXIT

(cd backend && uv run python -m uvicorn src.api.api:app --reload) &
pids+=($!)

(cd backend && uv run -m src.jobs.pinger) &
pids+=($!)

(cd frontend && npm run dev) &
pids+=($!)

wait
