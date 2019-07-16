''' 
Compare various acceptance and efficiency curves across each MC year
7 May 2018 Christian Schnaible (UCLA)
'''

import ROOT as R
import sys, os
import array
import argparse
import logging
import numpy as np
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
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
#years = [2017,2018]
plots_to_compare = ['AccNoPt','Acceptance','TrigWrtAcc','RecoWrtAcc','RecoWrtAccTrig','TotalReco']
plot_categories = ['all','bb','be']
categories = {'all':'','bb':'_bb','be':'_e'}
numden = ['Num','Den']

info = {
        2016:{
            'file':'mc_2016/ana_effres_dy50toInf.root',
            'our':'Our2016OppSignEfficiency',
            'ourZ':'Our2016AtZOppSignEfficiency',
            'legName':'80X',
            'color':R.kBlack,
            },
        2017:{
            'file':'mc_2017/ana_effres_dy50toInf.root',
            'our':'Our2018OppSignEfficiency',
            'ourZ':'Our2018AtZOppSignEfficiency',
            'legName':'94X',
            'color':R.kOrange+1,
            },
        2018:{
            'file':'mc/ana_effres_dy50toInf.root',
            'our':'Our2018OppSignEfficiency',
            'ourZ':'Our2018AtZOppSignEfficiency',
            'legName':'102X',
            'color':R.kBlue+1,
            },
        }

titles = {
        'AccNoPt':'Acceptance (no p_{T})',
        'Acceptance':'Acceptance',
        'TrigWrtAcc':'Trig Eff w.r.t. Acc',
        'RecoWrtAcc':'Reco Eff w.r.t. Acc',
        'RecoWrtAccTrig':'Reco Eff w.r.t. Acc & Trig',
        'TotalReco':'Reco & Trig & Acc',
        'bb':'Barrel-Barel',
        'be':'Barrel-Endcap + Endcap-Endcap',
        'all':'Combined',
        }

hists = {year:{plot:{cat:{r:{} for r in numden} for cat in plot_categories} for plot in plots_to_compare} for year in years}
for year in years:
    rfile = R.TFile(info[year]['file'])
    for plot in plots_to_compare:
        for cat in plot_categories:
            for r in numden:
                hname = r+plot+categories[cat]
                h = rfile.Get(info[year][args.which]+'/'+hname).Clone()
                if args.var_rebin:
                    #hists[year][plot][cat][r] = h.Rebin(len(bins)+1,h.GetName()+'_rebin',bins)
                    hists[year][plot][cat][r] = h.Rebin(len(bins)-1,h.GetName()+'_rebin',bins)
                else:
                    hists[year][plot][cat][r] = h.Rebin(args.rebin)
                hists[year][plot][cat][r].SetDirectory(0)
            hists[year][plot][cat]['Rat'] = hists[year][plot][cat]['Num'].Clone('Rat'+plot+categories[cat])
            hists[year][plot][cat]['Rat'].Divide(hists[year][plot][cat]['Den'])
            hists[year][plot][cat]['Rat'].SetDirectory(0)
    rfile.Close()
logy = True if args.atZ and args.which=='our' else False
plusminus = 1 if args.atZ and args.which=='our' else 0.15
print hists
for plot in plots_to_compare:
    for cat in plot_categories:
        canv = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation',ratioFactor=1./3,logy=logy)
        plots = {year:{} for year in years}
        for year in years:
            plots[year] = Plotter.Plot(hists[year][plot][cat]['Rat'],legName=info[year]['legName'],option='pe',legType='pe')
            canv.addMainPlot(plots[year])
        for year in years:
            plots[year].SetLineColor(info[year]['color'])
            plots[year].SetMarkerColor(info[year]['color'])
            plots[year].SetMarkerSize(0)
            plots[year].SetLineWidth(2)
        if logy:
            canv.firstPlot.GetYaxis().SetRangeUser(1e-4,1.1)
        else:
            canv.firstPlot.GetYaxis().SetRangeUser(0,1.1)
        canv.firstPlot.setTitles(Y=titles[plot])
        canv.drawText(titles[cat],pos=(0.25,0.85),align='tl',fontscale=1.5)
        canv.makeLegend(pos='br')
        canv.addRatioPlot(plots[2016],plots[2018],color=info[2017]['color'],legType='pe',option='pe',ytit='3.0 / 3.1',xtit='mass [GeV]',plusminus=plusminus)
        canv.addRatioPlot(plots[2016],plots[2017],color=info[2018]['color'],legType='pe',option='pe',ytit='3.0 / 3.1',xtit='mass [GeV]',plusminus=plusminus)
        #canv.addRatioPlot(plots[2017],plots[2018],color=R.kBlack,legType='pe',option='pe',ytit='94X/102X',xtit='mass [GeV]',plusminus=plusminus)
        canv.cleanup('www_pdf/'+plot+'_'+cat+'_'+args.which+('_atZ_' if args.atZ else '_')+args.output_name+'.png')
