import numpy as np
from .sequence_networks import stamp,source_admittance
from .phasors import phases,record,base_current

def contributions(n,voltages,delta,studied):
    index={b['id']:i for i,b in enumerate(n['buses'])};buses={b['id']:b for b in n['buses']};branches=[];sources=[]
    for b in n['branches']:
        if not b['status'] or index[b['from']] not in studied or index[b['to']] not in studied:continue
        i,j=index[b['from']],index[b['to']];end={};inc={}
        for label,values,target in [('total',voltages,end),('increment',delta,inc)]:
            first=[];second=[]
            for seq in [0,1,2]:
                ff,ft,tf,tt=stamp(b,seq);first.append(ff*values[seq][i]+ft*values[seq][j]);second.append(tf*values[seq][i]+tt*values[seq][j])
            for terminal,values_at in [('from',first),('to',second)]:
                amps=base_current(n['base_mva'],buses[b[terminal]]['base_kv']);target[terminal]=[record(x*amps) for x in phases(values_at)]
        branches.append({'id':b['id'],'from_bus':b['from'],'to_bus':b['to'],'from_phase_currents_a':end['from'],'to_phase_currents_a':end['to'],'from_increment_a':inc['from'],'to_increment_a':inc['to']})
    for s in n['sources']:
        i=index[s['bus']]
        if not s['status'] or i not in studied:continue
        current=[-source_admittance(s,seq)*delta[seq][i] for seq in [0,1,2]];amps=base_current(n['base_mva'],buses[s['bus']]['base_kv'])
        sources.append({'id':s['id'],'bus':s['bus'],'phase_increment_a':[record(x*amps) for x in phases(current)],'sequence_increment_pu':[record(x) for x in current]})
    return branches,sources
