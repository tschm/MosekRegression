#!/bin/bash

NAME="mosek"

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install jupyter jupyter-book ipykernel

ipython kernel install --name $NAME --user

jupyter-book clean book
jupyter-book build book
