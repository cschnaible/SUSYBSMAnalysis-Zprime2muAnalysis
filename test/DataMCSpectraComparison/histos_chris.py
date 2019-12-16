#!/usr/bin/env python

ex = '20190716_sa_2'

is2016 = False
is2017 = False
is2018 = True
doSimpleOnly = False
doGE = False
# Global tag, dataset, and cmssw for each year
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable

import sys, os, FWCore.ParameterSet.Config as cms
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cff import switch_hlt_process_name
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cfg import process
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cff import goodDataFiltersMiniAOD
from SUSYBSMAnalysis.Zprime2muAnalysis.NtupleFromPAT_cfi import NtupleFromPAT_MiniAOD,NtupleFromPAT
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples18, samples17, samples16

from SUSYBSMAnalysis.Zprime2muAnalysis.hltTriggerMatch_cfi import trigger_pt_threshold, offline_pt_threshold, prescaled_trigger_pt_threshold, prescaled_offline_pt_threshold, overall_prescale_2016, overall_prescale_2017, overall_prescale_2018, trigger_filters_16, trigger_path_names_16, trigger_path_full_names_16, prescaled_trigger_filters_16, prescaled_trigger_path_names_16, prescaled_trigger_path_full_names_16, trigger_match_2016, prescaled_trigger_match_2016, trigger_filters_18, trigger_path_names_18, trigger_path_full_names_18, prescaled_trigger_filters_18, prescaled_trigger_path_names_18, prescaled_trigger_path_full_names_18, trigger_match_2018, prescaled_trigger_match_2018, prescaled_trigger_path_name_list_16, prescaled_trigger_path_name_list_17, prescaled_trigger_path_name_list_18

from SUSYBSMAnalysis.Zprime2muAnalysis.goodlumis import *

# These modules define the basic selection cuts. For the monitoring
# sets below, we don't need to define a whole new module, since they
# just change one or two cuts -- see below.
import SUSYBSMAnalysis.Zprime2muAnalysis.OurSelectionDec2012_cff as OurSelectionDec2012
import SUSYBSMAnalysis.Zprime2muAnalysis.OurSelection2016_cff as OurSelection2016
import SUSYBSMAnalysis.Zprime2muAnalysis.OurSelection2018_cff as OurSelection2018

process.source.fileNames = [
        # 2016
       #'/store/data/Run2016F/SingleMuon/MINIAOD/23Sep2016-v1/50000/72773077-428F-E611-AAD7-0242AC130003.root',
       #'/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v2/000/284/035/00000/E6006CCE-4C9F-E611-9197-02163E01391D.root'
       #'/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v3/000/284/038/00000/C4A0BF0C-889F-E611-B27D-02163E0144FA.root'
       #'/store/data/Run2016B/SingleMuon/MINIAOD/23Sep2016-v3/00000/1A87BA45-1A98-E611-8CC7-002590E7E00A.root',
        #'/store/data/Run2016C/SingleMuon/MINIAOD/17Jul2018-v1/20000/FEC97F81-0097-E811-A7B9-90E2BACC5EEC.root',
        #'/store/data/Run2016C/SingleMuon/MINIAOD/17Jul2018-v1/20000/FEA9FE48-3997-E811-8BB3-C0BFC0E5682E.root',
        #'/store/data/Run2016G/SingleMuon/MINIAOD/17Jul2018-v1/00000/1A12A529-4490-E811-8ED1-008CFAFBDC0E.root',
        #'/store/mc/RunIISummer16MiniAODv2/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/701163A6-D5CF-E611-84D2-001E674FAF23.root',
        # 2017
        #'/store/mc/RunIIFall17MiniAODv2/ZToMuMu_NNPDF31_13TeV-powheg_M_6000_Inf/MINIAODSIM/MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/90000/0CFF28F9-56FF-E811-B62B-AC1F6B0DE3E8.root',
        #'/store/data/Run2017D/SingleMuon/MINIAOD/31Mar2018-v1/00000/04C38E6C-BF39-E811-9FA7-0CC47A4DEF06.root',
        # 2018
    #'/store/data/Run2018D/SingleMuon/MINIAOD/PromptReco-v2/000/322/068/00000/F8DCA3B9-41B0-E811-8B23-FA163E279E4C.root'
    #'/store/data/Run2018A/SingleMuon/MINIAOD/17Sep2018-v2/270000/40BFE1A5-BEFE-B34B-8836-4ADDB8966C78.root',
    #'/store/mc/RunIIAutumn18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/90000/DD89AFA9-BD25-F346-939F-A9CC68A04B84.root',
    '/store/mc/RunIIAutumn18MiniAOD/ZToMuMu_NNPDF31_13TeV-powheg_M_50_120/MINIAODSIM/102X_upgrade2018_realistic_v15-v2/120000/078DB2B1-40DD-634D-A3CF-D2E377CAFA48.root'
    #'/store/mc/RunIIAutumn18MiniAOD/ZToMuMu_NNPDF31_13TeV-powheg_M_2300_3500/MINIAODSIM/102X_upgrade2018_realistic_v15-v2/120000/E341A5B4-928D-7C43-934E-8529706D5EEA.root',
    #'/store/mc/RunIIAutumn18MiniAOD/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15_ext1-v2/110000/A4788EEA-F867-8349-985B-21AFDB0C9543.root',
    #'/store/mc/RunIIAutumn18MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/120000/8A620F3F-201E-7245-94DF-A9966919C1BD.root',
    #'/store/data/Run2018D/SingleMuon/MINIAOD/22Jan2019-v2/60002/FF86562D-76CB-4B43-90CC-1E76C7D3286C.root',
           ]

