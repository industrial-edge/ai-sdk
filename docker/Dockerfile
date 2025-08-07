# Copyright Siemens AG 2023
# SPDX-License-Identifier: MIT

# This Dockerfile is used to create a development container for the SAIL Vessel Python SDK.

# FROM cr.siemens.com/siemens-ai-launcher-sail/ai-on-edge/sail-vessel/sail-vessel-python-base/python-vessel-base:1.7.0
FROM python-vessel-base

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
