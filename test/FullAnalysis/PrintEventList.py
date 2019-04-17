import ROOT as R
from DataSamplesTEST import *
from Selection import *
R.gROOT.SetBatch(True)
import argparse
parser = argparse.ArgumentParser(description='Print event list for same sign data')
parser.add_argument('-d','--data',default=2018,type=int,help='Which year to print')
args = parser.parse_args()

if args.data==2018: reco='PromptReco'
elif args.data==2017: reco='17Nov2017'
elif args.data==2016: reco='07Aug2017'
else: 
    print args.data,'not a valid year'
    exit()
data = DataSample('Data '+str(args.data),args.data,reco=reco)

selectionList = ['base','cos_angle','same_sign','vertex_chi2','trigger','pt','eta','isTracker','isGlobal','rel_iso','dB','v_pix_hits','num_trk_lays','v_mu_hits_12','matched_station_16']

selection = GetSelection(args.data,selectionList)
selection += ' && vertex_m > 1000'

scanfield = 'run:lumi:event:vertex_m:lep_id[0]+lep_id[1]:lep_pt[0]:lep_eta[0]:lep_phi[0]:lep_pt[1]:lep_eta[1]:lep_phi[1]:met_pt:met_phi:nJets'

data.t.Scan(scanfield,selection,"colsize=11")

