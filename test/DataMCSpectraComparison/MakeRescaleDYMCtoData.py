'''
Make ROOT file storing Data / MC ratios
'''
import ROOT as R
R.gROOT.SetBatch(True)
import numpy as np
import array, math
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples# samples18, samples17, samples16
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools_chris import poisson_intervalize, divide_bin_width, clopper_pearson_poisson_means, cumulative_histogram
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d','--tdir',default='ourpre')
parser.add_argument('-n','--name',default='',help='Name the output')
args = parser.parse_args()

varDraw = {
        'lead_pt':{
            'bins':{
                'log':{'lims':[30.0,150.0],'nbins':30},
                'lin':{'lims':[30.0,150.0],'nbins':24}, # 5 GeV width
                },
            'cats':['b','e','all'],
            },
        'sub_pt':{
            'bins':{
                'log':{'lims':[30.0,150.0],'nbins':30},
                'lin':{'lims':[30.0,150.0],'nbins':24}, # 5 GeV width
                },
            'cats':['b','e','all'],
            },
        'gen_lead_pt':{
            'bins':{
                'log':{'lims':[30.0,150.0],'nbins':30},
                'lin':{'lims':[30.0,150.0],'nbins':24}, # 5 GeV width
                },
            'cats':['b','e','all'],
            },
        'gen_sub_pt':{
            'bins':{
                'log':{'lims':[30.0,150.0],'nbins':30},
                'lin':{'lims':[30.0,150.0],'nbins':24}, # 5 GeV width
                },
            'cats':['b','e','all'],
            },
        'mass':{
            'bins':{
                'lin':{'lims':[60.0,120.0],'nbins':30},
                },
            'cats':['bb','beee','all'],
            },
        'gen_mass':{
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
        'gen_dil_pt':{
            'bins':{
                'log':{'lims':[0.1,300.0],'nbins':30},
                'lin':{'lims':[0,300.0],'nbins':30},
                },
            'cats':['bb','beee','all'],
            },
        'dil_rap':{
            'bins':{
                'lin':{'lims':[-3.0,3.0],'nbins':15.0},
                },
            'cats':['bb','beee','all'],
            },
        'gen_dil_rap':{
            'bins':{
                'lin':{'lims':[-3.0,3.0],'nbins':15.0},
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
dataDrawList = ['lead_pt','sub_pt','mass','dil_pt','dil_rap']
mcDrawList = ['gen_lead_pt','gen_sub_pt','gen_mass','gen_dil_pt','gen_dil_rap']
allDrawList = dataDrawList + mcDrawList

dyLists = {
    'powheg' : ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf'],
    }

allMClist = dyLists['powheg']

print '\n','*'*15,'\n'
print args
print allMClist
print '\n','*'*15,'\n'

rescale_hist_name = '_'+args.name if args.name else ''
outFile = R.TFile('rescale/rescale_histograms'+rescale_hist_name+'.root','recreate')
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

dataHists = {year:{var:{cat:{x:{} for x in varDraw[var]['bins'].keys()} for cat in varDraw[var]['cats']} for var in dataDrawList} for year in allyears}
for year in allyears:
    for var in dataDrawList:
        for cat in varDraw[var]['cats']:
            for x in varDraw[var]['bins'].keys():
                hname = 'hdata_'+str(year)+'_'+var+'_'+cat+'_'+x
                bins = get_binning[x](varDraw[var]['bins'][x]['lims'],int(varDraw[var]['bins'][x]['nbins']))
                dataHists[year][var][cat][x] = R.TH1D(hname,'',int(varDraw[var]['bins'][x]['nbins']),bins)
                dataHists[year][var][cat][x].SetDirectory(0)

# Make Data histograms
for year in allyears:
    print 'Data',year
    f = R.TFile(info[year]['path']+info[year]['file'])
    t = f.Get(info[year][args.tdir]['dir']+'/t')
    t.SetBranchStatus('*',0)
    t.SetBranchStatus('lep_pt',1)
    t.SetBranchStatus('lep_eta',1)
    t.SetBranchStatus('vertex_m',1)
    t.SetBranchStatus('dil_pt',1)
    t.SetBranchStatus('dil_rap',1)
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
            dataHists[year]['lead_pt']['all'][x].Fill(lead_pt)
            dataHists[year]['lead_pt'][lead_cat][x].Fill(lead_pt)

        for x in varDraw['sub_pt']['bins'].keys():
            dataHists[year]['sub_pt']['all'][x].Fill(sub_pt)
            dataHists[year]['sub_pt'][sub_cat][x].Fill(sub_pt)

        for x in varDraw['mass']['bins'].keys():
            dataHists[year]['mass']['all'][x].Fill(t.vertex_m)
            dataHists[year]['mass'][Z_cat][x].Fill(t.vertex_m)

        for x in varDraw['dil_pt']['bins'].keys():
            dataHists[year]['dil_pt']['all'][x].Fill(t.dil_pt)
            dataHists[year]['dil_pt'][Z_cat][x].Fill(t.dil_pt)

        for x in varDraw['dil_rap']['bins'].keys():
            dataHists[year]['dil_rap']['all'][x].Fill(t.dil_rap)
            dataHists[year]['dil_rap'][Z_cat][x].Fill(t.dil_rap)
    f.Close()

# Write Data
outFile.cd()
for var in dataDrawList:
    for cat in varDraw[var]['cats']:
        for x in varDraw[var]['bins'].keys():
            for year in allyears:
                dataHists[year][var][cat][x].Write()

# Make MC histgrams
rels = ['80X','94X','102X']
dyHists = {rel:{name:{var:{cat:{x:{} for x in varDraw[var]['bins'].keys()} for cat in varDraw[var]['cats']} for var in allDrawList} for name in allMClist} for rel in rels}
for rel in rels:
    for name in allMClist:
        for var in allDrawList:
            for cat in varDraw[var]['cats']:
                for x in varDraw[var]['bins'].keys():
                    hname = 'hmc_'+name+'_'+rel+'_'+var+'_'+cat+'_'+x
                    bins = get_binning[x](varDraw[var]['bins'][x]['lims'],int(varDraw[var]['bins'][x]['nbins']))
                    dyHists[rel][name][var][cat][x] = R.TH1D(hname+'_tmp','',int(varDraw[var]['bins'][x]['nbins']),bins)
                    dyHists[rel][name][var][cat][x].SetDirectory(0)

for rel,year in zip(rels,allyears):
    for mc in reversed(allMClist):
        print mc,rel
        mcFile = R.TFile(info[year]['mcpath']+'ana_datamc_'+mc+'.root')
        info[year]['mc'][mc].sum_weights = get_sum_weights(mcFile)
        t = mcFile.Get(info[year][args.tdir]['dir']+'/t')
        t.SetBranchStatus('*',0)
        t.SetBranchStatus('lep_pt',1)
        t.SetBranchStatus('gen_lep_pt',1)
        t.SetBranchStatus('lep_eta',1)
        t.SetBranchStatus('gen_lep_eta',1)
        t.SetBranchStatus('vertex_m',1)
        t.SetBranchStatus('gen_res_mass',1)
        t.SetBranchStatus('dil_pt',1)
        t.SetBranchStatus('dil_rap',1)
        t.SetBranchStatus('gen_dil_pt',1)
        t.SetBranchStatus('gen_dil_rap',1)
        t.SetBranchStatus('genWeight',1)
        for e,entry in enumerate(t):
            t.GetEntry(e)
            #if not eval(sel_tree): continue
            if not (60 < t.vertex_m < 120): continue
            (lead_idx,sub_idx) = (0,1) if t.lep_pt[0]>t.lep_pt[1] else (1,0)
            (gen_lead_idx,gen_sub_idx) = (0,1) if t.gen_lep_pt[0]>t.gen_lep_pt[1] else (1,0)

            lead_pt,lead_eta = t.lep_pt[lead_idx],t.lep_eta[lead_idx]
            lead_cat = 'b' if abs(lead_eta)<=1.2 else 'e'
            gen_lead_pt,gen_lead_eta = t.gen_lep_pt[gen_lead_idx],t.gen_lep_eta[gen_lead_idx]
            gen_lead_cat = 'b' if abs(gen_lead_eta)<=1.2 else 'e'

            sub_pt,sub_eta = t.lep_pt[sub_idx],t.lep_eta[sub_idx]
            sub_cat = 'b' if abs(sub_eta)<=1.2 else 'e'
            gen_sub_pt,gen_sub_eta = t.gen_lep_pt[gen_sub_idx],t.gen_lep_eta[gen_sub_idx]
            gen_sub_cat = 'b' if abs(gen_sub_eta)<=1.2 else 'e'

            #lead_pt = t.lep_pt[0] if t.lep_pt[0]>t.lep_pt[1] else t.lep_pt[1]
            #lead_eta = t.lep_eta[0] if t.lep_pt[0]>t.lep_pt[1] else t.lep_eta[1]
            #lead_cat = 'b' if abs(lead_eta)<=1.2 else 'e'
            #sub_pt = t.lep_pt[0] if t.lep_pt[0]<t.lep_pt[1] else t.lep_pt[1]
            #sub_eta = t.lep_eta[0] if t.lep_pt[0]<t.lep_pt[1] else t.lep_eta[1]
            #sub_cat = 'b' if abs(sub_eta)<=1.2 else 'e'
            cat = 'bb' if (abs(lead_eta)<=1.2 and abs(sub_eta)<=1.2) else 'beee'
            gen_cat = 'bb' if (abs(gen_lead_eta)<=1.2 and abs(gen_sub_eta)<=1.2) else 'beee'
            for x in varDraw['lead_pt']['bins'].keys():
                dyHists[rel][mc]['lead_pt']['all'][x].Fill(lead_pt,t.genWeight)
                dyHists[rel][mc]['lead_pt'][lead_cat][x].Fill(lead_pt,t.genWeight)
                dyHists[rel][mc]['gen_lead_pt']['all'][x].Fill(gen_lead_pt,t.genWeight)
                dyHists[rel][mc]['gen_lead_pt'][gen_lead_cat][x].Fill(gen_lead_pt,t.genWeight)
            for x in varDraw['sub_pt']['bins'].keys():
                dyHists[rel][mc]['sub_pt']['all'][x].Fill(sub_pt,t.genWeight)
                dyHists[rel][mc]['sub_pt'][sub_cat][x].Fill(sub_pt,t.genWeight)
                dyHists[rel][mc]['gen_sub_pt']['all'][x].Fill(gen_sub_pt,t.genWeight)
                dyHists[rel][mc]['gen_sub_pt'][gen_sub_cat][x].Fill(gen_sub_pt,t.genWeight)
            for x in varDraw['mass']['bins'].keys():
                dyHists[rel][mc]['mass']['all'][x].Fill(t.vertex_m,t.genWeight)
                dyHists[rel][mc]['mass'][cat][x].Fill(t.vertex_m,t.genWeight)
                dyHists[rel][mc]['gen_mass']['all'][x].Fill(t.gen_res_mass,t.genWeight)
                dyHists[rel][mc]['gen_mass'][gen_cat][x].Fill(t.gen_res_mass,t.genWeight)
            for x in varDraw['dil_pt']['bins'].keys():
                dyHists[rel][mc]['dil_pt']['all'][x].Fill(t.dil_pt,t.genWeight)
                dyHists[rel][mc]['dil_pt'][cat][x].Fill(t.dil_pt,t.genWeight)
                dyHists[rel][mc]['gen_dil_pt']['all'][x].Fill(t.gen_dil_pt,t.genWeight)
                dyHists[rel][mc]['gen_dil_pt'][gen_cat][x].Fill(t.gen_dil_pt,t.genWeight)
            for x in varDraw['dil_rap']['bins'].keys():
                dyHists[rel][mc]['dil_rap']['all'][x].Fill(t.dil_rap,t.genWeight)
                dyHists[rel][mc]['dil_rap'][cat][x].Fill(t.dil_rap,t.genWeight)
                dyHists[rel][mc]['gen_dil_rap']['all'][x].Fill(t.gen_dil_rap,t.genWeight)
                dyHists[rel][mc]['gen_dil_rap'][gen_cat][x].Fill(t.gen_dil_rap,t.genWeight)
        mcFile.Close()

# Combine MC histograms
mcHists = {rel:{var:{cat:{x:{} for x in varDraw[var]['bins'].keys()} for cat in varDraw[var]['cats']} for var in allDrawList} for rel in rels}
for rel,year in zip(rels,allyears):
    for var in allDrawList:
        for cat in varDraw[var]['cats']:
            for x in varDraw[var]['bins'].keys():
                hname = 'hmc_'+rel+'_'+var+'_'+cat+'_'+x
                bins = get_binning[x](varDraw[var]['bins'][x]['lims'],int(varDraw[var]['bins'][x]['nbins']))
                mcHists[rel][var][cat][x] = R.TH1D(hname,'',int(varDraw[var]['bins'][x]['nbins']),bins)
                mcHists[rel][var][cat][x].SetDirectory(0)
                for m,mc in enumerate(reversed(allMClist)):
                    scale_by = info[year]['mc'][mc].cross_section / float(info[year]['mc'][mc].sum_weights)
                    dyHists[rel][mc][var][cat][x].Scale(scale_by)
                    mcHists[rel][var][cat][x].Add(dyHists[rel][mc][var][cat][x])
                mcHists[rel][var][cat][x].SetDirectory(0)
                outFile.cd()
                mcHists[rel][var][cat][x].Write()

# Make Data / MC ratios
dataRatios = {year:{rel:{var:{cat:{x:{} for x in varDraw[var]['bins'].keys()} for cat in varDraw[var]['cats']} for var in dataDrawList} for rel in rels} for year in allyears}

for year in allyears:
    for rel in rels:
        for var in dataDrawList:
            for cat in varDraw[var]['cats']:
                for x in varDraw[var]['bins'].keys():
                    # Need to scale each MC rel by the lumi of that year
                    hname = 'dataRat_'+str(year)+'_'+rel+'_'+var+'_'+cat+'_'+x
                    hrat = dataHists[year][var][cat][x].Clone(hname)
                    hrat.SetDirectory(0)
                    hmc = mcHists[rel][var][cat][x].Clone()
                    hmc.SetDirectory(0)
                    #scale_by = info[year][args.tdir]['lumi'] / info[year][args.tdir]['pre']
                    scale_by = info[year]['lumi'] / info[year][args.tdir]['pre']
                    hmc.Scale(scale_by)
                    hrat.Divide(hmc)
                    hrat.SetDirectory(0)
                    dataRatios[year][rel][var][cat][x] = hrat
                    dataRatios[year][rel][var][cat][x].SetDirectory(0)
                    outFile.cd()
                    dataRatios[year][rel][var][cat][x].Write()

# Make MC / MC ratios
mcRatios = {rel1:{rel2:{var:{cat:{x:{} for x in varDraw[var]['bins'].keys()} for cat in varDraw[var]['cats']} for var in allDrawList} for rel2 in rels} for rel1 in rels}

for rel1 in rels:
    for rel2 in rels:
        if rel1==rel2: continue
        for var in allDrawList:
            for cat in varDraw[var]['cats']:
                for x in varDraw[var]['bins'].keys():
                    hname = 'mcRat_'+rel1+'_'+rel2+'_'+var+'_'+cat+'_'+x
                    hrat = mcHists[rel1][var][cat][x].Clone(hname)
                    hrat.SetDirectory(0)
                    hden = mcHists[rel2][var][cat][x].Clone()
                    hden.SetDirectory(0)
                    hrat.Divide(hden)
                    hrat.SetDirectory(0)
                    mcRatios[rel1][rel2][var][cat][x] = hrat
                    mcRatios[rel1][rel2][var][cat][x].SetDirectory(0)
                    outFile.cd()
                    mcRatios[rel1][rel2][var][cat][x].Write()

# Save stuff
outFile.Close()

