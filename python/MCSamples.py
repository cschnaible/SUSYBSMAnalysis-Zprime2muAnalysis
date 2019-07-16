#!/usr/bin/env python

import os
from SUSYBSMAnalysis.Zprime2muAnalysis.tools import big_warn, files_from_dbs
from SUSYBSMAnalysis.Zprime2muAnalysis.crabtools import dataset_from_publish_log

miniAOD = True

class sample(object):
    def __init__(self, name, nice_name, dataset, nevents, color, syst_frac, cross_section, cross_section_uncert=0.0, k_factor=1, frac_neg_weight=0.0, filenames=None, scheduler='condor', hlt_process_name='HLT', ana_dataset=None, is_madgraph=False, is_zprime=False):
        self.name = name
        self.nice_name = nice_name
        self.dataset = dataset
        self.nevents = nevents
        self.color = color
        self.syst_frac = syst_frac
        self.cross_section = cross_section
        self.cross_section_uncert = cross_section_uncert
        self.frac_neg_weight = frac_neg_weight
        self.k_factor = k_factor
        self.filenames_ = filenames
        self.scheduler = scheduler
        self.hlt_process_name = hlt_process_name
        self.ana_dataset = ana_dataset
        self.is_madgraph = is_madgraph
        self.is_zprime = is_zprime
        # Effective number of events in case of negatively weighted events
        # Slide 32: 
        # https://indico.cern.ch/event/790963/contributions/3306139/attachments/1791391/2919088/CMSWeek201902.pdf
        self.nevents_eff = self.nevents * pow((1-2*self.frac_neg_weight),2)

    # the total weight is partial_weight * integrated_luminosity
    @property
    def partial_weight(self):
        return self.cross_section / float(self.nevents) * self.k_factor 

    @property
    def partial_weight_eff(self):
        return self.cross_section / float(self.nevents_eff) * self.k_factor

    @property
    def filenames(self):
        # Return a list of filenames for running the histogrammer not
        # using crab.
        if self.filenames_ is not None:
            return self.filenames_
        return files_from_dbs(self.ana_dataset, ana02=True)

    def __getitem__(self, key):
        return getattr(self, key)

    def _dump(self, redump_existing=False):
        dst = os.path.join('/uscmst1b_scratch/lpc1/3DayLifetime/tucker', self.name) 
        os.system('mkdir ' + dst)
        for fn in self.filenames:
            print fn
            if redump_existing or not os.path.isfile(os.path.join(dst, os.path.basename(fn))):
                os.system('dccp ~%s %s/' % (fn,dst))

class tupleonlysample(sample):
    def __init__(self, name, dataset, scheduler='condor', hlt_process_name='HLT'):
        super(tupleonlysample, self).__init__(name, 'dummy', dataset, 1, 1, 1, 1, scheduler=scheduler, hlt_process_name=hlt_process_name)

