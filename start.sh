#!/bin/bash
set -e

echo ".env파일을 읽어서 environment 추가"
if [[ -f .env ]]; then
  export $(cat .env | grep -v '^#' | xargs)
fi

sudo systemctl start worker
