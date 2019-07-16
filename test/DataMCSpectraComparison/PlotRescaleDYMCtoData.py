'''
Compare Data and MC after rescaling by some kinematic distribution
Necessary to run MakeRescaleDYMCtoData.py first
'''
import ROOT as R
R.gROOT.SetBatch(True)
import logging 
import numpy as np
import array, math
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples# samples18, samples17, samples16
import SUSYBSMAnalysis.Zprime2muAnalysis.lumberjack as lumberjack
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools_chris import poisson_intervalize, divide_bin_width, clopper_pearson_poisson_means, cumulative_histogram, move_overflow_into_last_bin
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d','--tdir',default='ourpre')
parser.add_argument('-w','--where',default='www_compare_datamc',help='Where to store plots')
parser.add_argument('-y','--year',default=2018,type=int,help='Which year(s) to compare to MC')
#parser.add_argument('-s','--selection',default='',help='Selection to apply in addition to Z-peak mass window')
parser.add_argument('-ly','--logy',action='store_true',default=False)
parser.add_argument('-n','--name',default='')
parser.add_argument('-bw','--bin-width',dest='bin_width',action='store_true')
parser.add_argument('--overflow',action='store_true',help='Move overflow into last bin')
parser.add_argument('--do-stack',dest='do_stack',action='store_true')
parser.add_argument('-cum','--cumulative',action='store_true')
parser.add_argument('-dy','--dy-sample',default='powheg',help='Which DY MC to use: powheg, ht, madgraph, amcatnlo')
parser.add_argument('-ds','--data-sel',default='',help='Additional selection to apply to data only (e.g. prescale)')
parser.add_argument('--rescale-hists',default='',help='Rescale histogram file name')
parser.add_argument('--rescale-by',default='lead_pt',help='Quantity to rescale by')
parser.add_argument('--rescale-to',default='data',help='Rescale to data or mc')
args = parser.parse_args()

rescale_hists = '_'+args.rescale_hists if args.rescale_hists else ''
year = args.year
rels = ['80X','94X','102X']
relYearMap = {
        2016:'80X',2017:'94X',2018:'102X'
        }
theRel = relYearMap[year]
theVar = args.rescale_by
theNum = args.rescale_to

varDraw = {
        'lead_pt':{
            'bins':{
                'log':{'lims':[30.0,150.0],'nbins':30},
                'lin':{'lims':[30.0,150.0],'nbins':24},
                },
            'cats':['b','e','all'],
            },
        'sub_pt':{
            'bins':{
                'log':{'lims':[30.0,150.0],'nbins':30},
                'lin':{'lims':[30.0,150.0],'nbins':24},
                },
            'cats':['b','e','all'],
            },
        'mass':{
            'bins':{
                'lin':{'lims':[60.0,120.0],'nbins':30},
                },
            'cats':['bb','beee','all'],
            },
        'dil_pt':{
            'bins':{
                'log':{'lims':[0.1,300.0],'nbins':30},
                'lin':{'lims':[0,300.0],'nbins':30},
                },
            'cats':['bb','beee','all'],
            },
        'dil_rap':{
            'bins':{
                'lin':{'lims':[-3.0,3.0],'nbins':15},
                },
            'cats':['bb','beee','all'],
            },
        'gen_dil_rap':{
            'bins':{
                'lin':{'lims':[-3.0,3.0],'nbins':15},
                },
            'cats':['bb','beee','all'],
            },
        }

def get_log_bins(lims,nbins):
    bins = np.logspace(np.log10(lims[0]),np.log10(lims[1]),nbins+1)
    return bins
def get_lin_bins(lims,nbins):
    bins = array.array('d',[lims[0] + i*(lims[1]-lims[0])/nbins for i in range(0,nbins+1)])
    return bins
get_binning = {
        'log':get_log_bins,
        'lin':get_lin_bins,
        }

#sel_tree = ' and '.join(['t.'+val.strip() for val in args.selection.split('&&')])
toDrawList = ['lead_pt','sub_pt','mass','dil_pt','dil_rap']

