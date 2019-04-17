'''
This script will be basic charge mis-ID study plotting:
    N(q_gen != q_reco) / N(all)
'''
import ROOT as R
import math,array
import Plotter
import SUSYBSMAnalysis.Zprime2muAnalysis.roottools as roottools
import argparse
parser = argparse.ArgumentParser(description='Options for charge mis-ID study')
parser.add_argument('-r','--recreate',action='store_true',help='Recreate histograms')
parser.add_argument('-y','--year',default='2016',help='MC production year')
parser.add_argument('-i','--inname',default='20181114',help='Input file name to grab histograms')
parser.add_argument('-o','--outname',default='',help='Additional name to add out output')
args = parser.parse_args()

NAME = args.year+'_'+args.outname

FILEBASE = '/afs/cern.ch/user/a/alfloren/public/DY_ROOT/'+args.year+'/ana_datamc_{SAMPLE}.root'

samples = ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300',\
        'dy2300to3500','dy3500to4500','dy4500to6000']


selections = ['pt','eta','rel_iso','rel_err','trigger',\
        'isTracker','isGlobal',\
        'v_pix_hits','num_trk_lays','dB','v_mu_hits_12','matched_station_16']

numden = ['num','den']
ptypes = ['gen']
cats = ['allcat','b','em','ep','e']
pts = ['allpt','0to300','300to450','450to800','800to1200','1200to1600','1600to2000','2000to3000']
charges = ['qall','qm','qp']

inFile = R.TFile('chargeMisID_'+args.year+'_'+args.inname+'.root')
etaHists = {pt:{} for pt in pts}
for pt in pts:
    rat = inFile.Get('eta_gen_allcat_'+pt+'_qm_den').Clone('eta_gen_allcat_'+pt+'_rat')
    den = inFile.Get('eta_gen_allcat_'+pt+'_qp_den').Clone()
    rat.Divide(den)
    rat.SetDirectory(0)
    etaHists[pt] = rat
inFile.Close()
def etaWeight(q,pt,eta):
    '''
    Scale mu+ to mu- eta distribution
    '''
    if q=='qp':
        ibin = etaHists[pt].FindBin(eta)
        return etaHists[pt].GetBinContent(ibin)
    else:
        return 1.


def sign(val):
    if val>0.:
        return 1
    elif val<0.:
        return -1
    else:
        print val,'val==0 evaluates to ',val==0
        return 0

def dR(t,gm,rm):
    '''
    gm = gen muon
    rm = reco muon
    '''
    eta1, phi1 = t.gen_lep_eta[gm], t.gen_lep_phi[gm]
    eta2, phi2 = t.gen_lep_eta[rm], t.gen_lep_phi[rm]
    return math.sqrt((eta2-eta1)**2 + (phi2-phi1)**2)

#def match_gen_dR(t):
#    '''
#    gen muon 0 is always negative muon
#    return ordered pair of 
#    (closest to minus, closest to plus)
#    '''
#    if dR(t,0,0) < dR(t,0,1):
#        return 0,1
#    else:
#        return 1,0

def match_to_gen_by_dR(t):
    '''
    Match the reco muon to the gen muon by distance in (eta,phi) plane
    '''
    matches = []
    skip = []
    for g in [0,1]:
        dR_list = []
        for r in [0,1]:
            if r in skip: continue
            dR_list.append([r,dR(t,g,r)])
        if len(dR_list)==0: continue
        dR_sort = sorted(dR_list,key=lambda a:a[1])
        #print dR_list
        #print dR_sort
        if dR_sort[0][1]>0.3: continue
        matches.append([g,dR_sort[0][0]])
        skip.append(dR_sort[0][0])
    return matches

