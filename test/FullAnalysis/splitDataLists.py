import sys
f = open(sys.argv[1],'r')
bb = []
be = []

for line in f:
    cols = line.strip('\n').split()
    mass = cols[0]
    if float(mass)<150: continue
    if len(mass)>9: print mass
    eta1 = float(cols[5])
    eta2 = float(cols[6])
    if abs(eta1)<=1.2 and abs(eta2)<=1.2:
        bb.append(mass)
    elif (abs(eta1)>1.2 or abs(eta2)>1.2):
        be.append(mass)

print bb[:10]
print be[:10]
open('lists/data_Run2017_ReReco_17Nov2017_BB.txt', 'wt').write('\n'.join(bb))
open('lists/data_Run2017_ReReco_17Nov2017_BE.txt', 'wt').write('\n'.join(be))
