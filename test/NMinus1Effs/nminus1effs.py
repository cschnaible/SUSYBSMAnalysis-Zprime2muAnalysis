#!/usr/bin/env python

miniAOD = True
ex='20190724'

import sys, os, FWCore.ParameterSet.Config as cms
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cfg import process
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cff import goodDataFiltersMiniAOD,switch_hlt_process_name
if miniAOD:
    from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cff import electrons_miniAOD
    electrons_miniAOD(process)
    from SUSYBSMAnalysis.Zprime2muAnalysis.HistosFromPAT_cfi import HistosFromPAT_MiniAOD as HistosFromPAT
else:
    from SUSYBSMAnalysis.Zprime2muAnalysis.HistosFromPAT_cfi import HistosFromPAT

from SUSYBSMAnalysis.Zprime2muAnalysis.OurSelection2018_cff import loose_cut, trigger_match_2018, tight_cut, allDimuons
#from SUSYBSMAnalysis.Zprime2muAnalysis.hltTriggerMatch_cfi import trigger_filters_18, trigger_path_names_18, prescaled_trigger_filters_18, prescaled_trigger_path_names, prescaled_trigger_match_2018, trigger_match_2018, prescaled_offline_pt_threshold, offline_pt_threshold, prescaled_trigger_paths, overall_prescale
from SUSYBSMAnalysis.Zprime2muAnalysis.hltTriggerMatch_cfi import trigger_pt_threshold, offline_pt_threshold, prescaled_trigger_pt_threshold, prescaled_offline_pt_threshold, overall_prescale_2016, overall_prescale_2017, overall_prescale_2018, trigger_filters_16, trigger_path_names_16, trigger_path_full_names_16, prescaled_trigger_filters_16, prescaled_trigger_path_names_16, prescaled_trigger_path_full_names_16, trigger_match_2016, prescaled_trigger_match_2016, trigger_filters_18, trigger_path_names_18, trigger_path_full_names_18, prescaled_trigger_filters_18, prescaled_trigger_path_names_18, prescaled_trigger_path_full_names_18, trigger_match_2018, prescaled_trigger_match_2018, prescaled_trigger_path_name_list_16, prescaled_trigger_path_name_list_17, prescaled_trigger_path_name_list_18


trigger_match = trigger_match_2018
trigger_filters = trigger_filters_18
trigger_path_names = trigger_path_names_18
trigger_path_full_names = trigger_path_full_names_18
prescaled_trigger_match = prescaled_trigger_match_2018
prescaled_trigger_filters = prescaled_trigger_filters_18
prescaled_trigger_path_names = prescaled_trigger_path_names_18
prescaled_trigger_path_full_names = prescaled_trigger_path_full_names_18
#prescale_common_path_name_list = prescaled_trigger_path_name_list_18
#overall_prescale = overall_prescale_2018
prescale_common_path_name_list = prescaled_trigger_path_name_list_17
overall_prescale = overall_prescale_2017

process.source.fileNames = [
        #'/store/data/Run2018A/SingleMuon/MINIAOD/06Jun2018-v1/410000/CCA4DBD1-FF83-E811-988F-FA163E5991FE.root'
        #'/store/data/Run2018D/SingleMuon/MINIAOD/PromptReco-v2/000/322/068/00000/F8DCA3B9-41B0-E811-8B23-FA163E279E4C.root'
        '/store/mc/RunIIAutumn18MiniAOD/ZToMuMu_NNPDF31_13TeV-powheg_M_50_120/MINIAODSIM/102X_upgrade2018_realistic_v15-v2/120000/078DB2B1-40DD-634D-A3CF-D2E377CAFA48.root'
           ]
#process.source = cms.Source ("PoolSource",
#                             fileNames =  cms.untracked.vstring(
#                                 '/store/data/Run2018C/SingleMuon/MINIAOD/17Sep2018-v1/120000/FAB77E55-E1DE-0D43-A907-BD709A4B2B1D.root'
#                                 ),
#                             )