def selection(t):
    # Loop through selections defined above and return whether tree entry passes selections
    Selections = {
        'base' : t.GoodDataRan and t.GoodVtx,
        'cos_angle' : (t.cos_angle > -0.9998),
        'opp_sign' : ((t.lep_id[0]*t.lep_id[1])<0),
        'same_sign' : ((t.lep_id[0]*t.lep_id[1])>0),
        'plus_sign' : (t.lep_id[0]>0 and t.lep_id[1]>0),
        'minus_sign' : (t.lep_id[0]<0 and t.lep_id[1]<0),
        'vertex_chi2' : (t.vertex_chi2 < 20.),
        'vertex_m' : (t.vertex_m > 50.),
        'trigger' : (t.lep_triggerMatchPt[0]>50. or t.lep_triggerMatchPt[1]>50.),
        #'trigger_18' : ((t.lep_Mu50_triggerMatchPt[0]>0. or t.lep_OldMu100_triggerMatchPt[0]>0. or t.lep_TkMu100_triggerMatchPt[0]>0.) or (t.lep_Mu50_triggerMatchPt[1]>0. or t.lep_OldMu100_triggerMatchPt[1]>0. or t.lep_TkMu100_triggerMatchPt[1]>0.)),
        'pt' : (t.lep_pt[0]>53. and t.lep_pt[1]>53.),
        'eta' : (abs(t.lep_eta[0])<2.4 and abs(t.lep_eta[1])<2.4),
        'isTracker' : (t.lep_isTrackerMuon[0]==1 and t.lep_isTrackerMuon[1]==1),
        'isGlobal' : (t.lep_isGlobalMuon[0]==1 and t.lep_isGlobalMuon[1]==1),
        'rel_iso' : ( (t.lep_sumPt[0]/t.lep_tk_pt[0])<0.10 and (t.lep_sumPt[1]/t.lep_tk_pt[1])<0.10 ),
        'rel_err' : ( (t.lep_pt_err[0]/t.lep_pt[0])<0.30 and (t.lep_pt_err[1]/t.lep_pt[1])<0.30 ),
        'v_pix_hits' : (t.lep_glb_numberOfValidPixelHits[0]>0 and t.lep_glb_numberOfValidPixelHits[1]>0),
        'num_trk_lays' : (t.lep_glb_numberOfValidTrackerLayers[0]>5 and t.lep_glb_numberOfValidTrackerLayers[1]>5),
        'dB' : ( abs(t.lep_dB[0])<0.2 and abs(t.lep_dB[1])<0.2 ),

        'v_mu_hits_12' : (t.lep_glb_numberOfValidMuonHits[0]>0 and t.lep_glb_numberOfValidMuonHits[1]>0),
        #'v_mu_hits_18' : ( (t.lep_glb_numberOfValidMuonHits[0]>0 or t.lep_tuneP_numberOfValidMuonHits[0]>0) or (t.lep_glb_numberOfValidMuonHits[1]>0 or t.lep_tuneP_numberOfValidMuonHits[1]>0) ),

        'matched_station_12' : (t.lep_numberOfMatchedStations[0]>1 and t.lep_numberOfMatchedStations[1]>1),
        'matched_station_16' : ((t.lep_numberOfMatchedStations[0] > 1 or (t.lep_numberOfMatchedStations[0]==1 and not (t.lep_stationMask[0]== 1 or t.lep_stationMask[0]==16)) or (t.lep_numberOfMatchedStations[0]==1 and (t.lep_stationMask[0]==1 or t.lep_stationMask[0]==16) and t.lep_numberOfMatchedRPCLayers[0]>2)) and (t.lep_numberOfMatchedStations[1] > 1 or (t.lep_numberOfMatchedStations[1]==1 and not (t.lep_stationMask[1]== 1 or t.lep_stationMask[1]==16)) or (t.lep_numberOfMatchedStations[1]==1 and (t.lep_stationMask[1]==1 or t.lep_stationMask[1]==16) and t.lep_numberOfMatchedRPCLayers[1]>2))),
        }

    passSelection = True
    for sel in selections:
        passSelection *= Selections[sel]

    return passSelection

hists = {p:{x:{cat:{pt:{q:{} for q in charges} for pt in pts} for cat in cats} for x in ptypes} for p in numden}

for p in numden:
    for x in ptypes:
        for cat in cats:
            for pt in pts:
                for q in charges:
                    hists[p][x][cat][pt][q] = {
                            #'pt':R.TH1F('pt_'+x+'_'+cat+'_'+p,';'+x+' muon p_{T} [GeV];N(#mu)',300,0,3000),
                            'pt':R.TH1F('pt_'+x+'_'+cat+'_'+pt+'_'+q+'_'+p,';'+x+' muon p_{T} [GeV];N(#mu)',7,array.array('d',[0,300,450,800,1200,1600,2000,3000])),
                            'eta':R.TH1F('eta_'+x+'_'+cat+'_'+pt+'_'+q+'_'+p,';'+x+' muon #eta;N(#mu)',50,-2.5,2.5),
                            'phi':R.TH1F('phi_'+x+'_'+cat+'_'+pt+'_'+q+'_'+p,';'+x+' muon #phi;N(#mu)',25,-R.TMath.Pi(),R.TMath.Pi()),
                            'mass':R.TH1F('mass_'+x+'_'+cat+'_'+pt+'_'+q+'_'+p,';'+x+' m(#mu#mu) [GeV];N(#mu)',60,0,6000),
                            'charge':R.TH1F('charge_'+x+'_'+cat+'_'+pt+'_'+q+'_'+p,';'+x+' muon charge;N(#mu)',3,-1,2),
                            }