dyLists = {
    'powheg' : ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf'],
    'ht' : ['dyJetsToLL_ht100to200','dyJetsToLL_ht200to400','dyJetsToLL_ht400to600','dyJetsToLL_ht600to800','dyJetsToLL_ht800to1200','dyJetsToLL_ht1200to2500','dyJetsToLL_ht2500toInf'],
    'madgraph' : ['dyInclusive50_madgraph'],
    'amcatnlo' : ['dyInclusive50_amcatnlo'],
    }
otherMCs = {
        2016:{
            'ttbar':['ttbar_lep_50to500','ttbar_lep_500to800','ttbar_lep_800to1200','ttbar_lep_1200to2500','ttbar_lep_2500toInf'],
            'diboson':['WW_50to200','WW_200to600','WW_600to1200','WW_1200to2500','WW_2500toInf','ZZ','WZ'],
            'singletop':['tW','tbarW'],
            'Wjets':['Wjets'],
            'tautau':['dyTauTau_madgraph'],
            },
        2017:{
            'ttbar':['ttbar_lep'],
            'diboson':['WW','ZZ','WZ'],
            'singletop':['tW','tbarW'],
            'Wjets':['Wjets'],
            'tautau':['dyTauTau_madgraph'],
            },
        2018:{
            'ttbar':['ttbar_lep'],
            'diboson':['WW','ZZ','WZ'],
            'singletop':['tW','tbarW'],
            'Wjets':['Wjets'],
            'tautau':['dyTauTau_madgraph'],
            },
        }

nonDYmc = ['ttbar','diboson','singletop','Wjets','tautau']

allMClist = list(dyLists[args.dy_sample])
nonDYlist = []
for nondy in nonDYmc:
    allMClist += otherMCs[year][nondy]
    nonDYlist += otherMCs[year][nondy]

cats = {
        'bb':  '(abs(t.lep_eta[0])<=1.2 and abs(t.lep_eta[1])<=1.2)',
        'beee':'(abs(t.lep_eta[0])>1.2   or abs(t.lep_eta[1]>1.2))',
        'ee':  '(abs(t.lep_eta[0])>1.2  and abs(t.lep_eta[1]>1.2))',
        # this really only works if you draw one of the muons
        # e.g. leading or sub-leading
        'b':'abs(t.lep_eta[draw_idx])<=1.2',
        'e':'abs(t.lep_eta[draw_idx])>1.2',
        'all':'True',
        }
#sel_tree = ' and '.join(['t.'+val.strip() for val in args.selection.split('&&')])
#sel = args.selection
#if args.category!='all':
#    #sel += ' && '+cats[args.category][0]
#    #sel_tree +=' and '+cats[args.category][1]
#    sel_tree +=' and '+cats[args.category]



allyears = [2016,2017,2018]
info = {
        2016:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/data/',
            'file':'ana_datamc_Run2016_17Jul2018.root',
            'lumi':36294.593964906585693,
            'our':{
                'dir':'Our2016MuonsOppSignNtuple',
                'pre':1.,
                #'lumi':36294.593964906585693,
                },
            'ourcommonpre':{
                'dir':'Our2016MuPrescaledCommonMuonsOppSignNtuple',
                'pre':500.,
                #'lumi':36285.0595135,
                },
            'ourpre':{
                'dir':'Our2016MuPrescaledMuonsOppSignNtuple',
                'pre':146.323326629,
                #'lumi':36285.0595135,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/mc/',
            'mc':samples[2016],
            },
        2017:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/data/',
            'file':'ana_datamc_Run2017_31Mar2018.root',
            'lumi':42079.880396,
            'our':{
                'dir':'Our2018MuonsOppSignNtuple',
                'pre':1.,
                #'lumi':42079.880396,
                },
            'ourcommonpre':{
                'dir':'Our2018MuPrescaledCommonMuonsOppSignNtuple',
                'pre':561.,
                #'lumi':42070.654731,
                },
            'ourpre':{
                'dir':'Our2018MuPrescaledMuonsOppSignNtuple',
                'pre':236.085072878,
                #'lumi':42070.654731,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/mc/',
            'mc':samples[2017],
            },
        2018:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/data/',
            'file':'ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root',
            'lumi':61298.775231718995,
            'our':{
                'dir':'Our2018MuonsOppSignNtuple',
                'pre':1.,
                #'lumi':61298.7752317,
                #'lumi':61302.3918373,
                },
            'ourcommonpre':{
                'dir':'Our2018MuPrescaledMuonsOppSignNtuple',
                'pre':500.,
                #'lumi':61291.8425445,
                #'lumi':61302.3918373,
                },
            'ourpre':{
                'dir':'Our2018MuPrescaledNoCommonMuonsOppSignNtuple',
                'pre':486.949643091,
                #'lumi':61291.8425445,
                #'lumi':61302.3918373,
                #'lumi':61298.775231718995,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/mc/',
            'mc':samples[2018],
            },
        }

