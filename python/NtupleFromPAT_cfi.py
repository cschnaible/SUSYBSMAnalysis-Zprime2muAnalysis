import FWCore.ParameterSet.Config as cms
from SUSYBSMAnalysis.Zprime2muAnalysis.HardInteraction_cff import hardInteraction,hardInteraction_MiniAOD
NtupleFromPAT_MiniAOD = cms.EDAnalyzer('SimpleNtupler_miniAOD',
                        hlt_src = cms.InputTag('TriggerResults','','HLT'),
                        dimu_src = cms.InputTag('SimpleMuonsAllSigns'),
                        met_src = cms.InputTag("slimmedMETs"),
                        jet_src = cms.InputTag("slimmedJets"),
                        beamspot_src = cms.InputTag('offlineBeamSpot'),
                        vertices_src = cms.InputTag('offlineSlimmedPrimaryVertices'),
                        pu_src = cms.InputTag('slimmedAddPileupInfo'),
                        doElectrons = cms.bool(False),
                        # This is re-set in histos.py for MC
                        trigger_paths = cms.vstring(),
                        TriggerResults_src = cms.InputTag('TriggerResults', '', 'RECO'),
                        Prescale_src = cms.InputTag('patTrigger','','RECO'),
                        L1Prescale_min_src = cms.InputTag('patTrigger','l1min','RECO'),
                        genEventInfo = cms.untracked.InputTag('generator'),
                        metFilter = cms.VInputTag(
                            cms.InputTag("Flag_HBHENoiseFilter"), 
                            cms.InputTag("Flag_HBHENoiseIsoFilter"), 
                            cms.InputTag("Flag_EcalDeadCellTriggerPrimitiveFilter"), 
                            cms.InputTag("Flag_eeBadScFilter"), 
                            cms.InputTag("Flag_globalTightHalo2016Filter")
                            )
                        )
NtupleFromPAT = cms.EDAnalyzer('SimpleNtupler',
                                dimu_src = cms.InputTag('SimpleMuonsAllSigns'),
                                met_src = cms.InputTag("patMETsPF"),
                                jet_src = cms.InputTag("cleanPatJets"),
                                doElectrons = cms.bool(False),
                                beamspot_src = cms.InputTag('offlineBeamSpot'),
                                vertices_src = cms.InputTag('offlinePrimaryVertices'),
                                TriggerResults_src = cms.InputTag('TriggerResults', '', 'PAT'),
                                genEventInfo = cms.untracked.InputTag('generator')
                                )
