import ROOT as R
import os,sys,math,logging,pdb
import numpy as np
import SUSYBSMAnalysis.Zprime2muAnalysis.lumberjack as lumberjack
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples# samples18, samples17, samples16

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-w','--where',default='www_res',
        help='where to save output')
parser.add_argument('-y','--year',default=2018,type=int,
        help='Which MC year to do')
parser.add_argument('-m','--mode',default=1,type=int,
        help='1 - 2016 method, 2 - fixed and +/- 1,2 sigma, 3 - pseudoexperiment, 4 - pseudoexperiment with sign constraint')
parser.add_argument('-npe','--npe',default=30,type=int,
        help='Number of pseudoexperiments (method 3 and 4 only, otherwise does nothing)')
args = parser.parse_args()

phiList = [-180,-60,60,180]
etaList = [-2.4,-2.1,-1.2,0,1.2,2.1,2.4]
# Import GE maps
ge_file = open('data_generalized_endpoint.data')
years = [2016,2017,2018]
ge_data = {year:{eta:{phi:{} for phi in phiList[:-1]} for eta in etaList[:-1]} for year in years}
for line in ge_file:
    if line[0]=='#': continue
    data = line.strip('\n').split()
    year = int(data[0])
    etaBin = float(data[1])
    b = float(data[2])
    berr = float(data[3])
    phiBin = float(data[4])
    ge_data[year][etaBin][phiBin] = [b,berr]

etaHists = ['all','b','e','efwd','p','bp','ep','epfwd','m','bm','em','emfwd']
qHists = ['qall','qp','qm']
massCats = ['bb','beee','ee']

# Generate copies of GE results
B = {etaBin:{phiBin:{} for phiBin in phiList} for etaBin in etaList}
for etaBin in etaList[:-1]:
    for phiBin in phiList[:-1]:
        b = ge_data[args.year][etaBin][phiBin][0]
        berr = ge_data[args.year][etaBin][phiBin][1]
        if args.mode==2:
            B[etaBin][phiBin] = {
                    0:b,
                    1:b+berr,
                    2:b-berr,
                    3:b+2*berr,
                    4:b-2*berr,
                    }
        elif args.mode==3:
            B[etaBin][phiBin] = {N:np.random.normal(b,berr) for N in range(args.npe)}
        elif args.mode==4:
            keepSign = True if (b+e)*(b-e)>0 else False
            for N in range(args.npe):
                thisB = np.random.normal(b,berr)
                while(b*thisB<0 and keepSign):
                    thisB = np.random.normal(b,berr)
                B[etaBin][phiBin][N] = thisB
        else:
            raise ValueError(args.mode)

print B

NCOPIES = 5 if args.mode==2 else args.npe
ptHists = {N:{q:{eta:R.TProfile(q+'_'+eta+'_'+str(N),'',28,200,3000) for eta in etaHists} for q in qHists} for N in range(NCOPIES)}
massHists = {N:{cat:R.TProfile(cat+'_'+str(N),'',59,100,6000) for cat in massCats} for N in range(NCOPIES)}
for N in range(NCOPIES):
    for cat in massCats:
        massHists[N][cat].SetDirectory(0)
    for q in qHists:
        for eta in etaHists:
            ptHists[N][q][eta].SetDirectory(0)

dyList = ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf']
info = {
        2016:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/data/',
            'file':'ana_datamc_Run2016_17Jul2018.root',
            'our':'Our2016MuonsOppSignNtuple',
            'ourcommonpre':'Our2016MuPrescaledCommonMuonsOppSignNtuple',
            'ourpre':'Our2016MuPrescaledMuonsOppSignNtuple',
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/mc/',
            'mc':samples[2016],
            },
        2017:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/data/',
            'file':'ana_datamc_Run2017_31Mar2018.root',
            'our':'Our2018MuonsOppSignNtuple',
            'ourcommonpre':'Our2018MuPrescaledCommonMuonsOppSignNtuple',
            'ourpre':'Our2018MuPrescaledMuonsOppSignNtuple',
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/mc/',
            'mc':samples[2017],
            },
        2018:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/data/',
            'file':'ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root',
            'our':'Our2018MuonsOppSignNtuple',
            'ourcommonpre':'Our2018MuPrescaledMuonsOppSignNtuple',
            'ourpre':'Our2018MuPrescaledNoCommonMuonsOppSignNtuple',
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/mc/',
            'mc':samples[2018],
            },
        }

for dy in dyList:
    dyFile = R.TFile(info[args.year]['mcpath']+'/ana_datamc_'+dy+'.root')
    t = dyFile.Get(info[args.year]['our']+'/t')
    for e,event in enumerate(t):
        for N in range(NCOPIES):
            eta = {}
            phi = {}
            kref = {} # TeV-1
            kcorr = {} # TeV-1
            ptcorr = {} # GeV
            for mu in [0,1]:
                eta[mu] = t.lep_eta[mu]
                phi[mu] = t.lep_phi[mu]*R.TMath.RadToDeg()
                kref[mu] = (-1./(t.lep_pt[mu]/1000.)) if mu==0 else (1./(t.lep_pt[mu]/1000.))
                etaBin, phiBin = -1,-1
                for e,eBin in enumerate(etaList):
                    if eta[mu]<etaList[e+1]:
                        etaBin = eBin
                        break
                for p,pBin in enumerate(phiList):
                    if phi[mu]<phiList[p+1]:
                        phiBin = pBin
                        break
                Q = {
                        'qall':True,
                        'qm':True if mu==0 else False,
                        'qp':False if mu==0 else True,
                        }
                ETA = {
                        'all':True,          'm':eta[mu]<0.,            'p':0.<=eta[mu],
                        'b':abs(eta[mu])<=1.2,  'bm':-1.2<=eta[mu]<0.,     'bp':0.<=eta[mu]<1.2,
                        'e':abs(eta[mu])>1.2,   'em':-2.4<=eta[mu]<-1.2,   'ep':1.2<=eta[mu]<2.4,
                        'efwd':abs(eta[mu])>2.1,'emfwd':-2.4<=eta[mu]<-2.1,'epfwd':2.1<=eta[mu]<2.4,
                        }
                kcorr[mu] = kref[mu] + B[etaBin][phiBin][N]
                ptcorr[mu] = pow(abs(kcorr[mu]),-1)*1000.
                for qHist in qHists:
                    for etaHist in etaHists:
                        if Q[qHist] and ETA[etaHist]: 
                            ptHists[N][qHist][etaHist].Fill(t.lep_pt[mu],ptcorr[mu])
            CAT = {
                    'all':True,
                    'bb':abs(eta[0])<=1.2 and abs(eta[1])<=1.2,
                    'beee':abs(eta[0])>1.2 or abs(eta[1])>1.2,
                    'ee':abs(eta[0])>1.2 and abs(eta[1])>1.2,
                    }
            mass_ref = t.dil_mass
            mass_corr = math.sqrt(2*math.cosh(eta[0])*math.cosh(eta[1])*(1-t.cos_angle)*ptcorr[0]*ptcorr[1])
            for cat in massCats:
                if CAT[cat]: massHists[N][cat].Fill(mass_ref,mass_corr)
    dyFile.Close()

outFile = R.TFile('ge_test.root','recreate')
outFile.cd()
for N in range(NCOPIES):
    for cat in massCats:
        massHists[N][cat].Write()
    for q in qHists:
        for eta in etaHists:
            ptHists[N][q][eta].Write()
outFile.Close()

