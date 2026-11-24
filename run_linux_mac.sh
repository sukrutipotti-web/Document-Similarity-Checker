#!/bin/sh
set -e
cd "$(dirname "$0")"
gcc -std=c11 -Wall -Wextra -O2 c_core/main.c -o similarity_engine
python3 server.py