process.maxEvents.input = 1000
#process.options.wantSummary = cms.untracked.bool(True)# false di default
process.MessageLogger.cerr.FwkReport.reportEvery = 1000 # default 1000

selMap = {
        'Our2016':OurSelection2016,
        'Our2018':OurSelection2018,
        'Simple':OurSelection2018,
        }

if is2016:
    #MCGT = '94X_mcRun2_asymptotic_v3'
    #dataGT = '94X_dataRun2_v10'
    MCGT = '80X_mcRun2_asymptotic_2016_miniAODv2_v1'
    dataGT_23Sep = '80X_dataRun2_2016SeptRepro_v7'
    #dataGT_p = '80X_dataRun2_Prompt_v16'
    dataGT_p = dataGT_23Sep 
    #dataGT = dataGT_23Sep
    #dataGT = dataGT_p
    dataset_details = [
            #('SingleMuonRun2016B-17Jul2018_ver1-v1', '/SingleMuon/Run2016B-17Jul2018_ver1-v1/MINIAOD', dataGT), # not in JSON!
            #('SingleMuonRun2016B-17Jul2018_ver2-v1', '/SingleMuon/Run2016B-17Jul2018_ver2-v1/MINIAOD', dataGT),
            #('SingleMuonRun2016C-17Jul2018-v1', '/SingleMuon/Run2016C-17Jul2018-v1/MINIAOD', dataGT),
            #('SingleMuonRun2016D-17Jul2018-v1', '/SingleMuon/Run2016D-17Jul2018-v1/MINIAOD', dataGT),
            #('SingleMuonRun2016E-17Jul2018-v1', '/SingleMuon/Run2016E-17Jul2018-v1/MINIAOD', dataGT),
            #('SingleMuonRun2016F-17Jul2018-v1', '/SingleMuon/Run2016F-17Jul2018-v1/MINIAOD', dataGT),
            #('SingleMuonRun2016G-17Jul2018-v1', '/SingleMuon/Run2016G-17Jul2018-v1/MINIAOD', dataGT),
            #('SingleMuonRun2016H-17Jul2018-v1', '/SingleMuon/Run2016H-17Jul2018-v1/MINIAOD', dataGT),
            #('SingleMuonRun2016B-ReReco-v3', '/SingleMuon/Run2016B-23Sep2016-v3/MINIAOD',dataGT_23Sep),
            #('SingleMuonRun2016C-ReReco-v1', '/SingleMuon/Run2016C-23Sep2016-v1/MINIAOD',dataGT_23Sep),
            #('SingleMuonRun2016D-ReReco-v1', '/SingleMuon/Run2016D-23Sep2016-v1/MINIAOD',dataGT_23Sep),
            #('SingleMuonRun2016E-ReReco-v1', '/SingleMuon/Run2016E-23Sep2016-v1/MINIAOD',dataGT_23Sep),
            ('SingleMuonRun2016F-ReReco-v1', '/SingleMuon/Run2016F-23Sep2016-v1/MINIAOD',dataGT_23Sep),
            #('SingleMuonRun2016G-ReReco-v1', '/SingleMuon/Run2016G-23Sep2016-v1/MINIAOD',dataGT_23Sep),
            ('SingleMuonRun2016H-PromptReco-v3', '/SingleMuon/Run2016H-PromptReco-v3/MINIAOD',dataGT_p),
            ('SingleMuonRun2016H-PromptReco-v2', '/SingleMuon/Run2016H-PromptReco-v2/MINIAOD',dataGT_p),
            ]
    trigger_match = trigger_match_2016
    trigger_filters = trigger_filters_16
    trigger_path_names = trigger_path_names_16
    trigger_path_full_names = trigger_path_full_names_16
    prescaled_trigger_match = prescaled_trigger_match_2016
    prescaled_trigger_filters = prescaled_trigger_filters_16
    prescaled_trigger_path_names = prescaled_trigger_path_names_16
    prescaled_trigger_path_full_names = prescaled_trigger_path_full_names_16
    prescale_common_path_name_list = prescaled_trigger_path_name_list_16
    overall_prescale = overall_prescale_2016
    GEyear = 2016
    ex = '2016_'+ex
    sel_names = ['Our2016']
    #OurSelection = OurSelection2016
    lumi_lists = ['Run2016MuonsOnly']
    samples = samples16
    mc_trigger_src = 'selectedPatTrigger'
    #data_trigger_src = 'slimmedPatTrigger' # 94X data
    data_trigger_src = 'selectedPatTrigger'