def get_sum_weights(f):
    weights = getattr(f,'EventCounter').Get('weights')
    return weights.GetBinContent(2)-weights.GetBinContent(1)

def get_log_bins(lims,nbins):
    bins = np.logspace(np.log10(lims[0]),np.log10(lims[1]),nbins+1)
    return bins
def get_lin_bins(lims,nbins):
    bins = array.array('d',[lims[0] + i*(lims[1]-lims[0])/nbins for i in range(0,nbins+1)])
    return bins
get_binning = {
        'log':get_log_bins,
        'lin':get_lin_bins,
        }

dataHists = {var:{cat:{x:{} for x in varDraw[var]['bins'].keys()} for cat in varDraw[var]['cats']} for var in toDrawList}
for var in toDrawList:
    for cat in varDraw[var]['cats']:
        for x in varDraw[var]['bins'].keys():
            hname = 'hdata_'+str(year)+'_'+var+'_'+cat+'_'+x
            bins = get_binning[x](varDraw[var]['bins'][x]['lims'],int(varDraw[var]['bins'][x]['nbins']))
            dataHists[var][cat][x] = R.TH1D(hname,'',int(varDraw[var]['bins'][x]['nbins']),bins)
            dataHists[var][cat][x].SetDirectory(0)

# Make Data histograms
# Data
print 'Data'
f = R.TFile(info[year]['path']+info[year]['file'])
t = f.Get(info[year][args.tdir]['dir']+'/t')
t.SetBranchStatus('*',0)
t.SetBranchStatus('lep_pt',1)
t.SetBranchStatus('lep_eta',1)
t.SetBranchStatus('vertex_m',1)
t.SetBranchStatus('dil_pt',1)
t.SetBranchStatus('dil_rap',1)
#hdata = hist.Clone('hdata')
for e,entry in enumerate(t):
    t.GetEntry(e)
    #if not eval(sel_tree): continue
    if not (60 < t.vertex_m < 120): continue

    (lead_idx,sub_idx) = (0,1) if t.lep_pt[0]>t.lep_pt[1] else (1,0)

    lead_pt,lead_eta = t.lep_pt[lead_idx],t.lep_eta[lead_idx]
    lead_cat = 'b' if abs(lead_eta)<=1.2 else 'e'

    sub_pt,sub_eta = t.lep_pt[sub_idx],t.lep_eta[sub_idx]
    sub_cat = 'b' if abs(sub_eta)<=1.2 else 'e'

    Z_cat = 'bb' if (abs(lead_eta)<=1.2 and abs(sub_eta)<=1.2) else 'beee'
    for x in varDraw['lead_pt']['bins'].keys():
        dataHists['lead_pt']['all'][x].Fill(lead_pt)
        dataHists['lead_pt'][lead_cat][x].Fill(lead_pt)

    for x in varDraw['sub_pt']['bins'].keys():
        dataHists['sub_pt']['all'][x].Fill(sub_pt)
        dataHists['sub_pt'][sub_cat][x].Fill(sub_pt)

    for x in varDraw['mass']['bins'].keys():
        dataHists['mass']['all'][x].Fill(t.vertex_m)
        dataHists['mass'][Z_cat][x].Fill(t.vertex_m)

    for x in varDraw['dil_pt']['bins'].keys():
        dataHists['dil_pt']['all'][x].Fill(t.dil_pt)
        dataHists['dil_pt'][Z_cat][x].Fill(t.dil_pt)

    for x in varDraw['dil_rap']['bins'].keys():
        dataHists['dil_rap']['all'][x].Fill(t.dil_rap)
        dataHists['dil_rap'][Z_cat][x].Fill(t.dil_rap)