process.maxEvents.input = 1000
#process.GlobalTag.globaltag ='dummy' # dummy value to be changed below
#process.MessageLogger.cerr.FwkReport.reportEvery = 1 # default 1000

# Define the numerators and denominators, removing cuts from the
# allDimuons maker. "NoX" means remove cut X entirely (i.e. the
# loose_cut denominators), "TiX" means move cut X from the loose_cut
# to the tight_cut (meaning only one muon instead of two has to pass
# the cut).  "NoNo" means remove nothing (i.e. the numerator). This
# will break if loose_, tight_cut strings are changed upstream, so we
# try to check those with a simple string test below.

cuts = [
    ('Pt',      'pt > 53'),
    ('DB',      'abs(dB) < 0.2'),
    ('Iso',     'isolationR03.sumPt / innerTrack.pt < 0.10'),
    ('TkLayers','globalTrack.hitPattern.trackerLayersWithMeasurement > 5'),
    ('PxHits',  'globalTrack.hitPattern.numberOfValidPixelHits >= 1'),
    ('MuHits',  '( (globalTrack.hitPattern.numberOfValidMuonHits > 0) || (tunePMuonBestTrack.hitPattern.numberOfValidMuonHits > 0) )'),
    ('MuMatch', '(( numberOfMatchedStations>1 ) || ( numberOfMatchedStations==1 && ( expectedNnumberOfMatchedStations<2 || !(stationMask==1 || stationMask==16) || numberOfMatchedRPCLayers>2)))'),
    ]

for name, cut in cuts:
    if type(cut) != tuple:
        cut = (cut,)
        
    lc = loose_cut
    for c in cut:
        if c not in lc:
            raise ValueError('cut "%s" not in cut string "%s"' % (c, lc))
        lc = lc.replace(' && ' + c, '') # Relies on none of the cuts above being first in the list.

    obj_no = allDimuons.clone(cut = 'daughter(0).pdgId() + daughter(1).pdgId() == 0', loose_cut = lc)
    #obj_no = allDimuons.clone(loose_cut = lc,tight_cut = tight_cut.replace(trigger_match, ''))#N-2
    setattr(process, 'allDimuonsNo' + name, obj_no)
    
    obj_ti = obj_no.clone(tight_cut = tight_cut + ' && ' + ' && '.join(cut))
    setattr(process, 'allDimuonsTi' + name, obj_ti)

process.allDimuonsNoNo = allDimuons.clone(cut = 'daughter(0).pdgId() + daughter(1).pdgId() == 0')
process.allDimuonsNoTrgMtch = allDimuons.clone(cut = 'daughter(0).pdgId() + daughter(1).pdgId() == 0', tight_cut = tight_cut.replace(trigger_match_2018, ''))

# Check trigger efficiency for Mu27 as well
# (assume that all other selection efficiencies are the same for both prescaled and unprescaled trigger paths)
# Replace (Mu50||OldMu100||TkMu100) with prescaled Mu27 and keep offline muon pt threshold at 53 GeV
process.allDimuonsNoNoMuPrescaledPt53 = allDimuons.clone(cut = 'daughter(0).pdgId() + daughter(1).pdgId() == 0',tight_cut=prescaled_trigger_match_2018)
# Replace (Mu50||OldMu100||TkMu100) with prescaled Mu27 and replace 53 GeV offline pt threshold with 27 GeV
loose_cut_prescaled = loose_cut.replace('pt > %s' % offline_pt_threshold, 'pt > %s' % prescaled_offline_pt_threshold)
process.allDimuonsNoNoMuPrescaledPt27 = allDimuons.clone(cut = 'daughter(0).pdgId() + daughter(1).pdgId() == 0',tight_cut=prescaled_trigger_match_2018,loose_cut=loose_cut_prescaled)
process.allDimuonsNoMuPrescaledTrgMtchPt27 = allDimuons.clone(cut = 'daughter(0).pdgId() + daughter(1).pdgId() == 0', tight_cut = tight_cut.replace(trigger_match_2018, ''),loose_cut=loose_cut_prescaled)
process.allDimuonsNoPtMuPrescaled = getattr(process,'allDimuonsNoPt').clone(tight_cut=prescaled_trigger_match_2018)
#process.allDimuonsNoNo      = allDimuons.clone(tight_cut = tight_cut.replace(trigger_match, ''))#N-2

