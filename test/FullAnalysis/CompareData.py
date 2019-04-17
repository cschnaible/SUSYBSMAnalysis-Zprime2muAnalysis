# This script is for drawing data from different data taking years together.
# Optionality to draw existing histograms from HistosFromPAT as well as
# to recreate histograms from SimpleNtupler. 
# Example usage: python makeplot.py -data 201X -data 201X -sel 2016 -r 
# Other example options
# -p LeptonPt -p LeptonEta
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
parser.add_argument('-bp','--baseplot',action='append',help='Which plot to draw from HistosFromPAT')
parser.add_argument('-do_bp','--do_baseplot',action='store_true',help='Turn off drawing histos from HistosFromPAT')
parser.add_argument('-tp','--treeplot',action='append',help='Which plot to draw from SimpleNtupler')
parser.add_argument('-no_tp','--no_treeplot',action='store_true',help='Turn off drawing histos from SimpleNtupler')
parser.add_argument('-sel','--selection',default='2016',help='Which set of selections for dimuons to draw')
parser.add_argument('-dir','--directory',default='plots',help='Directory to save plots')
parser.add_argument('-r','--recreate',action='store_true',help='Whether or not to recreate data lists')
parser.add_argument('-cum','--cumulative',action='store_true',help='Whether or not to make additionally make cumulative histograms')
parser.add_argument('-bw','--binwidth',action='store_true',help='Whether or not to divide bin content by the bin width')
parser.add_argument('-cats','--categories',action='append',help='Which analysis categories to draw')
parser.add_argument('-dil','--dilepton',default='MuonsPlusMuonsMinus',help='Which set of dimuons to draw')
parser.add_argument('-no_rat','--no_ratioplot',action='store_true',help='Option to turn off ratio plot')
parser.add_argument('-norm','--normalization',type=str,default='lumi',help='How to normalize plots')
parser.add_argument('-ml','--mlow',type=float,default=0.,help='Used with norm=nevts, lower mass value for normalization')
parser.add_argument('-mh','--mhigh',type=float,default=10000.,help='Used with norm=nevts, higher mass value for normalization')
parser.add_argument('-e','--extra',type=str,default='',help='Extra save name for pdf files')
args = parser.parse_args()

datalist = [int(year) for year in args.data]
print datalist
print 'recreate',args.recreate


if not args.categories:
    categorylist = ['','bb','be','ee']
else:
    categorylist = [cat for cat in args.categories]
print categorylist

TOPLOTLISTBASE = ['DimuonMassVertexConstrained','DimuonMassVtxConstrainedLog']
TOPLOTLIST = []
if args.baseplot is None:
    for cat in categorylist:
        if cat=='ee': continue
        TOPLOTLIST += [plot+('_'+cat if cat else '') for plot in TOPLOTLISTBASE]
else:
    TOPLOTLISTBASE = [plot for plot in args.baseplot]
    for plot in TOPLOTLISTBASE:
        if 'DimuonMass' in plot:
            if 'chi2' in plot: continue
            if 'prob' in plot: continue
            if 'Weight' in plot: continue
            if 'Un' in plot: continue
            if 'Error' in plot: continue
            for cat in categorylist:
                if cat in ['ee','']: continue
                TOPLOTLIST += [plot+'_'+cat]
print TOPLOTLIST

TOPLOTLISTTREE = []
if args.treeplot is None:
    TOPLOTLISTTREE = ['vertex_m','vertex_m_log']
else:
    TOPLOTLISTTREE = [str(plot) for plot in args.treeplot]
print TOPLOTLISTTREE



TOPLOTDIR = 'Our'+str(args.selection)+args.dilepton+'Histos'
SAVEDIR = args.directory
selection = {
        2016:2016,
        2017:2016,
        2018:2018,
        }

data = {
    2016 : DataSample('Data 2016 (36.3 fb^{-1})',2016,reco='07Aug2017',color=R.kBlue),
    2017 : DataSample('Data 2017 (42.1 fb^{-1})',2017,reco='17Nov2017',color=R.kRed),
    2018 : DataSample('Data 2018 (60.4 fb^{-1})',2018,reco='PromptReco'),
    #2016 : DataSample('Data 2016 ReReco',2016,reco='07Aug2017',color=R.kBlue),
    #2017 : DataSample('Data 2017 ReReco',2017,reco='17Nov2017',color=R.kRed),
    #2018 : DataSample('Data 2018 PromptReco',2018,reco='PromptReco'),
}

for year in datalist:
    print data[year]
    data[year].get_histos(TOPLOTDIR,TOPLOTLIST)
    data[year].setup(args.recreate,Selection[selection[year]],norm=args.normalization,mlow=args.mlow,mhigh=args.mhigh)

