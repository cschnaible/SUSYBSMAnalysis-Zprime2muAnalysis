# This script is for plotting one-off distributions for data 
# (and eventually MC as well)
# example usage : 
#

import ROOT as R
import os
import numpy as np
import argparse
import Plotter as Plotter
from DataSamplesTEST import *
from PlotsToMake import MAKEPLOTLIST
from Selection import *#Selection, Categories, Nminus1
import tools
R.gROOT.SetBatch(True)

parser = argparse.ArgumentParser(description='Options for making Z-prime --> dimuon plots')
parser.add_argument('-p','--plots',action='append',type=str,help='Which plots to make')
parser.add_argument('-d','--data',action='append',type=str,help='Which year of data to plot')
parser.add_argument('-cats','--categories',action='append',help='Which analysis categories to draw')
parser.add_argument('-r','--recreate',action='store_true',help='Remake base histos')
parser.add_argument('-n','--name',type=str,default='test',help='Extra name for output')
parser.add_argument('-bw','--binwidth',action='store_true',help='Divide by binwidth')
args = parser.parse_args()

datalist = [int(year) for year in args.data]
print datalist

if not args.categories:
    categorylist = ['','bb','be','ee']
else:
    categorylist = [cat for cat in args.categories]
print categorylist

data = {
    2016 : DataSample('Data 2016 ReReco',2016,reco='07Aug2017',color=R.kBlue),
    2017 : DataSample('Data 2017 ReReco',2017,reco='17Nov2017',color=R.kRed),
    2018 : DataSample('Data 2018 PromptReco',2018,reco='PromptReco'),
}

if not args.plots:
    toplot = ['vertex_m','vertex_m_log']
else:
    for plot in args.plots:
        toplot.append(plot)

selectionList = {
    'same_sign':
            ['base','cos_angle','same_sign','vertex_chi2','vertex_m',
            'trigger','pt','eta','isTracker','isGlobal',
            'rel_iso','dB',
            'v_pix_hits','num_trk_lays','v_mu_hits_12','matched_station_16'],
    'plus_sign':
            ['base','cos_angle','plus_sign','vertex_chi2','vertex_m',
            'trigger','pt','eta','isTracker','isGlobal',
            'rel_iso','dB',
            'v_pix_hits','num_trk_lays','v_mu_hits_12','matched_station_16'],
    'minus_sign':
            ['base','cos_angle','minus_sign','vertex_chi2','vertex_m',
            'trigger','pt','eta','isTracker','isGlobal',
            'rel_iso','dB',
            'v_pix_hits','num_trk_lays','v_mu_hits_12','matched_station_16'],
            }
xtitles = {
        'same_sign':'m(#mu^{#pm}#mu^{#pm}) [GeV]',
        'plus_sign':'m(#mu^{+}#mu^{+}) [GeV]',
        'minus_sign':'m(#mu^{-}#mu^{-}) [GeV]',
        }

# Make hists once (this takes a while?) and store them
hists = {}
if args.recreate:
    outBaseFile = R.TFile('hists/plots_base_'+args.name+'.root','recreate')
    outBaseFile.cd()
    for cat in categorylist:
        hists[cat] = {}
        for plot in toplot:
            hists[cat][plot] = {}
            for ptype in selectionList.keys():
                hists[cat][plot][ptype] = {}
                for y,year in enumerate(datalist):
                    selection = GetSelection(year,selectionList[ptype])
                    selection += (' && '+Categories[cat] if cat!='' else '')
                    hists[cat][plot][ptype][year] = \
                        data[year].make_hist_test(MAKEPLOTLIST[plot],plot,selection,year,cat,ptype)
                    hists[cat][plot][ptype][year].Write()
else: # Otherwise get the already made histograms
    outBaseFile = R.TFile('hists/plots_base_'+args.name+'.root')
    hists = {cat:{plot:{ptype:{year:{} for year in datalist} for ptype in selectionList.keys()} for plot in toplot} for cat in categorylist}
    for cat in categorylist:
        for plot in toplot:
            for ptype in selectionList.keys():
                for y,year in enumerate(datalist):
                    histname = plot+('_'+cat if cat else '')+'_'+str(year)+'_'+ptype
                    hists[cat][plot][ptype][year] = outBaseFile.Get(histname).Clone()