elif is2017:
    MCGT = '94X_mc2017_realistic_v17'
    dataGT = '94X_dataRun2_v11'
    dataset_details = [
            ('SingleMuonRun2017B-31Mar2018-v1', '/SingleMuon/Run2017B-31Mar2018-v1/MINIAOD', dataGT),
            ('SingleMuonRun2017C-31Mar2018-v1', '/SingleMuon/Run2017C-31Mar2018-v1/MINIAOD', dataGT),
            ('SingleMuonRun2017D-31Mar2018-v1', '/SingleMuon/Run2017D-31Mar2018-v1/MINIAOD', dataGT),
            ('SingleMuonRun2017E-31Mar2018-v1', '/SingleMuon/Run2017E-31Mar2018-v1/MINIAOD', dataGT),
            ('SingleMuonRun2017F-31Mar2018-v1', '/SingleMuon/Run2017F-31Mar2018-v1/MINIAOD', dataGT),
            ]
    trigger_match = trigger_match_2018
    trigger_filters = trigger_filters_18
    trigger_path_names = trigger_path_names_18
    trigger_path_full_names = trigger_path_full_names_18
    prescaled_trigger_match = prescaled_trigger_match_2018
    prescaled_trigger_filters = prescaled_trigger_filters_18
    prescaled_trigger_path_names = prescaled_trigger_path_names_18
    prescaled_trigger_path_full_names = prescaled_trigger_path_full_names_18
    prescale_common_path_name_list = prescaled_trigger_path_name_list_17
    overall_prescale = overall_prescale_2017
    GEyear = 2017
    ex = '2017_'+ex
    sel_names = ['Our2018']
    #OurSelection = OurSelection2018
    lumi_lists = ['Run2017MuonsOnly']
    samples = samples17
    #trigger_src = 'slimmedPatTrigger'
    data_trigger_src = mc_trigger_src = 'slimmedPatTrigger'
elif is2018:
    MCGT = '102X_upgrade2018_realistic_v18'
    dataGT = '102X_dataRun2_Sep2018ABC_v2'
    dataset_details = [
            ('SingleMuonRun2018A-17Sep2018-v2', '/SingleMuon/Run2018A-17Sep2018-v2/MINIAOD', '102X_dataRun2_Sep2018ABC_v2',100),
            ('SingleMuonRun2018B-17Sep2018-v1', '/SingleMuon/Run2018B-17Sep2018-v1/MINIAOD', '102X_dataRun2_Sep2018ABC_v2',100),
            ('SingleMuonRun2018C-17Sep2018-v1', '/SingleMuon/Run2018C-17Sep2018-v1/MINIAOD', '102X_dataRun2_Sep2018ABC_v2',100),
            #('SingleMuonRun2018D-22Jan2019-v2', '/SingleMuon/Run2018D-22Jan2019-v2/MINIAOD', '102X_dataRun2_Prompt_v13',125),
            ]
    trigger_match = trigger_match_2018
    trigger_filters = trigger_filters_18
    trigger_path_names = trigger_path_names_18
    trigger_path_full_names = trigger_path_full_names_18
    prescaled_trigger_match = prescaled_trigger_match_2018
    prescaled_trigger_filters = prescaled_trigger_filters_18
    prescaled_trigger_path_names = prescaled_trigger_path_names_18
    prescaled_trigger_path_full_names = prescaled_trigger_path_full_names_18
    prescale_common_path_name_list = prescaled_trigger_path_name_list_18
    overall_prescale = overall_prescale_2018
    GEyear = 2018
    ex = '2018_'+ex
    sel_names = ['Our2018']
    #OurSelection = OurSelection2018
    lumi_lists = ['Run2018MuonsOnly']
    samples = samples18
    data_trigger_src = mc_trigger_src = 'slimmedPatTrigger'
    

# The histogramming module that will be cloned multiple times below
# for making histograms with different cut/dilepton combinations.

from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cff import electrons_miniAOD
electrons_miniAOD(process)

