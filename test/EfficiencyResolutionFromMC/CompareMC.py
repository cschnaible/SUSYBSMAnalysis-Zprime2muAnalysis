''' 
Compare gen-leven mass distributions across each MC year
10 May 2018 Christian Schnaible (UCLA)
'''

import ROOT as R
import sys, os
import array
import argparse
import logging
import numpy as np
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples18,samples16,samples17
parser = argparse.ArgumentParser()

parser.add_argument('-w','--which',default='our',
        help='Histogram directory')
parser.add_argument('-c','--category',default='all',
        help='Eta category to plot. Defaults to [bb,beee,all]')
parser.add_argument('--rebin',type=int,default=80,
        help='Rebin factor')
parser.add_argument('-o','--output-name',dest='output_name',default='test',
        help='Extra name to apply to histogram output')
parser.add_argument('-vr','--var-rebin',dest='var_rebin',action='store_true',
        help='Use sample bin widths')
parser.add_argument('-atZ',action='store_true',
        help='Do window on Z: [60 GeV, 120 GeV]')

args = parser.parse_args()

if args.atZ:
    bins = array.array('d',[60+2*i for i in range(31)])
else:
    bins = array.array('d',[60,120,200,400,800,1400,2300,3500,4500,6000,8000])


#from SUSYBSMAnalysis.Zprime2muAnalysis.roottools import *
#setTDRStyle()
#set_zp2mu_style()
#R.gStyle.SetPadTopMargin(0.02)
#R.gStyle.SetPadRightMargin(0.04)
#R.TH1.AddDirectory(0)
R.gROOT.SetBatch(True)

years = [2016,2017,2018]
#plots_to_compare = ['AccNoPt','Acceptance','RecoWrtAcc','RecoWrtAccTrig','TotalReco']
plots_to_compare = ['Acceptance']
plot_categories = ['all','bb','be']
categories = {'all':'','bb':'_bb','be':'_e'}
numden = ['Num','Den']
dyInfo = {year:{
    'dy50to120':{'lims':(  50,   120)},
    'dy120to200':{'lims':( 120,   200)},
    'dy200to400':{'lims':( 200,   400)},
    'dy400to800':{'lims':( 400,   800)},
    'dy800to1400':{'lims':( 800,  1400)},
    'dy1400to2300':{'lims':(1400,  2300)},
    'dy2300to3500':{'lims':(2300,  3500)},
    'dy3500to4500':{'lims':(3500,  4500)},
    'dy4500to6000':{'lims':(4500,  6000)},
    'dy6000toInf':{'lims':(6000, 10000)},
    } for year in years}
dyList = ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf']

info = {
        2016:{
            'path':'mc_2016/',
            'our':'Our2016OppSignEfficiency',
            'ourZ':'Our2016AtZOppSignEfficiency',
            'legName':'80X',
            'color':R.kBlack,
            'samples':samples16,
            },
        2017:{
            'path':'mc_2017/',
            'our':'Our2018OppSignEfficiency',
            'ourZ':'Our2018AtZOppSignEfficiency',
            'legName':'94X',
            'color':R.kOrange+1,
            'samples':samples17,
            },
        2018:{
            'path':'mc/',
            'our':'Our2018OppSignEfficiency',
            'ourZ':'Our2018AtZOppSignEfficiency',
            'legName':'102X',
            'color':R.kBlue+1,
            'samples':samples18,
            },
        }
titles = {
        'AccNoPt':'Acceptance (no p_{T})',
        'Acceptance':'Acceptance',
        'RecoWrtAcc':'Reco Eff w.r.t. Acc',
        'RecoWrtAccTrig':'Reco Eff w.r.t. Acc & Trig',
        'TotalReco':'Reco & Trig & Acc',
        'bb':'Barrel-Barel',
        'be':'Barrel-Endcap + Endcap-Endcap',
        'all':'Combined',
        'Num':'Pass',
        'Den':'',
        }

def get_nevents(f):
    weights = getattr(f,'EventCounter').Get('weights')
    return weights.GetBinContent(2),weights.GetBinContent(1)

