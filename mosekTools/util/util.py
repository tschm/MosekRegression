from mosek.fusion import *


def QCone(model, expr1, expr2):
    model.constraint(Expr.vstack(expr1, expr2),
                     Domain.inQCone())


def rotQCone(model, expr1, expr2, expr3):
    model.constraint(Expr.vstack(expr1, expr2, expr3),
                     Domain.inRotatedQCone())


def abs(model, name, expr):
    t = model.variable(name, int(expr.size()),
                       Domain.unbounded())

    # (t_i, w_i) \in Q2
    for i in range(0, int(expr.size())):
        QCone(model, t.index(i), expr.index(i))

    return t


# squared residual, e.g. v = (2-norm [X*w - y])**
def lsq(model, name, X, w, y):
    v = model.variable(name, 1, Domain.unbounded())

    # (1/2, v, Xw-y) \in Qr
    res = Expr.sub(Expr.mul(DenseMatrix(X), w), y)
    rotQCone(model, 0.5, v, res)

    return v


def minimise(model, expr):
    model.objective(ObjectiveSense.Minimize, expr)
    model.solve()


def maximise(model, expr):
    model.objective(ObjectiveSense.Maximize, expr)
    model.solve()
