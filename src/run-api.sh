#!/bin/bash

gunicorn -k uvicorn.workers.UvicornWorker --access-logfile ./logs/gunicorn-access.log api.main:app --bind 0.0.0.0:8080 --workers 2 --daemon
