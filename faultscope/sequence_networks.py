import numpy as np
from .model import impedance

def stamp(branch,sequence):
    key='z'+str(sequence);zero=(0j,0j,0j,0j)
    if sequence==0:
        if branch['z0'] is None:return zero
        z=impedance(branch['z0'],'z0')
        if branch['kind']=='transformer':
            first,second=branch['from_winding'],branch['to_winding']
            zf=3*impedance(branch['from_neutral_z'],'neutral',True);zt=3*impedance(branch['to_neutral_z'],'neutral',True)
            if first=='Yg' and second=='D':return 1/(z+zf)/branch['tap']**2,0j,0j,0j
            if first=='D' and second=='Yg':return 0j,0j,0j,1/(z+zt)
            if first!='Yg' or second!='Yg':return zero
            z+=zf+zt
        tap=complex(branch['tap'])
    else:
        z=impedance(branch[key],key);angle=branch['shift_deg']*(1 if sequence==1 else -1);tap=branch['tap']*np.exp(1j*np.deg2rad(angle))
    y=1/z
    return y/abs(tap)**2,-y/tap.conjugate(),-y/tap,y

def source_admittance(source,sequence):
    if sequence==0:
        if not source['grounded'] or source['z0'] is None:return 0j
        return 1/(impedance(source['z0'],'z0')+3*impedance(source['neutral_z'],'neutral',True))
    return 1/impedance(source['z'+str(sequence)],'source impedance')

def build(network,sequence):
    index={b['id']:i for i,b in enumerate(network['buses'])};y=np.zeros((len(index),len(index)),complex)
    for b in network['branches']:
        if not b['status']:continue
        i,j=index[b['from']],index[b['to']];ff,ft,tf,tt=stamp(b,sequence);y[i,i]+=ff;y[i,j]+=ft;y[j,i]+=tf;y[j,j]+=tt
    for s in network['sources']:
        if s['status']:y[index[s['bus']],index[s['bus']]]+=source_admittance(s,sequence)
    if not np.all(np.isfinite(y)):raise ValueError('Sequence admittance exceeds numerical range')
    return y