from SUSYBSMAnalysis.Zprime2muAnalysis.HistosFromPAT_cfi import HistosFromPAT_MiniAOD as HistosFromPAT
####################################
HistosFromPAT.leptonsFromDileptons = True
HistosFromPAT.usekFactor = False #### Set TRUE to use K Factor #####
####################################
ZSkim = False #### Set TRUE to skim dy50to120 with a Z pt < 100 GeV #####
####################################

# Since the prescaled trigger comes with different prescales in
# different runs/lumis, this filter prescales it to a common factor to
# make things simpler.
process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrescaleToCommon_cff')
process.PrescaleToCommonMiniAOD.trigger_paths = prescale_common_path_name_list
process.PrescaleToCommonMiniAOD.overall_prescale = overall_prescale # 500 for 2018

# CandCombiner includes charge-conjugate decays with no way to turn it
# off. To get e.g. mu+mu+ separate from mu-mu-, cut on the sum of the
# pdgIds (= -26 for mu+mu+).
dils = [
    ('MuonsOppSign',    '%(leptons_name)s:muons@+ %(leptons_name)s:muons@-','daughter(0).pdgId() + daughter(1).pdgId() == 0'),
    #('MuonsPlusPlus',  '%(leptons_name)s:muons@+ %(leptons_name)s:muons@+','daughter(0).pdgId() + daughter(1).pdgId() == -26'),
    #('MuonsMinusMinus','%(leptons_name)s:muons@- %(leptons_name)s:muons@-','daughter(0).pdgId() + daughter(1).pdgId() == 26'),
    #('MuonsSameSign',  '%(leptons_name)s:muons@- %(leptons_name)s:muons@-',''),
    #('MuonsAllSigns',  '%(leptons_name)s:muons@- %(leptons_name)s:muons@-',''),
    ]

# Define sets of cuts for which to make plots. If using a selection
# that doesn't have a trigger match, need to re-add a hltHighLevel
# filter somewhere below.
if doSimpleOnly:
    sel_names = ['Simple']
cuts = {}
for sel_name in sel_names:
    if doSimpleOnly:
        cuts['Simple'] = selMap['Simple']
    else:
        cuts[sel_name] = selMap[sel_name]
        cuts[sel_name+'MuPrescaled'] = selMap[sel_name]
        cuts[sel_name+'MuPrescaledCommon'] = selMap[sel_name]


