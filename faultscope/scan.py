from .model import validate
from .solver import analyze

def scan(data,fault_types=None,buses=None):
    n=validate(data);fault_types=fault_types or ['3ph','slg','ll','dlg'];buses=buses or [b['id'] for b in n['buses']]
    if not isinstance(fault_types,list) or not 1<=len(fault_types)<=4 or any(t not in ['3ph','slg','ll','dlg'] for t in fault_types):raise ValueError('Invalid scan fault types')
    if not isinstance(buses,list) or not 1<=len(buses)<=50:raise ValueError('Select 1..50 scan buses')
    rows=[]
    for bus in buses:
        for kind in fault_types:
            try:
                r=analyze(n,bus=bus,fault_type=kind);rows.append({'bus':bus,'type':kind,'solved':True,'max_phase_ka':r['fault']['max_phase_rms_a']/1000,'ground_residual_ka':r['fault']['residual_a']['magnitude']/1000,'floating_zero':r['thevenin']['zero_sequence_floating']})
            except ValueError as exc:rows.append({'bus':bus,'type':kind,'solved':False,'error':str(exc)})
    return {'application':'faultscope','action':'scan','results':rows,'assumptions':['Each row is an independent classical RMS fault; failed/unsourced cases remain explicit.']}