alldimusprescaled = []
alldimus = []
for x in dir(process):
    if 'allDimuonsNo' in x or 'allDimuonsTi' in x: 
        if 'Prescaled' in x:
            alldimusprescaled.append(x)
        else:
            alldimus.append(x)

#alldimus = [x for x in dir(process) if 'allDimuonsNo' in x or 'allDimuonsTi' in x]

# Sanity check that the replaces above did something.
for x in alldimus:
    if 'NoNo' in x:
        continue
    o = getattr(process, x)
    assert o.loose_cut.value() != loose_cut or o.tight_cut.value() != tight_cut

process.load("SUSYBSMAnalysis.Zprime2muAnalysis.EventCounter_cfi")
# Since the prescaled trigger comes with different prescales in
# different runs/lumis, this filter prescales it to a common factor to
# make things simpler.
process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrescaleToCommon_cff')
process.PrescaleToCommonMiniAOD.trigger_paths = prescale_common_path_name_list
process.PrescaleToCommonMiniAOD.overall_prescale = overall_prescale # 500 for 2018
if miniAOD:
    #process.load('SUSYBSMAnalysis.Zprime2muAnalysis.DileptonPreselector_cfi')####?????
    leptons = process.leptonsMini.clone()
    leptons.trigger_filters = trigger_filters_18
    leptons.trigger_path_names = trigger_path_names
    leptons.prescaled_trigger_filters = prescaled_trigger_filters_18
    leptons.prescaled_trigger_path_names = prescaled_trigger_path_names
    process.leptons = leptons
    path = process.egmGsfElectronIDSequence * process.EventCounter * process.muonPhotonMatchMiniAOD * process.leptons * reduce(lambda x,y: x*y, [getattr(process, x) for x in alldimus])
    pathPrescaled = process.PrescaleToCommonMiniAOD * process.egmGsfElectronIDSequence * process.EventCounter * process.muonPhotonMatchMiniAOD * process.leptons * reduce(lambda x,y: x*y, [getattr(process, x) for x in alldimusprescaled])
    process.path = cms.Path(path)
    process.pathPrescaled = cms.Path(pathPrescaled)
else:
    process.leptons = process.leptons.clone()
    process.p = cms.Path(process.muonPhotonMatch * process.leptons * reduce(lambda x,y: x*y, [getattr(process, x) for x in alldimus]))



# For all the allDimuons producers, make dimuons producers, and
# analyzers to make the histograms.
for alld in alldimus+alldimusprescaled:
    dimu = process.dimuons.clone(src = alld)
    name = alld.replace('allD', 'd')
    setattr(process, name, dimu)
    hists = HistosFromPAT.clone(dilepton_src = name, leptonsFromDileptons = True)
    setattr(process, name.replace('dimuons', ''), hists)
    if 'Prescaled' in alld:
        process.pathPrescaled *= dimu * hists
    else:
        process.path *= dimu * hists

