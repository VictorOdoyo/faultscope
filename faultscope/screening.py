import math
from .solver import analyze
from .model import number

def peak_factor(r,x):
    if r<0 or x<0:raise ValueError('Equivalent R/X must be nonnegative')
    return 1.02 if x==0 and r>0 else 1.02+.98*math.exp(-3*r/x) if x>0 else 2.

def screen(data,bus=None,c_factor=1.1,frequency_hz=50,duration_s=.1,fault_z=None):
    c_factor=number(c_factor,'c_factor',.001);frequency_hz=number(frequency_hz,'frequency_hz',.001);duration_s=number(duration_s,'duration_s',0)
    r=analyze(data,bus=bus,fault_type='3ph',fault_z=fault_z,voltage_factor=c_factor);z=complex(r['thevenin']['z1_pu']['real'],r['thevenin']['z1_pu']['imag'])+complex(r['fault']['z_pu']['real'],r['fault']['z_pu']['imag']);kappa=peak_factor(z.real,z.imag);current=r['fault']['max_phase_rms_a'];peak=kappa*math.sqrt(2)*current
    r['screening']={'method':'equivalent_source_peak_screen','reference_edition':'IEC 60909-0:2016 concepts; incomplete screening implementation','initial_rms_ka':current/1000,'kappa':kappa,'peak_ka':peak/1000,'constant_rms_thermal_ka2s':(current/1000)**2*duration_s,'dc_time_constant_s':z.imag/(2*math.pi*frequency_hz*z.real) if z.real>0 else None,'duration_s':duration_s,'limitations':['Equivalent R/X peak formula is restricted here to a three-phase single-equivalent screening estimate. No meshed peak summation method, generator/transformer correction factors, motor decrement, inverter rules, breaking-current calculation or full IEC compliance is implemented. c scales the supplied reference voltage; use a 1 pu profile to interpret it directly as the standard-style voltage factor.']}
    return r
