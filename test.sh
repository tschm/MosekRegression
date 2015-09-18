#!/bin/bash
FOLDER="$(cd "$(dirname "$0")" && pwd)"
${FOLDER}/env/bin/nosetests