f.Close()


rescaleList = ['lead_pt','sub_pt','mass','dil_pt','dil_rap']
varCats = {
        #'lead_pt':{'cats':['b','e','f','all'],'bins':['log','lin']},
        #'sub_pt':{'cats':['b','e','f','all'],'bins':['log','lin']},
        #'mass':{'cats':['bb','beee','ee','all'],'bins':['lin']},
        'lead_pt':{'cats':['b','e','all'],'bins':['log','lin']},
        'sub_pt':{'cats':['b','e','all'],'bins':['log','lin']},
        'gen_lead_pt':{'cats':['b','e','all'],'bins':['log','lin']},
        'gen_sub_pt':{'cats':['b','e','all'],'bins':['log','lin']},
        'mass':{'cats':['bb','beee','all'],'bins':['lin']},
        'gen_mass':{'cats':['bb','beee','all'],'bins':['lin']},
        'dil_pt':{'cats':['bb','beee','all'],'bins':['lin','log']},
        'gen_dil_pt':{'cats':['bb','beee','all'],'bins':['lin','log']},
        'dil_rap':{'cats':['bb','beee','all'],'bins':['lin']},
        'gen_dil_rap':{'cats':['bb','beee','all'],'bins':['lin']},
        }
#ratioFile = R.TFile('rescale/rescale_histograms_20190522.root')
if theNum in ['2016','2017','2018']:
    scaleToWhatList = allyears
    scaleHistName = 'dataRat'
elif theNum in ['80X','94X','102X']:
    scaleToWhatList = rels
    scaleHistName = 'mcRat'
    rescaleList += ['gen_lead_pt','gen_sub_pt','gen_mass','gen_dil_pt','gen_dil_rap']
else:
    raise ValueError(theNum,'is not correct')

print 'Get rescale histograms'
ratioFile = R.TFile('rescale/rescale_histograms'+rescale_hists+'.root')
hratios = {num:{rel:{var:{cat:{x:{} for x in varCats[var]['bins']} for cat in varCats[var]['cats']} for var in rescaleList} for rel in rels} for num in scaleToWhatList}
for num in scaleToWhatList:
    for rel in rels:
        if num==rel: continue
        for var in rescaleList:
            for cat in varCats[var]['cats']:
                for x in varCats[var]['bins']:
                    hname = scaleHistName+'_'+str(num)+'_'+rel+'_'+var+'_'+cat+'_'+x
                    hratios[num][rel][var][cat][x] = ratioFile.Get(hname).Clone()
                    hratios[num][rel][var][cat][x].SetDirectory(0)
ratioFile.Close()

allMCHists = {name:{var:{cat:{x:{} for x in varDraw[var]['bins'].keys()} for cat in varDraw[var]['cats']} for var in toDrawList} for name in allMClist}
for mc in allMClist:
    for var in toDrawList:
        for cat in varDraw[var]['cats']:
            for x in varDraw[var]['bins'].keys():
                hname = 'hmc_'+mc+'_'+var+'_'+cat+'_'+x
                bins = get_binning[x](varDraw[var]['bins'][x]['lims'],int(varDraw[var]['bins'][x]['nbins']))
                allMCHists[mc][var][cat][x] = R.TH1D(hname,'',int(varDraw[var]['bins'][x]['nbins']),bins)
                allMCHists[mc][var][cat][x].SetDirectory(0)


