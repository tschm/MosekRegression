#!/bin/bash
FOLDER="$(cd "$(dirname "$0")" && pwd)"
rm -rf ${FOLDER}/env
conda create --yes -p ${FOLDER}/env python=2.7.6 pip=7.1.2 nose=1.3.7 matplotlib=1.4.3 pandas=0.16.2 ipython-notebook=4.0.4
${FOLDER}/env/bin/pip install -r requirements.txt



