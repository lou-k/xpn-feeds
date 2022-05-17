#!/bin/bash -x
set -euo pipefail
IFS=$'\n\t'

DIRECTORY=$(dirname $0)
pushd $DIRECTORY
pipenv install
pipenv run python generate.py
git add feeds
git commit -a -m "Feed Update for $(date)"
git push origin
popd
