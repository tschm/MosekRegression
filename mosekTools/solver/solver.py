from mosek.fusion import *
import mosekTools.util.util as Util


# min 2-norm (Xw - y)**
#        s.t. e'w = 1
#               w >= 0    
def lsqPosFullInv(X, y):
    # define model
    m = Model('lsqPos')
    # weight-variables
    w = m.variable('w', X.shape[1], Domain.greaterThan(0.0))

    # e'*w = 1
    m.constraint(Expr.sum(w), Domain.equalsTo(1.0))

    # sum of squared residuals
    v = Util.lsq(m, 'ssqr', X, w, y)

    Util.minimise(m, v)
    return w.level()

# min 2-norm (Xw - y)** + 1-norm(Gamma*(w-w0))
#        s.t. e'w = 1
#               w >= 0  
def lsqPosFullInvPenalty(X, y, Gamma, lamb, w0):
# define model
    m = Model('lsqSparse')
    # introduce variable and constraints
    w = m.variable('w', X.shape[1], Domain.greaterThan(0.0))

    # e'*w = 1
    m.constraint(Expr.sum(w), Domain.equalsTo(1.0))

    # sum of squared residuals
    v = Util.lsq(m, 'ssqr', X, w, y)

    # \Gamma*(w - w0), p is an expression
    p = Expr.mul(DenseMatrix(Gamma), Expr.sub(w, w0))
    t = Expr.sum(Util.abs(m, 'abs(weights)', p))

    # Minimise v + lambda * t
    Util.minimise(m, Expr.add(v, Expr.mul(lamb, t)))
    return w.level()


# min 2-norm (Xw -y)** + 1-norm(w)
def lasso(X, y, lamb):
    # define model	
    m = Model('lasso')
    # introduce variables and constraints 
    w = m.variable('w', X.shape[1], Domain.unbounded())
    v = Util.lsq(m, 'ssqr', X, w, y)
    t = Expr.sum(Util.abs(m, 'abs(weights)', w))

    # Minimise v + lambda * t
    Util.minimise(m, Expr.add(v, Expr.mul(lamb, t)))

    return w.level()     