# Handle the cuts that have to be applied at the
# Zprime2muCompositeCandidatePicker level.
process.allDimuonsBASE = allDimuons.clone(cut = 'daughter(0).pdgId() + daughter(1).pdgId() == 0')
process.path *= process.allDimuonsBASE
process.dimuonsNoB2B     = process.dimuons.clone(src = 'allDimuonsBASE')
process.dimuonsNoVtxProb = process.dimuons.clone(src = 'allDimuonsBASE')
process.dimuonsNoDptPt   = process.dimuons.clone(src = 'allDimuonsBASE')
#process.dimuonsNoB2B     = process.dimuons.clone(src = 'allDimuonsN2')#N-2
#process.dimuonsNoVtxProb = process.dimuons.clone(src = 'allDimuonsN2')#N-2
#process.dimuonsNoDptPt   = process.dimuons.clone(src = 'allDimuonsN2')#N-2
delattr(process.dimuonsNoB2B,     'back_to_back_cos_angle_min')
delattr(process.dimuonsNoVtxProb, 'vertex_chi2_max')
delattr(process.dimuonsNoDptPt,   'dpt_over_pt_max')

process.path *= process.allDimuons
for dimu in ['dimuonsNoB2B', 'dimuonsNoVtxProb', 'dimuonsNoDptPt']:
    hists = HistosFromPAT.clone(dilepton_src = dimu, leptonsFromDileptons = True)
    setattr(process, dimu.replace('dimuons', ''), hists)
    process.path *= getattr(process, dimu) * hists

# Special case to remove |dB| and B2B cuts simultaneously, as they can
# be correlated (anti-cosmics).
process.allDimuonsNoCosm = process.allDimuons.clone(cut = 'daughter(0).pdgId() + daughter(1).pdgId() == 0', loose_cut = loose_cut.replace(' && abs(dB) < 0.2', ''))
#process.allDimuonsNoCosm = process.allDimuons.clone(loose_cut = loose_cut.replace(' && abs(dB) < 0.2', ''), tight_cut = tight_cut.replace(trigger_match, '')) #N-2
process.dimuonsNoCosm = process.dimuons.clone(src = 'allDimuonsNoCosm')
delattr(process.dimuonsNoCosm, 'back_to_back_cos_angle_min')
process.NoCosm = HistosFromPAT.clone(dilepton_src = 'dimuonsNoCosm', leptonsFromDileptons = True)
process.path *= process.allDimuonsNoCosm * process.dimuonsNoCosm * process.NoCosm

def add_filters(process,is_mc=True):
    process.load('SUSYBSMAnalysis.Zprime2muAnalysis.goodData_cff')
    for dataFilter in goodDataFiltersMiniAOD:
        if is_mc:
            dataFilter.src = cms.InputTag('TriggerResults','','PAT') # to submit MC
        for path_name, path in process.paths.iteritems():
            getattr(process,path_name).insert(0,dataFilter)

def apply_gen_filters(process,sampleName):
    ZSkim = False
    from SUSYBSMAnalysis.Zprime2muAnalysis.MCFilters_cfi import DYPtZskim, TTbarGenMassFilter, DibosonGenMassFilter, TauTauFilter
    addFilter = False
    if miniAOD:
        process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrunedMCLeptons_cfi')
    if ('dy50to120' in sampleName or 'dyInclusive' in sampleName) and ZSkim:
        mcFilter = DYPtZskim.clone()
        addFilter = True
    elif 'ttbar_lep50to500' in sampleName:
        mcFilter = TTbarGenMassFilter.clone()
        addFilter = True
    elif 'WWinclusive' in sampleName:
        mcFilter = DibosonGenMassFilter.clone()
        addFilter = True
    elif 'dyInclusive50' in sampleName:
        mcFilter = TauTauFilter.clone()
        addFilter = True
    if addFilter:
        if not miniAOD:
            mcFilter.src = cms.InputTag('prunedMCLeptons')
        setattr(process,sampleName+'Filter',mcFilter)
        mcFilterPath = getattr(process,sampleName+'Filter')
        for path_name, path in process.paths.iteritems():
            getattr(process,path_name).insert(0,mcFilterPath)

