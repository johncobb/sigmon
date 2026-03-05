#!/bin/bash


# logging
export LOG_LEVEL="logging.INFO"
export LOG_FORMAT="%(asctime)s %(levelname)s: %(message)s"
export LOG_ERROR_FORMAT="%(asctime)s %(levelname)s: %(message)s -- %(filename)s(%(lineno)d)"
export LOG_RAW=false


PYTHONPATH=$PWD $PWD/env/bin/python src/signaler.py
