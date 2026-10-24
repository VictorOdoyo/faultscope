import numpy as np
from .thevenin import component
from .sequence_networks import source_admittance

def prefault(network,y,k,profile=None):
    ids=component(y,k);index={b['id']:i for i,b in enumerate(network['buses'])};v=np.zeros(len(index),complex)
    if profile is not None:
        if not isinstance(profile,dict):raise ValueError('Prefault profile must map bus IDs to [magnitude pu, angle degrees]')
        for i in ids:
            key=network['buses'][i]['id']
            if key not in profile or len(profile[key])!=2:raise ValueError('Missing prefault phasor for '+key)
            mag,angle=profile[key]
            from .model import number
            v[i]=number(mag,'prefault magnitude',.001)*np.exp(1j*np.deg2rad(number(angle,'prefault angle')))
    else:
        rhs=np.zeros(len(index),complex)
        for s in network['sources']:
            if s['status']:rhs[index[s['bus']]]+=source_admittance(s,1)*s['emf_pu']*np.exp(1j*np.deg2rad(s['angle_deg']))
        if not any(s['status'] and index[s['bus']] in ids for s in network['sources']):raise ValueError('Fault lies on an unsourced island')
        try:v[ids]=np.linalg.solve(y[np.ix_(ids,ids)],rhs[ids])
        except np.linalg.LinAlgError as exc:raise ValueError('Unsolvable prefault island') from exc
    return v,ids

def from_gridflow(result):
    if not isinstance(result,dict) or not result.get('converged'):raise ValueError('GridFlow import requires a converged result')
    return {b['id']:[b['vm_pu'],b['va_deg']] for b in result['buses']}
