"""Solver module."""

from __future__ import annotations

from contextlib import AbstractContextManager, contextmanager

import numpy as np
from mosek.fusion import Domain, Expr, Matrix, Model, ObjectiveSense, Variable


@contextmanager
def create_model() -> AbstractContextManager[Model]:
    """Create a Mosek optimization model.

    Yields:
        Model: Configured Mosek model instance

    """
    with Model("mosek") as model:
        yield model


def __sum_weighted(c1, expr1, c2, expr2):
    """Calculate the weighted sum of two expressions.

    Combines two expressions by multiplying each with its respective coefficient
    and then adding them together. The result is returned as a single expression.

    Args:
        c1: Coefficient for the first expression.
        expr1: The first expression to be weighted and summed.
        c2: Coefficient for the second expression.
        expr2: The second expression to be weighted and summed.

    Returns:
        An expression that represents the weighted sum of the two provided expressions.

    """
    return Expr.add(Expr.mul(c1, expr1), Expr.mul(c2, expr2))


def __residual(matrix: np.ndarray, rhs: np.ndarray, expr: Expr) -> Expr:
    """Compute the residual of a given matrix-vector product and a right-hand side (rhs).

    This function calculates the difference between the result of a matrix-vector multiplication
    and the provided rhs, using the given expression. The residual is computed as:
    residual = matrix * expr - rhs.

    Args:
        matrix: The coefficient matrix in the matrix-vector multiplication.
        rhs: The right-hand side vector to be subtracted from the result of
            the matrix-vector product.
        expr: The expression used in the matrix-vector multiplication.

    Returns:
        The residual, computed as a result of subtracting rhs from the matrix-vector
        multiplication of matrix and expr.

    """
    return Expr.sub(__mat_vec_prod(matrix, expr), rhs)


def __quad_cone(model: Model, expr1: Expr, expr2: Expr) -> None:
    """Add a quadratic cone constraint to a given optimization model.

    Args:
        model: The optimization model to which the quadratic cone constraint
            will be added. It should support methods for defining constraints
            and accessing domains.
        expr1: The first expression in the quadratic cone. This represents a
            component of the constraint being defined.
        expr2: The second expression in the quadratic cone. This represents a
            component of the constraint being defined.

    """
    model.constraint(Expr.vstack(expr1, expr2), Domain.inQCone())


def __rotated_quad_cone(model: Model, expr1: Expr, expr2: Expr, expr3: Expr) -> None:
    """Add a rotated quadratic cone constraint to the optimization model.

    Args:
        model: The optimization model to which the rotated quadratic cone constraint
            will be added.
        expr1: The first component of the rotated quadratic cone constraint.
        expr2: The second component of the rotated quadratic cone constraint.
        expr3: The third component of the rotated quadratic cone constraint.

    """
    model.constraint(Expr.vstack(expr1, expr2, expr3), Domain.inRotatedQCone())


def __absolute(model: Model, name: str, expr: Expr) -> Variable:
    """Create an absolute value variable in the given optimization model.

    This function generates a variable that represents the absolute value of another
    expression. The variable is defined as unbounded and linked with the original
    expression through quadratic cone constraints for each element in the
    expression's shape.

    Args:
        model: The mathematical optimization model to which the absolute value
            variable and constraints will be added.
        name: The name of the variable that will represent the absolute value.
        expr: The original expression whose absolute value is being represented.

    Returns:
        A variable representing the absolute value of the given expression.

    """
    t = model.variable(name, expr.getShape(), Domain.unbounded())

    # (t_i, w_i) \in Q2
    for i in range(0, int(expr.getShape())):
        __quad_cone(model, t.index(i), expr.index(i))

    return t


def __l1_norm(model: Model, name: str, expr: Variable) -> Expr:
    """Return given an expression (e.g. a vector) the L1-norm of this vector.

    Returns the L1-norm as an expression.
    It also introduces n (where n is the size of the expression) auxiliary
    variables. Mosek requires a name
    for any variable that is added to a model. The user has to specify
    this name explicitly.
    This requirement may disappear in future version of this API.

    ATTENTION: THIS WORKS ONLY IF expr is a VARIABLE
    """
    return Expr.sum(__absolute(model, name, expr))