# Loop over all the cut sets defined and make the lepton, allDilepton
# (combinatorics only), and dilepton (apply cuts) modules for them.
for cut_name, Selection in cuts.iteritems():
    # Keep track of modules to put in the path for this set of cuts.
    path_list = []

    # Clone the LeptonProducer to make leptons with the set of cuts
    # we're doing here flagged.  I.e., muon_cuts in LeptonProducer
    # just marks each muon with a userInt "cutFor" that is 0 if it
    # passes the cuts, and non-0 otherwise; it does not actually drop
    # any of the muons. The cutFor flag actually gets ignored by the
    # LooseTightPairSelector in use for all the cuts above, at
    # present.
    path_list.append(process.egmGsfElectronIDSequence)
        
    leptons_name = cut_name + 'Leptons'
    if cut_name == 'Simple':
        muon_cuts = ''
    elif 'MuPrescaled' in cut_name:
        muon_cuts = Selection.loose_cut.replace('pt > %s' % offline_pt_threshold, 'pt > %s' % prescaled_offline_pt_threshold)
    else:
        muon_cuts = Selection.loose_cut

    leptons = process.leptonsMini.clone(muon_cuts = muon_cuts)
    leptons.doGE = doGE
    leptons.GEyear = GEyear
    #leptons.trigger_summary = cms.InputTag(trigger_src)
    if (len(trigger_filters)>0 or len(prescaled_trigger_filters)>0) and cut_name!='Simple':
        leptons.trigger_filters = trigger_filters
        leptons.trigger_path_names = trigger_path_names
        leptons.trigger_path_full_names = trigger_path_full_names
        leptons.prescaled_trigger_filters = prescaled_trigger_filters
        leptons.prescaled_trigger_path_names = prescaled_trigger_path_names
        leptons.prescaled_trigger_path_full_names = prescaled_trigger_path_full_names

    setattr(process, leptons_name, leptons)
    path_list.append(leptons)

    # Make all the combinations of dileptons we defined above.
    for dil_name, dil_decay, dil_cut in dils:

        # For the EmuVeto path, we only care about e-mu events.
        if cut_name == 'EmuVeto' and 'Electron' not in dil_name:
            continue

        # For the MuPrescaled paths, we don't care about e-mu events.
        if 'MuPrescaled' in cut_name and 'Electron' in dil_name:
            continue

        # Only make opposite sign objects for Our2018 selection
        if 'Our2018'==cut_name and 'MuonsOppSign' not in dil_name:
            continue

        # Only make opposite-sign objects for MuPrescaled cut set
        if 'MuPrescaled' in cut_name and 'MuonsOppSign' not in dil_name:
            continue

        # Only make MuonsAllSigns objects for simple cut set
        if 'Simple' in cut_name and dil_name!='MuonsAllSigns':
            continue

        # Unique names for the modules: allname for the allDileptons,
        # and name for dileptons.
        name = cut_name + dil_name
        allname = 'all' + name

        alldil = Selection.allDimuons.clone(decay = dil_decay % locals(), cut = dil_cut)
        if 'AllSigns' in dil_name:
            alldil.checkCharge = cms.bool(False)

        dil = Selection.dimuons.clone(src = cms.InputTag(allname))

        # Implement the differences to the selections; currently, as
        # in Zprime2muCombiner, the cuts in loose_cut and
        # tight_cut are the ones actually used to drop leptons, and
        # not the ones passed into the LeptonProducer to set cutFor above.
        if cut_name == 'Simple':
            alldil.electron_cut_mask = cms.uint32(0)
            alldil.loose_cut = ''#'isGlobalMuon && pt > 20.'
            alldil.tight_cut = ''
            #dil.max_candidates = 100
            dil.max_candidates = 100
            dil.sort_by_pt = True
            dil.do_remove_overlap = True
            #dil.prefer_Z=False
            dil.prefer_Z=True
            if hasattr(dil, 'back_to_back_cos_angle_min'):
                delattr(dil, 'back_to_back_cos_angle_min')
            if hasattr(dil, 'vertex_chi2_max'):
                delattr(dil, 'vertex_chi2_max')
            if hasattr(dil, 'dpt_over_pt_max'):
                delattr(dil, 'dpt_over_pt_max')
        elif cut_name == 'OurNoIso':
            alldil.loose_cut = alldil.loose_cut.value().replace(' && isolationR03.sumPt / innerTrack.pt < 0.10', '')
        elif 'MuPrescaled' in cut_name:
            alldil.loose_cut = alldil.loose_cut.value().replace('pt > %s' % offline_pt_threshold, 'pt > %s' % prescaled_offline_pt_threshold)
            alldil.tight_cut = prescaled_trigger_match

        # Histos now just needs to know which leptons and dileptons to use.
        histos = HistosFromPAT.clone(lepton_src = cms.InputTag(leptons_name, 'muons'), dilepton_src = cms.InputTag(name))

        # Add all these modules to the process and the path list.
        setattr(process, allname, alldil)
        setattr(process, name, dil)
        setattr(process, name + 'Histos', histos)
        path_list.append(alldil * dil * histos)

    # Finally, make the path for this set of cuts.
    pathname = 'path' + cut_name
    process.load('SUSYBSMAnalysis.Zprime2muAnalysis.DileptonPreselector_cfi')
    process.load("SUSYBSMAnalysis.Zprime2muAnalysis.EventCounter_cfi")
    if cut_name=='Simple':
        pobj = process.EventCounter * process.muonPhotonMatchMiniAOD * reduce(lambda x,y: x*y, path_list)
    else:
        pobj = process.EventCounter * process.dileptonPreselector *  process.muonPhotonMatchMiniAOD * reduce(lambda x,y: x*y, path_list)


    if 'Common' in cut_name:
        ptc_name = 'PrescaleToCommon'
        ptc = process.PrescaleToCommonMiniAOD.clone()
        setattr(process, ptc_name, ptc)
        pobj = getattr(process,ptc_name) * pobj 

    path = cms.Path(pobj)
    setattr(process, pathname, path)

def switch_trigger_obj(process,inputName):
    for name in cuts.keys():
        getattr(process,name+'Leptons').trigger_summary = cms.InputTag(inputName)

def apply_gen_filters(process,sampleName):
    from SUSYBSMAnalysis.Zprime2muAnalysis.MCFilters_cfi import DYPtZskim, TTbarGenMassFilter, DibosonGenMassFilter, TauTauFilter
    addFilter = False
    process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrunedMCLeptons_cfi')
    if ('dy50to120' in sampleName or 'dyInclusive' in sampleName) and ZSkim:
        mcFilter = DYPtZskim.clone()
        addFilter = True
    elif 'ttbar_lep_50to500' in sampleName:
        mcFilter = TTbarGenMassFilter.clone()
        addFilter = True
    elif 'WW_50to200' in sampleName:
        mcFilter = DibosonGenMassFilter.clone()
        addFilter = True
    elif 'dyTauTau' in sampleName:
        mcFilter = TauTauFilter.clone()
        addFilter = True
    if addFilter:
        setattr(process,sampleName+'Filter',mcFilter)
        mcFilterPath = getattr(process,sampleName+'Filter')
        for path_name, path in process.paths.iteritems():
            getattr(process,path_name).insert(0,mcFilterPath)