outFile = R.TFile('chargeMisID'+'_'+NAME+'.root','recreate')
for SAMPLE in samples:
    print SAMPLE
    f = R.TFile(FILEBASE.format(**locals()))
    t = f.Get('SimpleNtupler/t')
    NUMEVENTS = t.GetEntries()
    for e in range(t.GetEntries()):
        if e%10000==0: print e,'/',NUMEVENTS
        # If multiple dimuons exist in the event, skip it
        if e+1>=t.GetEntries():
            nextEvent = -1
        else:
            t.GetEntry(e+1)
            nextEvent = t.event
        t.GetEntry(e)
        thisEvent = t.event
        if e==0:
            prevEvent = -1
        passSelection = selection(t)
        if not passSelection: 
            prevEvent = thisEvent
            continue # skip dimuon if it doesn't pass cuts
        if thisEvent==prevEvent or thisEvent==nextEvent:
            prevEvent = thisEvent
            continue # skip event if there are multiple in event
        else:
            # Only one dimuon in event and it passes cuts
            prevEvent = thisEvent
            #gm,gp = match_gen_dR(t)
            matches = match_to_gen_by_dR(t)
            # loop on gen muon
            #for gen,reco in [(0,gm),(1,gp)]:
            for match in matches:
                gen,reco = match
                Categories = {
                        'allcat':True,
                        'b': (abs(t.gen_lep_eta[gen])<=1.2),
                        'em': (t.gen_lep_eta[gen]<-1.2),
                        'ep': (t.gen_lep_eta[gen]>1.2),
                        'e':(abs(t.gen_lep_eta[gen])>1.2),
                        }
                Charge = {
                        'qall':True,
                        'qm':(gen==0),
                        'qp':(gen==1),
                        }
                Pt = {
                        'allpt':True,
                        '0to300':(t.gen_lep_pt[gen]>=0 and t.gen_lep_pt[gen]<=300),
                        '300to450':(t.gen_lep_pt[gen]>=300 and t.gen_lep_pt[gen]<450),
                        '450to800':(t.gen_lep_pt[gen]>=450 and t.gen_lep_pt[gen]<800),
                        '800to1200':(t.gen_lep_pt[gen]>=800 and t.gen_lep_pt[gen]<1200),
                        '1200to1600':(t.gen_lep_pt[gen]>=1200 and t.gen_lep_pt[gen]<1600),
                        '1600to2000':(t.gen_lep_pt[gen]>=1600 and t.gen_lep_pt[gen]<2000),
                        '2000to3000':(t.gen_lep_pt[gen]>=2000 and t.gen_lep_pt[gen]<3000),
                        }
                for cat in cats:
                    for q in charges:
                        for pt in pts:
                            if Categories[cat] and Charge[q] and Pt[pt]:
                                hists['den']['gen'][cat][pt][q]['pt'].Fill(t.gen_lep_pt[gen],etaWeight(q,pt,t.gen_lep_eta[gen]))
                                hists['den']['gen'][cat][pt][q]['eta'].Fill(t.gen_lep_eta[gen],etaWeight(q,pt,t.gen_lep_eta[gen]))
                                hists['den']['gen'][cat][pt][q]['phi'].Fill(t.gen_lep_phi[gen],etaWeight(q,pt,t.gen_lep_eta[gen]))
                                hists['den']['gen'][cat][pt][q]['mass'].Fill(t.gen_dil_mass,etaWeight(q,pt,t.gen_lep_eta[gen]))
                                hists['den']['gen'][cat][pt][q]['charge'].Fill(sign(t.gen_lep_qOverPt[gen]),etaWeight(q,pt,t.gen_lep_eta[gen]))
                                if sign(t.gen_lep_qOverPt[gen])!=sign(t.lep_tuneP_qOverPt[reco]):
                                    hists['num']['gen'][cat][pt][q]['pt'].Fill(t.gen_lep_pt[gen],etaWeight(q,pt,t.gen_lep_eta[gen]))
                                    hists['num']['gen'][cat][pt][q]['eta'].Fill(t.gen_lep_eta[gen],etaWeight(q,pt,t.gen_lep_eta[gen]))
                                    hists['num']['gen'][cat][pt][q]['phi'].Fill(t.gen_lep_phi[gen],etaWeight(q,pt,t.gen_lep_eta[gen]))
                                    hists['num']['gen'][cat][pt][q]['mass'].Fill(t.gen_dil_mass,etaWeight(q,pt,t.gen_lep_eta[gen]))
                                    hists['num']['gen'][cat][pt][q]['charge'].Fill(sign(t.gen_lep_qOverPt[gen]),etaWeight(q,pt,t.gen_lep_eta[gen]))

    for p in numden:
        for x in ptypes:
            for cat in cats:
                for pt in pts:
                    for q in charges:
                        for hist in hists[p][x][cat][pt][q].keys():
                            hists[p][x][cat][pt][q][hist].SetDirectory(0)
                            outFile.cd()
                            hists[p][x][cat][pt][q][hist].Write()
                            f.cd()

        
f.Close()
