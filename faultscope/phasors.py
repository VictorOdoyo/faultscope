import numpy as np
A=np.exp(2j*np.pi/3)
T=np.array([[1,1,1],[1,A*A,A],[1,A,A*A]],complex)
def phases(sequence):return T@np.asarray(sequence,complex)
def sequences(phase):return np.linalg.solve(T,np.asarray(phase,complex))
def record(value):return {'real':float(value.real),'imag':float(value.imag),'magnitude':float(abs(value)),'angle_deg':float(np.angle(value,deg=True))}
def base_current(base_mva,base_kv):return base_mva*1000/(np.sqrt(3)*base_kv)
