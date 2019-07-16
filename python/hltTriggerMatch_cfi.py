import FWCore.ParameterSet.Config as cms


muonTriggerMatchHLTMuons = cms.EDProducer('PATTriggerMatcherDRLessByR',
                                          src = cms.InputTag( 'cleanPatMuons' ),
                                          matched = cms.InputTag( 'patTrigger' ),
                                          matchedCuts = cms.string('type("TriggerMuon") && (path("HLT_Mu9*",1,0) || path("HLT_Mu15*",1,0) || path("HLT_Mu24_v*",1,0)|| path("HLT_Mu24*",1,0) || path("HLT_Mu30*",1,0) || path("HLT_Mu40*",1,0) || path("HLT_Mu45*",1,0) || path("HLT_Mu50*",1,0))'),
                                          maxDPtRel   = cms.double( 1. ), 
                                          maxDeltaR   = cms.double( 0.2 ),
                                          resolveAmbiguities    = cms.bool( True ),
                                          resolveByMatchQuality = cms.bool( True )
                                          )

muonTriggerMatchHLTMuonsMiniAOD = cms.EDProducer('PATTriggerMatcherDRLessByR',
                                          src = cms.InputTag( 'slimmedMuons' ),
                                          matched = cms.InputTag( 'patTrigger' ),
                                          matchedCuts = cms.string('type("TriggerMuon") && (path("HLT_Mu9*",1,0) || path("HLT_Mu15*",1,0) || path("HLT_Mu24_v*",1,0)|| path("HLT_Mu24*",1,0) || path("HLT_Mu30*",1,0) || path("HLT_Mu40*",1,0) || path("HLT_Mu45*",1,0) || path("HLT_Mu50*",1,0))'),
                                          maxDPtRel   = cms.double( 1. ), 
                                          maxDeltaR   = cms.double( 0.2 ),
                                          resolveAmbiguities    = cms.bool( True ),
                                          resolveByMatchQuality = cms.bool( True )
)
# To get filter paths
# Search run summary on cmswbm.cern.ch with a run number containing the trigger path name
# "TRIGGER_MODE" -> Search "MuXY" and click it

# -- for updated plugins/Zprime2muLeptonProducer_miniAOD.cc
# Mu50:     hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q::HLT
# OldMu100: hltL3fL1sMu22Or25L1f0L2f10QL3Filtered100Q::HLT
# TkMu100:  hltL3fL1sMu25f0TkFiltered100Q::HLT

# Mu27:     hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q::HLT # <-- This one
# Mu27      hltL3fL1sMu25L1f0L2f10QL3Filtered27Q::HLT (???)
# TkMu27:   hltL3fL1sMu22Or25f0TkFiltered27Q::HLT

def make_string_cut_for_trigger_matching( list_path_names, list_filters_pt, extra=''):
  cut = ''
  if len(list_path_names) != len(list_filters_pt):
    print 'len(list_path_names) != len(list_filters_pt) -> return ', cut
    return cut
  for i, f in enumerate(list_path_names):
    if f != list_path_names[-1]:
      cut += 'userFloat("%s%s_TriggerMatchPt")>=%i || ' % (extra,list_path_names[i], list_filters_pt[i])
    else:                  
      cut += 'userFloat("%s%s_TriggerMatchPt")>=%i ' % (extra,list_path_names[i], list_filters_pt[i])
  return cut

#trigger_pt_threshold = 45
#offline_pt_threshold = 48
trigger_pt_threshold = 50
offline_pt_threshold = 53
#trigger_paths = ['HLT_Mu50_v%i' % i for i in (6, 7, 8, 9, 10, 11)]
#trigger_paths = ['HLT_Mu45_eta2p1_v%i' % i for i in (1,2)]
#trigger_paths = ['HLT_Mu45_eta2p1_v1']
#trigger_paths = ['HLT_Mu50_v1']
#trigger_match = 'userFloat("TriggerMatchPt") > %(trigger_pt_threshold)i && abs(userFloat("TriggerMatchEta")) < 2.1' % locals()
trigger_match = 'userFloat("TriggerMatchPt") > %(trigger_pt_threshold)i ' % locals()

#overall_prescale = 1
prescaled_trigger_pt_threshold = 27
prescaled_offline_pt_threshold = 30
prescaled_trigger_match = trigger_match.replace('Trigger', 'prescaledTrigger').replace('%i' % trigger_pt_threshold, '%i' % prescaled_trigger_pt_threshold)

