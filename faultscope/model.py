from copy import deepcopy
import math

def number(value,name,minimum=None):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):raise ValueError(name+' must be a finite number')
    if minimum is not None and value<minimum:raise ValueError(name+' is below its minimum')
    return float(value)
def impedance(value,name,allow_zero=False):
    if not isinstance(value,list) or len(value)!=2:raise ValueError(name+' must be [resistance, reactance] in pu')
    z=complex(number(value[0],name+' R',0),number(value[1],name+' X',0))
    if not allow_zero and abs(z)==0:raise ValueError(name+' must not be zero')
    return z
def validate(data):
    if not isinstance(data,dict):raise ValueError('Network must be an object')
    n=deepcopy(data);n.setdefault('schema_version',1)
    if n['schema_version']!=1:raise ValueError('Unsupported schema version')
    n['base_mva']=number(n.get('base_mva',100),'base_mva',.001)
    for key in ['buses','branches','sources','equipment']:n.setdefault(key,[])
    if not 1<=len(n['buses'])<=150 or len(n['branches'])>600:raise ValueError('Require 1..150 buses and at most 600 branches')
    ids=set()
    for b in n['buses']:
        if not isinstance(b.get('id'),str) or not b['id'] or b['id'] in ids:raise ValueError('Bus IDs must be unique strings')
        ids.add(b['id']);b['base_kv']=number(b.get('base_kv',11),'base_kv',.001)
    for kind in ['branches','sources','equipment']:
        used=set()
        for item in n[kind]:
            if not isinstance(item.get('id'),str) or not item['id'] or item['id'] in used:raise ValueError(kind+' IDs must be unique strings')
            used.add(item['id']);item.setdefault('status',True)
            if not isinstance(item['status'],bool):raise ValueError('Equipment status must be boolean')
            keys=['from','to'] if kind=='branches' else ['bus']
            if any(item.get(key) not in ids for key in keys):raise ValueError('Unknown equipment bus')
            if kind=='equipment':
                for key in ['breaking_ka','making_ka_peak','thermal_ka2s']:
                    if key in item:item[key]=number(item[key],key,.001)
                continue
            item.setdefault('z1',[.01,.1]);item.setdefault('z2',deepcopy(item['z1']));item.setdefault('z0',None)
            impedance(item['z1'],'z1');impedance(item['z2'],'z2')
            if item['z0'] is not None:impedance(item['z0'],'z0')
            if kind=='sources':
                item['emf_pu']=number(item.get('emf_pu',1),'emf_pu',.001);item['angle_deg']=number(item.get('angle_deg',0),'angle_deg')
                item.setdefault('grounded',item['z0'] is not None);item.setdefault('neutral_z',[0,0]);impedance(item['neutral_z'],'neutral_z',True)
                if not isinstance(item['grounded'],bool):raise ValueError('Grounded must be boolean')
                if item['grounded'] and item['z0'] is None:raise ValueError('Grounded source requires z0')
            else:
                if item['from']==item['to']:raise ValueError('Self-connected branch')
                item.setdefault('kind','line');item['tap']=number(item.get('tap',1),'tap',.001);item['shift_deg']=number(item.get('shift_deg',0),'shift_deg')
                if item['kind'] not in ['line','transformer']:raise ValueError('Branch kind must be line or transformer')
                for end in ['from','to']:
                    item.setdefault(end+'_winding','Yg');item.setdefault(end+'_neutral_z',[0,0]);impedance(item[end+'_neutral_z'],end+'_neutral_z',True)
                    if item[end+'_winding'] not in ['Yg','Y','D']:raise ValueError('Winding must be Yg, Y or D')
    return n
