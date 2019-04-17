import ROOT as R
R.gROOT.SetBatch(True)

import argparse
parser = argparse.ArgumentParser(description='Print info out for specific event')
parser.add_argument('-d','--data',default='data/ana_datamc_data_Run2018_inc.root')
parser.add_argument('-r','--run',default=318877,help='Run number')
parser.add_argument('-l','--lumi',default=102,help='Lumi number')
parser.add_argument('-e','--event',default=151594226,help='Event number')
#parser.add_argument('-y','--year',default=2018,type=int,help='Year of data')
args = parser.parse_args()

data = R.TFile(args.data)
t = data.Our2018MuonsPlusMuonsMinusNtuple.Get('t')


cut = 'run=='+str(args.run)+' && lumi=='+str(args.lumi)+' && event=='+str(args.event)
toPrintEvent = 'run:lumi:event:vertex_m:vertex_m_err:vertex_chi2:dil_pt:dil_rap'
toPrintMu = 'lep_cocktail_choice[X]:lep_id[X]:lep_pt[X]:lep_pt_err[X]:lep_eta[X]:lep_phi[X]'
toPrintTrig = 'lep_Mu50_triggerMatchPt[X]:lep_OldMu100_triggerMatchPt[X]:lep_TkMu100_triggerMatchPt[X]'
toPrintOther = 'met_pt:met_phi:nJets'

t.Show(320734)
#t.Scan(toPrintEvent,cut)
#t.Scan(toPrintMu.replace('X','0'),cut)
#t.Scan(toPrintTrig.replace('X','0'),cut)
#t.Scan(toPrintMu.replace('X','1'),cut)
#t.Scan(toPrintTrig.replace('X','1'),cut)
#t.Scan(toPrintOther,cut)
