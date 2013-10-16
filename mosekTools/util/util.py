from mosek.fusion import *


def build_model(name):
    return Model(name)


def quad_cone(model, expr1, expr2):
    model.constraint(Expr.vstack(expr1, expr2),
                     Domain.inQCone())


def rotated_quad_cone(model, expr1, expr2, expr3):
    model.constraint(Expr.vstack(expr1, expr2, expr3),
                     Domain.inRotatedQCone())


def absolute(model, name, expr):
    t = model.variable(name, int(expr.size()),
                       Domain.unbounded())

    # (t_i, w_i) \in Q2
    for i in range(0, int(expr.size())):
        quad_cone(model, t.index(i), expr.index(i))

    return t


def l1_norm(model, name, expr):
    """
    Given an expression (e.g. a vector) this returns the L1-norm of this vector as an expression.
    It also introduces n (where n is the size of the expression) auxiliary variables. Mosek requires a name
    for any variable that is added to a model. The user has to specify this name explicitly.
    This requirement may disappear in future version of this API.
    """
    v = Expr.sum(absolute(model, name, expr))
    return v


def residual(matrix, rhs, w):
    """
    Introduce the residual matrix*w - rhs
    """
    return Expr.sub(Expr.mul(DenseMatrix(matrix), w), rhs)


def l2_norm(model, name, expr):
    """
    Given an expression (e.g. a vector) this returns the L2-norm of this vector as an expression.
    It also introduces an auxiliary variables. Mosek requires a name
    for any variable that is added to a model. The user has to specify this name explicitly.
    This requirement may disappear in future version of this API.
    """
    t = model.variable(name, 1, Domain.unbounded())
    quad_cone(model, t, expr)
    return t


def l2_norm_squared(model, name, expr):
    """
    Given an expression (e.g. a vector) this returns the squared L2-norm of this vector as an expression.
    It also introduces an auxiliary variables. Mosek requires a name
    for any variable that is added to a model. The user has to specify this name explicitly.
    This requirement may disappear in future version of this API.
    """
    t = model.variable(name, 1, Domain.unbounded())
    rotated_quad_cone(model, 0.5, t, expr)
    return t


def linfty_norm(model, name, expr):
    t = model.variable(name, 1, Domain.unbounded())

    # (t, w_i) \in Q2
    for i in range(0, int(expr.size())):
        quad_cone(model, t, expr.index(i))

    return t


def sum_weighted(c1, expr1, c2, expr2):
    return Expr.add(Expr.mul(c1, expr1), Expr.mul(c2, expr2))


def minimise(model, expr):
    model.objective(ObjectiveSense.Minimize, expr)
    model.solve()


def maximise(model, expr):
    model.objective(ObjectiveSense.Maximize, expr)
    model.solve()