for year in years:
    for sample in info[year]['samples']:
        for dy in dyList:
            if dy!=sample.name: continue
            dyInfo[year][dy]['xs'] = sample.cross_section
            if year==2016:
                dyInfo[year][dy]['nevents'] = sample.nevents
            else:
                pos,neg = get_nevents(R.TFile(info[year]['path']+'ana_datamc_'+dy+'.root'))
                dyInfo[year][dy]['nevents'] = pos-neg

def get_scale(year,dy):
    return float(dyInfo[year][dy]['xs']) / float(dyInfo[year][dy]['nevents'])

if args.atZ:
    bins = array.array('d',[60+2*i for i in range(31)])
else:
    bins = array.array('d',[60,120,200,400,800,1400,2300,3500,4500,6000,8000])

indv_hists = {year:{plot:{cat:{r:{dy:{} for dy in dyList} for r in numden} for cat in plot_categories} for plot in plots_to_compare} for year in years}
for year in years:
    for dy in dyList:
        f = R.TFile(info[year]['path']+'ana_effres_'+dy+'.root')
        for plot in plots_to_compare:
            for cat in plot_categories:
                for r in numden:
                    pname = r+plot+categories[cat]
                    h = f.Get(info[year][args.which]+'/'+pname).Clone()
                    h.SetDirectory(0)
                    if args.var_rebin:
                        indv_hists[year][plot][cat][r][dy] = h.Rebin(len(bins)-1,pname+'_rebin',bins)
                    else:
                        indv_hists[year][plot][cat][r][dy] = h.Rebin(args.rebin)
                    indv_hists[year][plot][cat][r][dy].Scale(get_scale(year,dy))
                    indv_hists[year][plot][cat][r][dy].SetDirectory(0)
        f.Close()


tot_hists = {year:{plot:{cat:{r:{} for r in numden} for cat in plot_categories} for plot in plots_to_compare} for year in years}
for year in years:
    for plot in plots_to_compare:
        for cat in plot_categories:
            for r in numden:
                for d,dy in enumerate(dyList):
                    if d==0:
                        name = pname+('_rebin' if args.var_rebin else '')
                        tot_hists[year][plot][cat][r] = indv_hists[year][plot][cat][r][dyList[0]].Clone(name+'_tot')
                    else:
                        tot_hists[year][plot][cat][r].Add(indv_hists[year][plot][cat][r][dy])

binname = ''
if args.var_rebin:
    if args.atZ:
        binname = '_atZ'
    else:
        binname = '_widebins'


for plot in plots_to_compare:
    for cat in plot_categories:
        for r in numden:
            canv = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation',logy=True,ratioFactor=1./3)
            plots = {}
            for year in years:
                plots[year] = Plotter.Plot(tot_hists[year][plot][cat][r],legName=info[year]['legName'],legType='pe',option='pe')
                canv.addMainPlot(plots[year])
            for year in years:
                plots[year].SetLineColor(info[year]['color'])
                plots[year].SetMarkerColor(info[year]['color'])
                plots[year].SetMarkerSize(0)
                plots[year].SetLineWidth(2)
            hmax = max([plots[year].GetMaximum() for year in years])
            hmin = max([plots[year].GetMinimum() for year in years])
            canv.firstPlot.GetYaxis().SetRangeUser(hmin*0.1, hmax*5)
            canv.firstPlot.setTitles(Y=titles[plot])
            canv.drawText(titles[cat],pos=(0.25,0.85),align='tl',fontscale=1.5)
            canv.makeLegend()
            plusminus = 1.
            #print plots[2016].Integral() / plots[2017].Integral()
            #print plots[2016].Integral() / plots[2018].Integral()
            canv.addRatioPlot(plots[2016],plots[2017],color=info[2017]['color'],legType='pe',option='pe',ytit='3.0 / 3.1',xtit='mass [GeV]',plusminus=plusminus)
            canv.addRatioPlot(plots[2016],plots[2018],color=info[2018]['color'],legType='pe',option='pe',ytit='3.0 / 3.1',xtit='mass [GeV]',plusminus=plusminus)
            
            name = r+'_'+plot+'_'+cat+'_'+args.which+binname+'_'+args.output_name
            canv.cleanup('www_pdf/'+name+'.png',extrascale=1.5)
