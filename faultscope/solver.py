import numpy as np
from .model import validate,impedance,number
from .sequence_networks import build
from .thevenin import driving_point
from .prefault import prefault
from .boundaries import sequence_fault,EQUATIONS
from .phasors import phases,record,base_current
from .contributions import contributions

def analyze(data,bus=None,fault_type='3ph',fault_z=None,prefault_profile=None,voltage_factor=1):
    n=validate(data);bus=bus or n['buses'][-1]['id'];index={b['id']:i for i,b in enumerate(n['buses'])}
    if bus not in index:raise ValueError('Unknown fault bus')
    k=index[bus];zf=impedance(fault_z if fault_z is not None else [0,0],'fault_z',True);factor=number(voltage_factor,'voltage_factor',.001)
    ys=[build(n,seq) for seq in [0,1,2]];pre,studied=prefault(n,ys[1],k,prefault_profile);pre*=factor
    equivalents=[driving_point(ys[seq],k,allow_floating=(seq==0)) for seq in [0,1,2]]
    z0,z1,z2=[item['z'] for item in equivalents];currents=sequence_fault(fault_type,pre[k],z1,z2,z0,zf)
    delta=[np.zeros(len(index),complex) for _ in range(3)]
    for seq in [0,1,2]:
        if equivalents[seq]['column'] is not None:delta[seq]=-equivalents[seq]['column']*currents[seq]
    voltages=[delta[0].copy(),pre+delta[1],delta[2].copy()]
    if equivalents[0]['floating']:
        required=-(voltages[1][k]+voltages[2][k]) if fault_type=='slg' else voltages[1][k] if fault_type=='dlg' else 0j
        delta[0]=equivalents[0]['mode']*required;voltages[0]=delta[0].copy()
    buses=[]
    for i in studied:
        b=n['buses'][i];voltage_base=b['base_kv']*1000/np.sqrt(3)
        buses.append({'id':b['id'],'base_kv':b['base_kv'],'sequence_voltage_pu':[record(voltages[seq][i]) for seq in [0,1,2]],'phase_voltage_v':[record(x*voltage_base) for x in phases([voltages[seq][i] for seq in [0,1,2]])]})
    branches,sources=contributions(n,voltages,delta,studied);amps=base_current(n['base_mva'],n['buses'][k]['base_kv']);phase=phases(currents)*amps
    result={'application':'faultscope','schema_version':1,'version':'1.0.0','fault':{'bus':bus,'type':fault_type,'z_pu':record(zf),'prefault_pu':record(pre[k]),'voltage_factor':factor,'sequence_currents_pu':[record(x) for x in currents],'phase_currents_a':[record(x) for x in phase],'max_phase_rms_a':float(max(abs(phase))),'residual_a':record(sum(phase))},'thevenin':{'z0_pu':record(z0) if z0 is not None else None,'z1_pu':record(z1),'z2_pu':record(z2),'zero_sequence_floating':equivalents[0]['floating']},'buses':buses,'branches':branches,'sources':sources,'studied_bus_ids':[n['buses'][i]['id'] for i in studied],'excluded_bus_ids':[b['id'] for i,b in enumerate(n['buses']) if i not in studied],'equations':EQUATIONS[fault_type],'assumptions':['Classical linear symmetrical-component RMS fault model; no current decrement, arc dynamics, inverter control or line shunt capacitance. Sources use supplied fault-period impedances.']}
    return result
