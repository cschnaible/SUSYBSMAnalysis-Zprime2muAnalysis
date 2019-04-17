''' 
Purpose of script is to fill simple histograms for charge mis-ID rate calculation
Assumed is that the MC sample used is a muon gun MC

Chris Schnaible (UCLA)
15 November 2018
'''

import ROOT as R
R.gROOT.SetBatch()
from DataFormats.FWLite import Events, Handle
import array
import math
import glob
import logging,lumberjack
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-y','--year',default='2016',help='MuGun year')
parser.add_argument('-o','--outname',default='',help='Name for output ROOT file')
parser.add_argument('-l','--log',action='store_true',help='Produce log file')
args = parser.parse_args()

NAME = args.year+'_mu_gun_mc_no_cuts'+('_'+args.outname if args.outname else '')

recoMuonHandle = Handle('std::vector<reco::Muon>')
recoMuonLabel = ('muons')
genParticleHandle = Handle('std::vector<reco::GenParticle>')
genParticleLabel = ('genParticles')
vertexHandle = Handle('std::vector<reco::Vertex>')
vertexLabel = ('offlinePrimaryVertices')

def dR(gen,reco):
    eta1, phi1 = gen.eta(),gen.phi() 
    eta2, phi2 = reco.eta(),reco.phi()
    return math.sqrt((eta2-eta1)**2 + (phi2-phi1)**2)

def match_to_gen_by_dR(genMuons,recoMuons):
    '''
    Match the reco muon to the gen muon by distance in (eta,phi) plane
    '''
    matches = []
    skip = []
    for g,gen in enumerate(genMuons):
        dR_list = []
        for r,reco in enumerate(recoMuons):
            if r in skip: continue
            dR_list.append([r,dR(gen,reco)])
        if len(dR_list)==0: continue
        dR_sort = sorted(dR_list,key=lambda a:a[1])
        #print dR_list
        #print dR_sort
        if dR_sort[0][1]>0.3: continue
        matches.append([gen,recoMuons[dR_sort[0][0]]])
        skip.append(dR_sort[0][0])
    return matches

def isHighPtMuon(muon,PV):
    #if not muon.isGlobalMuon(): return False
    glb = muon.isGlobalMuon()

    if glb:
        muValHits = (muon.globalTrack().hitPattern()).numberOfValidMuonHits()>0 or \
                muon.tunePMuonBestTrack().hitPattern().numberOfValidMuonHits()>0


        hits = muon.innerTrack().hitPattern().trackerLayersWithMeasurement() > 5 and \
                muon.innerTrack().hitPattern().numberOfValidPixelHits() > 0

        momQuality = muon.tunePMuonBestTrack().ptError() / muon.tunePMuonBestTrack().pt() < 0.3

        ipx = abs(muon.innerTrack().dxy(PV.position()))<0.2
        #ipz = abs(muon.innerTrack().dz(PV.position()))<0.5 # doesn't work in muon gun samples?
    else:
        muValHits = False
        hits = False
        momQuality = False
        ipx = False
        #ipz = False

    muMatchedSt = muon.numberOfMatchedStations() > 1
    if not muMatchedSt:
        if (muon.isTrackerMuon() and muon.numberOfMatchedStations()==1):
            if ( muon.expectedNnumberOfMatchedStations()<2 or \
                 (not (muon.stationMask()==1 or muon.stationMask()==16)) or \
                 muon.numberOfMatchedRPCLayers()>2 \
               ):
                muMatchedSt = True

    muID = muValHits and muMatchedSt
    return muID and hits and momQuality and ipx
    #return glb and muID and hits and momQuality and ip, glb, muID, hits, momQuality, ipx,ipz

def selection(muons,PV):
    '''
    Force all muons to pass 
    - high-pT ID, pT > 53 GeV, |eta| < 2.4
    - relative tracker isolation < 0.1
    - relative pt error < 0.3
    '''
    toReturn = []
    for muon in muons:
        # general acceptance cuts
        eta = abs(muon.eta()) < 2.4
        #eta = True

        # high-pT ID
        highPtID = isHighPtMuon(muon,PV)
        #highPtID = True

        # relative tracker isolation
        iso = (muon.isolationR03().sumPt / muon.pt()) < 0.1
        #iso = True

        #if True:
        if eta and highPtID and iso:
            toReturn.append(muon)
        else: 
            continue
    return toReturn

dumpLogName = 'muonDump_'+NAME
lumberjack.setup_logger(dumpLogName,'logs/'+dumpLogName+'.log')
dumpLog = logging.getLogger(dumpLogName)