# Make MC histograms for DY MC
#for mc in reversed(dyLists['powheg']):
for mc in reversed(allMClist):
    print mc
    mcFile = R.TFile(info[year]['mcpath']+'ana_datamc_'+mc+'.root')
    t = mcFile.Get(info[year][args.tdir]['dir']+'/t')
    t.SetBranchStatus('*',0)
    t.SetBranchStatus('lep_pt',1)
    t.SetBranchStatus('lep_eta',1)
    t.SetBranchStatus('gen_lep_pt',1)
    t.SetBranchStatus('gen_lep_eta',1)
    t.SetBranchStatus('vertex_m',1)
    t.SetBranchStatus('gen_dil_pt',1)
    t.SetBranchStatus('dil_pt',1)
    t.SetBranchStatus('dil_rap',1)
    t.SetBranchStatus('gen_dil_rap',1)
    t.SetBranchStatus('gen_res_mass',1)
    t.SetBranchStatus('genWeight',1)
    for e,entry in enumerate(t):
        t.GetEntry(e)
        #if not eval(sel_tree): continue
        if not (60 < t.vertex_m < 120): continue
        (lead_idx,sub_idx) = (0,1) if t.lep_pt[0]>t.lep_pt[1] else (1,0)
        (gen_lead_idx,gen_sub_idx) = (0,1) if t.gen_lep_pt[0]>t.gen_lep_pt[1] else (1,0)
        
        lead_pt,lead_eta = t.lep_pt[lead_idx],t.lep_eta[lead_idx]
        lead_cat = 'b' if abs(lead_eta)<=1.2 else 'e'

        gen_lead_pt,gen_lead_eta= t.gen_lep_pt[gen_lead_idx],t.gen_lep_eta[gen_lead_idx]
        gen_lead_cat = 'b' if abs(gen_lead_eta)<=1.2 else 'e'

        sub_pt,sub_eta = t.lep_pt[sub_idx],t.lep_eta[sub_idx]
        sub_cat = 'b' if abs(sub_eta)<=1.2 else 'e'

        gen_sub_pt,gen_sub_eta= t.gen_lep_pt[gen_sub_idx],t.gen_lep_eta[gen_sub_idx]
        gen_sub_cat = 'b' if abs(gen_sub_eta)<=1.2 else 'e'

        Z_cat = 'bb' if (abs(lead_eta)<=1.2 and abs(sub_eta)<=1.2) else 'beee'
        gen_Z_cat = 'bb' if (abs(gen_lead_eta)<=1.2 and abs(gen_sub_eta)<=1.2) else 'beee'

        if theVar=='mass': mass = t.vertex_m
        elif theVar=='gen_mass': gen_mass = t.gen_res_mass
        elif theVar=='dil_pt': dil_pt = t.dil_pt
        elif theVar=='gen_dil_pt': gen_dil_pt = t.gen_dil_pt
        elif theVar=='dil_rap': dil_rap = t.dil_rap
        elif theVar=='gen_dil_rap': gen_dil_rap = t.gen_dil_rap

        if theVar=='lead_pt': theCat = lead_cat
        if theVar=='gen_lead_pt': theCat = gen_lead_cat
        elif theVar=='sub_pt': theCat = sub_cat
        elif theVar=='gen_sub_pt': theCat = gen_sub_cat
        elif theVar in ['mass','dil_pt','dil_rap']: theCat = Z_cat
        elif theVar in ['gen_mass','gen_dil_pt','gen_dil_rap']: theCat = gen_Z_cat

        xbin = hratios[theNum][theRel][theVar][theCat]['lin'].FindBin(eval(theVar)) # requires theVar = ['lead_pt','sub_pt','mass']
        if 'dy' in mc and 'Tau' not in mc:
            weight = hratios[theNum][theRel][theVar][theCat]['lin'].GetBinContent(xbin)
            #print eval(theVar),weight
            #weighterr = hratios[theNum][theRel][theVar][theCat][x].GetBinError(xbin)
            weight *= t.genWeight
        else:
            weight = t.genWeight

        for x in varDraw[var]['bins'].keys():
            for var in ['lead_pt','sub_pt']:
                mucat = lead_cat if var=='lead_pt' else sub_cat
                allMCHists[mc][var]['all'][x].Fill(eval(var),weight)
                allMCHists[mc][var][mucat][x].Fill(eval(var),weight)
            allMCHists[mc]['dil_pt']['all'][x].Fill(t.dil_pt,weight)
            allMCHists[mc]['dil_pt'][Z_cat][x].Fill(t.dil_pt,weight)
            if x=='log': continue
            allMCHists[mc]['mass']['all'][x].Fill(t.vertex_m,weight)
            allMCHists[mc]['mass'][Z_cat][x].Fill(t.vertex_m,weight)
            allMCHists[mc]['dil_rap']['all'][x].Fill(t.dil_rap,weight)
            allMCHists[mc]['dil_rap'][Z_cat][x].Fill(t.dil_rap,weight)
    info[year]['mc'][mc].sum_weights = get_sum_weights(mcFile)
    mcFile.Close()



