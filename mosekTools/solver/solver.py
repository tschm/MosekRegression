from mosek.fusion import *
import mosekTools.util.util as util


# min 2-norm (Xw - y)**
#        s.t. e'w = 1
#               w >= 0    
def lsqPosFullInv(X, y):
    # define model
    M = Model('lsqPos')
    # weight-variables
    w = M.variable('w', X.shape[1], Domain.greaterThan(0.0))

    # e'*w = 1
    M.constraint(Expr.sum(w), Domain.equalsTo(1.0))

    # sum of squared residuals
    v = util.lsq(M, 'ssqr', X, w, y)

    util.minimise(M, v)
    return w.level()

# min 2-norm (Xw - y)** + 1-norm(Gamma*(w-w0))
#        s.t. e'w = 1
#               w >= 0  
def lsqPosFullInvPenalty(X, y, Gamma, lamb, w0):
# define model
    M = Model('lsqSparse')
    # introduce variable and constraints
    w = M.variable('w', X.shape[1], Domain.greaterThan(0.0))

    # e'*w = 1
    M.constraint(Expr.sum(w), Domain.equalsTo(1.0))

    # sum of squared residuals
    v = util.lsq(M, 'ssqr', X, w, y)

    # \Gamma*(w - w0), p is an expression
    p = Expr.mul(DenseMatrix(Gamma), Expr.sub(w, w0))
    t = Expr.sum(util.abs(M, 'abs(weights)', p))

    # Minimise v + lambda * t
    util.minimise(M, Expr.add(v, Expr.mul(lamb, t)))
    return w.level()

# min 2-norm (Xw -y)** + 1-norm(w)
def lasso(X, y, lamb):
    # define model	
    M = Model('lasso')
    # introduce variables and constraints 
    w = M.variable('w', X.shape[1], Domain.unbounded())
    v = util.lsq(M, 'ssqr', X, w, y)
    t = Expr.sum(util.abs(M, 'abs(weights)', w))

    # Minimise v + lambda * t
    util.minimise(M, Expr.add(v, Expr.mul(lamb, t)))

    return w.level()     
