#!/usr/bin/env bash
set -e

cleanup() {
  kill 0
}
trap cleanup EXIT INT TERM

(cd backend && uv run python -m uvicorn src.api.api:app --reload) &
(cd backend && uv run -m src.jobs.pinger) &
(cd frontend && npm run dev) &

wait
