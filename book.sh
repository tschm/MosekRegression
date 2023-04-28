#!/bin/bash

pip install jupyter-book
jupyter-book clean book
jupyter-book build book
cp -r /book/_build/html mosekbook


