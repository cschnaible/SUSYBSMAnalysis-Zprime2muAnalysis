import ROOT as R
from Selection import Selection, SelectionFull

fname = '/afs/cern.ch/work/c/cschnaib/Zprime2muAnalysis/Ana2018/data/zp2mu_histos_Run2018_All_PromptReco.root'
f = R.TFile(fname)
print fname
t = f.SimpleNtupler.Get('t')
def checkEventSelection(t):
    leptonBaseSel = \
        t.lep_pt[0]>53. and \
        abs(t.lep_eta[0])<2.4 and \
        t.lep_isTrackerMuon[0]==1 and \
        t.lep_isGlobalMuon[0]==1 and \
        (t.lep_sumPt[0]/t.lep_tk_pt[0])<0.10 and \
        (t.lep_pt_err[0]/t.lep_pt[0])<0.3 and \
        t.lep_glb_numberOfValidPixelHits[0]>=1 and \
        t.lep_glb_numberOfValidTrackerLayers[0]>5 and \
        abs(t.lep_dB[0])<0.2 and \
        (t.lep_glb_numberOfValidMuonHits[0]>0 or t.lep_tuneP_numberOfValidMuonHits[0]>0) and \
        t.lep_pt[1]>53. and \
        abs(t.lep_eta[1])<2.4 and \
        t.lep_isTrackerMuon[1]==1 and \
        t.lep_isGlobalMuon[1]==1 and \
        (t.lep_sumPt[1]/t.lep_tk_pt[1])<0.10 and \
        (t.lep_pt_err[1]/t.lep_pt[1])<0.3 and \
        t.lep_glb_numberOfValidPixelHits[1]>=1 and \
        t.lep_glb_numberOfValidTrackerLayers[1]>5 and \
        abs(t.lep_dB[1])<0.2 and \
        (t.lep_glb_numberOfValidMuonHits[1]>0 or t.lep_tuneP_numberOfValidMuonHits[1]>0)
    dimuonSel = t.GoodDataRan and t.GoodVtx and t.cos_angle>-0.9998 and (t.lep_id[0]*t.lep_id[1])<0 and t.vertex_chi2 < 20. and t.vertex_m>50.
    trigger_sel = ((t.lep_Mu50_triggerMatchPt[0]>0. or t.lep_OldMu100_triggerMatchPt[0]>0. or t.lep_TkMu100_triggerMatchPt[0]>0.) or (t.lep_Mu50_triggerMatchPt[1]>0. or t.lep_OldMu100_triggerMatchPt[1]>0. or t.lep_TkMu100_triggerMatchPt[1]>0.))

    return leptonBaseSel, dimuonSel, trigger_sel

def checkEvent(t,run,lumi,event):
    if t.run==run and t.lumi==lumi and t.event==event:
        lepton, dimuon, trigger = checkEventSelection(t)
        print '\n',t.run,t.lumi,t.event
        print t.vertex_m, t.lep_pt[0], t.lep_pt[1]
        print 'Our2018Sel',t.Our2018Sel,t.Our2018Sel>0
        print 'regular: lepton',lepton,'dimuon',dimuon,'trigger',trigger
        print 'matched stations lep 0', (t.lep_numberOfMatchedStations[0] > 1 or (t.lep_numberOfMatchedStations[0]==1 and not (t.lep_stationMask[0]== 1 or t.lep_stationMask[0]==16)) or (t.lep_numberOfMatchedStations[0]==1 and (t.lep_stationMask[0]==1 or t.lep_stationMask[0]==16) and t.lep_numberOfMatchedRPCLayers[0]>2))
        print 'matched stations lep 1', (t.lep_numberOfMatchedStations[1] > 1 or (t.lep_numberOfMatchedStations[1]==1 and not (t.lep_stationMask[1]== 1 or t.lep_stationMask[1]==16)) or (t.lep_numberOfMatchedStations[1]==1 and (t.lep_stationMask[1]==1 or t.lep_stationMask[1]==16) and t.lep_numberOfMatchedRPCLayers[1]>2))
        print 'matched stations lep 1 wrong', (t.lep_numberOfMatchedStations[1] > 1 or (t.lep_numberOfMatchedStations[1]==1 and not (t.lep_stationMask[1]== 1 or t.lep_stationMask[1]==16)) or (t.lep_numberOfMatchedStations[1]==1 and (t.lep_stationMask[1]==1 or t.lep_stationMask[1]==16) and t.lep_numberOfMatchedRPCLayers[0]>2))

for entry in t:
    checkEvent(t,316666,826,1174619365)
    #checkEvent(t,316944,1097,1451047546) # fixed
    checkEvent(t,319459,55,90216964)
    checkEvent(t,317182,238,301576586)
    checkEvent(t,316505,562,663947669)
    checkEvent(t,320060,20,32431796)
