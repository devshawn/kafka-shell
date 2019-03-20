#!/usr/bin/env bash

rm -r dist/ build/
python3 setup.py sdist bdist_wheel
