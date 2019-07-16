#!/usr/bin/env python

ex = '20190529'

# User beware: note do_all_track_fits=True can potentially cause memory problems on CRAB
# Remove unnecessary EDAnalyzers or cut sets from the path
do_all_track_fits = False 
is2016 = False 
is2017 = True
is2018 = False
# Global tag, dataset, and cmssw for each year
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable

import sys, os, FWCore.ParameterSet.Config as cms
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cfg import process
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cff import electrons_miniAOD
electrons_miniAOD(process)

from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples18, samples17, samples16

from SUSYBSMAnalysis.Zprime2muAnalysis.hltTriggerMatch_cfi import trigger_pt_threshold, offline_pt_threshold, prescaled_trigger_pt_threshold, prescaled_offline_pt_threshold, trigger_filters_16, trigger_path_names_16,trigger_path_full_names_16, prescaled_trigger_filters_16, prescaled_trigger_path_names_16, prescaled_trigger_path_full_names_16,trigger_match_2016, prescaled_trigger_match_2016, trigger_filters_18, trigger_path_names_18, trigger_path_full_names_18, prescaled_trigger_filters_18, prescaled_trigger_path_names_18, prescaled_trigger_path_full_names_18, trigger_match_2018, prescaled_trigger_match_2018

# These modules define the basic selection cuts. For the monitoring
# sets below, we don't need to define a whole new module, since they
# just change one or two cuts -- see below.
import SUSYBSMAnalysis.Zprime2muAnalysis.OurSelection2016_cff as OurSelection2016
import SUSYBSMAnalysis.Zprime2muAnalysis.OurSelection2018_cff as OurSelection2018

process.source.fileNames = [
        # 2016 
        '/store/mc/RunIISummer16MiniAODv2/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/F4380BF8-CBCF-E611-8891-0CC47A546E5E.root',
        # 2017
        #'/store/mc/RunIIFall17MiniAODv2/ZToMuMu_NNPDF31_13TeV-powheg_M_50_120/MINIAODSIM/MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/90000/FA79AB8D-87FE-E811-88F0-246E96D14B5C.root',
    #'/store/data/Run2018D/SingleMuon/MINIAOD/PromptReco-v2/000/322/068/00000/F8DCA3B9-41B0-E811-8B23-FA163E279E4C.root'
    #'/store/data/Run2018A/SingleMuon/MINIAOD/17Sep2018-v2/270000/40BFE1A5-BEFE-B34B-8836-4ADDB8966C78.root',
    #'/store/mc/RunIIAutumn18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/90000/DD89AFA9-BD25-F346-939F-A9CC68A04B84.root',
    #'/store/mc/RunIIAutumn18MiniAOD/ZToMuMu_NNPDF31_13TeV-powheg_M_50_120/MINIAODSIM/102X_upgrade2018_realistic_v15-v2/120000/078DB2B1-40DD-634D-A3CF-D2E377CAFA48.root'
    #'/store/mc/RunIIAutumn18MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/120000/8A620F3F-201E-7245-94DF-A9966919C1BD.root',
           ]

process.maxEvents.input = 1000
#process.options.wantSummary = cms.untracked.bool(True)# false di default
process.MessageLogger.cerr.FwkReport.reportEvery = 10000 # default 1000

if is2016:
    MCGT = '94X_mcRun2_asymptotic_v3'
    trigger_match = trigger_match_2016
    trigger_filters = trigger_filters_16
    trigger_path_names = trigger_path_names_16
    trigger_path_full_names = trigger_path_full_names_16
    prescaled_trigger_match = prescaled_trigger_match_2016
    prescaled_trigger_filters = prescaled_trigger_filters_16
    prescaled_trigger_path_names = prescaled_trigger_path_names_16
    prescaled_trigger_path_full_names = prescaled_trigger_path_full_names_16
    sel_name = 'Our2016'
    OurSelection = OurSelection2016
    samples = samples16
    ex = 'mc2016_'+ex
elif is2017:
    MCGT = '94X_mc2017_realistic_v17'
    trigger_match = trigger_match_2018
    trigger_filters = trigger_filters_18
    trigger_path_names = trigger_path_names_18
    trigger_path_full_names = trigger_path_full_names_18
    prescaled_trigger_match = prescaled_trigger_match_2018
    prescaled_trigger_filters = prescaled_trigger_filters_18
    prescaled_trigger_path_names = prescaled_trigger_path_names_18
    prescaled_trigger_path_full_names = prescaled_trigger_path_full_names_18
    sel_name = 'Our2018'
    OurSelection = OurSelection2018
    samples = samples17
    ex = 'mc2017_'+ex
