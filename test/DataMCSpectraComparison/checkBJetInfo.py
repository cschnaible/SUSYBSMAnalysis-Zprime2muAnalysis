import ROOT as R
from DataFormats.FWLite import Events, Handle

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
jet_handle = Handle('std::vector<pat::Jet>')
jet_label = ('slimmedJets')
muon_handle = Handle('std::vector<pat::Muon>')
muon_label = ('slimmedMuons')
pv_handle = Handle('vector<reco::Vertex>')
pv_label = ('offlineSlimmedPrimaryVertices')

for ifile in files:
    for event in ifile:
        print '\n','*'*30,'\n'
        event.getByLabel(jet_label,jet_handle)
        jets = jet_handle.product()
        event.getByLabel(muon_label,muon_handle)
        muons = muon_handle.product()
        event.getByLabel(pv_label,pv_handle)
        pvs = pv_handle.product()
        pv = pvs[0]

        # Pick the dimuon
        good_muons = [muon for muon in muons if muon.isHighPtMuon(pv) and muon.pt()>50 and abs(muon.eta())<2.4]
        dimuons = []
        for m1,muon1 in enumerate(good_muons):
            for m2,muon2 in enumerate(good_muons[m1:]):
                if muon1.charge()*muon2.charge()>0: continue
                dimuons.append([muon1,muon2])
        dimuons.sort(key=lambda d : d[0].pt()+d[1].pt())
        thedimuon = dimuons[0]

        print (thedimuon[0].p4()+thedimuon[1].p4()).M()
        for m in [0,1]:
            print thedimuon[m].pt(), thedimuon[m].eta(), thedimuon[m].phi()

        njets = 0
        for ij,jet in enumerate(jets):
#            #if ij>0:continue
#            print ij
#            print jet.pt()
#            print jet.eta()
#            print 'csv',jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")
#            print 'deepcsvb',jet.bDiscriminator("pfDeepCSVJetTags:probb")
#            print 'deepcsvbb',jet.bDiscriminator("pfDeepCSVJetTags:probbb")
#            print 'deepcsvb+bb',jet.bDiscriminator("pfDeepCSVJetTags:probbb")+jet.bDiscriminator("pfDeepCSVJetTags:probb")
#            print 
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
                #print 'deepcsv b ',jet.bDiscriminator("pfDeepCSVJetTags:probb")
                #print 'deepcsv bb',jet.bDiscriminator("pfDeepCSVJetTags:probbb")
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
                #print 'deepjet b',jet.bDiscriminator('pfDeepFlavourJetTags:probb')
                #print 'deepjet bb',jet.bDiscriminator('pfDeepFlavourJetTags:probbb')
                #print 'deepjet lepb',jet.bDiscriminator('pfDeepFlavourJetTags:problepb')
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