# http://fwyzard.web.cern.ch/fwyzard/hlt/2015/summary
#Path HLT_Mu27: 2015
# - first seen online on run 248036 (/cdaq/physics/Run2015/5e33/v1.0/HLT/V1)
# - last  seen online on run 260627 (/cdaq/physics/Run2015/25ns14e33/v4.4.5/HLT/V1)
# - V1: (runs 248036 - 252126)
# - V2: (runs 254227 - 260627)
#Path HLT_Mu50:
# - first seen online on run 248036 (/cdaq/physics/Run2015/5e33/v1.0/HLT/V1)
# - last  seen online on run 260627 (/cdaq/physics/Run2015/25ns14e33/v4.4.5/HLT/V1)
# - V1: (runs 248036 - 252126)
# - V2: (runs 254227 - 260627)

# http://fwyzard.web.cern.ch/fwyzard/hlt/2016/summary
#Path HLT_Mu27: 2016
# - first seen online on run 272760 (/cdaq/physics/Run2016/25ns10e33/v1.0/HLT/V16)
# - last  seen online on run 284044 (/cdaq/physics/Run2016/25ns15e33/v4.2.3/HLT/V2)
# - V2: (runs 272760 - 274443)
# - V3: (runs 274954 - 276244)
# - V4: (runs 276282 - 280385)
# - V5: (runs 281613 - 284044)
#Path HLT_TkMu27:
# - first seen online on run 272760 (/cdaq/physics/Run2016/25ns10e33/v1.0/HLT/V16)
# - last  seen online on run 284044 (/cdaq/physics/Run2016/25ns15e33/v4.2.3/HLT/V2)
# - V2: (runs 272760 - 274443)
# - V3: (runs 274954 - 275376)
# - V4: (runs 275656 - 276244)
# - V5: (runs 276282 - 284044)
#Path HLT_Mu50:
# - first seen online on run 272760 (/cdaq/physics/Run2016/25ns10e33/v1.0/HLT/V16)
# - last  seen online on run 284044 (/cdaq/physics/Run2016/25ns15e33/v4.2.3/HLT/V2)
# - V2: (runs 272760 - 274443)
# - V3: (runs 274954 - 276244)
# - V4: (runs 276282 - 280385)
# - V5: (runs 281613 - 284044)
#Path HLT_TkMu50:
# - first seen online on run 274954 (/cdaq/physics/Run2016/25ns10e33/v2.1.0/HLT/V14)
# - last  seen online on run 284044 (/cdaq/physics/Run2016/25ns15e33/v4.2.3/HLT/V2)
# - V1: (runs 274954 - 275376)
# - V2: (runs 275656 - 276244)
# - V3: (runs 276282 - 284044)

trigger_filters_16 = [
        'hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q',
        'hltL3fL1sMu25f0TkFiltered50Q',
        ]
trigger_path_names_16 = [
        'Mu50',
        'TkMu50',
        ]
trigger_path_full_names_16 = [
        'HLT_Mu50_v*',
        'HLT_TkMu50_v*',
        ]
trigger_filters_pt_16 = [
        50,
        50,
        ]
overall_prescale_2016 = 320 # 196 pb-1
#overall_prescale_2016 = 290  # 1828 pb-1
prescaled_trigger_filters_16 = [
        'hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q',
        'hltL3fL1sMu22Or25f0TkFiltered27Q',
        ]
prescaled_trigger_path_names_16 = [
        'Mu27',
        'TkMu27',
        ]
prescaled_trigger_path_full_names_16 = [
        'HLT_Mu27_v*',
        'HLT_TkMu27_v*',
        ]
prescaled_trigger_filters_pt_16 = [
        27,
        27,
        ]
prescaled_trigger_path_name_list_16  = ['HLT_Mu27_v%i' %i for i in (2,3,4,5)]
prescaled_trigger_path_name_list_16 += ['HLT_TkMu27_v%i' %i for i in (2,3,4,5)]
trigger_match_2016 = make_string_cut_for_trigger_matching( trigger_path_names_16, trigger_filters_pt_16 )
prescaled_trigger_match_2016 = make_string_cut_for_trigger_matching( prescaled_trigger_path_names_16, prescaled_trigger_filters_pt_16, extra='prescaled')

