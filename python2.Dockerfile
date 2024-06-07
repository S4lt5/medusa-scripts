FROM python:2.7.18-alpine3.11
RUN apk add --no-cache python2
COPY ../scripts /medusa/scripts
COPY ../tests /medusa/tests
RUN pip2 install pytest

COPY testfiles /testfiles
RUN ls /
RUN ls /testfiles
RUN /bin/sh /testfiles/setup-me-files.sh
WORKDIR /medusa
ENTRYPOINT [ "/usr/local/bin/pytest", "-s" ]