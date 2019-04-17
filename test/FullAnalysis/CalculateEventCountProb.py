import numpy as np
import ROOT as R
import math as math
from DataSamplesTEST import *
from Selection import Selection, Categories
import argparse
import tools

parser = argparse.ArgumentParser(description='Options for calculating p-values of data fluctuations')
parser.add_argument('-data',action='append',type=str,help='Which years of data to compare')
parser.add_argument('-sel','--selection',default='2016',help='Which set of selections for dimuons to draw')
parser.add_argument('-r','--recreate',action='store_true',help='Whether or not to recreate data lists')
parser.add_argument('-cats','--categories',action='append',help='Which analysis categories to draw')
args = parser.parse_args()

datalist = [int(year) for year in args.data]
print datalist
print 'recreate',args.recreate
if not args.categories:
    categorylist = ['all','bb','be','ee']
else:
    categorylist = [cat for cat in args.categories]
print categorylist

data = {
    2016 : DataSample('Data 2016 ReReco',2016,reco='07Aug2017',color=R.kBlue),
    2017 : DataSample('Data 2017 ReReco',2017,reco='17Nov2017',color=R.kRed),
    2018 : DataSample('Data 2018 PromptReco',2018,reco='PromptReco'),
}
for year in datalist:
    print data[year]
    if args.recreate: data[year].setup(Selection[int(args.selection]))

massRanges = {
        '900-950':[900,950],
        '950-1000':[950,1000],
        '1000-1100':[1000,1100],
        '1100-1300':[1100,1300],
        '1300-1500':[1300,1500],
        '1500-1800':[1500,1800],
        '1800-10000':[1800,10000],
        '900-10000':[900,10000],
        '1100-10000':[1100,10000],
        '1300-10000':[1300,10000],
        '1500-10000':[1500,10000],
        }

evtCounts = {}
for year in datalist:
    evtCounts[year] = {}
    for category in categorylist:
        evtCounts[year][category] = {}
        for massRange in massRanges:
            evtCounts[year][category][massRange] = 0.

# toprint = ['vertex_m','run','lumi','event','sumpt','eta1','eta2','pt1','pt2']
for year in datalist:
    eventlist = open(data[year].dataListName)
    for line in eventlist:
        dil = line.strip('\n').split()
        mass = float(dil[0])
        eta1 = float(dil[5])
        eta2 = float(dil[6])
        if mass<900.0: continue
        categories = {
                'bb':eta1<=1.2 and eta2<=1.2 and eta1>=-1.2 and eta2>=-1.2,
                'be':eta1>1.2 or eta2>1.2 or eta1<-1.2 or eta2<-1.2,
                'ee':(eta1>1.2 or eta1<-1.2) and (eta2>1.2 or eta2<-1.2),
                'all':True,
                }
        for massRange in massRanges:
            for category in categories:
                if mass>=massRanges[massRange][0] and mass<massRanges[massRange][1]:
                    if categories[category]: evtCounts[year][category][massRange] += 1
            
# Following Bob's presentation on inference in ratio of Poisson means
# https://indico.cern.ch/event/69012/contributions/2077354/attachments/1027518/1463126/cousins_binomial_physicsweek_oct09.pdf

p_hat = data[2018].lumi() / (data[2018].lumi() + data[2017].lumi())
lumiRatio = data[2018].lumi() / data[2017].lumi()
Pbi = {}
Zbi = {}
for category in categorylist:
    Pbi[category] = {}
    Zbi[category] = {}
    for massRange in massRanges:
        Pbi[category][massRange] = R.TMath.BetaIncomplete(p_hat, evtCounts[2018][category][massRange], evtCounts[2017][category][massRange]+1)
        Zbi[category][massRange] = math.sqrt(2) * R.TMath.ErfInverse(1-2*Pbi[category][massRange])

massrangelist = ['900-950','950-1000','1000-1100','1100-1300','1300-1500','1500-1800','1800-10000','900-10000','1100-10000','1300-10000','1500-10000']
print '\n'
print '2017 lumi',data[2017].lumi()
print '2018 lumi',data[2018].lumi()
print '\n', p_hat, lumiRatio, '\n'
for category in categorylist:
    print '{cat:>3} {mr:>11} {evt18:>4} {evt17:>4} {evtRatio:>6} {P:>6} {Z:>6}'.format(cat='cat',mr='mass range',evt18='2018',evt17='2017',evtRatio='18/17',P='P',Z='Z')
    for massRange in massrangelist:
        evt2018 = int(evtCounts[2018][category][massRange])
        evt2017 = int(evtCounts[2017][category][massRange])
        evtRatio = (float(evt2018)/evt2017) / float(lumiRatio)
        P = Pbi[category][massRange]
        Z = Zbi[category][massRange]
        toPrint = '{category:>3} {massRange:>11} {evt2018:>4} {evt2017:>4} {evtRatio:>6.3} {P:>6.3} {Z:>6.3}'
        print toPrint.format(**locals())
    print '\n'

