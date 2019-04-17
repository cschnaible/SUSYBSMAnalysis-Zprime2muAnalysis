# This module is for by-hand implementation of the analysis selection for use 
# with the SimpleNuptler. Eventually, this will be made obsolete by the Our201XSel
# branch that I've made in SimpleNtupler.

Sel = {
        2015 : ['base','cos_angle','opp_sign','vertex_chi2','vertex_m',\
                'trigger','pt53','eta','isTracker','isGlobal',\
                'rel_iso','rel_err','dB',\
                'v_pix_hits','num_trk_lays','v_mu_hits_12','matched_station_12'],

        2016 : ['base','cos_angle','opp_sign','vertex_chi2','vertex_m',\
                'trigger','pt53','eta','isTracker','isGlobal',\
                'rel_iso','rel_err','dB',\
                'v_pix_hits','num_trk_lays','v_mu_hits_12','matched_station_16'],

        2017 : ['base','cos_angle','opp_sign','vertex_chi2','vertex_m',\
                'trigger','pt53','eta','isTracker','isGlobal',\
                'rel_iso','rel_err','dB',\
                'v_pix_hits','num_trk_lays','v_mu_hits_12','matched_station_16'],

        2018 : ['base','cos_angle','opp_sign','vertex_chi2','vertex_m',\
                'trigger_18','pt53','eta','isTracker','isGlobal',\
                'rel_iso','rel_err','dB',\
                'v_pix_hits','num_trk_lays','v_mu_hits_18','matched_station_18'],
        }

AllSelections = {
    'base' : 'GoodDataRan && GoodVtx',
    'cos_angle' : 'cos_angle > -0.9998',
    'opp_sign' : '(lep_id[0]*lep_id[1])<0',
    'same_sign' : '(lep_id[0]*lep_id[1])>0',
    'plus_sign' : '(lep_id[0]>0 && lep_id[1]>0)',
    'minus_sign' : '(lep_id[0]<0 && lep_id[1]<0)',
    'vertex_chi2' : 'vertex_chi2 < 20.',
    'vertex_m' : 'vertex_m >= 60.',
    'trigger' : '(lep_triggerMatchPt[0]>50. || lep_triggerMatchPt[1]>50.)',
    'trigger_18' : '((lep_Mu50_triggerMatchPt[0]>50. || lep_OldMu100_triggerMatchPt[0]>100. || lep_TkMu100_triggerMatchPt[0]>100.) || (lep_Mu50_triggerMatchPt[1]>50. || lep_OldMu100_triggerMatchPt[1]>100. || lep_TkMu100_triggerMatchPt[1]>100.))',
    'pt53' : 'lep_pt[0]>53. && lep_pt[1]>53.',
    'pt30' : 'lep_pt[0]>30. && lep_pt[1]>30.',
    'eta' : 'fabs(lep_eta[0])<2.4 && fabs(lep_eta[1])<2.4',
    'isTracker' : '(lep_isTrackerMuon[0]==1 && lep_isTrackerMuon[1]==1)',
    'isGlobal' : '(lep_isGlobalMuon[0]==1 && lep_isGlobalMuon[1]==1)',
    'rel_iso' : '( (lep_sumPt[0]/lep_tk_pt[0])<0.10 && (lep_sumPt[1]/lep_tk_pt[1])<0.10 )',
    'rel_err' : '( (lep_pt_err[0]/lep_pt[0])<0.30 && (lep_pt_err[1]/lep_pt[1])<0.30 )',
    'v_pix_hits' : '(lep_glb_numberOfValidPixelHits[0]>0 && lep_glb_numberOfValidPixelHits[1]>0)',
    'num_trk_lays' : '(lep_glb_numberOfValidTrackerLayers[0]>5 && lep_glb_numberOfValidTrackerLayers[1]>5)',
    'dB' : '( fabs(lep_dB[0])<0.2 && fabs(lep_dB[1])<0.2 )',

    'v_mu_hits_12' : '(lep_glb_numberOfValidMuonHits[0]>0 && lep_glb_numberOfValidMuonHits[1]>0)',
    'v_mu_hits_18' : '( (lep_glb_numberOfValidMuonHits[0]>0 || lep_tuneP_numberOfValidMuonHits[0]>0) && (lep_glb_numberOfValidMuonHits[1]>0 || lep_tuneP_numberOfValidMuonHits[1]>0) )',

    'matched_station_12' : '(lep_numberOfMatchedStations[0]>1 && lep_numberOfMatchedStations[1]>1)',
    'matched_station_16' : '((lep_numberOfMatchedStations[0] > 1 || (lep_numberOfMatchedStations[0]==1 && !(lep_stationMask[0]== 1 || lep_stationMask[0]==16)) || (lep_numberOfMatchedStations[0]==1 && (lep_stationMask[0]==1 || lep_stationMask[0]==16) && lep_numberOfMatchedRPCLayers[0]>2)) && (lep_numberOfMatchedStations[1] > 1 || (lep_numberOfMatchedStations[1]==1 && !(lep_stationMask[1]== 1 || lep_stationMask[1]==16)) || (lep_numberOfMatchedStations[1]==1 && (lep_stationMask[1]==1 || lep_stationMask[1]==16) && lep_numberOfMatchedRPCLayers[1]>2)))',
    'matched_station_18' : '((lep_numberOfMatchedStations[0]>1 || (lep_numberOfMatchedStations[0]==1 && (lep_expectedNnumberOfMatchedStations[0]==1 || !(lep_stationMask[0]==1 || lep_stationMask[0]==16) || lep_numberOfMatchedRPCLayers[0]>2))) && (lep_numberOfMatchedStations[1]>1 || (lep_numberOfMatchedStations[1]==1 && (lep_expectedNnumberOfMatchedStations[1]==1 || !(lep_stationMask[1]==1 || lep_stationMask[1]==16) || lep_numberOfMatchedRPCLayers[1]>2))))',
    }