elif is2018:
    MCGT = '102X_upgrade2018_realistic_v18'
    trigger_match = trigger_match_2018
    trigger_filters = trigger_filters_18
    trigger_path_names = trigger_path_names_18
    trigger_path_full_names = trigger_path_full_names_18
    prescaled_trigger_match = prescaled_trigger_match_2018
    prescaled_trigger_filters = prescaled_trigger_filters_18
    prescaled_trigger_path_names = prescaled_trigger_path_names_18
    prescaled_trigger_path_full_names = prescaled_trigger_path_full_names_18
    sel_name = 'Our2018'
    OurSelection = OurSelection2018
    samples = samples18
    ex = 'mc2018_'+ex

process.GlobalTag.globaltag = MCGT

from SUSYBSMAnalysis.Zprime2muAnalysis.HistosFromPAT_cfi import HistosFromPAT_MiniAOD as HistosFromPAT
HistosFromPAT.leptonsFromDileptons = True

from SUSYBSMAnalysis.Zprime2muAnalysis.ResolutionUsingMC_cfi import ResolutionUsingMC
ResolutionUsingMC.leptonsFromDileptons = cms.bool(True)
ResolutionUsingMC.doQoverP = cms.bool(True)
ResolutionUsingMC.hardInteraction.src = cms.InputTag('prunedGenParticles')

from SUSYBSMAnalysis.Zprime2muAnalysis.EfficiencyFromMC_cfi import EfficiencyFromMCMini as EfficiencyFromMC
EfficiencyFromMC.check_l1=cms.bool(False)
EfficiencyFromMC.use_resonance_mass = cms.bool(True)
EfficiencyFromMC.use_resonance_mass_denom = cms.bool(True)


if do_all_track_fits:
    tracks = [('muons',''),('global','Global'), ('inner','Inner'), ('tpfms','TPFMS'), ('picky','Picky'), ('dyt','DYT')]
else:
    tracks = [('muons','')]

cuts = {
    sel_name : OurSelection,
    sel_name+'AtZ' : OurSelection,
    }

dils = [
        ('OppSign','%(leptons_name)s:%(track)s@+ %(leptons_name)s:%(track)s@-','daughter(0).pdgId() + daughter(1).pdgId() == 0')
        ]

process.load('SUSYBSMAnalysis.Zprime2muAnalysis.HardInteractionFilter_cfi')
process.HardInteractionFilterRes = process.HardInteractionFilter.clone(use_resonance_mass=True)
process.HardInteractionFilterRes.hardInteraction.src = cms.InputTag('prunedGenParticles')

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
    elif 'AtZ' in cut_name:
        muon_cuts = Selection.loose_cut.replace('pt > %s' % offline_pt_threshold, 'pt > %s' % prescaled_offline_pt_threshold)
    else:
        muon_cuts = Selection.loose_cut

    leptons = process.leptonsMini.clone(muon_cuts = muon_cuts)
    leptons.trigger_filters = trigger_filters
    leptons.trigger_path_names = trigger_path_names
    leptons.trigger_path_full_names = trigger_path_full_names
    leptons.prescaled_trigger_filters = prescaled_trigger_filters
    leptons.prescaled_trigger_path_names = prescaled_trigger_path_names
    leptons.prescaled_trigger_path_full_names = prescaled_trigger_path_full_names
    if is2016:
        leptons.trigger_summary = cms.InputTag('selectedPatTrigger')
    # put different tev muon reconstructors into event
    tracks_for_momentum = [track for track,name in tracks if track!="muons"] # muons is default TuneP
    leptons.muon_tracks_for_momentum = cms.vstring(tracks_for_momentum)

    setattr(process, leptons_name, leptons)
    path_list.append(leptons)

    # Loop on different tev muon track reconstructors
    for track,track_name in tracks:

        # Make all the combinations of dileptons we defined above.
        for dil_name, dil_decay, dil_cut in dils:

            # Unique names for the modules: allname for the allDileptons,
            # and name for dileptons.
            name = cut_name + track_name + dil_name
            allname = 'all' + name

            alldil = Selection.allDimuons.clone(decay = dil_decay % locals(), cut = dil_cut)
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
                dil.prefer_Z=False
                if hasattr(dil, 'back_to_back_cos_angle_min'):
                    delattr(dil, 'back_to_back_cos_angle_min')
                if hasattr(dil, 'vertex_chi2_max'):
                    delattr(dil, 'vertex_chi2_max')
                if hasattr(dil, 'dpt_over_pt_max'):
                    delattr(dil, 'dpt_over_pt_max')
            elif 'AtZ' in cut_name:
                alldil.loose_cut = alldil.loose_cut.value().replace('pt > %s' % offline_pt_threshold, 'pt > %s' % prescaled_offline_pt_threshold)
                alldil.tight_cut = prescaled_trigger_match

            # Histos now just needs to know which leptons and dileptons to use.

            #Histos = HistosFromPAT.clone(lepton_src = cms.InputTag(leptons_name,'muons'),dilepton_src=cms.InputTag(name))

            ResolutionUsingMC.lepton_src = cms.InputTag(leptons_name,'muons')
            ResolutionUsingMC.dilepton_src = cms.InputTag(name)
            Resolution = ResolutionUsingMC.clone()
            ResolutionVertex = ResolutionUsingMC.clone(use_vertex_mass=cms.bool(True))

            Efficiency = EfficiencyFromMC.clone()
            if is2016:
                Efficiency.trigger_summary = cms.InputTag('selectedPatTrigger')
            if 'AtZ' in cut_name:
                Efficiency.trigger_filters = prescaled_trigger_filters
                Efficiency.trigger_path_names = prescaled_trigger_path_names
                Efficiency.trigger_path_full_names = prescaled_trigger_path_full_names
                Efficiency.hlt_single_min_pt = prescaled_trigger_pt_threshold
                Efficiency.acceptance_min_pt = prescaled_offline_pt_threshold
                Efficiency.dimuon_src = cms.InputTag(name)
            else:
                Efficiency.trigger_filters = trigger_filters
                Efficiency.trigger_path_names = trigger_path_names
                Efficiency.trigger_path_full_names = trigger_path_full_names
                Efficiency.hlt_single_min_pt = trigger_pt_threshold
                Efficiency.acceptance_min_pt = offline_pt_threshold
                Efficiency.dimuon_src = cms.InputTag(name)

            setattr(process,allname,alldil)
            setattr(process,name,dil)
            #setattr(process,name+'Histos',Histos) # Histos is unnecessary since datamc already does it
            setattr(process,name+'Resolution',Resolution)
            setattr(process,name+'ResolutionVertex',ResolutionVertex)
            setattr(process,name+'Efficiency',Efficiency)
            #path_list.append(alldil * dil * Histos * Resolution * ResolutionVertex * Efficiency)
            path_list.append(alldil * dil * Resolution * ResolutionVertex * Efficiency)

    # Finally, make the path for this set of cuts.
    pathname = 'path' + cut_name
    process.load("SUSYBSMAnalysis.Zprime2muAnalysis.EventCounter_cfi")
    pobj = process.EventCounter * process.muonPhotonMatchMiniAOD * reduce(lambda x,y: x*y, path_list)
    path = cms.Path(pobj)
    setattr(process, pathname, path)

