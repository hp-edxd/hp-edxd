#!/usr/bin/env bash
rm -rf build
rm -rf dist
pyinstaller hpMCA.spec -y
