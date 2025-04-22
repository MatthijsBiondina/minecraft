#!/bin/bash

# Define daemons to run - just add one line per new daemon
DAEMONS=(
  "daemons.screencapture"
  "daemons.windowfocusmonitor"
  "daemons.backtogame"
  "daemons.playerstate"
)

# Array to store PIDs of started processes
declare -a PIDS

# Function to kill all started processes
cleanup() {
  echo "Stopping all daemons..."
  for pid in "${PIDS[@]}"; do
    echo "Killing process $pid"
    kill $pid 2>/dev/null
  done
  exit 0
}

# Set up trap to catch Ctrl+C (SIGINT)
trap cleanup SIGINT

# Start all daemons
for daemon in "${DAEMONS[@]}"; do
  python -m $daemon &
  PIDS+=($!)
  echo "Started $daemon with PID $!"
done

echo "All daemons started. Press Ctrl+C to stop all daemons."

# Wait forever (or until Ctrl+C)
while true; do
  sleep 1
done