def ntuplify(process, cut='Simple', dil_name='MuonsAllSigns', is_mc=False):
    dimu_src_tag = cut+dil_name
    ntuple = NtupleFromPAT_MiniAOD.clone(dimu_src=cms.InputTag(dimu_src_tag))
    ntuple.trigger_paths = prescale_common_path_name_list

    if is_mc:
        from SUSYBSMAnalysis.Zprime2muAnalysis.HardInteraction_cff import hardInteraction_MiniAOD
        ntuple.hardInteraction = hardInteraction_MiniAOD
        ntuple.TriggerResults_src = cms.InputTag('TriggerResults','','PAT')
        process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrunedMCLeptons_cfi')
        obj = process.prunedMCLeptons
        obj.src = cms.InputTag('prunedGenParticles')
        ntuple.Prescale_src = cms.InputTag('patTrigger','','PAT')
        ntuple.L1Prescale_min_src = cms.InputTag('patTrigger','','PAT')
    else:
        if is2016:
            #ntuple.Prescale_src = cms.InputTag('patTrigger','','DQM') # 94X rereco
            #ntuple.L1Prescale_min_src = cms.InputTag('patTrigger','','DQM') # 94X rereco
            ntuple.Prescale_src = cms.InputTag('patTrigger','','RECO')
            ntuple.L1Prescale_min_src = cms.InputTag('patTrigger','','RECO')
        elif is2017:
            ntuple.Prescale_src = cms.InputTag('patTrigger','','PAT')
            ntuple.L1Prescale_min_src = cms.InputTag('patTrigger','','PAT')

    if hasattr(process,'path'+cut): 
        ntuple_name = cut+dil_name+'Ntuple'
        setattr(process,ntuple_name,ntuple)
        ntuplepath = getattr(process,ntuple_name)

        path = getattr(process,'path'+cut)
        if is_mc:
            path *= obj * ntuplepath
        else:
            path *= ntuplepath

def printify(process):
    process.MessageLogger.categories.append('PrintEvent')

    process.load('HLTrigger.HLTcore.triggerSummaryAnalyzerAOD_cfi')
    process.triggerSummaryAnalyzerAOD.inputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT')
    if hasattr(process, 'pathSimple'):
        process.pathSimple *= process.triggerSummaryAnalyzerAOD

    process.PrintOriginalMuons = cms.EDAnalyzer('PrintEvent', muon_src = cms.InputTag('cleanPatMuonsTriggerMatch'), trigger_results_src = cms.InputTag('TriggerResults','','HLT'))
    process.pathSimple *= process.PrintOriginalMuons

    pe = process.PrintEventSimple = cms.EDAnalyzer('PrintEvent', dilepton_src = cms.InputTag('SimpleMuonsPlusMuonsMinus'))
    if hasattr(process, 'pathSimple'):
        process.pathSimple *= process.PrintEventSimple

    #- 2011-2012 selection (Nlayers > 8)
    #process.PrintEventOurNew = pe.clone(dilepton_src = cms.InputTag('OurNewMuonsPlusMuonsMinus'))
    #process.PrintEventOurNewSS = pe.clone(dilepton_src = cms.InputTag('OurNewMuonsSameSign'))
    #process.PrintEventOurNewEmu = pe.clone(dilepton_src = cms.InputTag('OurNewMuonsElectronsOppSign'))
    #process.pathOurNew *= process.PrintEventOurNew * process.PrintEventOurNewSS * process.PrintEventOurNewEmu

    #- December 2012 selection (Nlayers > 5, re-tuned TuneP, dpT/pT < 0.3)
    if hasattr(process, 'pathOur2012'):
        process.PrintEventOur2012    = pe.clone(dilepton_src = cms.InputTag('Our2012MuonsPlusMuonsMinus'))
        process.PrintEventOur2012SS  = pe.clone(dilepton_src = cms.InputTag('Our2012MuonsSameSign'))
        process.PrintEventOur2012Emu = pe.clone(dilepton_src = cms.InputTag('Our2012MuonsElectronsOppSign'))
        process.pathOur2012 *= process.PrintEventOur2012 * process.PrintEventOur2012SS * process.PrintEventOur2012Emu

def add_filters(process,is_mc=True):
    for cut_name, Selection in cuts.iteritems():
        path_name = 'path'+cut_name
        if hasattr(process,path_name) and cut_name != 'Simple':
            process.load('SUSYBSMAnalysis.Zprime2muAnalysis.goodData_cff')
            for dataFilter in goodDataFiltersMiniAOD:
                if is_mc:
                    dataFilter.src = cms.InputTag('TriggerResults','','PAT') # to submit MC
                getattr(process,path_name).insert(0,dataFilter)