def mc_stuff(name):
    if 'powheg'==name:
        return '#gamma/Z #rightarrow #mu^{+}#mu^{-} (POWHEG)',R.kAzure+1
    if 'madgraph'==name:
        return '#gamma/Z #rightarrow #mu^{+}#mu^{-} (MadGraph MLM)',R.kAzure+1
    if 'amcatnlo'==name:
        return '#gamma/Z #rightarrow #mu^{+}#mu^{-} (aMC@NLO FxFx)',R.kAzure+1
    if 'ht'==name:
        return '#gamma/Z #rightarrow #mu^{+}#mu^{-} (HT-bin MADGRAPH)',R.kAzure+1
    if 'ttbar'==name:
        return 't#bar{t}',R.kRed-4
    if 'singletop'==name:
        return 'single top', R.kViolet+1
    if 'diboson'==name:
        return 'diboson', R.kGreen+1
    if 'Wjets'==name:
        return 'jets',R.kOrange+1
    if 'tautau'== name:
        return '#gamma/Z #rightarrow #tau^{+}#tau^{-}',R.kBlue+1
    if name==2016:
        return '80X Simulation', R.kRed-4
    if name==2017:
        return '94X Simulation', R.kViolet+1
    if name==2018:
        return '102X Simulation', R.kAzure+1


def get_color(name):
    if name in dyLists['powheg']:
        return mc_stuff('powheg')[1]

    elif name in dyLists['ht']:
        return mc_stuff('ht')[1]

    elif name in dyLists['madgraph']:
        return mc_stuff('madgraph')[1]

    elif name in dyLists['amcatnlo']:
        return mc_stuff('amcatnlo')[1]

    elif name in otherMCs[year]['ttbar']:
        return mc_stuff('ttbar')[1]

    elif name in otherMCs[year]['singletop']:
        return mc_stuff('singletop')[1]

    elif name in otherMCs[year]['diboson']:
        return mc_stuff('diboson')[1]

    elif name in otherMCs[year]['tautau']:
        return mc_stuff('tautau')[1]

    elif name in otherMCs[year]['Wjets']:
        return mc_stuff('Wjets')[1]


def pretty(arg):
    ret = {
        'vertex_m':'m(#mu^{+}#mu^{-}) [GeV]',
        'mass':'m(#mu^{+}#mu^{-}) [GeV]',
        'cos_angle':'cos(#alpha)',
        'dil_pt':'p_{T}(#mu^{+}#mu^{-}) [GeV]',
        'dil_rap':'y(#mu^{+}#mu^{-})',
        'lep_pt':'p_{T}(#mu) [GeV]',
        'lead_pt':'leading p_{T}(#mu) [GeV]',
        'sub_pt':'sub-leading p_{T}(#mu) [GeV]',
        'n_dils':'N(#mu^{+}#mu^{-}) passing selection',
        'nvertices':'N(primary vertices)',
        'lep_Mu27_triggerMatchPt':'Mu27 trigger match p_{T}(#mu) [GeV]',
        }
    for val in ret.keys():
        if val in arg: return ret[val]

