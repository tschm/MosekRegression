#!/bin/bash

NAME="mosek"

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install jupyter

ipython kernel install --name $NAME --user
