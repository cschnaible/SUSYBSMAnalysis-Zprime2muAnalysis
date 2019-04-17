#!/usr/bin/env python

miniAOD = True

import argparse
import sys, os, FWCore.ParameterSet.Config as cms
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cff import switch_hlt_process_name
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cfg import process
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cff import goodDataFiltersMiniAOD
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples

parser = argparse.ArgumentParser()
parser.add_argument('-mc','--doMC',action='store_true',help='Run on MC samples defined in MCSamples')
parser.add_argument('-data','--doData',action='store_true',help='Run on CMS data')
parser.add_argument('--dry_run',action='store_true',help='Dry run - make all files but do not submit jobs')
parser.add_argument('-c','--crab',action='store_true',help='Submit jobs to CRAB')
parser.add_argument('-i','--int',action='store_true',help='Run jobs locally')
args = parser.parse_args()

if args.doMC==False and args.doData==False:
    raise ValueError('One of doMC and doData arguments must be set to true to do something')


process.source.fileNames = [
        #'/store/data/Run2018A/SingleMuon/MINIAOD/06Jun2018-v1/410000/CCA4DBD1-FF83-E811-988F-FA163E5991FE.root'
        '/store/data/Run2018D/SingleMuon/MINIAOD/PromptReco-v2/000/322/068/00000/F8DCA3B9-41B0-E811-8B23-FA163E279E4C.root'
           ]
process.maxEvents.input = -1
#process.options.wantSummary = cms.untracked.bool(True)# false di default
process.MessageLogger.cerr.FwkReport.reportEvery = 10000 # default 1000

from SUSYBSMAnalysis.Zprime2muAnalysis.hltTriggerMatch_cfi import trigger_match, prescaled_trigger_match, trigger_paths, prescaled_trigger_paths, overall_prescale, offline_pt_threshold, prescaled_offline_pt_threshold, trigger_filters, trigger_path_names, prescaled_trigger_filters, prescaled_trigger_path_names, prescaled_trigger_match_2018

# Since the prescaled trigger comes with different prescales in
# different runs/lumis, this filter prescales it to a common factor to
# make things simpler.
process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrescaleToCommon_cff')
process.PrescaleToCommon.trigger_paths = prescaled_trigger_paths
process.PrescaleToCommon.overall_prescale = overall_prescale

process.PrescaleToCommonMiniAOD.trigger_paths = prescaled_trigger_paths
process.PrescaleToCommonMiniAOD.overall_prescale = overall_prescale

# The histogramming module that will be cloned multiple times below
# for making histograms with different cut/dilepton combinations.

from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cff import electrons_miniAOD
electrons_miniAOD(process)

from SUSYBSMAnalysis.Zprime2muAnalysis.HistosFromPAT_cfi import HistosFromPAT_MiniAOD as HistosFromPAT
HistosFromPAT.leptonsFromDileptons = True
from SUSYBSMAnalysis.Zprime2muAnalysis.NtupleFromPAT_cfi import NtupleFromPAT_MiniAOD as NtupleFromPAT
from SUSYBSMAnalysis.Zprime2muAnalysis.EfficiencyFromMC_cfi import EfficiencyFromMCMini as EfficiencyFromMC
from SUSYBSMAnalysis.Zprime2muAnalysis.ResolutionUsingMC_cfi import ResolutionUsingMC_MiniAOD as ResolutionUsingMC
ResolutionUsingMC.leptonsFromDileptons = True
ResolutionUsingMC.doQoverP = True

####################################
HistosFromPAT.usekFactor = False #### Set TRUE to use K Factor #####
####################################
ZSkim = False #### Set TRUE to skim dy50to120 with a Z pt < 100 GeV #####
####################################

# These modules define the basic selection cuts. For the monitoring
# sets below, we don't need to define a whole new module, since they
# just change one or two cuts -- see below.
import SUSYBSMAnalysis.Zprime2muAnalysis.OurSelectionDec2012_cff as OurSelectionDec2012
import SUSYBSMAnalysis.Zprime2muAnalysis.OurSelection2016_cff as OurSelection2016
import SUSYBSMAnalysis.Zprime2muAnalysis.OurSelection2018_cff as OurSelection2018