def do_logging(logger,var,cat,x):
    logger.info('\n'+'*'*15+'\n')
    logger.info(var+' '+cat+' '+x)
    logger.info(args)
    logger.info(theNum+' '+theRel+' '+theVar)
    logger.info(allMClist)
    #logger.info(sel_tree) # always Z-mass window
    logger.info('\n'+'*'*15+'\n')
    logger.info('Data')
    data_int = dataHists[var][cat][x].Integral()
    logger.info(data_int)
    logger.info('\n'+'*'*15+'\n')
    logger.info('MC')
    mc_int = 0
    mc_entries= 0
    for mc in reversed(allMClist):
        logger.info('{mc} {integral}'.format(mc=mc,integral=allMCHists[mc][var][cat][x].Integral()))
        mc_int += allMCHists[mc][var][cat][x].Integral()
        mc_entries += allMCHists[mc][var][cat][x].GetEntries()
    logger.info('\n'+'*'*15+'\n')
    logger.info('{integral} {entries}'.format(integral=mc_int,entries=mc_entries))
    logger.info('\n'+'*'*15+'\n')
    r,l,h = clopper_pearson_poisson_means(data_int,mc_int)
    logger.info('{} {}'.format(data_int, 1./math.sqrt(data_int)))
    logger.info('{} {} {}'.format(mc_int, mc_entries, 1./math.sqrt(mc_entries)))
    err1 = r*math.sqrt(pow(1./math.sqrt(data_int),2) + pow(1./math.sqrt(mc_entries),2))
    logger.info('{d} / {mc} = {rat} {err1} {err2}'.format(d=data_int, mc=mc_int, rat=r, err1=err1, err2=(h-r + r-l)/2))
    tau = 1.0 # data/mc 'should' be one
    p_bi = R.TMath.BetaIncomplete(1./(1+tau),data_int,int(mc_int)+1)
    z_bi = math.sqrt(2)*R.TMath.ErfInverse(1-2*p_bi)
    logger.info('P-value '+str(p_bi)+' Z-value '+str(z_bi))
    logger.info('\n'+'*'*15+'\n')

