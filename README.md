# MosekTools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/tschm/MosekRegression/actions/workflows/ci.yml/badge.svg)](https://github.com/tschm/MosekRegression/actions/workflows/ci.yml)
[![CodeQL](https://github.com/tschm/MosekRegression/actions/workflows/codeql.yml/badge.svg)](https://github.com/tschm/MosekRegression/actions/workflows/codeql.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/tschm/MosekRegression/badge)](https://www.codefactor.io/repository/github/tschm/MosekRegression)
[![Renovate enabled](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://github.com/renovatebot/renovate)

**MosekTools** is a Python package providing high-level optimization tools for regression and portfolio optimization problems, built on top of the powerful [MOSEK](https://www.mosek.com/) optimization solver.

## 🎯 Features

- **Regression Methods**
  - Least Squares (unconstrained and positivity-constrained)
  - LASSO Regression (L1-regularized)
  - L1-penalized Least Squares
  
- **Portfolio Optimization**
  - Markowitz Mean-Variance Optimization
  - Minimum Variance Portfolio
  - Risk-Objective Portfolio Optimization
  
- **Built on MOSEK Fusion API**
  - Efficient conic optimization
  - Production-grade solver performance
  - Support for large-scale problems

## 📚 Documentation

Full documentation and interactive examples are available at [https://tschm.github.io/MosekRegression/book](https://tschm.github.io/MosekRegression/book)

## 🚀 Quick Start

### Installation

```bash
pip install mosektools
```

**Important**: You need a valid [MOSEK license](https://www.mosek.com/products/academic-licenses/) to use this package. Academic licenses are available free of charge.

**Note**: The package is installed as `mosektools` (no underscore), but imported as `mosek_tools` (with underscore).

### Basic Usage

#### Least Squares Regression

```python
import numpy as np
from mosek_tools.solver import lsq_ls

# Generate sample data
A = np.random.randn(100, 10)
b = np.random.randn(100)

# Solve unconstrained least squares: min ||Ax - b||_2^2
x = lsq_ls(A, b)
```

#### LASSO Regression

```python
from mosek_tools.solver import lasso

# Solve LASSO: min ||Ax - b||_2^2 + lambda * ||x||_1
lambda_param = 0.1
x = lasso(A, b, lambda_param)
```

#### Portfolio Optimization

```python
from mosek_tools.solver import markowitz
import numpy as np

# Expected returns and covariance matrix
expected_returns = np.array([0.12, 0.10, 0.07, 0.03])
covariance = np.array([
    [0.04, 0.01, 0.00, 0.00],
    [0.01, 0.02, 0.00, 0.00],
    [0.00, 0.00, 0.01, 0.00],
    [0.00, 0.00, 0.00, 0.005]
])

# Solve Markowitz problem with risk aversion parameter
risk_aversion = 2.0
weights = markowitz(expected_returns, covariance, risk_aversion)
```

## 📖 API Reference

### Regression Functions

- `lsq_ls(matrix, rhs)` - Unconstrained least squares
- `lsq_pos(matrix, rhs)` - Least squares with positivity constraints
- `lsq_pos_l1_penalty(matrix, rhs, gamma, lamb)` - L1-penalized least squares
- `lasso(matrix, rhs, lamb)` - LASSO regression

### Portfolio Optimization Functions

- `markowitz(exp_ret, covariance_mat, aversion)` - Mean-variance optimization
- `markowitz_riskobjective(exp_ret, covariance_mat, bound)` - Risk-objective formulation

### Utility Functions

- `create_model()` - Create a MOSEK optimization model context manager

## 🔧 Requirements

- Python >= 3.11
- NumPy >= 2.3.4
- MOSEK >= 11.0.29 (with valid license)

## 💡 Motivation

This package was created to support the experiments described in the paper:
> **"A Least Squares Approach to Direct Data-Driven Control"**  
> Schmelzer, Hauser, Dahl, and Andersen  
> [arXiv:1310.3397](http://arxiv.org/abs/1310.3397)

The tools have since been extended to support a broader range of optimization problems in regression and portfolio management.

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Running tests and linting
- Submitting pull requests
- Code style guidelines

To get started with development:

```bash
git clone https://github.com/tschm/MosekRegression.git
cd MosekRegression
make install
make test
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Note**: While this package is MIT licensed, MOSEK itself requires a separate license. Academic licenses are available free of charge from [MOSEK](https://www.mosek.com/products/academic-licenses/).

## 🔗 Links

- **Documentation**: [https://tschm.github.io/MosekRegression/book](https://tschm.github.io/MosekRegression/book)
- **Repository**: [https://github.com/tschm/MosekRegression](https://github.com/tschm/MosekRegression)
- **Issues**: [https://github.com/tschm/MosekRegression/issues](https://github.com/tschm/MosekRegression/issues)
- **MOSEK**: [https://www.mosek.com/](https://www.mosek.com/)

## 🙏 Acknowledgments

Built on the shoulders of [MOSEK](https://www.mosek.com/) - a powerful commercial-grade optimization solver for large-scale mathematical optimization problems.