# CandCombiner includes charge-conjugate decays with no way to turn it
# off. To get e.g. mu+mu+ separate from mu-mu-, cut on the sum of the
# pdgIds (= -26 for mu+mu+).
dils = [('MuonsPlusMuonsMinus',          '%(leptons_name)s:muons@+ %(leptons_name)s:muons@-',         'daughter(0).pdgId() + daughter(1).pdgId() == 0'),
    #('MuonsPlusMuonsPlus',           '%(leptons_name)s:muons@+ %(leptons_name)s:muons@+',         'daughter(0).pdgId() + daughter(1).pdgId() == -26'),
    #('MuonsMinusMuonsMinus',         '%(leptons_name)s:muons@- %(leptons_name)s:muons@-',         'daughter(0).pdgId() + daughter(1).pdgId() == 26'),
    #('MuonsSameSign',                '%(leptons_name)s:muons@- %(leptons_name)s:muons@-',         ''),
    #('MuonsAllSigns',                '%(leptons_name)s:muons@- %(leptons_name)s:muons@-',         ''),
    ]

# Define sets of cuts for which to make plots. If using a selection
# that doesn't have a trigger match, need to re-add a hltHighLevel
# filter somewhere below.
cuts = {
    #'Our2012'  : OurSelectionDec2012,
    #'Our2016'  : OurSelection2016,
    'Our2018'  : OurSelection2018,
    #'OurNoIso' : OurSelectionDec2012,
    'Simple'   : OurSelectionDec2012, # The selection cuts in the module listed here are ignored below.
    #'OurMuPrescaledNew'  : OurSelectionNew,
    #'OurMuPrescaled2012' : OurSelectionDec2012
    }

    

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
    if len(trigger_filters)>0 and (cut_name=='Our2018' or cut_name=='Simple'):
        leptons.trigger_filters = trigger_filters
        leptons.trigger_path_names = trigger_path_names
        leptons.prescaled_trigger_filters = prescaled_trigger_filters
        leptons.prescaled_trigger_path_names = prescaled_trigger_path_names

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
            alldil.loose_cut = 'isGlobalMuon && pt > 20.'
            alldil.tight_cut = ''
            dil.max_candidates = 100
            dil.sort_by_pt = True
            dil.do_remove_overlap = False
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
            assert alldil.tight_cut == trigger_match
            if len(prescaled_trigger_filters)>0:
                alldil.tight_cut = prescaled_trigger_match_2018
            else:
                alldil.tight_cut = prescaled_trigger_match

        # Histos now just needs to know which leptons and dileptons to use.
        histos = HistosFromPAT.clone(lepton_src = cms.InputTag(leptons_name, 'muons'), dilepton_src = cms.InputTag(name))
        setattr(process, allname, alldil)
        setattr(process, name, dil)
        setattr(process, name + 'Histos', histos)
        # only do this for MC!
        if 'no_mc' not in sys.argv:
            efficiency = EfficiencyFromMC.clone(dimuon_src=name,acceptance_max_eta_2=2.4)
            resolution = ResolutionUsingMC.clone(lepton_src = cms.InputTag(leptons_name, 'muons'), dilepton_src = cms.InputTag(name))
            setattr(process, name + 'Resolution', resolution)
            setattr(process, name + 'Efficiency', efficiency)
        # Add all these modules to the process and the path list.
        if cut=='Our2018' and dil_name=='MuonsPlusMuonsMinus':
            # Add Ntuple with only dimuons that pass best selection
            ntuple = NtupleFromPAT.clone(dimu_src = cms.InputTag(name))
            setattr(process, name + 'Ntuple', ntuple)
            path_list.append(alldil * dil * histos * resolution * efficiency * ntuple)
        else:
            path_list.append(alldil * dil * histos * resolution * efficiency)



    # Finally, make the path for this set of cuts.
    pathname = 'path' + cut_name
    process.load('SUSYBSMAnalysis.Zprime2muAnalysis.DileptonPreselector_cfi')
    process.load("SUSYBSMAnalysis.Zprime2muAnalysis.EventCounter_cfi")
    pobj = process.EventCounter * process.dileptonPreseletor *  process.muonPhotonMatchMiniAOD * reduce(lambda x,y: x*y, path_list)


    if 'VBTF' not in cut_name and cut_name != 'Simple':
        process.load('SUSYBSMAnalysis.Zprime2muAnalysis.goodData_cff')
        for dataFilter in goodDataFiltersMiniAOD:
            #setattr(process,dataFilter 
            pobj = dataFilter * pobj


    ####### Now it seems that there are no prescaled path ########
    if 'MuPrescaled' in cut_name:
        pobj = process.PrescaleToCommonMiniAOD * pobj 

    # This is a MC-specific bloc of code
    # define the list of MC samples to be read here. be careful that if WWinclusive or tautau sample are not commented it will apply the filters when running locally.

    if 'no_mc' not in sys.argv:
        for sample in samples:
            
            if 'dy50to120' in sample.name and ZSkim:
                process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrunedMCLeptons_cfi')
                process.DYGenMassFilter = cms.EDFilter('DyPt_ZSkim',
                                   src = cms.InputTag('prunedGenParticles'),
                                   min_mass = cms.double(0),
                                   max_mass = cms.double(100), 
                                   )
                pobj = process.DYGenMassFilter * pobj

            if 'ttbar_lep50to500' in sample.name:
                process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrunedMCLeptons_cfi')
                process.DYGenMassFilter = cms.EDFilter('TTbarSelection',
                                   src = cms.InputTag('prunedGenParticles'),
                                   min_mass = cms.double(50),
                                   max_mass = cms.double(500), 
                                   )
                pobj = process.DYGenMassFilter * pobj
                
            if 'WWinclusive' in sample.name:
                process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrunedMCLeptons_cfi')
                process.DYGenMassFilter = cms.EDFilter('DibosonGenMass',
                                       src = cms.InputTag('prunedGenParticles'),
                                       min_mass = cms.double(50),
                                       max_mass = cms.double(200), 
                                       )
                pobj = process.DYGenMassFilter * pobj
                     
            if 'dyInclusive50' in sample.name:
                process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrunedMCLeptons_cfi')
                process.DYGenMassFilter = cms.EDFilter('TauTauSelection',
                                       src = cms.InputTag('prunedGenParticles'),                                      
                                       )
                pobj = process.DYGenMassFilter * pobj


        
    path = cms.Path(pobj)
    setattr(process, pathname, path)