def __l2_norm(model: Model, name: str, expr: Expr) -> Variable:
    """Return given an expression (e.g. a vector) the L2-norm of this vector.

    Returns the L2-norm as an expression.
    It also introduces an auxiliary variables. Mosek requires a name
    for any variable that is added to a model. The user has to specify
    this name explicitly.
    This requirement may disappear in future version of this API.
    """
    t = model.variable(name, 1, Domain.unbounded())
    __quad_cone(model, t, expr)
    return t


def __l2_norm_squared(model: Model, name: str, expr: Expr) -> Variable:
    """Return the squared L2-norm of an expression.

    It also introduces auxiliary variables.
    Mosek requires a name
    for any variable that is added to a model. The user has to
    specify this name explicitly.
    This requirement may disappear in future version of this API.
    """
    t = model.variable(name, 1, Domain.unbounded())
    __rotated_quad_cone(model, 0.5, t, expr)
    return t


def __linfty_norm(model: Model, name: str, expr: Expr) -> Variable:
    """Compute the infinity norm (L-infinity norm) of a given vector.

    The L-infinity norm is the maximum absolute value among the elements of the
    input vector.

    This function utilizes an auxiliary variable `t` and enforces the relationship
    between `t` and each element of the input vector `expr` via quadratic cone
    constraints, ensuring that `t` represents the maximum absolute value.

    Args:
        model: Optimization model. Provides the context in which the variable
            and constraints are defined.
        name: Name assigned to the auxiliary variable representing the norm.
        expr: Input vector. Represents the vector whose L-infinity norm is to
            be calculated.

    Returns:
        Auxiliary variable representing the computed L-infinity norm of the
        provided input vector within the specified optimization model.

    """
    t = model.variable(name, 1, Domain.unbounded())

    # (t, w_i) \in Q2
    for i in range(0, expr.size()):
        __quad_cone(model, t, expr.index(i))

    return t


def __mat_vec_prod(matrix: np.ndarray, expr: Expr) -> Expr:
    """Perform a matrix-vector multiplication.

    This function computes the product of a dense matrix and a vector-like
    expression. The operation leverages the multiplication method from
    specific external classes to handle the math involved.

    Args:
        matrix: Dense matrix representation.
        expr: Vector-like expression to multiply with the matrix.

    Returns:
        Expression resulting from the matrix-vector multiplication.

    """
    return Expr.mul(Matrix.dense(matrix), expr)


def __stdev(model: Model, name: str, weights: Expr, covar: np.ndarray) -> Variable:
    """Calculate the standard deviation.

    Do it by performing matrix operations involving a
    Cholesky decomposition, a matrix-vector product, and L2 norm calculation.

    Args:
        model: The model object used in the computation. Typically represents
            the model being evaluated.
        name: The name or identifier for the variable, feature, or parameter
            being processed.
        weights: A vector containing weights or coefficients for the calculation.
            This parameter is used during the matrix-vector product operation.
        covar: The covariance matrix representing variability and relationships
            among variables. This matrix will be subjected to Cholesky decomposition.

    Returns:
        Result of the final L2 norm computation, representing the standard
        deviation for the given inputs.

    """
    a = np.linalg.cholesky(covar)
    return __l2_norm(model, name, __mat_vec_prod(np.transpose(a), weights))


def __variance(model: Model, name: str, weights: Expr, covar: np.ndarray) -> Variable:
    """Compute the variance by using the Cholesky decomposition of the covariance matrix.

    This function involves matrix-vector
    multiplication, Cholesky decomposition of the covariance matrix, and an internal
    helper function to compute the squared L2 norm.

    Args:
        model: Model object, which logically groups required operations or data.
        name: str. Name identifier used to track or log the calculation.
        weights: np.ndarray. Weight vector applied to the transformed covariance matrix.
        covar: np.ndarray. Covariance matrix to be decomposed and used in the operation.

    Returns:
        np.number: Scalar representing the computed variance obtained via the specified
        operations.

    """
    a = np.linalg.cholesky(covar)
    return __l2_norm_squared(model, name, __mat_vec_prod(np.transpose(a), weights))


