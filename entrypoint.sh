#!/bin/bash
set -e
alembic upgrade head
python run.py
