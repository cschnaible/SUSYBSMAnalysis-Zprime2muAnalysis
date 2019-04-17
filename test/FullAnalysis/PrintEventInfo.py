import ROOT as R
from DataSamplesTEST import *
R.gROOT.SetBatch(True)

import argparse
parser = argparse.ArgumentParser(description='Print info out for specific event')
parser.add_argument('-r','--run',default=318877,help='Run number')
parser.add_argument('-l','--lumi',default=102,help='Lumi number')
parser.add_argument('-e','--event',default=151594226,help='Event number')
parser.add_argument('-y','--year',default=2018,type=int,help='Year of data')
args = parser.parse_args()

if args.year==2018: reco='PromptReco'
elif args.year==2017: reco='17Nov2017'
elif args.year==2016: reco='07Aug2017'
else: 
    print args.year,'not a valid year'
    exit()
data = DataSample('Data '+str(args.year),args.year,reco=reco)

cut = 'run=='+str(args.run)+' && lumi=='+str(args.lumi)+' && event=='+str(args.event)
toPrint1 = 'run:lumi:event:vertex_m:vertex_m_err:vertex_chi2'
toPrint2 = 'lep_id[0]:lep_pt[0]:lep_pt_err[0]:lep_eta[0]:lep_phi[0]'
if args.year==2018:
    toPrint3 = 'lep_Mu50_triggerMatchPt[0]:lep_OldMu100_triggerMatchPt[0]:lep_TkMu100_triggerMatchPt[0]'
    toPrint5 = 'lep_Mu50_triggerMatchPt[1]:lep_OldMu100_triggerMatchPt[1]:lep_TkMu100_triggerMatchPt[1]'
else:
    toPrint3 = 'lep_triggerMatchPt[0]'
    toPrint5 = 'lep_triggerMatchPt[1]'
toPrint4 = 'lep_id[1]:lep_pt[1]:lep_pt_err[1]:lep_eta[1]:lep_phi[1]'
toPrint6 = 'met_pt:met_phi:nJets'

data.t.Scan(toPrint1,cut)
data.t.Scan(toPrint2,cut)
data.t.Scan(toPrint3,cut)
data.t.Scan(toPrint4,cut)
data.t.Scan(toPrint5,cut)
data.t.Scan(toPrint6,cut)