def ntuplify(process, fill_gen_info=False):
    process.SimpleNtupler = NtupleFromPAT.clone() # Default is SimpleNtuple
    if fill_gen_info: # mc
        process.SimpleNtupler.TriggerResults_src = cms.InputTag('TriggerResults', '', 'PAT')
        from SUSYBSMAnalysis.Zprime2muAnalysis.HardInteraction_cff import hardInteraction
        process.SimpleNtupler.hardInteraction = hardInteraction
    else: # data
        process.SimpleNtupler.TriggerResults_src = cms.InputTag('TriggerResults', '', 'RECO')

    if hasattr(process, 'pathSimple'): # if the simple path exists, add SimpleNtuple to it
        if fill_gen_info:
            process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrunedMCLeptons_cfi')
            obj = process.prunedMCLeptons
            obj.src = cms.InputTag('prunedGenParticles')
            process.pathSimple *=obj * process.SimpleNtupler 
        else:
            process.pathSimple *= process.SimpleNtupler 

# to have ntuples also running in interactive way
process.GlobalTag.globaltag = '101X_dataRun2_Prompt_v11'
ntuplify(process)

def printify(process):
    process.MessageLogger.categories.append('PrintEvent')

    process.load('HLTrigger.HLTcore.triggerSummaryAnalyzerAOD_cfi')
    process.triggerSummaryAnalyzerAOD.inputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT')
    if hasattr(process, 'pathSimple'):
        process.pathSimple *= process.triggerSummaryAnalyzerAOD

    process.PrintOriginalMuons = cms.EDAnalyzer('PrintEvent', muon_src = cms.InputTag('cleanPatMuonsTriggerMatch'), trigger_results_src = cms.InputTag('TriggerResults','','HLT'))
    process.pathSimple *= process.PrintOriginalMuons

    pe = process.PrintEventSimple = cms.EDAnalyzer('PrintEvent', dilepton_src = cms.InputTag('SimpleMuonsPlusMuonsMinus'))

    # Simple selection
    if hasattr(process, 'pathSimple'):
        process.pathSimple *= process.PrintEventSimple

    #- December 2012 selection (Nlayers > 5, re-tuned TuneP, dpT/pT < 0.3)
    if hasattr(process, 'pathOur2012'):
        process.PrintEventOur2012    = pe.clone(dilepton_src = cms.InputTag('Our2012MuonsPlusMuonsMinus'))
        process.PrintEventOur2012SS  = pe.clone(dilepton_src = cms.InputTag('Our2012MuonsSameSign'))
        process.PrintEventOur2012Emu = pe.clone(dilepton_src = cms.InputTag('Our2012MuonsElectronsOppSign'))
        process.pathOur2012 *= process.PrintEventOur2012 * process.PrintEventOur2012SS * process.PrintEventOur2012Emu
    #- 2016 Selection (2012 + matched muon station)
    if hasattr(process, 'pathOur2016'):
        process.PrintEventOur2016    = pe.clone(dilepton_src = cms.InputTag('Our2016MuonsPlusMuonsMinus'))
        process.PrintEventOur2016SS  = pe.clone(dilepton_src = cms.InputTag('Our2016MuonsSameSign'))
        process.PrintEventOur2016Emu = pe.clone(dilepton_src = cms.InputTag('Our2016MuonsElectronsOppSign'))
        process.pathOur2016 *= process.PrintEventOur2016 * process.PrintEventOur2016SS * process.PrintEventOur2016Emu
    #- 2018 Selection (2016 + prefer Z candidates + (glb||tuneP) valid hits)
    if hasattr(process, 'pathOur2018'):
        process.PrintEventOur2018    = pe.clone(dilepton_src = cms.InputTag('Our2018MuonsPlusMuonsMinus'))
        process.PrintEventOur2018SS  = pe.clone(dilepton_src = cms.InputTag('Our2018MuonsSameSign'))
        process.PrintEventOur2018Emu = pe.clone(dilepton_src = cms.InputTag('Our2018MuonsElectronsOppSign'))
        process.pathOur2018 *= process.PrintEventOur2018 * process.PrintEventOur2018SS * process.PrintEventOur2018Emu