# XS, cross_section_uncert, frac_neg_weight for all MC samples taken from XSDB which is linked from the DAS page of each dataset
# For example Drell-Yan samples:
# https://cms-gen-dev.cern.ch/xsdb/?columns=57394461&currentPage=0&ordDirection=1&ordFieldName=process_name&pageSize=10&searchQuery=DAS%3DZToMuMu_NNPDF31_13TeV-powheg_M_%2A_%2A
samples18 = [

    sample('dy50to120', 'DY50to120', '/ZToMuMu_NNPDF31_13TeV-powheg_M_50_120/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 2982000, 209 , 1., 2113.0, cross_section_uncert=0.9976,  k_factor=1., frac_neg_weight=0.00974),
    sample('dy120to200', 'DY120to200', '/ZToMuMu_NNPDF31_13TeV-powheg_M_120_200/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 100000, 210, 1., 20.55, cross_section_uncert=0.01372, k_factor=1., frac_neg_weight=0.00497),
    sample('dy200to400', 'DY200to400', '/ZToMuMu_NNPDF31_13TeV-powheg_M_200_400/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 100000, 211, 1., 2.886, cross_section_uncert=0.001993, k_factor=1., frac_neg_weight=0.00194),
    sample('dy400to800', 'DY400to800', '/ZToMuMu_NNPDF31_13TeV-powheg_M_400_800/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 100000, 212, 1., 0.2513, cross_section_uncert=0.000179, k_factor=1., frac_neg_weight=0.00048),
    sample('dy800to1400', 'DY800to1400', '/ZToMuMu_NNPDF31_13TeV-powheg_M_800_1400/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100000, 72, 1., 0.01707, k_factor=1., cross_section_uncert=1.253e-05, frac_neg_weight=0.00017),
    sample('dy1400to2300', 'DY1400to2300', '/ZToMuMu_NNPDF31_13TeV-powheg_M_1400_2300/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 100000, 70, 1., 0.001366, k_factor=1., cross_section_uncert=1.013E-06, frac_neg_weight=9E-05),
    sample('dy2300to3500', 'DY2300to3500', '/ZToMuMu_NNPDF31_13TeV-powheg_M_2300_3500/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 100000, 70, 1.,8.178e-05, k_factor=1., cross_section_uncert=5.997e-08, frac_neg_weight=0.00015),
    sample('dy3500to4500', 'DY3500to4500', '/ZToMuMu_NNPDF31_13TeV-powheg_M_3500_4500/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 100000, 70, 1., 3.191e-06, k_factor=1., cross_section_uncert=2.243e-09, frac_neg_weight=0.00101),
    sample('dy4500to6000', 'DY4500to6000', '/ZToMuMu_NNPDF31_13TeV-powheg_M_4500_6000/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 100000, 70, 1., 2.787e-07, k_factor=1., cross_section_uncert=1.702e-10, frac_neg_weight=0.00349),
    sample('dy6000toInf', 'DY6000toInf', '/ZToMuMu_NNPDF31_13TeV-powheg_M_6000_Inf/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 100000, 70, 1., 9.569e-09, k_factor=1., cross_section_uncert=8.431e-12, frac_neg_weight=0.00933),

    # XS taken from 2017 samples w/o "PSweights"
    #sample('dyJetsToLL_ht70to100','dyJetsToLL_ht70to100','/DYJetsToLL_M-50_HT-70to100_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',10019684,70,1.,XXXX),
    #sample('dyJetsToLL_ht100to200_v2','DYJetsToLL_HT-100to200','/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',11530510,70,1.,174.0),
    #sample('dyJetsToLL_ht100to200_v1','DYJetsToLL_HT-100to200','/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',6353263,70,1.,174.0), # in production
    sample('dyJetsToLL_ht100to200','DYJetsToLL_HT-100to200','/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',6353263,70,1.,174.0), # in production
    sample('dyJetsToLL_ht200to400','DYJetsToLL_HT-200to400','/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',11225887,70,1.,53.27),
    #sample('dyJetsToLL_ht400to600_ext2v3','DYJetsToLL_HT-400to600','/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext2-v3/MINIAODSIM',9358053,70,1.,7.79),
    #sample('dyJetsToLL_ht400to600_v7','DYJetsToLL_HT-400to600','/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v7/MINIAODSIM',9697098,70,1.,7.79),
    #sample('dyJetsToLL_ht400to600_v4','DYJetsToLL_HT-400to600','/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v4/MINIAODSIM',7718938,70,1.,7.79),
    #sample('dyJetsToLL_ht400to600_v3','DYJetsToLL_HT-400to600','/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v3/MINIAODSIM',9840466,70,1.,7.79),
    #sample('dyJetsToLL_ht400to600_v2','DYJetsToLL_HT-400to600','/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',9643184,70,1.,7.79),
    sample('dyJetsToLL_ht400to600','DYJetsToLL_HT-400to600','/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',9643184,70,1.,7.79),
    sample('dyJetsToLL_ht600to800','DYJetsToLL_HT-600to800','/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',8862104,70,1.,1.882),
    sample('dyJetsToLL_ht800to1200','DYJetsToLL_HT-800to1200','/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',3138129,70,1.,0.8729),
    sample('dyJetsToLL_ht1200to2500','DYJetsToLL_HT-1200to2500','/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',536416,70,1.,0.2079), # in production
    sample('dyJetsToLL_ht2500toInf','DYJetsToLL_HT-2500toInf','/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',427051,70,1.,0.003765),

    # Diboson
    #sample('WZ', 'WZ', '/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v3/MINIAODSIM', 3885000, 98, 1., 27.6, k_factor=1., cross_section_uncert=0.04),
    #sample('WZ', 'WZ', '/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', XXXX, 98, 1., 27.6, k_factor=1., cross_section_uncert=0.04), # in production
    sample('WZTo3LNu','WZ','/WZTo3LNu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',1976600,98,1.,4.42965), # NLO
    sample('WZTo2L2Q','WZ','/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',28193648,98,1.,5.595), # NLO ... XSDB has 6.331 or 5.606

    #sample('ZZ', 'ZZ', '/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 1979000, 94, 1., 12.14, k_factor=1., cross_section_uncert=0.01964),
    sample('ZZTo2L2Nu','ZZ',None,8382600,94,1.,0.564), # XS FIXME
    sample('ZZTo2L2Nu_ext1','ZZ','/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',8382600,94,1.,0.564), # XS FIXME
    sample('ZZTo2L2Nu_ext2','ZZ','/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext2-v2/MINIAODSIM',48046000,94,1.,0.564), # XS FIXME
    sample('ZZTo4L','ZZ',None,6689900,94,1.,1.212), # for plotting
    sample('ZZTo4L_ext1','ZZ','/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',6689900,94,1.,1.212), # XS FIXME
    sample('ZZTo4L_ext2','ZZ','/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext2-v2/MINIAODSIM',99009000,94,1.,1.212), # XS FIXME
    sample('ZZTo2L2Q','ZZ','/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',27900469,94,1.,1.999), # XSDB has 3.222 or 3.688 ...

    # WW Samples still in production
    sample('WW', 'WW', '/WW_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 3885000, 208, 1., 75.8, k_factor=1., cross_section_uncert=0.1123),
    #sample('WW', 'WW', '/WW_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', XXXX, 208, 1., 75.8, k_factor=1., cross_section_uncert=0.1123), # in production
    sample('WW_50to200', 'WW', None, 2000000, 208, 1., 12.178 ),
    sample('WW_200to600','WW',None,7957790,208,1.,1.39),
    sample('WW_600to1200','WW',None,1064000,208,1.,5.7E-2), # this one is for plotting
    sample('WW_1200to2500','WW',None,166261,208,1.,3.6E-3),
    sample('WW_2500toInf','WW',None ,2495,208,1.,5.4E-5),

 
 	#sample('Wjets', 'Wjets', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall18MiniAOD-102X_upgrade2018_realistic_v12-v1/MINIAODSIM', 60750603, 52, 1., 52940.0, k_factor=1, cross_section_uncert=121.9, frac_neg_weight=0.0004079), # Usable for now? Switch to recommended Autumn18MiniAOD campaign
    sample('Wjets', 'Wjets', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM', 71026861, 52, 1., 52940.0, k_factor=1, cross_section_uncert=121.9, frac_neg_weight=0.0004079), # This one is the recommended MC Campaign
 
    # t-tbar samples binned in dilepton mass still in production
    sample('ttbar_lep', 'ttbar', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 64310000, 4 , 1., 88.29, k_factor=1.),
    sample('ttbar_lep_50to500', 'ttbar',None, 960752, 4 , 1., 87.31, k_factor=1.),
    sample('ttbar_lep_500to800','ttbar',None,740400,4,1.,0.32611), # use this one for plotting
    sample('ttbar_lep_800to1200','ttbar',None,222158,4,1.,3.265E-2),
    sample('ttbar_lep_1200to1800','ttbar',None,20617,4,1.,3.05E-3),
    sample('ttbar_lep_1800toInf','ttbar',None,1157,4,1.,1.74E-4),
 	
    # Single-Top
 	#sample('tbarW', 'tbarW', '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall18MiniAOD-102X_upgrade2018_realistic_v12-v1/MINIAODSIM', 8000000, 63 , 1., 34.97, k_factor=1., cross_section_uncert=0.02827, frac_neg_weight=0.0034),
 	#sample('tbarW_ext', 'tbarW', '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v1/MINIAODSIM', 7623000, 63 , 1., 34.97, k_factor=1., cross_section_uncert=0.02827, frac_neg_weight=0.0034),
     #sample('tW', 'tW', '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall18MiniAOD-102X_upgrade2018_realistic_v12-v1/MINIAODSIM', 9438000, 66 , 1., 34.91, k_factor=1., cross_section_uncert=0.02817, frac_neg_weight=0.003758),
     #sample('tW_ext', 'tW', '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v1/MINIAODSIM', 6952830, 66 , 1., 34.91, k_factor=1.,cross_section_uncert=0.02817, frac_neg_weight=0.003758),

     sample('tbarW','tbarW',None,5823328,66,1.,19.47),
     sample('tbarW_v3','tbarW','/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v3/MINIAODSIM',5823328,66,1.,19.47),
     sample('tbarW_v2','tbarW','/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',1086487,66,1.,19.47),
     sample('tW','tW',None,7636887,66,1.,19.47),
     sample('tW_v3','tW','/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v3/MINIAODSIM',7636887,66,1.,19.47),
     sample('tW_v2','tW','/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',1085847,66,1.,19.47),

    # DYJetsToLL - in the past we've used amcatnloFXFX but why?
    #sample('dyInclusive50_amcatnlo', 'DYInclusive50', '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 997561, 209 , 1., 6529.0, k_factor=1., is_madgraph=True, cross_section_uncert=28.29, frac_neg_weight=0.1624),
    sample('dyInclusive50_amcatnlo', 'DYInclusive50', '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 997561, 209 , 1., 6489.0, k_factor=1., is_madgraph=True, cross_section_uncert=28.29, frac_neg_weight=0.1624),
 	#sample('dyInclusive50_madgraph', 'DYInclusive50', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100194597, 209 , 1., 5343.0, k_factor=1., is_madgraph=True, cross_section_uncert=12.64, frac_neg_weight=0.0004962),
 	sample('dyInclusive50_madgraph', 'DYInclusive50', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100194597, 209 , 1., 6225.45, k_factor=1., is_madgraph=True, cross_section_uncert=12.64, frac_neg_weight=0.0004962),
 	sample('dyTauTau_madgraph', 'DYInclusive50', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM', 100194597, 209 , 1., 6225.45/3., k_factor=1., is_madgraph=True, cross_section_uncert=12.64, frac_neg_weight=0.0004962), # TauTau in sample.name guarantees that it will have TauTau filter applied
    
    # NNLO XS is 6225.42 for madgraph and has fractional uncertainty of 2% see 
    # https://indico.cern.ch/event/746829/contributions/3138541/attachments/1717905/2772129/Drell-Yan_jets_crosssection.pdf

    ]
samples18.reverse()

# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

samples17 = [
    sample('dy50to120', 'DY50to120', '/ZToMuMu_NNPDF31_13TeV-powheg_M_50_120/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 2982000, 209 , 1., 2113.0, cross_section_uncert=0.9976,  k_factor=1., frac_neg_weight=0.00974),
    sample('dy120to200', 'DY120to200', '/ZToMuMu_NNPDF31_13TeV-powheg_M_120_200/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 210, 1., 20.55, cross_section_uncert=0.01372, k_factor=1., frac_neg_weight=0.00497),
    sample('dy200to400', 'DY200to400', '/ZToMuMu_NNPDF31_13TeV-powheg_M_200_400/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 211, 1., 2.886, cross_section_uncert=0.001993, k_factor=1., frac_neg_weight=0.00194),
    sample('dy400to800', 'DY400to800', '/ZToMuMu_NNPDF31_13TeV-powheg_M_400_800/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 212, 1., 0.2513, cross_section_uncert=0.000179, k_factor=1., frac_neg_weight=0.00048),
    sample('dy800to1400', 'DY800to1400', '/ZToMuMu_NNPDF31_13TeV-powheg_M_800_1400/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 72, 1., 0.01707, k_factor=1., cross_section_uncert=1.253e-05, frac_neg_weight=0.00017),
    sample('dy1400to2300', 'DY1400to2300', '/ZToMuMu_NNPDF31_13TeV-powheg_M_1400_2300/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70, 1., 0.001366, k_factor=1., cross_section_uncert=1.013E-06, frac_neg_weight=9E-05),
    sample('dy2300to3500', 'DY2300to3500', '/ZToMuMu_NNPDF31_13TeV-powheg_M_2300_3500/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70, 1.,8.178e-05, k_factor=1., cross_section_uncert=5.997e-08, frac_neg_weight=0.00015),
    sample('dy3500to4500', 'DY3500to4500', '/ZToMuMu_NNPDF31_13TeV-powheg_M_3500_4500/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70, 1., 3.191e-06, k_factor=1., cross_section_uncert=2.243e-09, frac_neg_weight=0.00101),
    sample('dy4500to6000', 'DY4500to6000', '/ZToMuMu_NNPDF31_13TeV-powheg_M_4500_6000/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70, 1., 2.787e-07, k_factor=1., cross_section_uncert=1.702e-10, frac_neg_weight=0.00349),
    sample('dy6000toInf', 'DY6000toInf', '/ZToMuMu_NNPDF31_13TeV-powheg_M_6000_Inf/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70, 1., 9.569e-09, k_factor=1., cross_section_uncert=8.431e-12, frac_neg_weight=0.00933),

    # Diboson
    sample('WZ', 'WZ', '/WZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 3928630, 98, 1., 27.6, k_factor=1., cross_section_uncert=0.04),
    sample('WZTo3LNu','WZ','/WZTo3LNu_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',976400,98,1.,4.42965),
    sample('WZTo2L2Q','WZ','/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',27582164,98,1.,5.606),

    sample('ZZ', 'ZZ', '/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM', 1925931, 94, 1., 12.14, k_factor=1., cross_section_uncert=0.01964),
    #sample('ZZ_v1', 'ZZ', '/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1949768, 94, 1., 12.14, k_factor=1., cross_section_uncert=0.01964),
    sample('ZZTo2L2Nu','ZZ','/ZZTo2L2Nu_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',8744768,94,1.,0.564),
    sample('ZZTo4L','ZZ',None,98091559,94,1.,1.212),
    sample('ZZTo4L_ext1','ZZ','/ZZTo4L_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',98091559,94,1.,1.212),
    sample('ZZTo4L_v2','ZZ','/ZZTo4L_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',16075000,94,1.,1.212),
    sample('ZZTo4L_v1','ZZ','/ZZTo4L_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',6967853,94,1.,1.212),
    sample('ZZTo2L2Q','ZZ','/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',27840918,94,1.,1.999),

    sample('WW', 'WW', '/WW_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 7765828, 208, 1., 75.8, k_factor=1., cross_section_uncert=0.1123),
    #sample('WW_v1', 'WW', '/WW_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 7791498, 208, 1., 75.8, k_factor=1., cross_section_uncert=0.1123), # need to resubmit
    #sample('WW_v2', 'WW', '/WW_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 7765828, 208, 1., 75.8, k_factor=1., cross_section_uncert=0.1123),
    sample('WW_50to200', 'WW', '/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 2000000, 208, 1., 12.178 ),
    sample('WW_200to600','WW','/WWTo2L2Nu_MLL_200To600_NNPDF31_13TeV-powheg/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',7957790,208,1.,1.39),
    sample('WW_600to1200','WW',None,1064000,208,1.,5.7E-2), # this one is for plotting
    sample('WW_600to1200_v1','WW','/WWTo2L2Nu_MLL_600To1200_v1_NNPDF31_13TeV-powheg/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',1064000,208,1.,5.7E-2),
    sample('WW_600to1200_v2','WW','/WWTo2L2Nu_MLL_600To1200_v2_NNPDF31_13TeV-powheg/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',1017984,208,1.,5.7E-2),
    sample('WW_600to1200_v3','WW','/WWTo2L2Nu_MLL_600To1200_v3_NNPDF31_13TeV-powheg/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',574960,208,1.,5.7E-2),
    sample('WW_1200to2500','WW','/WWTo2L2Nu_MLL_1200To2500_NNPDF31_13TeV-powheg/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',166261,208,1.,3.6E-3),
    sample('WW_2500toInf','WW','/WWTo2L2Nu_MLL_2500ToInf_NNPDF31_13TeV-powheg/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',2495,208,1.,5.4E-5),


 	sample('Wjets_ext', 'Wjets', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM', 44627200, 52, 1., 52940.0, k_factor=1, cross_section_uncert=121.9, frac_neg_weight=0.0004079), # Usable for now? Switch to recommended Autumn18MiniAOD campaign
 	sample('Wjets', 'Wjets', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 33073306, 52, 1., 52940.0, k_factor=1, cross_section_uncert=121.9, frac_neg_weight=0.0004079), # Usable for now? Switch to recommended Autumn18MiniAOD campaign
 
    # t-tbar samples binned in dilepton mass still in production
    sample('ttbar_lep', 'ttbar', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM', 9000000, 4 , 1., 88.29, k_factor=1.),
    #sample('ttbar_lep_v2', 'ttbar', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 960752, 4 , 1., 88.29, k_factor=1.),
    #sample('ttbar_lep_v1', 'ttbar', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 8705576, 4 , 1., 88.29, k_factor=1.),
    sample('ttbar_lep_50to500', 'ttbar',None, 960752, 4 , 1., 87.31, k_factor=1.),
    sample('ttbar_lep_50to500_v2', 'ttbar', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 960752, 4 , 1., 87.31, k_factor=1.),
    sample('ttbar_lep_50to500_v1', 'ttbar', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 8705576, 4 , 1., 87.31, k_factor=1.),
    sample('ttbar_lep_500to800','ttbar',None,740400,4,1.,0.32611), # use this one for plotting
    sample('ttbar_lep_500to800_0to20','ttbar','/TTToLL_MLL_500To800_0to20_NNPDF31_13TeV-powheg/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',740400,4,1.,0.32611),
    #sample('ttbar_lep_500to800_21to40','ttbar','/TTToLL_MLL_500To800_21to40_NNPDF31_13TeV-powheg/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',800431,4,1.,1.0),
    sample('ttbar_lep_500to800_41to65','ttbar','/TTToLL_MLL_500To800_41to65_NNPDF31_13TeV-powheg/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',800431,4,1.,0.32611),
    sample('ttbar_lep_800to1200','ttbar','/TTToLL_MLL_800To1200_NNPDF31_13TeV-powheg/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',222158,4,1.,3.265E-2),
    sample('ttbar_lep_1200to1800','ttbar','/TTToLL_MLL_1200To1800_NNPDF31_13TeV-powheg/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',20617,4,1.,3.05E-3),
    sample('ttbar_lep_1800toInf','ttbar','/TTToLL_MLL_1800ToInf_NNPDF31_13TeV-powheg/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',1157,4,1.,1.74E-4),
 	
    # Single-Top
 	sample('tbarW_inclusive', 'tbarW', '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 7780870, 63 , 1., 34.97),
 	#sample('tbarW_v2', 'tbarW', '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 7977430, 63 , 1., 34.97),
    sample('tW_inclusive', 'tW', '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 7581624, 66 , 1., 34.91),
    #sample('tW_v2', 'tW', '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 7794186, 66 , 1., 34.91),

     sample('tW','tW','/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',4974435,66,1.,19.47),
     sample('tbarW','tbarW','/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',5375230,66,1.,19.47),
     
    # DYJetsToLL - in the past we've used amcatnloFXFX but why?
    sample('dyInclusive50_amcatnlo', 'DYInclusive50', '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext2-v1/MINIAODSIM', 8875401, 209 , 1., 6529.0, k_factor=1., is_madgraph=True, cross_section_uncert=28.29, frac_neg_weight=0.1624),  
    #sample('dyTauTau_amcatnlo', 'DYInclusive50', '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext2-v1/MINIAODSIM', 8875401, 209 , 1., 6529.0/3, k_factor=1., is_madgraph=True, cross_section_uncert=28.29, frac_neg_weight=0.1624),  

    #sample('dyJetsToLL_ht70to100','DYJetsToLL_HT-70to100','/DYJetsToLL_M-50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',10019684,70,1.,XXXX),
    sample('dyJetsToLL_ht100to200',    'DYJetsToLL_HT-100to200',  '/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',10235418,70,1.,174.0),
    sample('dyJetsToLL_ht100to200_ext','DYJetsToLL_HT-100to200',  '/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',3950339,70,1.,174.0),
    sample('dyJetsToLL_ht200to400_v1', 'DYJetsToLL_HT-200to400',  '/DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',10298412,70,1.,53.27),
    sample('dyJetsToLL_ht200to400_v2', 'DYJetsToLL_HT-200to400',  '/DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',10728447,70,1.,53.27),
    sample('dyJetsToLL_ht200to400_ext','DYJetsToLL_HT-200to400',  '/DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',1200863,70,1.,53.27),
    sample('dyJetsToLL_ht400to600',    'DYJetsToLL_HT-400to600',  '/DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',9533635,70,1.,7.79),
    sample('dyJetsToLL_ht400to600_ext','DYJetsToLL_HT-400to600',  '/DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',1124294,70,1.,7.79),
    sample('dyJetsToLL_ht600to800',    'DYJetsToLL_HT-600to800',  '/DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',8153358,70,1.,1.882),
    sample('dyJetsToLL_ht800to1200',   'DYJetsToLL_HT-800to1200' ,'/DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',3089861,70,1.,0.8729),
    sample('dyJetsToLL_ht1200to2500',  'DYJetsToLL_HT-1200to2500','/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',625517,70,1.,0.2079),
    sample('dyJetsToLL_ht2500toInf',   'DYJetsToLL_HT-2500toInf', '/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',404986,70,1.,0.003765),

 	sample('dyInclusive50_madgraph', 'DYInclusive50', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 48675378, 209 , 1., 6225.42, k_factor=1., is_madgraph=True, cross_section_uncert=12.64, frac_neg_weight=0.0004962), # NNLO XS is 6225.42 and has fractional uncertainty of 2% see 
 	sample('dyInclusive50_madgraph_ext', 'DYInclusive50', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 49125561, 209 , 1., 6225.42, k_factor=1., is_madgraph=True, cross_section_uncert=12.64, frac_neg_weight=0.0004962), # NNLO XS is 6225.42 and has fractional uncertainty of 2% see 

 	sample('dyTauTau_madgraph', 'DYTauTau', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 48675378, 209 , 1., 6225.42/3., k_factor=1., is_madgraph=True, cross_section_uncert=12.64, frac_neg_weight=0.0004962), # NNLO XS is 6225.42 and has fractional uncertainty of 2% see 
 	sample('dyTauTau_madgraph_ext', 'DYTauTau', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 49125561, 209 , 1., 6225.42, k_factor=1., is_madgraph=True, cross_section_uncert=12.64, frac_neg_weight=0.0004962), # NNLO XS is 6225.42 and has fractional uncertainty of 2% see 
    # https://indico.cern.ch/event/746829/contributions/3138541/attachments/1717905/2772129/Drell-Yan_jets_crosssection.pdf

    ]

samples17.reverse()

samples16 = [
    sample('dy50to120',   'DY50to120', '/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 2977600, 209 , 1., 1975.0,   k_factor=1.),#NLO xs and k-factor applied to reach NLO
    sample('dy120to200',  'DY120to200',  '/ZToMuMu_NNPDF30_13TeV-powheg_M_120_200/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',  100000, 210, 1., 19.32),#mcm 19.32
    sample('dy200to400',  'DY200to400',  '/ZToMuMu_NNPDF30_13TeV-powheg_M_200_400/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',  100000, 211, 1., 2.731),#mcm 2.731
    sample('dy400to800',  'DY400to800',  '/ZToMuMu_NNPDF30_13TeV-powheg_M_400_800/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',   98400, 212, 1., 0.241),
    sample('dy800to1400', 'DY800to1400', '/ZToMuMu_NNPDF30_13TeV-powheg_M_800_1400/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 100000,  72, 1., 0.01678),
    sample('dy1400to2300','DY1400to2300','/ZToMuMu_NNPDF30_13TeV-powheg_M_1400_2300/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',100000,  70, 1., 0.00139),
    sample('dy2300to3500','DY2300to3500','/ZToMuMu_NNPDF30_13TeV-powheg_M_2300_3500/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',100000,  70, 1., 0.00008948),
    sample('dy3500to4500','DY3500to4500','/ZToMuMu_NNPDF30_13TeV-powheg_M_3500_4500/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',100000,  70, 1., 0.0000041),
    sample('dy4500to6000','DY4500to6000','/ZToMuMu_NNPDF30_13TeV-powheg_M_4500_6000/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',100000,  70, 1., 4.56E-7),    
    sample('dy6000toInf', 'DY6000toInf', '/ZToMuMu_NNPDF30_13TeV-powheg_M_6000_Inf/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 100000,  70, 1., 2.06E-8),

    
    sample('WZ', 'WZ', '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1000000, 98, 1., 47.13, k_factor=1.),#NLO from MCFM
    sample('WZ_ext', 'WZ_ext', '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 2995828, 98, 1., 47.13, k_factor=1.),
 
    sample('ZZ',   'ZZ', '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 990064, 94, 1.,16.523, k_factor=1.),#NLO from MCFM
    sample('ZZ_ext',   'ZZ_ext', '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', 998034, 94, 1.,16.523, k_factor=1.),
 
    #sample('WW_inclusive', 'WWinclusive', '/WWTo2L2Nu_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1999000, 208, 1., 12.178, k_factor=1.),#already NNLO xs
    sample('WW_50to200', 'WWinclusive', '/WWTo2L2Nu_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 1999000, 208, 1., 12.178, k_factor=1.),#already NNLO xs
    sample('WW_200to600', 'WW200to600', '/WWTo2L2Nu_Mll_200To600_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 200000, 208, 1., 1.385, k_factor=1.),#already NNLO xs
    sample('WW_600to1200', 'WW600to1200', '/WWTo2L2Nu_Mll_600To1200_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 200000, 208, 1., 0.0566, k_factor=1.),#already NNLO xs
    sample('WW_1200to2500', 'WW1200to2500', '/WWTo2L2Nu_Mll_1200To2500_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 200000, 208, 1., 0.003557, k_factor=1.),#already NNLO xs
    sample('WW_2500toInf', 'WW2500','/WWTo2L2Nu_Mll_2500ToInf_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 38969, 208, 1., 0.00005395, k_factor=1.),#already NNLO xs
 
    sample('Wjets', 'Wjets', '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',29705748,52,1.,61526.7,k_factor=1),#already NNLO xs
 
    sample('ttbar_lep',     'ttbar_lep', '/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 79092400, 4 , 1., 87.31, k_factor=1.),
    sample('ttbar_lep_50to500','ttbar_lep', '/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 79092400, 4 , 1., 87.31, k_factor=1.),
    sample('ttbar_lep_500to800',     'ttbar_lep', '/TTToLL_MLL_500To800_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 200000, 4 , 1., 0.32611, k_factor=1.),
    sample('ttbar_lep_800to1200',     'ttbar_lep', '/TTToLL_MLL_800To1200_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 199800, 4 , 1., 0.03265, k_factor=1.),
    sample('ttbar_lep_1200to1800',     'ttbar_lep', '/TTToLL_MLL_1200To1800_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 200000, 4 , 1., 0.00305, k_factor=1.),
    sample('ttbar_lep_1800toInf',     'ttbar_lep', '/TTToLL_MLL_1800ToInf_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 40829, 4 , 1., 0.000174, k_factor=1.),
    
    sample('tbarW', 'tbarW', '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',6933094,63 , 1., 35.6, k_factor=1.),#already NNLO xs          
    sample('tW',     'tW', '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',6952830,66 , 1., 35.6, k_factor=1.),#already NNLO xs
 
    #sample('qcd50to80', 'QCD50to80', '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 9954370,43,1.,1,k_factor=1),
    #sample('qcd80to120', 'QCD80to120', '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',6986740,43,1.,2762530,k_factor=1),
    #sample('qcd120to170', 'QCD120to170', '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',6708572,43,1.,471100,k_factor=1),
    #sample('qcd170to300', 'QCD170to300', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',6958708,43,1.,117276,k_factor=1),
    #sample('qcd300to470', 'QCD300to470', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 4150588,43,1.,7823,k_factor=1),
    #sample('qcd470to600', 'QCD470to600', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',3959986,43,1.,648.2,k_factor=1),
    #sample('qcd600to800', 'QCD600to800', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',3896412,43,1.,186.9,k_factor=1),
    #sample('qcd800to1000', 'QCD800to1000', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',3992112,43,10,32.293,k_factor=1),
    #sample('qcd1000to1400', 'QCD1000to1400', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',2999069,43,1.,9.4183,k_factor=1),
    #sample('qcd1400to1800', 'QCD1400to1800', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',396409,43,1.,0.84265,k_factor=1),
    #sample('qcd1800to2400', 'QCD1800to2400', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',397660,43,1.,0.114943,k_factor=1),
    #sample('qcd2400to3200', 'QCD2400to3200', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',399226,43,1.,0.00682981,k_factor=1),
    #sample('qcd3200', 'QCD3200', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM',391735,43,1.,0.000165445,k_factor=1),
 
    # N_EVENT scaled by: -N_EVENT * n_neg/n + n * n_pos/n (N_EVENT from report = 28968252; n from weight = 9112991 n_neg = 1507200 (0.1654); n_pos = 7605790 (0.8346); )
    #sample('dyInclusive50_amcatnlo', 'DYInclusive50', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 19385554, 209 , 1., 5765.4,    k_factor=1., is_madgraph=True),  
    sample('dyInclusive50_amcatnlo_ext','DYInclusive50','/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',122055388,209,1.,5941.0),
    sample('dyInclusive50_amcatnlo','DYInclusive50','/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 19385554, 209 , 1., 5765.4,    k_factor=1.),  

    #sample('dyTauTau_amcatnlo_ext','DYInclusive50','/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',122055388,209,1.,5941.0),
    #sample('dyTauTau_amcatnlo','DYInclusive50','/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 19385554, 209 , 1., 5765.4,    k_factor=1., is_madgraph=True),  

    sample('dyInclusive50_madgraph_ext1','DYInclusive50','/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM',49144274,209,1.,5763.36,is_madgraph=True),
    sample('dyInclusive50_madgraph_ext2','DYInclusive50','/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',96658943,209,1.,5763.36,is_madgraph=True),
    sample('dyTauTau_madgraph','DYTauTau','/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM',49144274,209,1.,5763.36/3,is_madgraph=True),
    #sample('dyTauTau_madgraph_ext1','DYTauTau','/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM',49144274,209,1.,5763.36,is_madgraph=True),
    #sample('dyTauTau_madgraph_ext2','DYTauTau','/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',96658943,209,1.,5763.36,is_madgraph=True),

    #sample('dyJetsToLL_ht70to100','DYJetsToLL_HT-70to100','/DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',9616188,70,1.,XXXX),
    sample('dyJetsToLL_ht100to200',    'DYJetsToLL_HT-100to200',  '/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',2751187,70,1.,147.4),
    sample('dyJetsToLL_ht100to200_ext','DYJetsToLL_HT-100to200',  '/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',7856020,70,1.,147.4),
    sample('dyJetsToLL_ht200to400',    'DYJetsToLL_HT-200to400',  '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',962195,70,1.,41.04),
    sample('dyJetsToLL_ht200to400_ext','DYJetsToLL_HT-200to400',  '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',8691536,70,1.,41.04),
    sample('dyJetsToLL_ht400to600',    'DYJetsToLL_HT-400to600',  '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',1070454,70,1.,5.674),
    sample('dyJetsToLL_ht400to600_ext','DYJetsToLL_HT-400to600',  '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',8938322,70,1.,5.674),
    sample('dyJetsToLL_ht600to800',    'DYJetsToLL_HT-600to800',  '/DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM',8292957,70,1.,1.358),
    sample('dyJetsToLL_ht800to1200',   'DYJetsToLL_HT-800to1200' ,'/DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',2668730,70,1.,0.6229),
    sample('dyJetsToLL_ht1200to2500',  'DYJetsToLL_HT-1200to2500','/DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',596079,70,1.,0.1512),
    sample('dyJetsToLL_ht2500toInf',   'DYJetsToLL_HT-2500toInf', '/DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',399492,70,1.,0.003659),

    ]

samples16.reverse()

__all__ = ['samples'] + [s.name for s in samples18+samples17+samples16]

samples = {y:{} for y in [2016,2017,2018]}
samples[2016] = {sample.name:sample for sample in samples16}
samples[2017] = {sample.name:sample for sample in samples17}
samples[2018] = {sample.name:sample for sample in samples18}

if __name__ == '__main__':
    if False:
        from dbstools import dbsparents
        for s in samples:
            print s.dataset
            parents = dbsparents(s.dataset)
            for parent in parents:
                for line in os.popen('dbss rel %s' % parent):
                    if 'CMSSW' in line:
                        print parent, line,
            print

    if False:
        import os
        from dbstools import dbsparents
        for s in [ww,wz,zz]:
            print s.dataset
            parents = dbsparents(s.dataset)
            print parents
            os.system('dbsconfig %s > %s' % (parents[-1], s.name))

        os.system('dbss nevents %s' % x.replace('RECO','RAW'))
        os.system('dbss nevents %s' % x)

    if False:
        import os
        from dbstools import dbsparents
        for s in samples:
            print s.dataset
            def fuf(y):
                x = os.popen(y).read()
                for line in x.split('\n'):
                    try:
                        print int(line)
                    except ValueError:
                        pass
            fuf('dbss nevents %s' % s.dataset)
            fuf('dbss nevents %s' % s.dataset.replace('AODSIM','GEN-SIM-RECO'))

    if False:
        for s in samples:
            print s.name
            os.system('grep "total events" ~/nobackup/crab_dirs/384p3/publish_logs/publish.crab_datamc_%s' % s.name)
            os.system('grep "total events" ~/nobackup/crab_dirs/413p2/publish_logs/publish.crab_datamc_%s' % s.name)
            print

    if False:
        os.system('mkdir ~/scratch/wjets')
        for fn in wjets.filenames:
            assert fn.startswith('/store')
            fn = '/pnfs/cms/WAX/11' + fn
            cmd = 'dccp %s ~/scratch/wjets/' % fn
            print cmd
            os.system(cmd)

    if False:
        for s in samples:
            print s.name
            os.system('dbss site %s' % s.dataset)
            print

    if False:
        for s in samples:
            if s.ana_dataset is None:
                continue
            c = []
            for line in os.popen('dbss ana02 find file.numevents where dataset=%s' % s.ana_dataset):
                try:
                    n = int(line)
                except ValueError:
                    continue
                c.append(n)
            c.sort()
            print s.name, c
