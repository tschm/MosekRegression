from mosek.fusion import *
import sys


def lsqPosFull(X, y):
    X = DenseMatrix(X)
    M = Model('lsqPos')
    # variables
    w = M.variable('w', X.numColumns(), 
                        Domain.greaterThan(0.0))
    v = M.variable('v', 1, Domain.unbounded())

    # e'*w = 1
    M.constraint(Expr.sum(w), Domain.equalsTo(1.0))

    # (v, X*w-y) \in Qn
    M.constraint(Expr.vstack(v.asExpr(),
                 Expr.sub(Expr.mul(X, w), y)),
                 Domain.inQCone())

    # Minimize v (norm of X*w - y)
    M.objective(ObjectiveSense.Minimize, v)
    # Solve the problem
    M.solve()
    return w.level()


def lsqSparse(X, y, Gamma, lamb):
    X = DenseMatrix(X) 
    Gamma = DenseMatrix(Gamma)     
    M = Model('lsqSparse') 
    # variables 
    w = M.variable('w', X.numColumns(), 
                        Domain.greaterThan(0.0)) 
    v = M.variable('v', 1, Domain.unbounded()) 
    t = M.variable('t', X.numColumns(), 
                        Domain.unbounded())
    
    # e'*w = 1 
    M.constraint(Expr.sum(w), Domain.equalsTo(1.0)) 
    # (v, 1/2, Xw-y) \in Qr
    M.constraint(Expr.vstack(0.5,
                             v, 
                             Expr.sub(Expr.mul(X,w),y) ), 
                             Domain.inRotatedQCone())
    # (t_i, [Gamma*(w-w0)]_i) \in Q2
    M.constraint(Expr.hstack(t.asExpr(), 
                             Expr.mul(Gamma,w)), 
                             Domain.inQCone())
    
    # Minimize v + lambda * sum(t)
    M.objective(ObjectiveSense.Minimize, 
                Expr.add(v, Expr.mul(lamb, Expr.sum(t)))) 
    # Solve the problem 
    M.solve() 
    return w.level() 


def lasso2(X, y, lamb):
    X = DenseMatrix(X) 
    M = Model('lasso') 
    # variables 
    w = M.variable('w', X.numColumns(), 
                        Domain.unbounded()) 
    v = M.variable('v', 1, 
                        Domain.unbounded()) 
    
    t = M.variable('t', X.numColumns(), 
                        Domain.unbounded())
                        
    # (v, 1/2, Xw-y) \in Qr
    M.constraint(Expr.vstack(0.5,
                             v, 
                             Expr.sub(Expr.mul(X,w),y) ), 
                             Domain.inRotatedQCone())
    # (t_i, w_i) \in Q2
    M.constraint(Expr.hstack(t.asExpr(), 
                             w.asExpr(), 
                             Domain.inQCone()))
    
    # Minimize v + lambda * sum(t)
    M.objective(ObjectiveSense.Minimize, 
                Expr.add(v, Expr.mul(lamb, Expr.sum(t)))) 
    # Solve the problem 
    M.solve() 
    return w.level() 