SelectionFull = {
        2015:'Our2015Sel>0',
        2016:'Our2016Sel>0',
        2017:'Our2016Sel>0',
        2018:'Our2018Sel>0',
        }

Categories = {
        '':'',
        'bb':'(lep_eta[0] < 1.2 && lep_eta[0] > -1.2 && lep_eta[1] < 1.2 && lep_eta[1] > -1.2)',
        'be':'(lep_eta[0] > 1.2 || lep_eta[0] < -1.2 || lep_eta[1] > 1.2 || lep_eta[1] < -1.2)',
        'ee':'((lep_eta[0] > 1.2 || lep_eta[0] < -1.2) && (lep_eta[1] > 1.2 || lep_eta[1] < -1.2))',
        }

def Nminus1(year,nm1):
    selection = ''
    for s,sel in enumerate(Sel[year]):
        if nm1==sel: continue
        selection += (' && ' if s>0 else '')+AllSelections[sel]
    return selection

def GetSelection(year,selectionList):
    selection = ''
    for s,sel in enumerate(selectionList):
        if sel=='trigger' and year==2018: # kinda messy but workable
            selection += (' && ' if s>0 else '')+AllSelections['trigger_18']
        elif sel=='v_mu_hits_12' and year==2018: # kinda messy but workable
            selection += (' && ' if s>0 else '')+AllSelections['v_mu_hits_18']
        else: selection += (' && ' if s>0 else '')+AllSelections[sel]
    return selection

Selection = {year:'' for year in Sel.keys()}
for year in Sel.keys():
    Selection[year] += GetSelection(year,Sel[year])
#    for s,sel in enumerate(Sel[year]):
#        SelectionTest[year] += (' && ' if s>0 else '')+AllSelections[sel]



# old 

baseSelections = {
    'base' : 'GoodDataRan && GoodVtx',
    'dil_cuts'    : 'cos_angle>-0.9998 && (lep_id[0]*lep_id[1])<0 && vertex_chi2 < 20. && vertex_m>50.',
    }

triggerSel = {
    'trigger'     : '(lep_triggerMatchPt[0]>50. || lep_triggerMatchPt[1]>50.)',
    'trigger18'     : '(lep_triggerMatchPt[0]>0. || lep_triggerMatchPt[1]>0.)',
    'trigger_18' : '((lep_Mu50_triggerMatchPt[0]>0. || lep_OldMu100_triggerMatchPt[0]>0. || lep_TkMu100_triggerMatchPt[0]>0.)'\
                ' || (lep_Mu50_triggerMatchPt[1]>0. || lep_OldMu100_triggerMatchPt[1]>0. || lep_TkMu100_triggerMatchPt[1]>0.))'\
    }
    
