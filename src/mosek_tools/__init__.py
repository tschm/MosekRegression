"""Mosek optimization tools for portfolio optimization and regression problems.

This package provides a collection of functions for solving optimization problems
using the Mosek optimization library, including least squares, LASSO regression,
and Markowitz portfolio optimization.
"""

import importlib.metadata

# Get the version of the package from metadata
__version__ = importlib.metadata.version("mosektools")
