#!/bin/bash

set -m

uvicorn main:app --host 0.0.0.0 --port 7898 &
python updating.py

fg %1