def subtitleize(dilepton):
    return {
        'MuonsPlusMuonsMinus': '#mu^{+}#mu^{-}',
        'MuonsPlusMuonsPlus':  '#mu^{+}#mu^{+}',
        'MuonsMinusMuonsMinus': '#mu^{-}#mu^{-}',
        'MuonsSameSign': '#mu^{#pm}#mu^{#pm}',
        'MuonsAllSigns': '#mu#mu',
        'ElectronsPlusElectronsMinus': 'e^{+}e^{-}',
        'ElectronsPlusElectronsPlus': 'e^{+}e^{+}',
        'ElectronsMinusElectronsMinus': 'e^{-}e^{-}',
        'ElectronsSameSign': 'e^{#pm}e^{#pm}',
        'ElectronsAllSigns': 'ee',
        'MuonsPlusElectronsMinus': '#mu^{+}e^{-}',
        'MuonsMinusElectronsPlus': '#mu^{-}e^{+}',
        'MuonsPlusElectronsPlus': '#mu^{+}e^{+}',
        'MuonsMinusElectronsMinus': '#mu^{-}e^{-}',
        'MuonsElectronsOppSign': '#mu^{+}e^{-}/#mu^{-}e^{+}',
        'MuonsElectronsSameSign': '#mu^{#pm}e^{#pm}',
        'MuonsElectronsAllSigns': 'e#mu',
        }[dilepton]

def titleize(quantity_to_compare):
    return {
        'DileptonMass': 'm(%s)%s',
        'DimuonMassVertexConstrained': 'm(%s)%s',
        'DimuonMassVtxConstrainedLog': 'm(%s)%s',
        'DileptonPt': '%s p_{T}%s',
        'DileptonRap': '%s rapidity%s',
        'LeptonPt': "%s leptons' p_{T}%s",
        'LeptonEta': "%s leptons' #eta%s",
        'RelIsoSumPt': "%s leptons' relative tk. iso.%s",
        'RelCombIso': "%s leptons' relative comb. iso.%s",
        }.get(quantity_to_compare, quantity_to_compare + ', %s, %s')

def unitize(quantity_to_compare):
    return {
        'DileptonMass': ' [GeV]',
        'DimuonMassVertexConstrained': ' [GeV]',
        'DimuonMassVtxConstrainedLog': ' [GeV]',
        'DileptonPt': ' [GeV]',
        'LeptonPt': ' [GeV]',
        'LeptonEta': '',
        'LeptonPhi': ' [rad]',
        'DileptonPhi': ' [rad]',
        'DileptonRap': '',
        'RelCombIso': '',
        'RelIsoSumPt': '',
        }.get(quantity_to_compare, ' [XXX]')

def get_rebin_factor(quantity_to_compare):
    # For the combination of the arguments, figure out by which
    # factor to rebin the input histograms. E.g. for DileptonMass
    # the input is currently 1-GeV bins; here we change this to
    # 10-GeV bins.
    if quantity_to_compare in ['DileptonMass', 'DimuonMassVertexConstrained', 'DileptonPt', 'LeptonPt','DileptonPz']:
        return 20
    if quantity_to_compare in ['DileptonPhi', 'DileptonRap', 'LeptonPhi', 'LeptonEta']:
        return 5
    return 1

def get_x_axis_range(quantity_to_compare):
    # For the given combination of the arguments, return the
    # desired restriction on the viewable x-axis range, if
    # any. E.g. for DileptonMass, only show from 60-2000 GeV on
    # the displayed plot.
    if quantity_to_compare in ['DileptonMass', 'DimuonMassVertexConstrained','DimuonMassVtxConstrainedLog',
            'DimuonMassVertexConstrained_be','DimuonMassVtxConstrainedLog_be',
            'DimuonMassVertexConstrained_bb','DimuonMassVtxConstrainedLog_bb']:
        return 50, 3500
#            return 60, 2000
#            return 120, 1120
    elif quantity_to_compare in ['DileptonPt', 'LeptonPt']:
        return 0, 2000
    elif quantity_to_compare in ['LeptonEta','DileptonRap']:
        return -2.5,2.5
    elif quantity_to_compare in ['DileptonPz']:
        return 0,5000
    return None
    
