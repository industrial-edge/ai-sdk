# Copyright Siemens AG 2023
# SPDX-License-Identifier: MIT
# This Dockerfile is used to create a development container for the SAIL Vessel Python SDK.

FROM python-vessel-base:latest

ENV LD_LIBRARY_PATH=/usr/local/lib64

# Install simaticai
# Before copying the file, you need to build the simaticai wheel files and copy to the .devcontainer folder
COPY simaticai-*.whl /tmp/

# Create .ai_sdk_docker marker file
RUN touch /.ai_sdk_docker
RUN python3.10 -m pip install --no-cache-dir simaticai -f /tmp && \
    python3.11 -m pip install --no-cache-dir simaticai -f /tmp

# Set the working directory to /workspace
WORKDIR /workspace
