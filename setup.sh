#!/bin/bash

# .env 파일의 경로
env_file=".env"

# .env 파일이 존재하는지 확인
if [ -f "$env_file" ]; then
    # .env 파일을 줄 단위로 읽어서 환경 변수로 설정
    while IFS= read -r line || [ -n "$line" ]; do
        # 공백 제거
        line="${line#"${line%%[![:space:]]*}"}"
        line="${line%"${line##*[![:space:]]}"}"
        
        # 빈 줄이나 주석은 무시
        if [ -n "$line" ] && [ "${line:0:1}" != "#" ]; then
            # 등호로 분리해서 키와 값을 가져옴
            key="${line%=*}"
            value="${line#*=}"
            
            # 환경 변수로 등록
            export "$key=$value"
        fi
    done < "$env_file"
else
    echo "No .env file found."
fi