if args.do_baseplot:
    # This block of code is for drawing histograms from ROOT files together
    # e.g. Our2016MuonsPlusMuonsMinusHistos/DimuonMassVertexConstrained
    for plot in TOPLOTLIST:
        ratioFactor = 1./3 if len(datalist)>1 else 0.
        canvas = Plotter.Canvas(lumi='',ratioFactor=ratioFactor,extra='Preliminary')
        plots = {}
        for y,year in enumerate(datalist):
            hist = data[year].histos[plot]
            if args.binwidth: hist = tools.divide_bin_width(hist)
            if args.cumulative: hist = tools.cumulative_histogram(hist)
            plots[year] = Plotter.Plot(hist,legName=data[year].nicename,legType='pe',option='hpe')
            canvas.addMainPlot(plots[year])
        canvas.makeLegend(pos='tr')
        canvas.legend.moveLegend(X=-0.1,Y=-0.05)
        canvas.setMaximum()
        xtitle = titleize(plot) % (subtitleize(args.dilepton), unitize(plot))
        canvas.firstPlot.setTitles(X='Dimuon Mass [GeV]',Y='Events')
        for year in datalist:
            #if year!=2018: plots[year].Scale(data[2018].lumi()/data[year].lumi())
            if year!=2018: plots[year].Scale(data[2018].norm[norm]/data[year].norm[norm])
            plots[year].SetLineColor(data[year].color)
            plots[year].SetMarkerColor(data[year].color)
            plots[year].SetMarkerStyle(10)
            plots[year].SetLineWidth(1)
            xrange = get_x_axis_range(plot)
            plots[year].GetXaxis().SetRangeUser(*xrange)
            plots[year].Rebin(get_rebin_factor(plot))
        if 'Log' in plot:
            canvas.mainPad.SetLogx(True)
            canvas.ratPad.SetLogx(True)
        for year in datalist:
            if year==2018: continue
            canvas.addRatioPlot(\
                plots[2018],plots[year],color=data[year].color,\
                legName='2018/'+str(year),ytit='Ratio',xtit=xtitle)
        canvas.makeRatioLegend()
        canvas.mainPad.SetLogy(True)
        savename = SAVEDIR+'/'+plot
        for year in datalist: savename+='_'+str(year)
        canvas.cleanup(savename+'.pdf')

if not args.no_treeplot:
    # This block of code is for remaking plots using the SimpleNtupler ttree
    # Necessary ingredients are MAKEPLOTLIST defined in PlotsToMake.py 
    # and a dataSample from DataSamples.py
    # (For now only do vertex_m and vertex_m_log since ttree->Draw() 
    #  will not pick out the correct dimuon. I have to do ttree->Scan()
    #  to get an event list that that I can then process)
    for plot in TOPLOTLISTTREE:
        for category in categorylist:
            ratioFactor = 0. if args.no_ratioplot else 1./3
            canvas = Plotter.Canvas(lumi='(13 TeV)',ratioFactor=ratioFactor,extra='Preliminary')
            plots = {}
            for y,year in enumerate(datalist):
                hist = data[year].make_hist_from_list(MAKEPLOTLIST[plot],plot,year,category)
                hist.Rebin(MAKEPLOTLIST[plot]['rebin'])
                if args.binwidth: hist = tools.divide_bin_width(hist)
                if args.cumulative: hist = tools.cumulative_histogram(hist)
                plots[year] = Plotter.Plot(hist,legName=data[year].nicename,legType='pe',option='pe')
            for y,year in enumerate(datalist):
                canvas.addMainPlot(plots[year])
            canvas.makeLegend(pos='tr')
            canvas.legend.moveLegend(X=-0.2,Y=-0.05)
            #canvas.setMaximum()
            canvas.firstPlot.GetYaxis().SetRangeUser(1e-3,1e6) # for Bob
            xtitle = MAKEPLOTLIST[plot]['titles'].split(';')[1]
            ytitle = MAKEPLOTLIST[plot]['titles'].split(';')[2]
            canvas.firstPlot.setTitles(X=xtitle,Y=ytitle+(' / GeV' if args.binwidth else ''))
            for year in datalist:
                #plots[year].Scale(data[2018].norm[args.normalization]/data[year].norm[args.normalization])
                #print year,data[year].norm[args.normalization],data[2018].norm[args.normalization]/data[year].norm[args.normalization]
                #print year,data[year].lumi(),data[2018].lumi()/data[year].lumi()
                plots[year].SetLineColor(data[year].color)
                plots[year].SetMarkerColor(data[year].color)
                plots[year].SetMarkerStyle(10)
                plots[year].SetLineWidth(1)
                xmin = MAKEPLOTLIST[plot]['lims']['min']
                xmax = MAKEPLOTLIST[plot]['lims']['max']
                plots[year].GetXaxis().SetRangeUser(xmin,xmax)
            if not args.no_ratioplot:
                for year in datalist:
                    if year==2018: continue
                    canvas.addRatioPlot(\
                        plots[2018],plots[year],color=data[year].color,\
                        legName='2018/'+str(year),ytit='Ratio',xtit=xtitle)
                canvas.makeRatioLegend()
                canvas.ratPad.SetLogx(MAKEPLOTLIST[plot]['log']['x'])
                if MAKEPLOTLIST[plot]['log']['x']: 
                    canvas.ratPad.cd()
                    canvas.firstRatioPlot.GetXaxis().SetMoreLogLabels()
                    canvas.firstRatioPlot.GetXaxis().SetNoExponent()
                    canvas.cd()
            canvas.mainPad.SetLogy(MAKEPLOTLIST[plot]['log']['y'])
            canvas.mainPad.SetLogx(MAKEPLOTLIST[plot]['log']['x'])
            canvas.firstPlot.GetXaxis().SetMoreLogLabels()
            canvas.firstPlot.GetXaxis().SetNoExponent()
            savename = SAVEDIR+'/'+plot+('_'+category if category else '')
            for year in datalist: savename+='_'+str(year)
            savename+= ('_'+args.extra if args.extra!='' else '')
            canvas.cleanup(savename+'.pdf')
