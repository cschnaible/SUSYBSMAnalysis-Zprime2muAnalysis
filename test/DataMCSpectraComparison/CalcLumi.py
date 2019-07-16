import math
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-y','--year',default=2018,type=int,help='Which year to do')
args = parser.parse_args()

# Important! Need to run CalcLumi.sh first to get brilcalc output
data = {
        2016:{
            'mu50':[x.strip('\n').split() for x in open('lumi/processed_Mu50_Run2016_17Jul2018.lumi')],
            'mu27':[x.strip('\n').split() for x in open('lumi/processed_Mu27_Run2016_17Jul2018.lumi')],
            'prescales':[14,35, 40, 70, 100, 120, 140, 150, 160, 170, 180, 200, 230, 250, 260, 290, 320],
            'other':[4,7,10,20],
            'skip':15,
            },
        2017:{
            'mu50':[x.strip('\n').split() for x in open('lumi/processed_Mu50_Run2017_31Mar2018.lumi')],
            'mu27':[x.strip('\n').split() for x in open('lumi/processed_Mu27_Run2017_31Mar2018.lumi')],
            'prescales':[59,70,74,117,120,140,148,176,210,222,234,280,281,296,315,328,336,341,356,375,385,392,415,422,445,449,458,480,505,561],
            'other':[],
            'skip':18,
            },
        2018:{
            'mu50':[x.strip('\n').split() for x in open('lumi/processed_Mu50_Run2018ABCD_17Sep2018_Run2018D_22Jan2019_20190502.lumi')],
            'mu27':[x.strip('\n').split() for x in open('lumi/processed_Mu27_Run2018ABCD_17Sep2018_Run2018D_22Jan2019_20190502.lumi')],
            #'mu50':[x.strip('\n').split() for x in open('lumi/Full2018MuonPhys_Mu50.lumi')],
            #'mu27':[x.strip('\n').split() for x in open('lumi/Full2018MuonPhys_Mu27.lumi')],
            'prescales':[148,222,296,385,445,500],
            'other':[],
            'skip':13,
            },
        }

others = []
total = {
        'mu50':0.,
        'mu27':0.,
        }
totalByPrescale = {trig:{p:0. for p in data[args.year]['prescales']+[1,'other']} for trig in ['mu27','mu50']}

nlines50 = len(data[args.year]['mu50'])
nlines27 = len(data[args.year]['mu27'])
print nlines50,nlines27
other = []
zeros = []

print '\n','*'*15,'\n'
print 'run:fill lsbegin:lsend mu27lumi mu50lumi'
for l,(mu50,mu27) in enumerate(zip(data[args.year]['mu50'],data[args.year]['mu27'])):
    if 3<l<nlines50-data[args.year]['skip']:
        if (mu50[1]!=mu27[1]) or (mu50[3]!=mu27[3]): print l,mu50[1],mu50[3],mu27[1],mu27[3]
        if mu50[12]=='nan' or mu27[12]=='nan': continue
        mu50lumi = float(mu50[12])/1000./1000. # in ub-1
        mu27lumi = float(mu27[12])/1000./1000.
        if mu27lumi==0:
            zeros.append(mu27[1]+':'+mu27[3])
            continue
        thisPrescale = mu50lumi / mu27lumi
        found = False
        for p in data[args.year]['prescales']:
            if p=='other': continue
            if abs(thisPrescale-float(p))<0.1:
                found = True
                totalByPrescale['mu27'][p] += mu27lumi
                totalByPrescale['mu50'][p] += mu50lumi
        if not found:
            if thisPrescale==1.:
                print mu50[1],mu50[3],mu50lumi,mu27lumi
                totalByPrescale['mu27'][1] += mu27lumi
                totalByPrescale['mu50'][1] += mu50lumi
            else:
                totalByPrescale['mu27']['other'] += mu27lumi
                totalByPrescale['mu50']['other'] += mu50lumi
                if round(thisPrescale) not in other:
                    other.append(round(thisPrescale))

        if thisPrescale>1:
            total['mu27']+=mu27lumi
            total['mu50']+=mu50lumi

        #if l>7: continue
        #print '\n',l
        #print mu50
        #print mu27

num50 = 0
den50 = 0
num27 = 0
den27 = 0
for p in data[args.year]['prescales']:
    num50 += p*totalByPrescale['mu50'][p]
    den50 += totalByPrescale['mu50'][p]
    num27 += p*totalByPrescale['mu27'][p]
    den27 += totalByPrescale['mu27'][p]
avg50 = num50/den50
avg27 = num27/den27

print '\n','*'*15,'\n'
print 'Average Prescale by Lumi from Mu50 :',avg50
#print 'Average Prescale by Lumi from Mu27 :',avg27
print 'Ratio of Lumis :',total['mu50']/total['mu27']

print 'Mu50'
print 'Total',total['mu50']
#print '\t1',totalByPrescale['mu50'][1]
for p in data[args.year]['prescales']:
    print '\t'+str(p),totalByPrescale['mu50'][p]
#print '\t222',totalByPrescale['mu50'][222]
#print '\t296',totalByPrescale['mu50'][296]
#print '\t385',totalByPrescale['mu50'][385]
#print '\t445',totalByPrescale['mu50'][445]
#print '\t500',totalByPrescale['mu50'][500]

print '\nMu27'
print 'Total',total['mu27']
#print '\t1',totalByPrescale['mu27'][1]
for p in data[args.year]['prescales']:
    print '\t'+str(p),totalByPrescale['mu27'][p]
#print '\t148',totalByPrescale['mu27'][148]
#print '\t222',totalByPrescale['mu27'][222]
#print '\t296',totalByPrescale['mu27'][296]
#print '\t385',totalByPrescale['mu27'][385]
#print '\t445',totalByPrescale['mu27'][445]
#print '\t500',totalByPrescale['mu27'][500]

print '\nOther Prescaled',other
print 'Mu27 other prescales :',totalByPrescale['mu27']['other']
print 'Mu50 other prescales :',totalByPrescale['mu50']['other']
print 'Mu27 prescale 1 :',totalByPrescale['mu27'][1]
print 'Mu50 prescale 1 :',totalByPrescale['mu50'][1]