def dumpEvent(gen,reco):
    ret = '{gqop:.4E} {gpt:8.2f} | {rqop:.4E} {rpt:8.2f} | {nsig:4.2f}'
    #gqopt = gen.charge()/gen.pt()
    gqop = gen.charge()/gen.p()
    gpt = gen.pt()
    #rqopt = reco.tunePMuonBestTrack().charge()/reco.tunePMuonBestTrack().pt()
    rqop = reco.tunePMuonBestTrack().qoverp()
    rpt = reco.tunePMuonBestTrack().pt()
    nsig = abs(gqop-rqop) / reco.tunePMuonBestTrack().qoverpError()
    dumpLog.info(ret.format(**locals()))

numden = ['num','den']
cats = ['allcat','b','e','em','ep']
charges = [ 'qall', 'qm', 'qp' ]
# will not use pT binning according to Begona's study
# instead use pT binning from Simranjit's study
# (it looks nice)
# https://indico.cern.ch/event/771991/
pts = [ 'allpt', '0to100', '100to200', '200to400', '400to700',\
        '700to1000', '1000to1500', '1500to2000', '2000to2500']
histTypes= ['p','pt','eta','charge','phi']

# Construct histograms
hists = {r:{cat:{pt:{q:{} for q in charges} for pt in pts} for cat in cats} for r in numden}
for r in numden:
    for cat in cats:
        for pt in pts:
            for q in charges:
                hists[r][cat][pt][q] = {
                        'pt':R.TH1F('pt_gen_'+cat+'_'+pt+'_'+q+'_'+r,';gen muon p_{T} [GeV];N(#mu)',8,array.array('d',[0,100,200,400,700,1000,1500,2000,2500])),
                        'p':R.TH1F('p_gen_'+cat+'_'+pt+'_'+q+'_'+r,';gen muon p_{T} [GeV];N(#mu)',8,array.array('d',[0,100,200,400,700,1000,1500,2000,2500])),
                        'eta':R.TH1F('eta_gen_'+cat+'_'+pt+'_'+q+'_'+r,';gen muon #eta;N(#mu)',50,-2.5,2.5),
                        'phi':R.TH1F('phi_gen_'+cat+'_'+pt+'_'+q+'_'+r,';gen muon #phi;N(#mu)',25,-R.TMath.Pi(),R.TMath.Pi()),
                        'charge':R.TH1F('charge_gen_'+cat+'_'+pt+'_'+q+'_'+r,';gen muon charge;N(#mu)',3,-1,2),
                        }

if args.year=='2016':
    fileName = '/eos/cms/store/group/phys_muon/abbiendi/MuonGun/MuonGun_16_PTOT-5-2500/crab_MuonGun_16_step3_asympt/180622_181848/*/*APE*.root'
elif args.year=='2017-old':
    fileName = '/eos/cms/store/group/phys_muon/abbiendi/MuonGun/MuonGun_PTOT-5-2500/crab_MuonGun_step3_asympt/180317_111820/*/*APE*.root'
elif args.year=='2017-noAPE':
    fileName = '/eos/cms/store/group/phys_muon/abbiendi/MuonGun/MuonGun_PTOT-5-2500/crab_MuonGun_step3_asymptNoAPE_ReReco-TrkAli2017-v3/181119_093517/*/*.root'
elif args.year=='2017':
    fileName = '/eos/cms/store/group/phys_muon/abbiendi/MuonGun/MuonGun_PTOT-5-2500/crab_MuonGun_step3_asympt_ReReco-TrkAli2017-v3/181119_083420/0000/*.root'
fileList = [f for f in glob.glob(fileName) if 'inDQM' not in f]
print fileList

#npass = 0
#nglb = 0
#nmuhits = 0
#ntrkhits = 0
#nperr = 0
#nipx = 0
#nipz = 0
#nall = 0
#npassmatch = 0
#nmatchglb = 0
#nmatchmuhits = 0
#nmatchtrkhits = 0
#nmatchperr = 0
#nmatchipx = 0
#nmatchipz = 0
#nmatchall = 0
#nrealpass = 0
#nrealpassmatch = 0

npassid = 0
for FILE in fileList:
    print FILE

    events = Events(FILE)
    #events = Events('/eos/cms/store/group/phys_muon/abbiendi/MuonGun/MuonGun_16_PTOT-5-2500/crab_MuonGun_16_step3_asympt/180622_181848/0000/step3_16_asympt_APE_1.root')


    for e,event in enumerate(events):
        # Get RECO muons
        event.getByLabel(recoMuonLabel,recoMuonHandle)
        recoMuons = recoMuonHandle.product()
        # Get Gen particles
        event.getByLabel(genParticleLabel,genParticleHandle)
        genParticles = genParticleHandle.product()
        # Get vertices
        event.getByLabel(vertexLabel,vertexHandle)
        vertices = vertexHandle.product()
        PV = vertices[0]

        #
        # MC sample is a muon gun so there are always 2 muons 
        # with opposite sign, opposite eta, and opposite phi
        # 
        
        # Require muon to be well-measured
        # For now use selection based off of Begona's study from
        # https://indico.cern.ch/event/767004/
