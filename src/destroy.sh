#!/bin/bash

docker rm -f roop-img2img-api webserver
docker rmi roop-img2img-api nginx:alpine
