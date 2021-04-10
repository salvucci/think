#!/bin/bash

sphinx-apidoc -f -o . ..
make clean
make html
