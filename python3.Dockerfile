FROM python:alpine3.11
RUN pip install pytest
COPY ../scripts /medusa/scripts
COPY ../tests /medusa/tests

WORKDIR /medusa
ENTRYPOINT [ "/usr/local/bin/pytest", "-s" ]