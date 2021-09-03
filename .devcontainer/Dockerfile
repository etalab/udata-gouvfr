ARG VARIANT="3.7"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="14"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

RUN mkdir -p /tmp/

COPY requirements/ /tmp/requirements
RUN git clone https://github.com/opendatateam/udata.git /tmp/udata
COPY udata.cfg /tmp/udata/
RUN pip install /tmp/udata \
                -r /tmp/requirements/install.pip \
                -r /tmp/requirements/test.pip \
                -r /tmp/requirements/develop.pip

RUN cd /tmp/udata && npm install --unsafe-perm && inv assets-build
