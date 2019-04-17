# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 -s DIGI,L1,DIGI2RAW,RAW2DIGI,L1Reco,RECO --pileup=NoPileUp --filein outputFile.root --geometry DB --conditions auto:run2_mc --eventcontent=FEVTDEBUG --dirout=./ -n 50 --fileout file:mb_13TeV_mu_digi_test.root --mc --python_filename=DIGI_TEST.py --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('RECO')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13TeVEarly2017Collision_cfi')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    fileNames = cms.untracked.vstring('file:SingleMuPt1000_pythia8_cfi_GEN_SIM.root'),
    inputCommands = cms.untracked.vstring('keep *', 
        'drop *_genParticles_*_*', 
        'drop *_genParticlesForJets_*_*', 
        'drop *_kt4GenJets_*_*', 
        'drop *_kt6GenJets_*_*', 
        'drop *_iterativeCone5GenJets_*_*', 
        'drop *_ak4GenJets_*_*', 
        'drop *_ak7GenJets_*_*', 
        'drop *_ak8GenJets_*_*', 
        'drop *_ak4GenJetsNoNu_*_*', 
        'drop *_ak8GenJetsNoNu_*_*', 
        'drop *_genCandidatesForMET_*_*', 
        'drop *_genParticlesForMETAllVisible_*_*', 
        'drop *_genMetCalo_*_*', 
        'drop *_genMetCaloAndNonPrompt_*_*', 
        'drop *_genMetTrue_*_*', 
        'drop *_genMetIC5GenJs_*_*'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('testReco.root'),
    outputCommands = process.FEVTDEBUGEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

process.XMLFromDBSource.label = cms.string("Extended")
# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag.toGet = cms.VPSet(
#
# fixed TrackerAlignment scenario (vd mail/thread Patrick Connor 8.Aug.2018)
# fixed for 2018 productions, corrects a huge weak mode (twist-like ?)
# not built within a GT yet to date... will go inside a GT for the ultralegacy rereco of 2017 MC
# -->  TrackerAlignment_Upgrade2017_realistic_v3 
        cms.PSet(record = cms.string("TrackerAlignmentRcd"),
                 tag = cms.string("TrackerAlignment_Upgrade2017_realistic_v3"),
                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                 )
#
# startup
#        cms.PSet(record = cms.string("DTAlignmentRcd"),
#                 tag = cms.string("DTAlignment_CRAFT15HWBased_v1_mc"),
#                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
#                 ),
#        cms.PSet(record = cms.string("CSCAlignmentRcd"),
#                 tag = cms.string("CSCAlignment_CRAFT15HWBased_v1_mc"),
#                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
#                 ),
#        cms.PSet(record = cms.string("DTAlignmentErrorExtendedRcd"),
#                 tag = cms.string("DTAlignmentErrorsExt_2016_StartupHW_mc"),
#                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
#                 ),
#        cms.PSet(record = cms.string("CSCAlignmentErrorExtendedRcd"),
#                 tag = cms.string("CSCAlignmentErrorsExt_2016_StartupHW_mc"),
#                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
#                 )
# zero APE
#        cms.PSet(record = cms.string("DTAlignmentErrorExtendedRcd"),
#                 tag = cms.string("MuonDTAPEObjectsExtended_v0_mc"),
#                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
#                 ),
#        cms.PSet(record = cms.string("CSCAlignmentErrorExtendedRcd"),
#                 tag = cms.string("MuonCSCAPEObjectsExtended_v0_mc"),
#                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
#                 )
        )

# Path and EndPath definitions
process.digitisation_step = cms.Path(process.pdigi)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.raw2digi_step = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGoutput_step = cms.EndPath(process.FEVTDEBUGoutput)

# Schedule definition
process.schedule = cms.Schedule(process.digitisation_step,process.digi2raw_step,process.raw2digi_step,process.reconstruction_step,process.endjob_step,process.FEVTDEBUGoutput_step)


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
