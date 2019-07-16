import argparse
import ROOT as R
from DataFormats.FWLite import Events, Handle

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',dest='FILE',default=None)
args = parser.parse_args()

if args.FILE==None:
    files = [
        Events('www_hme/root/event_318877_102_151594226_1.root'),
        Events('www_hme/root/event_322322_457_853668408_1.root'),
        Events('www_hme/root/event_321414_703_1208387821_1.root'),
        Events('www_hme/root/event_316702_24_32590116_1.root'),
        Events('www_hme/root/event_316944_1157_1528669353_1.root'),
        Events('www_hme/root/event_315357_486_401600258_1.root'),
        Events('www_hme/root/event_320934_641_1014119992_1.root'),
        Events('www_hme/root/event_323525_708_1214685221_1.root'),
        Events('www_hme/root/event_325159_83_58982334_1.root'),
        Events('www_hme/root/event_323693_74_80992155_1.root'),
        Events('www_hme/root/event_321396_782_1236586961_1.root'),
        Events('www_hme/root/event_321434_151_247411653_1.root'),
        Events('www_hme/root/event_325057_130_166770884_1.root'),
        Events('www_hme/root/event_315770_101_111782115_1.root'),
        Events('www_hme/root/event_317527_175_201232187_1.root'),
    ]
else:
    files = [Events(args.FILE)]

jet_handle = Handle('std::vector<pat::Jet>')
jet_label = ('slimmedJets')
muon_handle = Handle('std::vector<pat::Muon>')
muon_label = ('slimmedMuons')
pv_handle = Handle('vector<reco::Vertex>')
pv_label = ('offlineSlimmedPrimaryVertices')
triggerBit_handle, triggerBit_label = Handle('edm::TriggerResults'),('TriggerResults','','HLT')
triggerObject_handle, triggerObject_label = Handle('std::vector<pat::TriggerObjectStandAlone>'),'slimmedPatTrigger'
triggerPrescale_handle, triggerPrescale_label = Handle('pat::PackedTriggerPrescales'),'patTrigger'

for ifile in files:
    for event in ifile:
        print '\n','*'*30,'\n'
        #print dir(event.object())
        #exit()
        event.getByLabel(jet_label,jet_handle)
        jets = jet_handle.product()

        event.getByLabel(muon_label,muon_handle)
        muons = muon_handle.product()

        event.getByLabel(pv_label,pv_handle)
        pvs = pv_handle.product()
        pv = pvs[0]

        event.getByLabel(triggerBit_label, triggerBit_handle)
        triggerBits = triggerBit_handle.product()

        event.getByLabel(triggerObject_label, triggerObject_handle)
        triggerObjects = triggerObject_handle.product()

        event.getByLabel(triggerPrescale_label, triggerPrescale_handle)
        triggerPrescales = triggerPrescale_handle.product()

        triggerNames = event.object().triggerNames(triggerBits)
        print '\n','*'*30,'\n'
        for j,obj in enumerate(triggerObjects):
            obj.unpackNamesAndLabels(event.object(),triggerBits)
            for h,filter_labels in enumerate(obj.filterLabels()):
                for trigger_path,trigger_filter in zip(['HLT_Mu50_v*','HLT_OldMu100_v*','HLT_TkMu100_v*'],['hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q','hltL3fL1sMu22Or25L1f0L2f10QL3Filtered100Q','hltL3fL1sMu25f0TkFiltered100Q']):
                    if obj.filterLabels()[h]==trigger_filter:
                        print trigger_path,trigger_filter,obj.hasPathName(trigger_path)
                for trigger_path,trigger_filter in zip(['HLT_Mu27_v*'],['hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q']):
                    if obj.filterLabels()[h]==trigger_filter:
                        print trigger_path,trigger_filter,obj.hasPathName(trigger_path)




        # Pick the dimuon
        #good_muons = [muon for muon in muons if muon.isHighPtMuon(pv) and muon.pt()>50 and abs(muon.eta())<2.4]
        good_muons = [muon for muon in muons if muon.pt()>30 and abs(muon.eta())<2.4]
        dimuons = []
        for m1,muon1 in enumerate(good_muons):
            for m2,muon2 in enumerate(good_muons[m1:]):
                if muon1.charge()*muon2.charge()>0: continue
                dimuons.append([muon1,muon2])
        dimuons.sort(key=lambda d : d[0].pt()+d[1].pt())
        thedimuon = dimuons[0]

        print 'dilepton mass (no vtx)',(thedimuon[0].p4()+thedimuon[1].p4()).M(),'\n'
        for m in [0,1]:
            muon = thedimuon[m]
            print 'pt',muon.pt(),'eta',muon.eta(),'phi',muon.phi(),'q',muon.charge()
            print 'picky',muon.pickyTrack().pt(),
            print 'dyt',muon.dytTrack().pt(),
            print 'tracker',muon.innerTrack().pt(),
            print 'global',muon.globalTrack().pt()
            print 'dB',muon.dB(), 'iso',muon.isolationR03().sumPt/muon.innerTrack().pt(),'pt err',muon.tunePMuonBestTrack().ptError()/muon.pt()
            print 'px hits',muon.innerTrack().hitPattern().numberOfValidPixelHits(),'tracker layers',muon.innerTrack().hitPattern().trackerLayersWithMeasurement()
            print 'glb mu hits',muon.globalTrack().hitPattern().numberOfValidMuonHits(),'tuneP mu hits',muon.tunePMuonBestTrack().hitPattern().numberOfValidMuonHits()
            print 'match st',muon.numberOfMatchedStations(),'exp match st',muon.expectedNnumberOfMatchedStations(),'st mask',muon.stationMask(),'n match rpc',muon.numberOfMatchedRPCLayers()
            print 

        njets = 0
        for ij,jet in enumerate(jets):
            if (abs(jet.eta()) < 2.4 and jet.pt() > 30 \
                and jet.neutralHadronEnergyFraction() < 0.90 
                and jet.neutralEmEnergyFraction() < 0.90 
                and jet.nConstituents()>1
                #and (jet.chargedMultiplicity()+jet.neutralMultiplicity()) > 1  
                and jet.muonEnergyFraction() < 0.8 
                and jet.chargedHadronEnergyFraction() > 0
                and jet.chargedMultiplicity() > 0 
                and jet.chargedEmEnergyFraction() < 0.80 ):
                #and deltaR((*jet),dil.daughter(0).p4()) > 0.4 
                #and deltaR((*jet),dil.daughter(1).p4())):

                print 
                print jet.pt()
                print jet.eta(),jet.phi()
                print 'csv',jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")
                deepCSV = jet.bDiscriminator("pfDeepCSVJetTags:probbb")+jet.bDiscriminator("pfDeepCSVJetTags:probb")
                if deepCSV>0.7527:
                    deepcsv_wp = 'tight'
                elif deepCSV>0.4184:
                    deepcsv_wp = 'medium'
                elif deepCSV>0.1241:
                    deepcsv_wp = 'loose'
                else:
                    deepcsv_wp = ''
                print 'deepCSV',deepCSV,deepcsv_wp
                deepJet = jet.bDiscriminator('pfDeepFlavourJetTags:probb')+jet.bDiscriminator('pfDeepFlavourJetTags:probbb')+jet.bDiscriminator('pfDeepFlavourJetTags:problepb')
                if deepJet>0.7264:
                    deepjet_wp = 'tight'
                elif deepJet>0.2770:
                    deepjet_wp = 'medium'
                elif deepJet>0.0494:
                    deepjet_wp = 'loose'
                else: 
                    deepjet_wp = ''
                print 'deepJet',deepJet,deepjet_wp



