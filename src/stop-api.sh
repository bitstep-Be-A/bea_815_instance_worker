#!/bin/bash

# Find and kill gunicorn processes
pids=$(ps aux | grep gunicorn | grep -v grep | awk '{print $2}')
for pid in $pids; do
    echo "Killing process $pid..."
    kill $pid
done

echo "All gunicorn processes have been killed."
