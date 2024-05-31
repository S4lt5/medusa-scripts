FROM python:2.7.18-alpine3.11
RUN apk add --no-cache python2
COPY ../scripts /medusa/scripts
COPY ../tests /medusa/tests
RUN pip2 install pytest

WORKDIR /medusa
ENTRYPOINT [ "/usr/local/bin/pytest", "-s" ]