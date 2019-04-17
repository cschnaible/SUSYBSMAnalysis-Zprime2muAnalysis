# This script is for plotting N-1 distributions for data 
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
parser.add_argument('-data',action='append',type=str,help='Which year of data to plot')
parser.add_argument('-cats','--categories',action='append',help='Which analysis categories to draw')
parser.add_argument('-r','--recreate',action='store_true',help='Remake base histos')
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

Nm1s = {
        # 'PlotsToMake' : 'Selection'
        'dimuon_cos_angle':'cos_angle',
        'dimuon_vertex_chi2':'vertex_chi2',
        'muon_trk_rel_iso':'rel_iso',
        'muon_rel_pt_err':'rel_err',
        'muon_rel_pt_err_log':'rel_err',
        'muon_dB':'dB',
        'muon_dB_log':'dB',
        'muon_num_v_pix_hits':'v_pix_hits',
        'muon_num_v_trk_lays':'num_trk_lays',
        'muon_num_v_glb_mu_hits':'v_mu_hits_18',
        'muon_num_match_mu_st':'matched_station_16'
        }

# Make hists once (this takes a while?) and store them
hists = {}
if args.recreate:
    outBaseFile = R.TFile('hists/nm1_base.root','recreate')
    outBaseFile.cd()
    for cat in categorylist:
        hists[cat] = {}
        for plot in Nm1s:
            hists[cat][plot] = {}
            nm1 = Nm1s[plot]
            for y,year in enumerate(datalist):
                print cat, plot, year
                thisNm1Sel = (Categories[cat]+' && ' if cat else '')+Nminus1(year,nm1)
                hists[cat][plot][year] = \
                    data[year].make_hist_test(MAKEPLOTLIST[plot],plot,thisNm1Sel,year,cat)
                hists[cat][plot][year].Write()
else: # Otherwise get the already made histograms
    outBaseFile = R.TFile('hists/nm1_base.root')
    print outBaseFile
    hists = {cat:{plot:{year:{} for year in datalist} for plot in Nm1s} for cat in categorylist}
    for cat in categorylist:
        for plot in Nm1s:
            for y,year in enumerate(datalist):
                histname = plot+('_'+cat if cat else '')+'_'+str(year)
                print histname
                hists[cat][plot][year] = outBaseFile.Get(histname).Clone()


plots = {cat:{plot:{year:{} for year in datalist} for plot in Nm1s} for cat in categorylist}
for cat in categorylist:
    for plot in Nm1s:
        print cat, plot
        canvas = Plotter.Canvas(lumi='',ratioFactor=1./3,extra='Preliminary')
        for y,year in enumerate(datalist):
            hists[cat][plot][year].Rebin(MAKEPLOTLIST[plot]['rebin'])
            if MAKEPLOTLIST[plot]['overflow']: hist = tools.draw_overflow(hists[cat][plot][year],\
                    MAKEPLOTLIST[plot]['underflow'])
            else: hist = hists[cat][plot][year]
            plots[cat][plot][year] = Plotter.Plot(hist,\
                    legName=data[year].nicename,legType='pe',option='hpe')
            canvas.addMainPlot(plots[cat][plot][year])
        canvas.makeLegend(pos='tr')
        canvas.legend.moveLegend(X=-0.2,Y=-0.05)
        canvas.setMaximum()
        xtitle = MAKEPLOTLIST[plot]['titles'].split(';')[1]
        ytitle = MAKEPLOTLIST[plot]['titles'].split(';')[2]
        canvas.firstPlot.setTitles(X=xtitle,Y=ytitle)
        for year in datalist:
            plots[cat][plot][year].Scale(1./data[year].lumi())
            plots[cat][plot][year].SetLineColor(data[year].color)
            plots[cat][plot][year].SetMarkerColor(data[year].color)
            plots[cat][plot][year].SetMarkerStyle(10)
            plots[cat][plot][year].SetLineWidth(1)
            if MAKEPLOTLIST[plot]['lims']['reset']:
                xmin = MAKEPLOTLIST[plot]['lims']['min']
                xmax = MAKEPLOTLIST[plot]['lims']['max']
                plots[cat][plot][year].GetXaxis().SetRangeUser(xmin,xmax)
        for year in datalist:
            if year==2018: continue
            canvas.addRatioPlot(\
                plots[cat][plot][2018],plots[cat][plot][year],color=data[year].color,\
                legName='2018/'+str(year),ytit='Ratio',xtit=xtitle)
        canvas.makeRatioLegend()
        canvas.mainPad.SetLogy(MAKEPLOTLIST[plot]['log']['y'])
        canvas.mainPad.SetLogx(MAKEPLOTLIST[plot]['log']['x'])
        canvas.ratPad.SetLogx(MAKEPLOTLIST[plot]['log']['x'])
        savename = 'plots/nm1_'+plot+('_'+cat if cat else '')
        for year in datalist: savename+='_'+str(year)
        canvas.cleanup(savename+'.pdf')