def for_data(process):
    # Add filters
    add_filters(process,is_mc=False)
    #process.GlobalTag.globaltag = '102X_dataRun2_Sep2018Rereco_v1'
    #process.GlobalTag.globaltag = '102X_dataRun2_Prompt_v11'

def for_mc(process, hlt_process_name):
    process.GlobalTag.globaltag = '102X_upgrade2018_realistic_v12'
    # Add filters
    add_filters(process)
    # this must be done last (i.e. after anything that might have an InputTag for something HLT-related)
    switch_hlt_process_name(process, hlt_process_name)

if 'int_data' in sys.argv:
    for_data(process)
    #printify(process)

if 'int_mc' in sys.argv:
    for_mc(process, 'HLT')
    #printify(process)

if __name__ == '__main__' and 'submit' in sys.argv:
    crab_cfg = \
'''
from CRABClient.UserUtilities import config,getUsernameFromSiteDB
config = config()
config.General.requestName = 'ana_nminus1_%(name)s%(extra)s'
config.General.workArea = 'crab'
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'nminus1effs_crab.py'
config.JobType.allowUndistributedCMSSW = True
config.Data.inputDataset =  '%(ana_dataset)s' 
config.Data.inputDBS = 'global'
config.Data.publication = False
job_control
config.Data.outputDatasetTag = 'ana_nminus1_%(name)s'
config.Data.outLFNDirBase = '/store/user/'+getUsernameFromSiteDB()
config.Site.storageSite = 'T2_CH_CERN'
'''
#config.Data.outLFNDirBase = '/store/group/phys_exotica/dimuon/2018/nminus1effs'

    just_testing = 'testing' in sys.argv
    extra = '_'+ex if ex!='' else ''
    if not 'no_data' in sys.argv:
        from SUSYBSMAnalysis.Zprime2muAnalysis.goodlumis import *
        dataset_details = [
            # Prompt Reco for ABC
            #('SingleMuonRun2018A-06June2018-v1', '/SingleMuon/Run2018A-06Jun2018-v1/MINIAOD'), 
            #('SingleMuonRun2018A-PromptReco-v3', '/SingleMuon/Run2018A-PromptReco-v3/MINIAOD'),
            #('SingleMuonRun2018B-PromptReco-v1', '/SingleMuon/Run2018B-PromptReco-v1/MINIAOD'),
            #('SingleMuonRun2018B-PromptReco-v2', '/SingleMuon/Run2018B-PromptReco-v2/MINIAOD'),
            #('SingleMuonRun2018C-PromptReco-v1', '/SingleMuon/Run2018C-PromptReco-v1/MINIAOD'),
            #('SingleMuonRun2018C-PromptReco-v2', '/SingleMuon/Run2018C-PromptReco-v2/MINIAOD'),
            #('SingleMuonRun2018C-PromptReco-v3', '/SingleMuon/Run2018C-PromptReco-v3/MINIAOD'),

            # PPD recommendation to use 17Sep2018 ReReco for ABC, 22Jan2019 for D
            #('SingleMuonRun2018A-17Sep2018-v2', '/SingleMuon/Run2018A-17Sep2018-v2/MINIAOD', '102X_dataRun2_Sep2018ABC_v2'),#100),
            #('SingleMuonRun2018B-17Sep2018-v1', '/SingleMuon/Run2018B-17Sep2018-v1/MINIAOD', '102X_dataRun2_Sep2018ABC_v2'),#100),
            ('SingleMuonRun2018C-17Sep2018-v1', '/SingleMuon/Run2018C-17Sep2018-v1/MINIAOD', '102X_dataRun2_Sep2018ABC_v2'),#100),
            #('SingleMuonRun2018D-22Jan2019-v2', '/SingleMuon/Run2018D-22Jan2019-v2/MINIAOD', '102X_dataRun2_Prompt_v13'),#125),
        ]
        lumi_lists = [
			'Run2018MuonsOnly',
		]
        jobs = []
        for lumi_name in lumi_lists:
            ll = eval(lumi_name + '_ll') if lumi_name != 'NoLumiMask' else None
            for dd in dataset_details:
                jobs.append(dd + (lumi_name, ll))


        for dataset_name, ana_dataset, globaltag, lumi_name, lumi_list in jobs:
            json_fn = 'tmp.json'
            lumi_list.writeJSON(json_fn)
            lumi_mask = json_fn

            name = '%s_%s' % (lumi_name, dataset_name)
            print name
            print ana_dataset
            print globaltag
            print lumi_name

            new_py = open('nminus1effs.py').read()
            new_py += "\nprocess.GlobalTag.globaltag = '%s'"%(globaltag)
            new_py += "\nfor_data(process)\n"
            #if '17Sep2018' in dataset_name:
            #    new_py += "\nprocess.GlobalTag.globaltag = '102X_dataRun2_Sep2018Rereco_v1'\n"
            #else:
            #    new_py += "\nprocess.GlobalTag.globaltag = '102X_dataRun2_Prompt_v11'\n"
            open('nminus1effs_crab.py', 'wt').write(new_py)

            new_crab_cfg = crab_cfg % locals()
            job_control = \
