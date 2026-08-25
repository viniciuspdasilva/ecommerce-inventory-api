FROM ubuntu:latest
LABEL authors="b-boy"

ENTRYPOINT ["top", "-b"]