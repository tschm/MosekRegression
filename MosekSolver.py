from mosek.fusion import *

def __unitsum__(M,w):
    # e'*w = 1
    M.constraint(Expr.sum(w), Domain.equalsTo(1.0))
    
def __abs__(M,w):
    t = M.variable('t', int(w.size()), Domain.unbounded())
                        
    # (t_i, w_i) \in Q2
    for i in range(0, w.size()):
        M.constraint(Expr.vstack(t.index(i),w.index(i)), 
                                 Domain.inQCone())

    return t

def __lsq__(M,X,w,y):
    v = M.variable('v', 1, Domain.unbounded())
    
    # (v, 1/2, Xw-y) \in Qr
    M.constraint(Expr.vstack(0.5,
                             v, 
                             Expr.sub(Expr.mul(X,w),y) ), 
                             Domain.inRotatedQCone())
    
    return v

def __minimise__(M, expr):
    M.objective(ObjectiveSense.Minimize, expr)
    M.solve()
    
                
def lsqPosFullInv(X, y):
    X = DenseMatrix(X)
    M = Model('lsqPos')
    
    # weight-variables
    w = M.variable('w', X.numColumns(), Domain.greaterThan(0.0))
                        
    # e'*w = 1
    __unitsum__(M,w)
       
    # (v, 1/2, Xw-y) \in Qr
    __minimise__(M, __lsq__(M,X,w,y))
    
    return w.level()


def lsqPosFullInvPenalty(X, y, Gamma, lamb):
    X = DenseMatrix(X) 
    Gamma = DenseMatrix(Gamma)     
    M = Model('lsqSparse') 
    # variables 
    w = M.variable('w', X.numColumns(), 
                        Domain.greaterThan(0.0)) 

    __unitsum__(M,w)
    
    v = __lsq__(M,X,w,y)
    t = Expr.sum(__abs__(M, Expr.mul(Gamma,w)))
    
    # Minimize v + lambda * t
    __minimise__(M, Expr.add(v, Expr.mul(lamb, t)))
    return w.level() 


def lasso(X, y, lamb):
    X = DenseMatrix(X) 
    M = Model('lasso') 
    # variables 
    w = M.variable('w', X.numColumns(), Domain.unbounded()) 
    
    v = __lsq__(M,X,w,y)   
    t = Expr.sum(__abs__(M, w))
        
    # Minimize v + lambda*t
    __minimise__(M, Expr.add(v, Expr.mul(lamb, t))) 
    return w.level() 
