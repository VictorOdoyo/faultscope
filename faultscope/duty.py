from .model import validate
from .screening import screen
from .solver import analyze

def duty(data,bus=None,fault_type='3ph',duration_s=.1,c_factor=1.1):
    n=validate(data);result=screen(n,bus=bus,c_factor=c_factor,duration_s=duration_s) if fault_type=='3ph' else analyze(n,bus=bus,fault_type=fault_type)
    fault=result['fault'];rows=[];rms=fault['max_phase_rms_a']/1000;screening=result.get('screening')
    for e in n['equipment']:
        if not e['status'] or e['bus']!=fault['bus']:continue
        comparisons=[]
        for key,value in [('breaking_ka',rms),('making_ka_peak',screening['peak_ka'] if screening else None),('thermal_ka2s',rms*rms*duration_s)]:
            if key not in e:continue
            comparisons.append({'rating':key,'rated':e[key],'calculated':value,'utilization_percent':100*value/e[key] if value is not None else None,'within_rating':value<=e[key] if value is not None else None})
        rows.append({'id':e['id'],'comparisons':comparisons})
    result['equipment_duty']=rows;result['duty_note']='Breaking rating comparison uses initial RMS only, not a time-dependent breaking-current calculation. Peak is withheld for unbalanced faults. Ratings and application conditions must be supplied consistently.'
    return result
