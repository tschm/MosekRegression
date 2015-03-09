#!/bin/bash
rm -rf ./env
conda create --yes -p ./env python=2.7.6 pip nose numpy matplotlib pandas ipython
./env/bin/pip install -r requirements.txt



