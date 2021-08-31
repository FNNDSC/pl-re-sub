FROM docker.io/library/pypy:3-7-slim-bullseye

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="ChRIS Regex Substitution" \
      org.opencontainers.image.description="A ChRIS ds plugin for using regular expressions to perform find-and-replace."

WORKDIR /usr/local/src

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
RUN pip3 install .

CMD ["resub", "--help"]
