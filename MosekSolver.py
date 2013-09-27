from mosek.fusion import *

def __QCone__(M,expr1,expr2):
    M.constraint(Expr.vstack(expr1,expr2), 
                 Domain.inQCone())

def __rotQCone__(M,expr1,expr2,expr3):
    M.constraint(Expr.vstack(expr1,expr2,expr3), 
                 Domain.inRotatedQCone())
        
def __unitsum__(M,expr):
    # e'*w = 1
    M.constraint(Expr.sum(expr), 
                 Domain.equalsTo(1.0))
    
def __abs__(M,name,expr):
    t = M.variable(name, int(expr.size()), 
                   Domain.unbounded())
                        
    # (t_i, w_i) \in Q2
    for i in range(0, expr.size()):
        __QCone__(M,t.index(i),expr.index(i))

    return t

def __lsq__(M,name,X,w,y):
    v = M.variable(name, 1, Domain.unbounded())
    
    # (v, 1/2, Xw-y) \in Qr
    __rotQCone__(M,0.5,v,
                 Expr.sub(Expr.mul(
                 DenseMatrix(X),w),y
                 ))
    
    return v

def __minimise__(M, expr):
    M.objective(ObjectiveSense.Minimize, expr)
    M.solve()
                     

def lsqPosFullInv(X, y):
    M = Model('lsqPos')  
    # weight-variables
    w = M.variable('weights', X.shape[1], 
                   Domain.greaterThan(0.0))                      
    # e'*w = 1
    __unitsum__(M,w)     
    # (v, 1/2, Xw-y) \in Qr
    __minimise__(M, __lsq__(M,'residual',X,w,y))
    
    return w.level()


def lsqPosFullInvPenalty(X, y, Gamma, lamb): 
    M = Model('lsqSparse')   
    # weight-variables 
    w = M.variable('weights', X.shape[1], 
                   Domain.greaterThan(0.0)) 
    # e'*w = 1
    __unitsum__(M,w)  
    v = __lsq__(M,'residual',X,w,y)
    t = Expr.sum(__abs__(M, 'abs(weights)', 
                 Expr.mul(DenseMatrix(Gamma),w)))   
    # Minimise v + lambda * t
    __minimise__(M, Expr.add(v, Expr.mul(lamb, t)))
    return w.level() 


def lasso(X, y, lamb):
    M = Model('lasso') 
    # weight-variables 
    w = M.variable('weights', X.shape[1], 
                   Domain.unbounded())    
    v = __lsq__(M,'residual',X,w,y)   
    t = Expr.sum(__abs__(M,'abs(weights)',w))
        
    # Minimise v + lambda * t
    __minimise__(M, Expr.add(v, Expr.mul(lamb, t))) 
    return w.level()     