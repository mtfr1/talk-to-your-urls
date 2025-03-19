#!/bin/bash
echo Starting Uvicorn

if [[ -z "${HOST}" ]]; then
  HOST="0.0.0.0"
fi

if [[ -z "${PORT}" ]]; then
  PORT="6000"
fi

if [[ -z "${NUM_WORKERS}" ]]; then
  NUM_WORKERS=1
fi

UVICORN_CMD="uvicorn app.main:app --host $HOST --port $PORT --workers $NUM_WORKERS"

eval $UVICORN_CMD