'''
config.Data.splitting = 'Automatic'
config.Data.lumiMask = '%(lumi_mask)s'
''' % locals()

            new_crab_cfg = new_crab_cfg.replace('job_control', job_control)
            open('crabConfig.py', 'wt').write(new_crab_cfg)

            if not just_testing:
                os.system('crab submit -c crabConfig.py') #--dryrun
                os.system('rm crabConfig.py nminus1effs_crab.py nminus1effs_crab.pyc tmp.json')

    if not 'no_mc' in sys.argv:
        #from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples18 as samples
        #mclist = ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300',\
        #        'dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf',\
        #        'WZTo3LNu','WZTo2L2Q','ZZTo2L2Nu_ext1','ZZTo2L2Nu_ext2','ZZTo4L_ext1','ZZTo4L_ext2','ZZTo2L2Q',\
        #        'tbarW_v3','tbarW_v2','tW_v3','tW_v2','dyTauTau_madgraph']
        from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples17 as samples
        mclist = ['WW_50to200','WW_200to600','WW_600to1200_v1','WW_600to1200_v2','WW_600to1200_v3',\
                'WW_1200to2500','WW_2500toInf',\
                'ttbar_lep_50to500_v2','ttbar_lep_500to800_0to20','ttbar_lep_500to800_41to65',\
                'ttbar_lep_500to800','ttbar_lep_1200to1800','ttbar_lep_1800toInf']
        for sample in samples:
            name = sample.name
            ana_dataset = sample.dataset
            if ana_dataset==None: continue
            if name not in mclist: continue
            print name
            print ana_dataset

            new_py = open('nminus1effs.py').read()
            #new_py += "\nprocess.GlobalTag.globaltag = '102X_upgrade2018_realistic_v18'\n"
            new_py += "\nprocess.GlobalTag.globaltag = '94X_mc2017_realistic_v17'\n"
            new_py += "\nfor_mc(process,'HLT')\n"
            new_py += "\napply_gen_filters(process,\"%(name)s\")\n"%locals()
            open('nminus1effs_crab.py', 'wt').write(new_py)

            new_crab_cfg = crab_cfg % locals()
            neventsperjob = 10000 if 'dy' in name else 200000
            job_control = \
'''
config.Data.splitting = 'EventAwareLumiBased'
config.Data.totalUnits = -1
config.Data.unitsPerJob  = %(neventsperjob)s
'''%locals()
            new_crab_cfg = new_crab_cfg.replace('job_control',job_control)
            open('crabConfig.py','wt').write(new_crab_cfg)

            if not just_testing:
                os.system('crab submit -c crabConfig.py')
                os.system('rm crabConfig.py nminus1effs_crab.py nminus1effs_crab.pyc')
