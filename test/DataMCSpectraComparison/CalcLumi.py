import math

ext = 'nocommon_20190512'
#ext = 'ana_common_20190512'
mu50data = [x.strip('\n').split() for x in open('lumi/processed_Run2017BCDEF_Mu50_'+ext+'.lumi')]
mu27data = [x.strip('\n').split() for x in open('lumi/processed_Run2017BCDEF_Mu27_'+ext+'.lumi')]

prescales = [59,70,74,117,120,140,148,176,210,222,234,280,281,296,315,328,336,341,356,375,385,392,415,422,445,449,458,480,505,561]
others = []
total = {
        'mu50':0.,
        'mu27':0.,
        }

totalByPrescale = {trig:{p:0. for p in prescales+[1,'other']} for trig in ['mu27','mu50']}

nlines50 = len(mu50data)
nlines27 = len(mu27data)
print nlines50,nlines27
zeros = []

for l,(mu50,mu27) in enumerate(zip(mu50data,mu27data)):
    if 3<l<nlines50-18:
        if (mu50[1]!=mu27[1]) or (mu50[3]!=mu27[3]): print l,mu50[1],mu50[3],mu27[1],mu27[3]
        if mu50[12]=='nan' or mu27[12]=='nan': continue
        mu50lumi = float(mu50[12])/1000.
        mu27lumi = float(mu27[12])/1000.
        if mu27lumi==0:
            zeros.append(mu27[1]+':'+mu27[3])
            continue
        thisPrescale = mu50lumi / mu27lumi
        found = False
        for p in prescales:
            if abs(thisPrescale-float(p))<0.5:
                found = True
                totalByPrescale['mu27'][p] += mu27lumi
                totalByPrescale['mu50'][p] += mu50lumi
        if found:
            total['mu27']+=mu27lumi
            total['mu50']+=mu50lumi
        else:
            if thisPrescale==1:
                totalByPrescale['mu27'][1] += mu27lumi
                totalByPrescale['mu50'][1] += mu50lumi
            else:
                others.append(thisPrescale)
                totalByPrescale['mu27']['other'] += mu27lumi
                totalByPrescale['mu50']['other'] += mu50lumi

num50 = 0
den50 = 0
num27 = 0
den27 = 0
for p in prescales:
    num50 += p*totalByPrescale['mu50'][p]
    den50 += totalByPrescale['mu50'][p]
    num27 += p*totalByPrescale['mu27'][p]
    den27 += totalByPrescale['mu27'][p]
avg50 = num50/den50
avg27 = num27/den27

print 'Average Prescale by Lumi from Mu50 :',avg50
print 'Average Prescale by Lumi from Mu27 :',avg27
print 'Ratio of Lumis :',total['mu50']/total['mu27']
print 'Ratio of Lumis :',(total['mu50']+totalByPrescale['mu50'][1])/(total['mu27']+totalByPrescale['mu27'][1]),'(include prescale=1)'

print 'Mu50'
print 'Total',total['mu50']
for p in prescales:
    print '\t'+str(p),totalByPrescale['mu50'][p]

print 'Mu27'
print 'Total',total['mu27']
for p in prescales:
    print '\t'+str(p),totalByPrescale['mu27'][p]
        

print '\nZeros'
print zeros
print '\nOthers'
print 'mu50 1',totalByPrescale['mu50'][1]
print 'mu27 1',totalByPrescale['mu27'][1]
print sorted(others)
print 'other mu50',totalByPrescale['mu50']['other']
print 'other mu27',totalByPrescale['mu27']['other']
