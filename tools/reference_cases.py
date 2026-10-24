import json,math,cmath,copy,argparse
import numpy as np

def fault_reference(group,kind):
    n={'schema_version':1,'name':group.replace('_',' ').title(),'base_mva':100,'buses':[{'id':'source','base_kv':11},{'id':'fault','base_kv':11}],
       'sources':[{'id':'utility','bus':'source','z1':[.01,.12],'z2':[.01,.14],'z0':[.025,.2],'neutral_z':[0,0],'grounded':True,'emf_pu':1.,'angle_deg':0.,'status':True}],
       'branches':[{'id':'feeder','from':'source','to':'fault','kind':'line','z1':[.02,.18],'z2':[.02,.18],'z0':[.06,.4],'tap':1.,'shift_deg':0.,'from_winding':'Yg','to_winding':'Yg','from_neutral_z':[0,0],'to_neutral_z':[0,0],'status':True}],
       'equipment':[{'id':'CB-1','bus':'fault','breaking_ka':25,'making_ka_peak':63,'thermal_ka2s':625}]}
    zf=[0.,0.]
    if group=='equal_sequences':
        for x in n['sources']+n['branches']:x['z2']=x['z1'][:];x['z0']=x['z1'][:]
    elif group=='resistive':
        for x in n['sources']+n['branches']:
            for key in ['z1','z2','z0']:x[key][0]*=5
    elif group=='fault_resistance':zf=[.08,0]
    elif group=='fault_reactance':zf=[0,.07]
    elif group=='source_neutral':n['sources'][0]['neutral_z']=[.05,.025]
    elif group=='high_zero_impedance':n['branches'][0]['z0']=[.1,1.2]
    elif group in ['transformer_ygyg','transformer_yg_delta','transformer_delta_yg']:
        b=n['branches'][0];b['kind']='transformer';n['buses'][1]['base_kv']=.415
        if group=='transformer_yg_delta':b['to_winding']='D';b['shift_deg']=30
        elif group=='transformer_delta_yg':b['from_winding']='D';b['shift_deg']=-30
        else:b['from_neutral_z']=[.01,.02];b['to_neutral_z']=[.02,.01]
    elif group=='parallel_sources':
        second=copy.deepcopy(n['sources'][0]);second['id']='generator';second['z1']=[.02,.2];second['z2']=[.02,.25];second['z0']=[.03,.3];n['sources'].append(second)
    elif group=='parallel_paths':
        second=copy.deepcopy(n['branches'][0]);second['id']='parallel';second['z1']=[.03,.25];second['z2']=[.03,.27];second['z0']=[.08,.6];n['branches'].append(second)
    elif group=='phase_shifter':n['branches'][0]['kind']='transformer';n['branches'][0]['shift_deg']=20;n['branches'][0]['tap']=1.05
    elif group=='open_neutral':n['sources'][0]['grounded']=False;n['sources'][0]['z0']=None
    elif group=='high_xr':
        for x in n['sources']+n['branches']:
            for key in ['z1','z2','z0']:x[key][0]=.0001
    # Full phase-domain modified nodal oracle. No sequence fault formula is used.
    count=len(n['buses']);idx={b['id']:i for i,b in enumerate(n['buses'])};ys=[np.zeros((count,count),complex) for _ in range(3)];js=[np.zeros(count,complex) for _ in range(3)];stamps=[]
    for b in n['branches']:
        per=[]
        for seq in [0,1,2]:
            z=complex(*b['z'+str(seq)]);t=b['tap']*cmath.exp(1j*math.radians(b['shift_deg']*(1 if seq==1 else -1 if seq==2 else 0)));y=1/z;ff,ft,tf,tt=y/abs(t)**2,-y/t.conjugate(),-y/t,y
            if seq==0 and b['kind']=='transformer':
                first,second=b['from_winding'],b['to_winding']
                if first=='Yg' and second=='Yg':z+=3*(complex(*b['from_neutral_z'])+complex(*b['to_neutral_z']));y=1/z;ff,ft,tf,tt=y/abs(t)**2,-y/t.conjugate(),-y/t,y
                elif first=='Yg' and second=='D':ff=1/(z+3*complex(*b['from_neutral_z']))/abs(t)**2;ft=tf=tt=0j
                elif first=='D' and second=='Yg':tt=1/(z+3*complex(*b['to_neutral_z']));ff=ft=tf=0j
                else:ff=ft=tf=tt=0j
            i,j=idx[b['from']],idx[b['to']];ys[seq][i,i]+=ff;ys[seq][i,j]+=ft;ys[seq][j,i]+=tf;ys[seq][j,j]+=tt;per.append([ff,ft,tf,tt])
        stamps.append(per)
    for source in n['sources']:
        i=idx[source['bus']]
        for seq in [0,1,2]:
            if seq==0 and not source['grounded']:continue
            z=complex(*source['z'+str(seq)])+(3*complex(*source['neutral_z']) if seq==0 else 0);ys[seq][i,i]+=1/z
            if seq==1:js[seq][i]+=cmath.rect(source['emf_pu'],math.radians(source['angle_deg']))/z
    a=cmath.exp(2j*math.pi/3);t=np.array([[1,1,1],[1,a*a,a],[1,a,a*a]],complex);ti=np.linalg.inv(t);yabc=np.zeros((3*count,3*count),complex);jabc=np.zeros(3*count,complex)
    for i in range(count):
        jabc[3*i:3*i+3]=t@np.array([js[k][i] for k in range(3)])
        for j in range(count):yabc[3*i:3*i+3,3*j:3*j+3]=t@np.diag([ys[k][i,j] for k in range(3)])@ti
    k=idx['fault'];unit=np.eye(3*count,dtype=complex)
    if kind=='3ph':c=unit[:,3*k:3*k+3];zf_matrix=complex(*zf)*np.eye(3)
    elif kind=='slg':c=unit[:,[3*k]];zf_matrix=np.array([[complex(*zf)]])
    elif kind=='ll':c=(unit[:,3*k+1]-unit[:,3*k+2]).reshape(-1,1);zf_matrix=np.array([[complex(*zf)]])
    else:c=unit[:,[3*k+1,3*k+2]];zf_matrix=complex(*zf)*np.ones((2,2))
    augmented=np.block([[yabc,c],[c.T,-zf_matrix]]);rhs=np.r_[jabc,np.zeros(c.shape[1])];answer=np.linalg.lstsq(augmented,rhs,rcond=1e-13)[0]
    if max(abs(augmented@answer-rhs))>1e-8:raise RuntimeError('Independent phase-domain fault oracle residual failed')
    voltage=answer[:3*count].reshape(count,3);current=(c@answer[3*count:])[3*k:3*k+3];base=100000/(math.sqrt(3)*n['buses'][k]['base_kv']);expected={'fault_current_real_a':(current*base).real.tolist(),'fault_current_imag_a':(current*base).imag.tolist(),'bus_voltage_real_pu':voltage.real.tolist(),'bus_voltage_imag_pu':voltage.imag.tolist(),'mna_residual_pu':float(max(abs(augmented@answer-rhs)))}
    return n,zf,expected

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--group',required=True);p.add_argument('--fault',choices=['3ph','slg','ll','dlg'],required=True);args=p.parse_args()
    network,zf,expected=fault_reference(args.group,args.fault)
    print(json.dumps({'network':network,'fault_z':zf,'expected':expected},indent=2))