import sys, os
if __name__ == '__main__' and 'submit' in sys.argv:
    crab_cfg = '''
from CRABClient.UserUtilities import config,getUsernameFromSiteDB
config = config()

config.General.requestName = 'ana_effres_%(name)s%(extra)s'
config.General.workArea = 'crab'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'histos_crab.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset =  '%(dataset)s'
config.Data.inputDBS = 'global'
config.Data.publication = False
config.Data.splitting = 'EventAwareLumiBased'
config.Data.totalUnits = -1
config.Data.unitsPerJob  = 10000
config.Data.outputDatasetTag = 'ana_effres_%(name)s%(extra)s'
config.Data.outLFNDirBase = '/store/user/'+getUsernameFromSiteDB()
config.Site.storageSite = 'T2_CH_CERN'
                          
'''
#config.Data.outLFNDirBase = '/store/group/phys_exotica/dimuon/2018/effres'
        
    # Only do DY MC samples and apply HardInteractionFilter
    FilterInfo = {
        #'name':        (  lo,    hi),
        'dy50to120':    (  50,   120),
        'dy120to200':   ( 120,   200),
        'dy200to400':   ( 200,   400),
        'dy400to800':   ( 400,   800),
        'dy800to1400':  ( 800,  1400),
        'dy1400to2300': (1400,  2300),
        'dy2300to3500': (2300,  3500),
        'dy3500to4500': (3500,  4500),
        'dy4500to6000': (4500,  6000),
        'dy6000toInf':  (6000, 10000),
        }
    dySamples = [sample for sample in samples if sample.name in FilterInfo.keys()]

    just_testing = 'testing' in sys.argv

    for sample in dySamples:

        name = sample.name
        dataset = sample.dataset
        lo = FilterInfo[name][0]
        hi = FilterInfo[name][1]
        print name,lo,hi,dataset
        extra = '_'+ex if ex!='' else ''

        open('crabConfig.py', 'wt').write(crab_cfg % locals())

        new_py = open('histos_chris.py').read()
        new_py += '\nprocess.HardInteractionFilter.min_mass = %i\n' % lo
        new_py += '\nprocess.HardInteractionFilter.max_mass = %i\n' % hi
        new_py += '\nprocess.HardInteractionFilterRes.min_mass = %i\n' % lo
        new_py += '\nprocess.HardInteractionFilterRes.max_mass = %i\n' % hi
        open('histos_crab.py', 'wt').write(new_py)
        
        if not just_testing:
            os.system('crab submit -c crabConfig.py')
            os.system('rm crabConfig.py histos_crab.py histos_crab.pyc')
