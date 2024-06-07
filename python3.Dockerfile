FROM python:alpine3.11
RUN pip install pytest
COPY ../scripts /medusa/scripts
COPY ../tests /medusa/tests


COPY testfiles /testfiles
RUN /bin/sh /testfiles/setup-me-files.sh

WORKDIR /medusa
ENTRYPOINT [ "/usr/local/bin/pytest", "-s" ]