for var in toDrawList:
    for cat in varDraw[var]['cats']:
        for x in varDraw[var]['bins'].keys():
            outName = var+'_'+cat+'_'+x+'_'+str(year)+'_'+theVar+'_'+args.name
            fullOutName = args.where+'/'+outName
            # Combine MCs
            hname = 'hmc_'+var+'_'+cat+'_'+x
            bins = get_binning[x](varDraw[var]['bins'][x]['lims'],int(varDraw[var]['bins'][x]['nbins']))
            hmc  = R.TH1D(hname,'',int(varDraw[var]['bins'][x]['nbins']),bins)
            for m,mc in enumerate(reversed(allMClist)):
                scale_by = info[year]['mc'][mc].cross_section / float(info[year]['mc'][mc].sum_weights)
                scale_by *= info[year]['lumi'] / info[year][args.tdir]['pre']
                allMCHists[mc][var][cat][x].Scale(scale_by)
                if args.overflow: move_overflow_into_last_bin(allMCHists[mc][var][cat][x])
                hmc.Add(allMCHists[mc][var][cat][x])
            # Do Logging -- needs to be done after (xs/nevents) * (lumi/pre) scaling
            lumberjack.setup_logger(outName,fullOutName+'.log')
            logger = logging.getLogger(outName)
            do_logging(logger,var,cat,x)
            # Do bin width and cumulative
            if args.bin_width:
                gdata = poisson_intervalize(dataHists[var][cat][x],bin_width=args.bin_width,zero_ex=True)
                divide_bin_width(hmc)
                divide_bin_width(dataHists[var][cat][x])
            elif args.cumulative:
                hmc = cumulative_histogram(hmc)
                dataHists[var][cat][x] = cumulative_histogram(dataHists[var][cat][x])
                gdata = poisson_intervalize(dataHists[var][cat][x],bin_width=False,zero_ex=True)
            elif args.overflow:
                move_overflow_into_last_bin(dataHists[var][cat][x])
                gdata = poisson_intervalize(dataHists[var][cat][x],bin_width=False,zero_ex=True)
            else:
                gdata = poisson_intervalize(dataHists[var][cat][x],bin_width=False,zero_ex=True)
            #
            # Actually make the thing
            #
            lumi = '{:5.2f}'.format(info[year]['lumi']/1000.)
            canvas = Plotter.Canvas(lumi='{lumi}'.format(lumi=lumi)+' fb^{-1} (13 TeV)',extra='Preliminary',ratioFactor=1./3,logy=args.logy)
            # Do stack stuff
            if args.do_stack:
                sname = 'smc_'+var+'_'+cat+'_'+x
                s = R.THStack(sname,'')
                for mc in reversed(allMClist):
                    allMCHists[mc][var][cat][x].SetLineWidth(0)
                    allMCHists[mc][var][cat][x].SetMarkerStyle(0)
                    allMCHists[mc][var][cat][x].SetFillColor(get_color(mc))
                    if args.bin_width: divide_bin_width(allMCHists[mc][var][cat][x])
                    elif args.cumulative: allMCHists[mc][var][cat][x] = cumulative_histogram(allMCHists[mc][var][cat][x])
                    s.Add(allMCHists[mc][var][cat][x])
                pmc    = Plotter.Plot(s,legName='',legType='',option='hist')
                pdy    = Plotter.Plot(allMCHists[dyLists[args.dy_sample][0]][var][cat][x],legName=mc_stuff(args.dy_sample)[0],legType='F')
                ptt    = Plotter.Plot(allMCHists[otherMCs[year]['ttbar'][0]][var][cat][x],legName=mc_stuff('ttbar')[0],legType='F')
                pst    = Plotter.Plot(allMCHists[otherMCs[year]['singletop'][0]][var][cat][x],legName=mc_stuff('singletop')[0],legType='F')
                pdib   = Plotter.Plot(allMCHists[otherMCs[year]['diboson'][0]][var][cat][x],legName=mc_stuff('diboson')[0],legType='F')
                pwjets = Plotter.Plot(allMCHists[otherMCs[year]['Wjets'][0]][var][cat][x],legName=mc_stuff('Wjets')[0],legType='F')
                ptau   = Plotter.Plot(allMCHists[otherMCs[year]['tautau'][0]][var][cat][x],legName=mc_stuff('tautau')[0],legType='F')
            else:
                pmc = Plotter.Plot(hmc,  legName=mc_stuff(year),legType='hist',option='hist')
            pdata = Plotter.Plot(gdata,legName='Data',           legType='pe',  option='pe')
            canvas.addMainPlot(pmc,addToPlotList=False)
            canvas.addMainPlot(pdata)
            canvas.makeLegend(pos='tr')
            if args.do_stack:
                canvas.legend.addLegendEntry(pdy)
                canvas.legend.addLegendEntry(ptt)
                canvas.legend.addLegendEntry(pdib)
                canvas.legend.addLegendEntry(pst)
                canvas.legend.addLegendEntry(pwjets)
                canvas.legend.addLegendEntry(ptau)
                canvas.legend.resizeHeight(1.1)
                canvas.legend.moveLegend(X=-0.1)
            xtit = pretty(var)
            canvas.firstPlot.setTitles(X=xtit,Y='Events'+(' / GeV' if args.bin_width else ''))
            canvas.addRatioPlot(dataHists[var][cat][x],hmc,ytit='Data / MC',xtit=xtit,plusminus=1.)
            hmax = max([hmc.GetMaximum(),dataHists[var][cat][x].GetMaximum()])
            hmin = min([hmc.GetMinimum(),dataHists[var][cat][x].GetMinimum()])
            if hmin==0. and args.logy: hmin=0.1
            hmin = hmin/10 if args.logy else 0.
            hmax = hmax*10 if args.logy else hmax*1.2
            pmc.GetXaxis().SetTitleSize(0)
            pmc.GetXaxis().SetLabelSize(0)
            if args.do_stack:
                canvas.firstPlot.SetMinimum(hmin)
                canvas.firstPlot.SetMaximum(hmax)
            else:
                canvas.firstPlot.GetYaxis().SetRangeUser(hmin,hmax)
            if x=='log': 
                canvas.mainPad.SetLogx()
                canvas.ratPad.SetLogx()
                canvas.ratList[0].GetXaxis().SetMoreLogLabels(True)
                canvas.ratList[0].GetXaxis().SetNoExponent(True)
            canvas.Update()
            canvas.cleanup(fullOutName+'.png',extrascale=1.5)