def for_data(process):
    # Add filters
    add_filters(process,is_mc=False)
    # make a SimpleMuonsAllSignsNtuple
    ntuplify(process) 
    for sel_name in sel_names:
        if sel_name=='Simple': continue
        # make a Our2018MuonsOppSignNtuple
        ntuplify(process,cut=sel_name,dil_name='MuonsOppSign') 
        # make a Our2018MuPrescaledMuonsOppSignNtuple
        ntuplify(process,cut=sel_name+'MuPrescaled',dil_name='MuonsOppSign') 
        ntuplify(process,cut=sel_name+'MuPrescaledCommon',dil_name='MuonsOppSign') 
    switch_trigger_obj(process,data_trigger_src)
    if is2016 or is2017:
        getattr(process,'PrescaleToCommon').Prescale_src = cms.InputTag('patTrigger')
        getattr(process,'PrescaleToCommon').L1Prescale_min_src = cms.InputTag('patTrigger','l1min')
        getattr(process,'PrescaleToCommon').L1Prescale_max_src = cms.InputTag('patTrigger','l1max')

def for_mc(process, hlt_process_name):
    process.GlobalTag.globaltag = MCGT
    # Add filters
    add_filters(process)
    # make a SimpleMuonsAllSignsNtuple
    ntuplify(process,is_mc=True) 
    for sel_name in sel_names:
        if sel_name=='Simple': continue
        # make a Our2018MuonsOppSignNtuple
        ntuplify(process,cut=sel_name,dil_name='MuonsOppSign',is_mc=True)
        # make a Our2018MuPrescaledMuonsOppSignNtuple
        ntuplify(process,cut=sel_name+'MuPrescaled',dil_name='MuonsOppSign',is_mc=True) 
        ntuplify(process,cut=sel_name+'MuPrescaledCommon',dil_name='MuonsOppSign',is_mc=True) 
    # this must be done last (i.e. after anything that might have an InputTag for something HLT-related)
    switch_hlt_process_name(process, hlt_process_name)
    #apply_gen_filters(process,'dyInclusive50_madgraph')
    #apply_gen_filters(process,'ttbar_lep_50to500_v1')
    switch_trigger_obj(process,mc_trigger_src)
    #if is2016 or is2017:
    getattr(process,'PrescaleToCommon').Prescale_src = cms.InputTag('patTrigger','','PAT')
    getattr(process,'PrescaleToCommon').L1Prescale_min_src = cms.InputTag('patTrigger','l1min','PAT')
    getattr(process,'PrescaleToCommon').L1Prescale_max_src = cms.InputTag('patTrigger','l1max','PAT')

if 'int_data' in sys.argv:
    process.GlobalTag.globaltag = dataGT 
    for_data(process)
    #printify(process)
    #from FWCore.PythonUtilities.LumiList import LumiList
    #jsonname = 'json/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON_MuonPhys.txt'
    #jsonname = 'Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON_MuonPhys.txt'
    #process.source.lumisToProcess = LumiList(filename = jsonname).getVLuminosityBlockRange()
    
if 'int_mc' in sys.argv:
    for_mc(process, 'HLT')
    #printify(process)
    
# Automatic addition of the customisation function from Validation.Performance.TimeMemoryInfo
#from Validation.Performance.TimeMemoryInfo import customise
#process = customise(process)
#f = file('outfile_histos1', 'w')
#f.write(process.dumpPython())
#f.close()

