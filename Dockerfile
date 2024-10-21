FROM ubuntu:latest
LABEL authors="tsir"

ENTRYPOINT ["top", "-b"]