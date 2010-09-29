import FWCore.ParameterSet.Config as cms

from SUSYBSMAnalysis.Zprime2muAnalysis.HardInteraction_cff import hardInteraction
from SUSYBSMAnalysis.Zprime2muAnalysis.TriggerDecision_cff import triggerDecision

EfficiencyFromMC = cms.EDAnalyzer('EfficiencyFromMC',
                                  hardInteraction = hardInteraction,
                                  triggerDecision = triggerDecision,
                                  nbins = cms.uint32(2000),
                                  min_mass = cms.double(0),
                                  max_mass = cms.double(2000),
                                  use_resonance_mass = cms.bool(False),
                                  dimuon_src = cms.InputTag('dimuons')
                                  )
