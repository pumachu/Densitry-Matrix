import numpy as np
import sys

def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs


f = open(sys.argv[1],'r')
fo = open('density-matrix.fchk','w')
l = f.readlines()
coeff = []
for i,line in enumerate(l):
    if 'Number of electrons' in line:
        NOCC = int(int(line.split()[-1])/2) #### Number of occupied MO
    if 'Alpha Orbital Energies' in line:
        NMO = int(line.split()[-1]) #### Number of MO
    if 'Alpha MO coefficients' in line:
        N = int(line.split()[-1])   #### Number of MO coefficient matrix
        if N%5 == 0:
            NLINES = int(N/5)
        else:
            NLINES = int(N/5)+1
        for j in range(NLINES):
            for k in l[i+j+1].split():
                coeff.append(k)
coeff = np.array(coeff,dtype='float')
coeff = coeff.reshape(NMO,int(N/NMO))
occ = coeff[0:NOCC]
DM = np.matmul(occ.T,occ)*2.0     #### calculate the density matrix
#print (np.shape(DM))
TRL =  np.tril(DM)
TRIL_DM_1D = []
for i in range(len(TRL)):
    for j in range(i+1):
        TRIL_DM_1D.append(TRL[i][j])

fo.write('Total SCF Density                          R   N=          '+str(len(TRIL_DM_1D))+'\n')

for vec in split(TRIL_DM_1D,5):
    for value in vec:
        form = '{:>16.8E}'.format(value)
        fo.write(form)
    fo.write('\n')
