# SQS worker process

## 요구 사항

version: python 3.10.6

필수 설치 사항

``` console
sudo apt-get -y update && \
sudo apt-get install -y --no-install-recommends \
build-essential \
openssl libssl-dev \
python3-dev \
ffmpeg \
tk \
&& sudo apt-get clean \
&& rm -rf /var/lib/apt/lists/*
```

## 실행 방법

1. 먼저 프로젝트 루트 디렉토리에 .env파일을 생성하고 전달 받은 .env 키, 값을 넣어주세요

2. firebase service key 파일을 루트 디렉토리에 넣어줍니다.

3. 콘솔에 아래와 같이 입력하세요

```console
./setup.sh
./start.sh
```