def check_prescale(process, trigger_paths, hlt_process_name='HLT'):
    process.load('SUSYBSMAnalysis.Zprime2muAnalysis.CheckPrescale_cfi')
    process.CheckPrescale.trigger_paths = cms.vstring(*trigger_paths)
    process.pCheckPrescale = cms.Path(process.CheckPrescale)

def for_data(process):
    process.GlobalTag.globaltag = '101X_dataRun2_Prompt_v11'
    ntuplify(process)# SimpleNtuple
    #check_prescale(process, trigger_paths) ####### Now it seams that there are no prescaled path ########

def for_mc(process, hlt_process_name, fill_gen_info):
    # Change to MC for 2018 when it's available
    process.GlobalTag.globaltag = '102X_upgrade2018_realistic_v15'
    ntuplify(process, fill_gen_info) # SimpleNtuple
    # this must be done last (i.e. after anything that might have an InputTag for something HLT-related)
    switch_hlt_process_name(process, hlt_process_name)

if 'int_data' in sys.argv:
    for_data(process)
    printify(process)
    
if 'int_mc' in sys.argv:
    for_mc(process, 'HLT', False)
    printify(process)
    
if 'gogo' in sys.argv:
    for_data(process)
    printify(process)
    
    n = sys.argv.index('gogo')
    run, lumi, event = sys.argv[n+1], sys.argv[n+2], sys.argv[n+3]
    print run, lumi, event
    run = int(run)
    lumi = int(lumi)
    event = int(event)
    filename = [x for x in sys.argv if x.endswith('.root')]
    if filename:
        filename = filename[0]
    else:
        dataset = get_dataset(run)
        print dataset
        output = os.popen('dbs search --url https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet --query="find file where dataset=%s and run=%s and lumi=%s"' % (dataset, run, lumi)).read()
        print repr(output)
        filename = [x for x in output.split('\n') if x.endswith('.root')][0]
    print filename
    process.source.fileNames = [filename]
    from SUSYBSMAnalysis.Zprime2muAnalysis.cmsswtools import set_events_to_process
    set_events_to_process(process, [(run, event)])

