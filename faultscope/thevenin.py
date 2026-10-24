import numpy as np

def component(y,k):
    seen=set();queue=[k]
    while queue:
        i=queue.pop()
        if i in seen:continue
        seen.add(i);queue.extend(j for j in range(len(y)) if j!=i and (abs(y[i,j])>1e-14 or abs(y[j,i])>1e-14) and j not in seen)
    return sorted(seen)

def driving_point(y,k,allow_floating=False):
    ids=component(y,k);local=y[np.ix_(ids,ids)];target=ids.index(k);rhs=np.zeros(len(ids),complex);rhs[target]=1
    if np.linalg.matrix_rank(local,tol=1e-10)==len(ids):
        column=np.linalg.solve(local,rhs);full=np.zeros(len(y),complex);full[ids]=column
        return {'z':complex(column[target]),'column':full,'floating':False,'ids':ids}
    if not allow_floating:raise ValueError('Fault island has no adequate sequence source reference')
    _,_,vh=np.linalg.svd(local);mode=vh[-1].conjugate()
    if abs(mode[target])<1e-10 or np.linalg.norm(local@mode)>1e-7:raise ValueError('Unsupported singular zero-sequence component')
    full=np.zeros(len(y),complex);full[ids]=mode/mode[target]
    return {'z':None,'column':None,'floating':True,'mode':full,'ids':ids}