# http://fwyzard.web.cern.ch/fwyzard/hlt/2017/summary
#Path HLT_Mu27: 2017
# - first seen online on run 296070 (/cdaq/physics/Run2017/2e34/v1.0.0/HLT/V2)
# - last  seen online on run 306460 (/cdaq/physics/Run2017/2e34/v4.2.1/HLT/V2)
# - V6: (runs 296070 - 297057)
# - V7: (runs 297099 - 297505)
# - V8: (runs 297557 - 299329)
# - V9: (runs 299368 - 299649)
# - V10: (runs 300079 - 302019)
# - V11: (runs 302026 - 306171)
# - V12: (runs 306416 - 306460)
#Path HLT_Mu50:
# - first seen online on run 296070 (/cdaq/physics/Run2017/2e34/v1.0.0/HLT/V2)
# - last  seen online on run 306460 (/cdaq/physics/Run2017/2e34/v4.2.1/HLT/V2)
# - V6: (runs 296070 - 297057)
# - V7: (runs 297099 - 297505)
# - V8: (runs 297557 - 299329)
# - V9: (runs 299368 - 299649)
# - V10: (runs 300079 - 302019)
# - V11: (runs 302026 - 306171)
# - V12: (runs 306416 - 306460)
#Path HLT_OldMu100:
# - first seen online on run 299368 (/cdaq/physics/Run2017/2e34/v2.0.0/HLT/V3)
# - last  seen online on run 306460 (/cdaq/physics/Run2017/2e34/v4.2.1/HLT/V2)
# - V1: (runs 299368 - 299649)
# - V2: (runs 300079 - 302019)
# - V3: (runs 302026 - 306460)
#Path HLT_TkMu100:
# - first seen online on run 299368 (/cdaq/physics/Run2017/2e34/v2.0.0/HLT/V3)
# - last  seen online on run 306460 (/cdaq/physics/Run2017/2e34/v4.2.1/HLT/V2)
# - V1: (runs 299368 - 299649)
# - V2: (runs 300079 - 306460)

# http://fwyzard.web.cern.ch/fwyzard/hlt/2018/summary
#Path HLT_Mu27: 2018
# - first seen online on run 315252 (/cdaq/physics/Run2018/2e34/v1.1.0/HLT/V4)
# - last  seen online on run 325175 (/cdaq/physics/Run2018/2e34/v3.6.1/HLT/V2)
# - V12: (runs 315252 - 316271)
# - V13: (runs 316361 - 325175)
#Path HLT_Mu50:
# - first seen online on run 315252 (/cdaq/physics/Run2018/2e34/v1.1.0/HLT/V4)
# - last  seen online on run 325175 (/cdaq/physics/Run2018/2e34/v3.6.1/HLT/V2)
# - V12: (runs 315252 - 316271)
# - V13: (runs 316361 - 325175)
#Path HLT_OldMu100:
# - first seen online on run 315252 (/cdaq/physics/Run2018/2e34/v1.1.0/HLT/V4)
# - last  seen online on run 325175 (/cdaq/physics/Run2018/2e34/v3.6.1/HLT/V2)
# - V3: (runs 315252 - 325175)
#Path HLT_TkMu100:
# - first seen online on run 315252 (/cdaq/physics/Run2018/2e34/v1.1.0/HLT/V4)
# - last  seen online on run 325175 (/cdaq/physics/Run2018/2e34/v3.6.1/HLT/V2)
# - V2: (runs 315252 - 325175)

trigger_filters_18 = [
        'hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q',
        'hltL3fL1sMu22Or25L1f0L2f10QL3Filtered100Q',
        'hltL3fL1sMu25f0TkFiltered100Q',
        ]
trigger_path_names_18 = [
        'Mu50',
        'OldMu100',
        'TkMu100'
        ]
trigger_path_full_names_18 = [
        'HLT_Mu50_v*',
        'HLT_OldMu100_v*',
        'HLT_TkMu100_v*'
        ]
trigger_filters_pt_18 = [
        50,
        100,
        100
        ]
overall_prescale_2017 = 561
overall_prescale_2018 = 500
prescaled_trigger_filters_18 = [
        'hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q'
        ]
prescaled_trigger_path_names_18 = [
        'Mu27'
        ]
prescaled_trigger_path_full_names_18 = [
        'HLT_Mu27_v*'
        ]
prescaled_trigger_path_name_list_17 = ['HLT_Mu27_v%i' % i for i in (6,7,8,9,10,11,12)]
prescaled_trigger_path_name_list_18 = ['HLT_Mu27_v%i' % i for i in (12,13)]
prescaled_trigger_filters_pt_18 = [
        27,
        ]

trigger_match_2018 = make_string_cut_for_trigger_matching( trigger_path_names_18, trigger_filters_pt_18 )
prescaled_trigger_match_2018 = make_string_cut_for_trigger_matching( prescaled_trigger_path_names_18, prescaled_trigger_filters_pt_18, extra='prescaled')