def lsq_ls(matrix: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    """Solve Min 2-norm (matrix*w - rhs)^2.

    Subject to:
    e'w = 1.
    """
    # define model
    with create_model() as model:
        weights = model.variable("weights", matrix.shape[1], Domain.inRange(-np.infty, +np.infty))

        # e'*w = 1
        model.constraint(Expr.sum(weights), Domain.equalsTo(1.0))

        v = __l2_norm(model, "2-norm(res)", expr=__residual(matrix, rhs, weights))

        # minimization of the residual
        model.objective(ObjectiveSense.Minimize, v)
        # solve the problem
        model.solve()

        return np.array(weights.level())


def lsq_pos(matrix: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    """Solve Min 2-norm (matrix*w - rhs)^2.

    Subject to:
    e'w = 1
    w >= 0.
    """
    # define model
    with create_model() as model:
        # introduce n non-negative weight variables
        weights = model.variable("weights", matrix.shape[1], Domain.inRange(0.0, 1.0))

        # e'*w = 1
        model.constraint(Expr.sum(weights), Domain.equalsTo(1.0))

        v = __l2_norm(model, "2-norm(res)", expr=__residual(matrix, rhs, weights))

        # minimization of the residual
        model.objective(ObjectiveSense.Minimize, v)
        # solve the problem
        model.solve()

        return np.array(weights.level())


def lsq_pos_l1_penalty(
    matrix: np.ndarray, rhs: np.ndarray, cost_multiplier: np.ndarray, weights_0: np.ndarray
) -> np.ndarray:
    """Solve Min 2-norm (matrix*w - rhs)** + 1-norm(cost_multiplier*(w-w0)).

    Subject to:
    e'w = 1
    w >= 0.
    """
    # define model
    with Model("lsqSparse") as model:
        # introduce n non-negative weight variables
        weights = model.variable("weights", matrix.shape[1], Domain.inRange(0.0, +np.infty))

        # e'*w = 1
        model.constraint(Expr.sum(weights), Domain.equalsTo(1.0))

        # sum of squared residuals
        v = __l2_norm_squared(model, "2-norm(res)**", __residual(matrix, rhs, weights))

        # \Gamma*(w - w0), p is an expression
        p = Expr.mulElm(cost_multiplier, Expr.sub(weights, weights_0))

        cost = model.variable("cost", matrix.shape[1], Domain.unbounded())
        model.constraint(Expr.sub(cost, p), Domain.equalsTo(0.0))

        t = __l1_norm(model, "abs(weights)", cost)

        # Minimise v + t
        model.objective(ObjectiveSense.Minimize, __sum_weighted(1.0, v, 1.0, t))
        # solve the problem
        model.solve()

        return np.array(weights.level())


def lasso(matrix: np.ndarray, rhs: np.ndarray, lamb: float) -> np.ndarray:
    """Min 2-norm (matrix*w - rhs)^2 + lamb * 1-norm(w).

    Solves the LASSO regression problem with L1 regularization.
    """
    # define model
    with Model("lasso") as model:
        weights = model.variable("weights", matrix.shape[1])  # , Domain.inRange(-np.infty, +np.infty))
        # introduce variables and constraints

        v = __l2_norm_squared(model, "2-norm(res)**", __residual(matrix, rhs, weights))
        t = __l1_norm(model, "1-norm(w)", weights)

        model.objective(ObjectiveSense.Minimize, __sum_weighted(c1=1.0, expr1=v, c2=lamb, expr2=t))
        # solve the problem
        model.solve()

        return np.array(weights.level())


def markowitz_riskobjective(exp_ret: np.ndarray, covariance_mat: np.ndarray, bound: float) -> np.ndarray:
    """Compute the optimal weight allocation using the Markowitz model, subject to a risk bound.

    The function utilizes quadratic programming to maximize the expected return
    of a portfolio given an expected return vector and covariance matrix, while
    restricting the portfolio's standard deviation up to the specified bound.

    Args:
        exp_ret (np.ndarray): Expected returns for each asset in the portfolio.
        covariance_mat (np.ndarray): Covariance matrix representing the
            variances and covariances between the assets.
        bound (float): Upper bound on the portfolio's standard deviation
            (risk constraint).

    Returns:
        np.ndarray: Optimal allocation weights for each asset in the portfolio
            that maximize the expected return subject to the given risk bound.

    """
    # define model
    with Model("mean var") as model:
        # set of n weights (unconstrained)
        weights = model.variable("weights", len(exp_ret), Domain.inRange(0.0, 1.0))

        # standard deviation induced by covariance matrix
        stdev = __stdev(model, "std", weights, covariance_mat)

        # impose a bound on this standard deviation
        # mBound.upper(model, stdev, bound)
        model.constraint(stdev, Domain.lessThan(bound))

        # mModel.maximise(model=model, expr=Expr.dot(exp_ret, weights))
        model.objective(ObjectiveSense.Maximize, Expr.dot(exp_ret, weights))
        # solve the problem
        model.solve()

        return np.array(weights.level())


def markowitz(exp_ret: np.ndarray, covariance_mat: np.ndarray, aversion: float) -> np.ndarray:
    """Optimize a portfolio using the Markowitz mean-variance model.

    The function maximizes the
    expected return of the portfolio while penalizing risk represented by portfolio variance.

    Args:
        exp_ret (np.ndarray): A 1D array representing the expected returns of individual assets.
        covariance_mat (np.ndarray): A 2D array representing the covariance matrix of asset returns.
            Each element [i, j] corresponds to the covariance between asset i and asset j.
        aversion (float): A risk aversion coefficient. Higher values reflect greater emphasis on risk
            minimization versus return maximization.

    Returns:
        np.ndarray: An array of portfolio weights for each asset that optimizes the mean-variance
            equilibrium.

    """
    # define model
    with Model("mean var") as model:
        # set of n weights (unconstrained)
        weights = model.variable("weights", len(exp_ret), Domain.inRange(-np.infty, +np.infty))

        model.constraint(Expr.sum(weights), Domain.equalsTo(1.0))

        # standard deviation induced by covariance matrix
        var = __variance(model, "var", weights, covariance_mat)

        model.objective(
            ObjectiveSense.Maximize,
            Expr.sub(Expr.dot(exp_ret, weights), Expr.mul(aversion, var)),
        )
        model.solve()
        return np.array(weights.level())


def minimum_variance(matrix: np.ndarray) -> np.ndarray:
    """Compute the weights for a minimum variance portfolio based on a matrix of returns.

    Each column in the matrix represents a series of asset returns.
    This function solves for portfolio weights that minimize the variance of the
    portfolio, under the constraints that all weights are non-negative and sum
    to 1, representing the left-most point on the efficiency frontier in the
    classic Markowitz portfolio theory.

    Args:
        matrix: A numpy 2D array where each column represents returns of an
            asset. The matrix dimensions are (n_periods, n_assets).

    Returns:
        numpy.ndarray: A 1D array containing the weights for the minimum
            variance portfolio.

    Raises:
        ValueError: Raised if the matrix is not a numpy 2D array or if its shape
            is invalid for the operation (e.g., less than 2 assets or periods).

    """
    # Given the matrix of returns a (each column is a series of returns) this method
    # computes the weights for a minimum variance portfolio, e.g.

    # min   2-Norm[a*w]^2
    # s.t.
    #         w >= 0
    #     sum[w] = 1

    # This is the left-most point on the efficiency frontier in the classic
    # Markowitz theory

    # build the model
    with Model("Minimum Variance") as model:
        # introduce the weight variable

        weights = model.variable("weights", matrix.shape[1], Domain.inRange(0.0, 1.0))
        # sum of weights has to be 1
        model.constraint(Expr.sum(weights), Domain.equalsTo(1.0))
        # returns
        r = Expr.mul(Matrix.dense(matrix), weights)
        # compute l2_norm squared of those returns
        # minimize this l2_norm
        model.objective(ObjectiveSense.Minimize, __l2_norm_squared(model, "2-norm^2(r)", expr=r))
        # solve the problem
        model.solve()
        # return the series of weights
        return np.array(weights.level())
