def sequence_fault(kind,e,z1,z2,z0,zf):
    if kind not in ['3ph','slg','ll','dlg']:raise ValueError('Fault type must be 3ph, slg, ll or dlg')
    if kind=='3ph':return 0j,e/(z1+zf),0j
    if kind=='slg':
        if z0 is None:return 0j,0j,0j
        i=e/(z1+z2+z0+3*zf);return i,i,i
    if kind=='ll' or z0 is None:
        i=e/(z1+z2+(zf if kind=='ll' else 0));return 0j,i,-i
    ground=z0+3*zf;den=z2+ground;i1=e/(z1+z2*ground/den)
    return -i1*z2/den,i1,-i1*ground/den

EQUATIONS={
 '3ph':['I1 = E / (Z1 + Zf); I0 = I2 = 0'],
 'slg':['I0 = I1 = I2 = E / (Z0 + Z1 + Z2 + 3 Zf)','Faulted phase A; IA = 3 I0'],
 'll':['I1 = E / (Z1 + Z2 + Zf); I2 = -I1; I0 = 0','Faulted phases B-C; Zf is between the two phases'],
 'dlg':['I1 = E / (Z1 + Z2 (Z0 + 3 Zf) / (Z2 + Z0 + 3 Zf))','I0 = -I1 Z2 / (Z2 + Z0 + 3 Zf)','I2 = -I1 (Z0 + 3 Zf) / (Z2 + Z0 + 3 Zf)','Faulted phases B,C joined at a common impedance Zf to ground']}
