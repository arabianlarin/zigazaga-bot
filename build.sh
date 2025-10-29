#!/usr/bin/env bash
# build.sh

pip install -r requirements.txt
apt-get update
apt-get install -y chromium chromium-driver