if __name__ == '__main__' and 'submit' in sys.argv:
    crab_cfg = '''
from CRABClient.UserUtilities import config,getUsernameFromSiteDB
config = config()
config.General.requestName = 'ana_datamc_%(name)s%(extra)s'
config.General.workArea = 'crab'
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'histos_crab.py'   
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB  = 4000
config.Data.inputDataset =  '%(ana_dataset)s'
config.Data.inputDBS = 'global'
config.Data.publication = False
job_control
config.Data.outputDatasetTag = 'ana_datamc_%(name)s%(extra)s'
config.Data.outLFNDirBase = '/store/user/'+getUsernameFromSiteDB()
config.Site.storageSite = 'T2_CH_CERN'
'''
#config.Data.outLFNDirBase = '/store/group/phys_exotica/dimuon/2018/datamc'
    
    just_testing = 'testing' in sys.argv
    extra = '_'+ex if ex!='' else ''
    # Run on data.
    if 'no_data' not in sys.argv:


        jobs = []
        for lumi_name in lumi_lists:
            ll = eval(lumi_name + '_ll') if lumi_name != 'NoLumiMask' else None
            for dd in dataset_details:
                jobs.append(dd + (lumi_name, ll))
                
        for dataset_name, ana_dataset, globaltag, njobs, lumi_name, lumi_list in jobs:

            json_fn = 'tmp.json'
            lumi_list.writeJSON(json_fn)
            lumi_mask = json_fn

            name = '%s_%s' % (lumi_name, dataset_name)
            print name

            new_py = open('histos_chris.py').read()
            new_py += "\nfor_data(process)\n"
            new_py += "\nprocess.GlobalTag.globaltag = '%s'"%(globaltag)
            #process.GlobalTag.globaltag = globaltag
            open('histos_crab.py', 'wt').write(new_py)

            new_crab_cfg = crab_cfg % locals()

            job_control = '''
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = %(njobs)s
config.Data.lumiMask = '%(lumi_mask)s'
''' % locals()
#config.Data.splitting = 'Automatic'

            new_crab_cfg = new_crab_cfg.replace('job_control', job_control)
            open('crabConfig.py', 'wt').write(new_crab_cfg)

            if not just_testing:
                os.system('crab submit -c crabConfig.py')
            else:
                os.system('crab submit -c crabConfig.py --dryrun')
                #cmd = 'diff histos.py histos_crab.py | less'
                #print cmd
                #os.system(cmd)
                #cmd = 'less crab.py'
                #print cmd
                #os.system(cmd)

        if not just_testing:
            os.system('rm crabConfig.py crabConfig.pyc histos_crab.py histos_crab.pyc tmp.json')

    if 'no_mc' not in sys.argv:
        # Set crab_cfg for MC.
        crab_cfg = crab_cfg.replace('job_control','''
config.Data.splitting = 'EventAwareLumiBased'
config.Data.totalUnits = -1
config.Data.unitsPerJob  = %(neventsperjob)s
    ''')

       
        #dyList = ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf']
        dyList = ['dy400to800']
        #mcList = ['WW_50to200','WW_200to600','WW_600to1200_v1','WW_600to1200_v2','WW_600to1200_v3','WW_1200to2500','WW_2500toInf']
        #mcList += ['ttbar_lep_50to500_v1','ttbar_lep_50to500_v2','ttbar_lep_500to800_0to20','ttbar_lep_500to800_41to65','ttbar_lep_800to1200','ttbar_lep_1200to1800','ttbar_lep_1800toInf','ttbar_lep_500to800']
        mcList = ['WW_50to200','WW_200to600']
        mcList += ['ttbar_lep_50to500_v1','ttbar_lep_800to1200']
        #mcList = ['WZTo3LNu','WZTo2L2Q','ZZTo2L2Nu_ext1','ZZTo2L2Nu_ext2','ZZTo2L2Nu','ZZTo4L_ext1','ZZTo4L_ext2','ZZTo4L_v1','ZZTo4L_v2','ZZTo2L2Q','tW','tbarW','tW_v2','tW_v3','tbarW_v2','tbarW_v3']
        for sample in samples:
            name = sample.name
            ana_dataset = sample.dataset
            if ana_dataset==None: continue
            #if name not in mcList: continue
            if name not in dyList: continue
            #print name, ana_dataset

            new_py = open('histos_chris.py').read()
            new_py += "\nfor_mc(process,'HLT')\n"
            new_py += "\napply_gen_filters(process,\"%(name)s\")\n"%locals()
            open('histos_crab.py', 'wt').write(new_py)

            if 'ttbar_lep_50to500' in name or name=='WW_50to200' or name=='WW_200to600': 
                neventsperjob = 100000
            elif name in ['tW_v3','tbarW_v3','ZZTo2L2Q','ZZTo4L_ext2','ZZTo4L_ext1','ZZTo2L2Nu_ext2','ZZTo2L2Nu_ext1','WZTo2L2Q']:
                neventsperjob = 200000
            else:
                neventsperjob = 10000
            print name,ana_dataset
            print sample.nevents,neventsperjob,sample.nevents/float(neventsperjob)

            #neventsperjob = 50000
            # in case i need to resubmit, the 1 i
            #if 'madgraph' in name or 'amcatnlo' in name: 
            #    neventsperjob=100000 # down from 500000
            #elif 'dyJetsToLL' in name:
            #    neventsperjob= 10000 # down from 50000
            #elif 'dy' in name:
            #    neventsperjob=10000
            #else:
            #    neventsperjob= 500000
            #print name, neventsperjob, sample.nevents, sample.nevents/float(neventsperjob)
            #print
            #continue

            open('crabConfig.py', 'wt').write(crab_cfg % locals())
            if not just_testing:
                os.system('crab submit -c crabConfig.py')
            else:
                os.system('crab submit -c crabConfig.py --dryrun')
                #cmd = 'diff histos.py histos_crab.py | less'
                #print cmd
                #os.system(cmd)
                #cmd = 'less crabConfig.py'
                #print cmd
                #os.system(cmd)

        if not just_testing:
            os.system('rm crabConfig.py histos_crab.py histos_crab.pyc')

