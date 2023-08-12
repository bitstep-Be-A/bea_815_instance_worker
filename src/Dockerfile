FROM python:3.10.6-slim

RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    openssl libssl-dev \
    python3-dev \
    ffmpeg \
    tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /src/roop

WORKDIR /src/roop

RUN pip3 install -r requirements-api.txt

EXPOSE 7860

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
