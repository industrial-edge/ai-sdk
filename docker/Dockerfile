# SPDX-FileCopyrightText: Copyright (C) 2023 Siemens AG
# SPDX-License-Identifier: MIT
# This Dockerfile creates the Python runner base and final AI SDK image in one build.

FROM debian:trixie-slim AS python-vessel-base

USER root

ENV HOME=/root

WORKDIR /usr/sail/

COPY ./openssl-3.6.2.tar.gz \
     ./sqlite-autoconf-3500400.tar.gz \
     ./Python-3.10.20.tar.xz \
     ./Python-3.11.15.tar.xz \
     ./Python-3.12.13.tar.xz \
     ./setuptools-80.9.0_clean.tar.gz \
     ./pip-26.0.1.tar.gz \
     ./flit_core-3.12.0-py3-none-any.whl \
     ./unzip_6.0-23+deb10u3.debian_cleared.tar.xz \
     ./bzip2-latest-1.0.8_Clean.tar.gz \
     ./xz-5.8.1_clean.tar.gz \
     ./libffi-3.4.2.tar.gz /usr/sail/

# Beware: openssl not allowing multithread builds
# bzip required for some Python packages (pandas)
RUN mkdir -p /usr/sail/build && \
    apt-get update && \
    apt-get -y install --no-install-recommends adduser build-essential && \
    echo "installing unzip" >&2 && \
    tar xf unzip_6.0-23+deb10u3.debian_cleared.tar.xz -C /usr/sail/build && \
    rm unzip_6.0-23+deb10u3.debian_cleared.tar.xz && \
    cd /usr/sail/build/unzip60/ && \
    make -j "$(nproc)" -f unix/Makefile linux_noasm && \
    mv unzip funzip unzipsfx /usr/bin/ && \
    echo "installing openssl" >&2 && \
    tar xzf /usr/sail/openssl-3.6.2.tar.gz -C /usr/sail/build/ && \
    rm /usr/sail/openssl-3.6.2.tar.gz && \
    cd /usr/sail/build/openssl-3.6.2/ && \
    ./config --openssldir=/usr/lib/ssl && \
    make install && \
    ldconfig /usr/local/lib64/ && \
    echo "installing libffi" >&2 && \
    tar xzf /usr/sail/libffi-3.4.2.tar.gz -C /usr/sail/build && \
    rm /usr/sail/libffi-3.4.2.tar.gz && \
    cd /usr/sail/build/libffi-3.4.2/ && \
    ./configure --disable-static && \
    make -j "$(nproc)" install && \
    ldconfig && \
    apt-get -y install --no-install-recommends zlib1g-dev=1:1.3.dfsg+really1.3.1-1+b1 && \
    echo "installing xz" >&2 && \
    tar xzf /usr/sail/xz-5.8.1_clean.tar.gz -C /usr/sail/build && \
    rm /usr/sail/xz-5.8.1_clean.tar.gz && \
    cd /usr/sail/build/xz-5.8.1/ && \
    ./configure --disable-xz \
    --disable-xzdec \
    --disable-lzmadec \
    --disable-lzmainfo \
    --disable-scripts \
    --disable-doc \
    --disable-static && \
    make install && \
    ldconfig && \
    echo "installing bzip2" >&2 && \
    tar xvfz /usr/sail/bzip2-latest-1.0.8_Clean.tar.gz -C /usr/sail/build && rm /usr/sail/bzip2-latest-1.0.8_Clean.tar.gz && \
    cd /usr/sail/build/bzip2-1.0.8/ && make -j "$(nproc)" install PREFIX=/usr/local/bzip2/1_0_8 && \
    rm -vrf /usr/local/bzip2/1_0_8/bin && \
    rm /usr/local/bzip2/1_0_8/lib/libbz2.a && \
    ln -s /usr/local/bzip2/1_0_8/include/bzlib.h /usr/local/include/ && \
    ln -s /usr/local/bzip2/1_0_8/lib/libbz2.so.1.0.8 /usr/local/bzip2/1_0_8/lib/libbz2.so.1.0 && \
    ln -s /usr/local/bzip2/1_0_8/lib/libbz2.so.1.0 /usr/local/lib/ && \
    ln -s /usr/local/bzip2/1_0_8/lib/libbz2.so.1.0 /usr/local/lib/libbz2.so && \
    ldconfig && \
    make -j "$(nproc)" clean && make -j "$(nproc)" -f Makefile-libbz2_so && \
    mv libbz2.so.1.0.8 /usr/local/bzip2/1_0_8/lib/ && \
    export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib64 && \
    echo "installing sqlite" >&2 && \
    tar xf /usr/sail/sqlite-autoconf-3500400.tar.gz -C /usr/sail/build && \
    rm -vrf /usr/sail/sqlite-autoconf-3500400.tar.gz && \
    cd /usr/sail/build/sqlite-autoconf-3500400 && \
    ./configure --disable-static && make -j "$(nproc)" install && \
    ldconfig && \
    rm -f /usr/local/bin/sqlite3 && \
    echo "installing python 3.10" >&2 && \
    tar xf /usr/sail/Python-3.10.20.tar.xz -C /usr/sail/build && \
    rm -vrf /usr/sail/Python-3.10.20.tar.xz && \
    cd /usr/sail/build/Python-3.10.20 && \
    sed -i -e '207 s/#//g' -e '211 s/ OPENSSL=.*/ OPENSSL=\/usr\/local\/ssl/g' -e '211 s/#//g' -e '212 s/#//g' -e '213 s/#//g' -e '214 s/#//g' Modules/Setup && \
    ./configure --enable-optimizations --enable-shared --with-openssl=/usr/local && make -j "$(nproc)" LDFLAGS="-Wl,--strip-all" altinstall && \
    ldconfig && \
    echo "installing python 3.11" >&2 && \
    tar xf /usr/sail/Python-3.11.15.tar.xz -C /usr/sail/build && \
    rm -vrf /usr/sail/Python-3.11.15.tar.xz && \
    cd /usr/sail/build/Python-3.11.15 && \
    sed -i -e '215 s/#//g' -e '216 s/#//g' Modules/Setup && \
    ./configure --enable-optimizations --enable-shared --with-openssl=/usr/local && \
    make -j "$(nproc)" LDFLAGS="-Wl,--strip-all" && make -j "$(nproc)" LDFLAGS="-Wl,--strip-all" altinstall && \
    ldconfig && \
    echo "installing python 3.12" >&2 && \
    tar xf /usr/sail/Python-3.12.13.tar.xz -C /usr/sail/build && \
    rm -vrf /usr/sail/Python-3.12.13.tar.xz && \
    cd /usr/sail/build/Python-3.12.13 && \
    sed -i -e '214 s/#//g' -e '215 s/#//g' Modules/Setup && \
    ./configure --enable-optimizations --enable-shared --with-openssl=/usr/local && \
    make -j "$(nproc)" LDFLAGS="-Wl,--strip-all" && make -j "$(nproc)" LDFLAGS="-Wl,--strip-all" altinstall && \
    ldconfig && \
    echo "installing setuptools" >&2 && \
    tar xvzf /usr/sail/setuptools-80.9.0_clean.tar.gz -C /usr/sail/build && rm /usr/sail/setuptools-80.9.0_clean.tar.gz && \
    cd /usr/sail/build/setuptools-80.9.0/ && \
    python3.10 -m pip install . && \
    python3.11 -m pip install . && \
    python3.12 -m pip install . && \
    echo "installing pip" >&2 && \
    tar xvzf /usr/sail/pip-26.0.1.tar.gz -C /usr/sail/build && rm /usr/sail/pip-26.0.1.tar.gz && \
    cd /usr/sail/build/pip-26.0.1/ && \
    mv /usr/sail/flit_core-3.12.0-py3-none-any.whl /usr/sail/build/ && \
    python3.10 -m pip install /usr/sail/build/flit_core-3.12.0-py3-none-any.whl && \
    python3.11 -m pip install /usr/sail/build/flit_core-3.12.0-py3-none-any.whl && \
    python3.12 -m pip install /usr/sail/build/flit_core-3.12.0-py3-none-any.whl && \
    python3.10 -m pip install . --no-build-isolation && \
    python3.11 -m pip install . --no-build-isolation && \
    python3.12 -m pip install . --no-build-isolation && \
    python3.10 -m pip uninstall -y flit_core && \
    python3.11 -m pip uninstall -y flit_core && \
    python3.12 -m pip uninstall -y flit_core && \
    echo "cleaning up" >&2 && \
    rm -vrf /usr/local/bzip2/1_0_8/include && \
    rm -vrf /usr/local/lib/gcc && \
    rm -vrf /usr/local/include && \
    find /usr/local/ -name "*.la" -delete && \
    rm -vrf /usr/sail/build && \
    find /usr/local -depth \
    \( \
    \( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
    -o \
    \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
    \) -exec rm -vrf '{}' +  && \
    apt-get -y remove --purge build-essential zlib1g-dev && apt -y autoremove && \
    ## TODO with the kaniko build docker image the 'find' command fails for one of these last commands, needs investigation \
    # rm -vrf /usr/local/share/doc && \
    # rm -vrf /usr/local/share/man && \
    # find / -name "*.html" -delete && \
    # rm -vrf /var/lib/apt/lists/* && \
    # rm -vrf /etc/apt/apt.conf && \
    # find /usr/local/lib/python3* -type d -a \( \
    # -name __pycache__ -o \
    # -name test -o \
    # -name tests -o \
    # -name idlelib -o \
    # -name idle_test -o \
    # -name turtledemo -o \
    # -name pydoc_data -o \
    # -name tkinter \) \
    # -exec rm -vrf '{}' + && \
    # find /usr/local/lib/python3* -type f -a \( \
    # -name '*.a' -o \
    # -name '*.pyc' -o \
    # -name '*.pyo' -o \
    # -name '*.exe' \) \
    # -exec rm '{}' + \
    echo "FINISHED base image"

FROM python-vessel-base AS iai-sdk-python-runner

ENV LD_LIBRARY_PATH=/usr/local/lib64

RUN touch /.ai_sdk_docker && \
    python3.10 -m pip install --no-cache-dir simaticai && \
    python3.11 -m pip install --no-cache-dir simaticai && \
    python3.12 -m pip install --no-cache-dir simaticai && \
    echo "FINISHED AI SDK container"

WORKDIR /workspace