#        for recoMuon in recoMuons:
#            good,glb,muHits,trkHits,pErr,ipx,ipz = isHighPtMuon(recoMuon,PV)
#            if good: npass += 1
#            if glb: nglb += 1
#            if muHits: nmuhits += 1
#            if trkHits: ntrkhits += 1
#            if pErr: nperr += 1
#            if ipx: nipx += 1
#            if ipz: nipz += 1
#            nall += 1
#            #print recoMuon.selectors()
#            if recoMuon.passed(16): nrealpass +=1
        cleanRecoMuons = selection(recoMuons,PV)
        if len(cleanRecoMuons)==0: continue

        # Match reco muon to closest gen muon
        matches = match_to_gen_by_dR(genParticles,cleanRecoMuons)

        #print matches
        for match in matches:
            gen,reco = match
            npassid += 1
#            #good = isHighPtMuon(reco,PV)
#            good,glb,muHits,trkHits,pErr,ipx,ipz = isHighPtMuon(reco,PV)
#            if good: npassmatch += 1
#            if glb: nmatchglb += 1
#            if muHits: nmatchmuhits += 1
#            if trkHits: nmatchtrkhits += 1
#            if pErr: nmatchperr += 1
#            if ipx: nmatchipx += 1
#            if ipz: nmatchipz += 1
#            nmatchall += 1
#            if reco.passed(16): nrealpassmatch +=1
            if args.log: dumpEvent(gen,reco)
            Category = {
                    'allcat':True,
                    'b':(abs(gen.eta())<=1.2),
                    'e':(abs(gen.eta())>1.2),
                    'em':(gen.eta()<-1.2),
                    'ep':(gen.eta()>1.2),
                    }
            Charge = {
                    'qall':True,
                    'qm':(gen.charge()==-1),
                    'qp':(gen.charge()==1),
                    }
            Pt = {
                    'allpt':True,
                    '0to100':(gen.pt()>=0 and gen.pt()<100),
                    '100to200':(gen.pt()>=100 and gen.pt()<200),
                    '200to400':(gen.pt()>=200 and gen.pt()<400),
                    '400to700':(gen.pt()>=400 and gen.pt()<700),
                    '700to1000':(gen.pt()>=700 and gen.pt()<1000),
                    '1000to1500':(gen.pt()>=1000 and gen.pt()<1500),
                    '1500to2000':(gen.pt()>=1500 and gen.pt()<2000),
                    '2000to2500':(gen.pt()>=2000 and gen.pt()<=2500),
                    }
            for cat in cats:
                for q in charges:
                    for pt in pts:
                        if Category[cat] and Charge[q] and Pt[pt]:
                            # fill denominators
                            hists['den'][cat][pt][q]['pt'].Fill(gen.pt())
                            hists['den'][cat][pt][q]['p'].Fill(gen.p())
                            hists['den'][cat][pt][q]['eta'].Fill(gen.eta())
                            hists['den'][cat][pt][q]['phi'].Fill(gen.phi())
                            hists['den'][cat][pt][q]['charge'].Fill(gen.charge())
                            if gen.charge()!=reco.charge():
                                # fill numerators
                                hists['num'][cat][pt][q]['pt'].Fill(gen.pt())
                                hists['num'][cat][pt][q]['p'].Fill(gen.p())
                                hists['num'][cat][pt][q]['eta'].Fill(gen.eta())
                                hists['num'][cat][pt][q]['phi'].Fill(gen.phi())
                                hists['num'][cat][pt][q]['charge'].Fill(gen.charge())
    for r in numden:
        for cat in cats:
            for pt in pts:
                for q in charges:
                    for hist in histTypes:
                        hists[r][cat][pt][q][hist].SetDirectory(0)

#print 'Number of muons passing high-pT ID (no gen matching just all of the reco muons)'
#print 'all cuts',npass,nall
#print 'global',nglb
#print 'muon hits',nmuhits
#print 'tracker hits',ntrkhits
#print 'rel pt err',nperr
#print 'ipx',nipx
#print 'ipz',nipz
#print 'real pass',nrealpass
#print
#print 'Number of muons passing high-pT ID (reco muons matching to gen muons)'
#print 'all cuts',npassmatch,nmatchall
#print 'global',nmatchglb
#print 'muon hits',nmatchmuhits
#print 'tracker hits',nmatchtrkhits
#print 'rel pt err',nmatchperr
#print 'ipx',nmatchipx
#print 'ipz',nmatchipz
#print 'real pass',nrealpassmatch
print 'Number of muons that pass ID and match to gen muon',npassid
# Write histograms to output file
outFile = R.TFile('chargeMisIDPlots'+'_'+NAME+'.root','recreate')
for r in numden:
    for cat in cats:
        for pt in pts:
            for q in charges:
                for hist in histTypes:
                    hists[r][cat][pt][q][hist].Write()
outFile.Close()