leptonBaseSel = {
    'pt'          : 'lep_pt[X]>53.',
    'eta'         : 'fabs(lep_eta[X])<2.4',
    'isTracker'   : 'lep_isTrackerMuon[X]==1',
    'isGlobal'    : 'lep_isGlobalMuon[X]==1',
    'rel_iso'     : '(lep_sumPt[X]/lep_tk_pt[X])<0.10',
    'rel_err'     : '(lep_pt_err[X]/lep_pt[X])<0.3',
    'v_pix_hits'  : 'lep_glb_numberOfValidPixelHits[X]>=1',
    'num_trk_lays' : 'lep_glb_numberOfValidTrackerLayers[X]>5',
    'dB'          : 'fabs(lep_dB[X])<0.2',
    }

leptonSel2012 = {
    'v_mu_hits_12'   : 'lep_glb_numberOfValidMuonHits[X]>0',
    'matched_station_12' : 'lep_numberOfMatchedStations[X]>1 ',
    }

leptonSel2016 = {
    'v_mu_hits_12'   : 'lep_glb_numberOfValidMuonHits[X]>0',
    'matched_station_16' : \
        '(lep_numberOfMatchedStations[X] > 1 '+\
        '|| (lep_numberOfMatchedStations[X]==1 &&'+\
            '!(lep_stationMask[X]== 1 || lep_stationMask[X]==16)) '+\
        '|| (lep_numberOfMatchedStations[X]==1 && '+\
            '(lep_stationMask[X]==1 || lep_stationMask[X]==16) '+\
            '&& lep_numberOfMatchedRPCLayers[X]>2))',
    }

leptonSel2018 = {
    'v_mu_hits_18'   : '(lep_glb_numberOfValidMuonHits[X]>0 || lep_tuneP_numberOfValidMuonHits[X]>0)',
    'matched_station_16' : \
        '(lep_numberOfMatchedStations[X] > 1 '+\
        '|| (lep_numberOfMatchedStations[X]==1 &&'+\
            '!(lep_stationMask[X]== 1 || lep_stationMask[X]==16)) '+\
        '|| (lep_numberOfMatchedStations[X]==1 && '+\
            '(lep_stationMask[X]==1 || lep_stationMask[X]==16) '+\
            '&& lep_numberOfMatchedRPCLayers[X]>2))',
    }

selection2012 = baseSelections['base']+' && '+baseSelections['dil_cuts']+' && '+triggerSel['trigger']
selection2016 = baseSelections['base']+' && '+baseSelections['dil_cuts']+' && '+triggerSel['trigger']
selection2018 = baseSelections['base']+' && '+baseSelections['dil_cuts']+' && '+triggerSel['trigger18']
#selection2012 = baseSelections['dil_cuts']+' && '+triggerSel['trigger']
#selection2016 = baseSelections['dil_cuts']+' && '+triggerSel['trigger']
#selection2018 = baseSelections['dil_cuts']+' && '+triggerSel['trigger_18']

for sel in leptonBaseSel.keys():
    for mu in [0,1]:
        selection2012 += ' && '+leptonBaseSel[sel].replace('X',str(mu))
        selection2016 += ' && '+leptonBaseSel[sel].replace('X',str(mu))
        selection2018 += ' && '+leptonBaseSel[sel].replace('X',str(mu))

for sel in leptonSel2012.keys():
    for mu in [0,1]:
        selection2012 += ' && '+leptonSel2012[sel].replace('X',str(mu))

for sel in leptonSel2016.keys():
    for mu in [0,1]:
        selection2016 += ' && '+leptonSel2016[sel].replace('X',str(mu))

for sel in leptonSel2018.keys():
    for mu in [0,1]:
        selection2018 += ' && '+leptonSel2018[sel].replace('X',str(mu))


#Selection = {
#        2012:selection2012,
#        2016:selection2016,
#        2018:selection2018,
#        }


if __name__=='__main__':
    print Selection[2018]
    print 
    #print Selection[2018]
    print
    print Nminus1(2018,'matched_station_16')