if __name__ == '__main__' and 'submit' in sys.argv:
    crab_cfg = '''
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()
config.General.requestName = 'ana_datamc_%(name)s'
config.General.workArea = 'crab'
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'histos_crab.py'   
config.Data.inputDataset =  '%(ana_dataset)s'
config.Data.inputDBS = 'global'
job_control
config.Data.publication = False
config.Data.outputDatasetTag = 'ana_datamc_%(name)s'
config.Data.outLFNDirBase = '/store/group/phys_exotica/dimuon/2018/crab'
config.Site.storageSite = 'T2_CH_CERN'
'''
    
    just_testing = 'testing' in sys.argv
        
    # Run on data.
    if 'no_data' not in sys.argv:
        from SUSYBSMAnalysis.Zprime2muAnalysis.goodlumis import *


        dataset_details = [
            # PPD recommendation for 2018A PromptReco 
            # 06Jun2018-v1 + PromptReco-v3
            ('SingleMuonRun2018A-06June2018-v1', '/SingleMuon/Run2018A-06Jun2018-v1/MINIAOD'), 
            ('SingleMuonRun2018A-PromptReco-v3', '/SingleMuon/Run2018A-PromptReco-v3/MINIAOD'),
            ('SingleMuonRun2018B-PromptReco-v1', '/SingleMuon/Run2018B-PromptReco-v1/MINIAOD'),
            ('SingleMuonRun2018B-PromptReco-v2', '/SingleMuon/Run2018B-PromptReco-v2/MINIAOD'),
            ('SingleMuonRun2018C-PromptReco-v1', '/SingleMuon/Run2018C-PromptReco-v1/MINIAOD'),
            ('SingleMuonRun2018C-PromptReco-v2', '/SingleMuon/Run2018C-PromptReco-v2/MINIAOD'),
            ('SingleMuonRun2018C-PromptReco-v3', '/SingleMuon/Run2018C-PromptReco-v3/MINIAOD'),
            ('SingleMuonRun2018D-PromptReco-v2', '/SingleMuon/Run2018D-PromptReco-v2/MINIAOD'),
        ]

        lumi_lists = ['Run2018MuonsOnly']

        jobs = []
        for lumi_name in lumi_lists:
            ll = eval(lumi_name + '_ll') if lumi_name != 'NoLumiMask' else None
            for dd in dataset_details:
                jobs.append(dd + (lumi_name, ll))
                
        for dataset_name, ana_dataset, lumi_name, lumi_list in jobs:

            json_fn = 'tmp.json'
            lumi_list.writeJSON(json_fn)
            lumi_mask = json_fn

            name = '%s_%s' % (lumi_name, dataset_name)
            print name

            new_py = open('histos.py').read()
            new_py += "\nfor_data(process)\n"
            open('histos_crab.py', 'wt').write(new_py)

            new_crab_cfg = crab_cfg % locals()

            job_control = '''
config.Data.splitting = 'Automatic'
config.Data.lumiMask = '%(lumi_mask)s'
''' % locals()

            new_crab_cfg = new_crab_cfg.replace('job_control', job_control)
            open('crabConfig.py', 'wt').write(new_crab_cfg)

            if not just_testing:
                os.system('crab submit -c crabConfig.py')
            else:
                cmd = 'diff histos.py histos_crab.py | less'
                print cmd
                os.system(cmd)
                cmd = 'less crab.py'
                print cmd
                os.system(cmd)

        if not just_testing:
            os.system('rm crabConfig.py crabConfig.pyc histos_crab.py histos_crab.pyc tmp.json')

    if 'no_mc' not in sys.argv:
        # Set crab_cfg for MC.
        crab_cfg = crab_cfg.replace('job_control','''
config.Data.splitting = 'EventAwareLumiBased'
#config.Data.splitting = 'FileBased'
config.Data.totalUnits = -1
config.Data.unitsPerJob  = 10000
''')

       
        for sample in samples:
            ana_dataset = sample.dataset
            print sample.name
            print ana_dataset

            new_py = open('histos.py').read()
            new_py += "\nfor_mc(process,fill_gen_info=True)\n"
            open('histos_crab.py', 'wt').write(new_py)

            open('crabConfig.py', 'wt').write(crab_cfg % locals())
            if not just_testing:
                os.system('crab submit -c crabConfig.py')
            else:
                cmd = 'diff histos.py histos_crab.py | less'
                print cmd
                os.system(cmd)
                cmd = 'less crabConfig.py'
                print cmd
                os.system(cmd)

        if not just_testing:
            os.system('rm crabConfig.py histos_crab.py histos_crab.pyc')

