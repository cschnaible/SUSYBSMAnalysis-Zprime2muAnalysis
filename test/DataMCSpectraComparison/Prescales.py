'''
Requires output of 
brilcalc trg --prescales --hltpath HLT_Mu27_v12 > HLTMu27_prescaleInfo.txt
brilcalc trg --prescales --hltpath HLT_Mu27_v13 >> HLTMu27_prescaleInfo.txt
and 
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /pb  -i Run2018MuonPhys.json --hltpath HLT_Mu50_v* | tee Run2018MuonPhys.lumi 

Outer loop on lumi file, find corresponding run in trigger file (skipping 0 prescale lumi sections)
and sum lumi for each prescale. 
'''

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-l','--lumi-file',dest='lumi_file',default='Mu50_MuonPhys.lumi',help='Lumi file output from brilcalc')
args = parser.parse_args()
lumiFile = open(args.lumi_file)
#prescales = open('HLTMu27_prescaleInfo.txt')

data = {}
names_lumi = ['run','fill','date','h','m','s','nls','ncms','delivered','recorded']
names_prescales = ['run','cmsls','prescidx','totprescval','hltpath/prescval','logic','l1bit/prescval']


for lumi_line in lumiFile:
    lumicols = lumi_line.replace(':',' ').replace('|',' ').strip('\n').split()
    if len(lumicols) != 10: continue
    if lumi_line[0]=='#': continue
    lumidata = {name:data for name,data in zip(names_lumi,lumicols)}
    found = False
    for prescale_line in open('HLTMu27_prescaleInfo.txt'):
        if found: break
        #prescale_line_tmp = '%s'%prescale_line
        if prescale_line[0]=='#': continue
        prescalecols = prescale_line.strip('\n').split()
        prescalecols = [d for d in prescalecols if d!='|']
        if len(prescalecols)!=8: continue
        prescaledata = {name:data for name,data in zip(names_prescales,prescalecols)}
        if prescaledata['run']==lumidata['run']:
            if prescaledata['totprescval']=='0': continue
            print lumidata['run'],prescaledata['totprescval'],lumidata['recorded']
            if prescaledata['totprescval'] in data.keys():
                data[prescaledata['totprescval']] += float(lumidata['recorded'])
            else:
                data[prescaledata['totprescval']] = float(lumidata['recorded'])
            found = True
        else:
            continue

print

lumitot = 0.
for d in data:
    if d=='222': 
        #data[d] += 2.855987
        data[d] += 2.350079
    elif d=='385': 
        #data[d] += 238.34616
        data[d] += 236.27652099999975
    elif d=='296': 
        #data[d] += 255.674147
        data[d] += 251.98841200000018
    print d,data[d]
    lumitot += data[d]
print 'tot',lumitot