plots = {cat:{plot:{ptype:{year:{} for year in datalist} for ptype in selectionList.keys()} for plot in toplot} for cat in categorylist}
for cat in categorylist:
    for plot in toplot:
        for ptype in selectionList.keys():
            canvas = Plotter.Canvas(lumi='',ratioFactor=1./3,extra='Preliminary')
            #canvas = Plotter.Canvas(lumi='',extra='Preliminary')
            for y,year in enumerate(datalist):
                hist = hists[cat][plot][ptype][year].Clone()

                hist.Rebin(MAKEPLOTLIST[plot]['rebin'])
                if MAKEPLOTLIST[plot]['overflow']: hist = tools.draw_overflow(hist,\
                        MAKEPLOTLIST[plot]['underflow'])
                #if args.binwidth: hist = tools.divide_bin_width(hists[cat][plot][year])
                #elif args.cumulative: hist = tools.cumulative_histogram(hist)

                plots[cat][plot][ptype][year] = Plotter.Plot(hist,\
                        legName=data[year].nicename,legType='pe',option='pe')
                canvas.addMainPlot(plots[cat][plot][ptype][year])
            canvas.makeLegend(pos='tr')
            canvas.legend.moveLegend(X=-0.2,Y=-0.05)
            canvas.setMaximum()
            #xtitle = 'm(#mu^{#pm}#mu^{#pm}) [GeV]'#MAKEPLOTLIST[plot]['titles'].split(';')[1]
            ytitle = MAKEPLOTLIST[plot]['titles'].split(';')[2]
            canvas.firstPlot.setTitles(X=xtitles[ptype],Y=ytitle)
            for year in datalist:
                plots[cat][plot][ptype][year].Scale(data[2018].lumi()/data[year].lumi())
                plots[cat][plot][ptype][year].SetLineColor(data[year].color)
                plots[cat][plot][ptype][year].SetMarkerColor(data[year].color)
                plots[cat][plot][ptype][year].SetMarkerStyle(10)
                plots[cat][plot][ptype][year].SetLineWidth(1)
                if MAKEPLOTLIST[plot]['lims']['reset']:
                    xmin = MAKEPLOTLIST[plot]['lims']['min']
                    xmax = MAKEPLOTLIST[plot]['lims']['max']
                    plots[cat][plot][ptype][year].GetXaxis().SetRangeUser(xmin,xmax)
            for year in datalist:
                if year==2018: continue
                canvas.addRatioPlot(\
                    plots[cat][plot][ptype][2018],plots[cat][plot][ptype][year],color=data[year].color,\
                    legName='2018/'+str(year),ytit='Ratio',xtit=xtitles[ptype])
            canvas.makeRatioLegend()
            canvas.mainPad.SetLogy(MAKEPLOTLIST[plot]['log']['y'])
            canvas.mainPad.SetLogx(MAKEPLOTLIST[plot]['log']['x'])
            canvas.ratPad.SetLogx(MAKEPLOTLIST[plot]['log']['x'])
            canvas.firstRatioPlot.GetXaxis().SetMoreLogLabels()
            canvas.firstRatioPlot.GetXaxis().SetNoExponent()
            savename = 'plots/'+plot+('_'+cat if cat else '')+'_'+ptype
            for year in datalist: savename+='_'+str(year)
            canvas.cleanup(savename+'.pdf')

for cat in categorylist:
    for plot in toplot:
        for ptype in selectionList.keys():
            lumi = ''
            for y,year in enumerate(datalist):
                if y>0: lumi += ' + '
                lumi+='{:4.1f}'.format(data[year].lumi())
            canvas = Plotter.Canvas(lumi=lumi+' fb^{-1} (13 TeV)',extra='Preliminary')
            sumhist = hists[cat][plot][ptype][datalist[0]].Clone()
            sumhist.Rebin(MAKEPLOTLIST[plot]['rebin'])
            for y,year in enumerate(datalist):
                if y==0: continue
                h = hists[cat][plot][ptype][year].Clone()
                h.Rebin(MAKEPLOTLIST[plot]['rebin'])
                sumhist.Add(h)
            sumplot = Plotter.Plot(sumhist,legName = '2016 + 2017 + 2018 Data',legType='pe',option='pe')
            canvas.addMainPlot(sumplot)
            canvas.makeLegend(pos='tr')
            canvas.legend.moveLegend(X=-0.2)
            if MAKEPLOTLIST[plot]['lims']['reset']:
                xmin = MAKEPLOTLIST[plot]['lims']['min']
                xmax = MAKEPLOTLIST[plot]['lims']['max']
                canvas.firstPlot.GetXaxis().SetRangeUser(xmin,xmax)
            ytitle = MAKEPLOTLIST[plot]['titles'].split(';')[2]
            canvas.firstPlot.setTitles(X=xtitles[ptype],Y=ytitle)
            canvas.firstPlot.SetMarkerStyle(10)
            canvas.mainPad.SetLogy(MAKEPLOTLIST[plot]['log']['y'])
            canvas.mainPad.SetLogx(MAKEPLOTLIST[plot]['log']['x'])
            canvas.firstPlot.GetXaxis().SetMoreLogLabels()
            canvas.firstPlot.GetXaxis().SetNoExponent()
            savename = 'plots/'+plot+('_'+cat if cat else '')+'_'+ptype+'_sum'
            for year in datalist: savename+='_'+str(year)
            canvas.cleanup(savename+'.pdf')

