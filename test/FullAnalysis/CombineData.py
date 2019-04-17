# This script is for drawing data from different data taking years as a sum.
# Example usage: python CombineData.py -data 201X -data 201X -sel 2016 -r 
# Other example options
import ROOT as R
import os
import numpy as np
import argparse
import Plotter as Plotter
from DataSamplesTEST import *
from PlotsToMake import MAKEPLOTLIST
from Selection import *
import tools
R.gROOT.SetBatch(True)

parser = argparse.ArgumentParser(description='Options for making Z-prime --> dimuon plots')
parser.add_argument('-data',action='append',type=str,help='Which year of data to plot')
parser.add_argument('-dir','--directory',default='plots',help='Directory to save plots')
parser.add_argument('-r','--recreate',action='store_true',help='Whether or not to recreate data lists')
parser.add_argument('-tp','--treeplot',action='append',help='Which plot to draw from SimpleNtupler')
parser.add_argument('-cum','--cumulative',action='store_true',help='Whether or not to make additionally make cumulative histograms')
parser.add_argument('-bw','--binwidth',action='store_true',help='Whether or not to divide bin content by the bin width')
parser.add_argument('-cats','--categories',action='append',help='Which analysis categories to draw')
parser.add_argument('-dil','--dilepton',default='MuonsPlusMuonsMinus',help='Which set of dimuons to draw')
parser.add_argument('-e','--extra',default='',type=str,help='Extra name to add to output')
args = parser.parse_args()

datalist = [int(year) for year in args.data]
print datalist
print 'recreate',args.recreate

if not args.categories:
    categorylist = ['','bb','be','ee']
else:
    categorylist = [cat for cat in args.categories]
print categorylist

TOPLOTLISTTREE = []
if args.treeplot is None:
    TOPLOTLISTTREE = ['vertex_m','vertex_m_log']
else:
    TOPLOTLISTTREE = [str(plot) for plot in args.treeplot]
print TOPLOTLISTTREE

SAVEDIR = args.directory
selection = {
        2016:2016,
        2017:2016,
        2018:2018,
        }

data = {
    2016 : DataSample('Data 2016 ReReco',2016,reco='07Aug2017',color=R.kBlue),
    2017 : DataSample('Data 2017 ReReco',2017,reco='17Nov2017',color=R.kRed),
    2018 : DataSample('Data 2018 PromptReco',2018,reco='PromptReco'),
}

for year in datalist:
    print data[year]
    if args.recreate: data[year].setup(args.recreate,Selection[selection[year]])

for plot in TOPLOTLISTTREE:
    for category in categorylist:
        lumi='36.3 + 42.1 + 60.4 fb^{-1} (13 TeV)'
        canvas = Plotter.Canvas(lumi=lumi,extra='Preliminary')
        plots = {}
        for y,year in enumerate(datalist):
            hist = data[year].make_hist_from_list(MAKEPLOTLIST[plot],plot,year,category)
            hist.Rebin(MAKEPLOTLIST[plot]['rebin'])
            if args.binwidth: hist = tools.divide_bin_width(hist)
            if args.cumulative: hist = tools.cumulative_histogram(hist)
            plots[year] = Plotter.Plot(\
                hist,\
                legName=data[year].nicename,legType='pe',option='pe')
        name = plot+('_'+category if category else '')+'_sum'
        for year in datalist: name += '_'+str(year)
        sumHist = plots[datalist[0]].Clone(name)
        for year in datalist[1:]: sumHist.Add(plots[year].plot)
        sumPlot = Plotter.Plot(sumHist,legName='Data 2016 + 2017 + 2018',legType='pe',option='pe')
        canvas.addMainPlot(sumPlot)
        canvas.makeLegend(pos='tr')
        sumPlot.SetLineWidth(1)
        canvas.legend.moveLegend(X=-0.2,Y=-0.05)
        canvas.legend.resizeHeight()
        #canvas.setMaximum()
        xtitle = MAKEPLOTLIST[plot]['titles'].split(';')[1]
        ytitle = MAKEPLOTLIST[plot]['titles'].split(';')[2]
        canvas.firstPlot.setTitles(X=xtitle,Y=ytitle+(' / GeV' if args.binwidth else ''))
        xmin = MAKEPLOTLIST[plot]['lims']['min']
        xmax = MAKEPLOTLIST[plot]['lims']['max']
        sumPlot.GetXaxis().SetRangeUser(xmin,xmax)
        sumPlot.GetYaxis().SetRangeUser(1e-3,1e6)
        canvas.mainPad.SetLogy(MAKEPLOTLIST[plot]['log']['y'])
        canvas.mainPad.SetLogx(MAKEPLOTLIST[plot]['log']['x'])
        if MAKEPLOTLIST[plot]['log']['x']:
            canvas.firstPlot.GetXaxis().SetMoreLogLabels()
            canvas.firstPlot.GetXaxis().SetNoExponent()
        savename = SAVEDIR+'/'+name+('_'+args.extra if args.extra else '')
        canvas.cleanup(savename+'.pdf')
