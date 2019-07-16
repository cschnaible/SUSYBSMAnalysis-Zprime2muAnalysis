import ROOT as R
import os,sys,math,logging,pdb,array,string
import numpy as np
import SUSYBSMAnalysis.Zprime2muAnalysis.lumberjack as lumberjack
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples# samples18, samples17, samples16
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools import binomial_divide
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-w','--where',default='www_acceff',help='Where to save plots')
parser.add_argument('-s','--selection',default='our',help='Selection cutset: our, ourZ')
parser.add_argument('-y','--year',default=2018,type=int,help='Year')
parser.add_argument('-b','--binning',default='var',help='Which binning to do, fixed 100 GeV widths or variable width')
args = parser.parse_args()


savedir = args.where+'/'+args.selection+'_'+str(args.year)+'_'+args.binning
os.system('mkdir -p '+savedir)

dyList = ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf']
 

categories = ['all','bb','beee']
catNameMap = {'all':'','bb':'_bb','beee':'_e'}

info = {
        2016:{
            'file':'mc_2016/ana_effres_dy50toInf.root',
            'our':'Our2016OppSignEfficiency',
            'ourZ':'Our2016AtZOppSignEfficiency',
            },
        2017:{
            'file':'mc_2017/ana_effres_dy50toInf.root',
            'our':'Our2018OppSignEfficiency',
            'ourZ':'Our2018AtZOppSignEfficiency',
            },
        2018:{
            'file':'mc/ana_effres_dy50toInf.root',
            'our':'Our2018OppSignEfficiency',
            'ourZ':'Our2018AtZOppSignEfficiency',
            },
        }

binning = {
        'var':[0]+[120+i*40 for i in range(22)]+[1000+i*100 for i in range(10)]+[2000+i*200 for i in range(21)],
        'fixed':[i*100 for i in range(61)],
        'big':[0,60,120,200,400,800,1400,2300,3500,4500,6000,8000],
        }

plots = ['AccNoPt', 'Acceptance', 'RecoWrtAcc', 'RecoWrtAccTrig', 'TotalReco', 'TrigWrtAcc']

if args.year in [2017,2018]:
    if args.selection=='our':
        plots += ['HLTPath_Mu50','HLTPath_OldMu100','HLTPath_TkMu100']
    elif args.selection=='ourZ':
        plots += ['HLTPath_Mu27']
elif args.year==2016:
    if args.selection=='our':
        plots += ['HLTPath_Mu50','HLTPath_TkMu50']
    elif args.selection=='ourZ':
        plots += ['HLTPath_Mu27','HLTPath_TkMu27']


theFile = R.TFile(info[args.year]['file'])
hists = {cat:{plot:{r:{} for r in ['Num','Den','Rat']} for plot in plots} for cat in categories}
for cat in categories:
    for plot in plots:
        for r in ['Num','Den']:
            hist = theFile.Get(info[args.year][args.selection]+'/'+r+plot+catNameMap[cat]).Clone()
            hists[cat][plot][r] = hist.Rebin(len(binning[args.binning])-1,'ratio_'+plot+'_'+cat,array.array('d',binning[args.binning]))
            hists[cat][plot][r].SetDirectory(0)
        hists[cat][plot]['Rat'],y,eyl,eyh = binomial_divide(hists[cat][plot]['Num'],hists[cat][plot]['Den'])

fit_funcs = {
        'low':{
            'func':'[0]+[1]*exp(-1*(x-[2])/[3])+[4]*pow(x,[5])',
            'lims':{
                'all':[120,800,5],
                'bb':[120,600,5],
                'beee':[120,450,6],
                },
            },
        'all':{
            'func':'[0]+[1]*pow(x+[2],-3)+[3]*pow(x,2)',
            'lims':[800,6000,4],
            },
        'bb':{
            'func':'[0]+[1]*pow(x+[2],-1)+[3]*x',
            'lims':[600,6000,4],
            },
        'beee':{
            'func':'[0]+[1]*pow(x,[2])*exp(-1*(x-[3])/[4])',
            'lims':[450,6000,5],
            },
        }
legNames = {
        'AccNoPt':'Acceptance (no p_{T} cut)',
        'Acceptance':'Acceptance (within #eta category)',
        'RecoWrtAcc':'Reco+ID Efficiency / Accecptance',
        'RecoWrtAccTrig':'Reco+ID Efficiency / (Acceptance #times Trigger Fired)',
        'TotalReco':'Total Acceptance #times Efficiency',
        'TrigWrtAcc':'Trigger Fired / Acceptance',
        'HLTPath_Mu27':'HLT_Mu27 Fired',
        'HLTPath_TkMu27':'HLT_TkMu27 Fired',
        'HLTPath_Mu50':'HLT_Mu50 Fired',
        'HLTPath_TkMu50':'HLT_TkMu50 Fired',
        'HLTPath_OldMu100':'HLT_OldMu100 Fired',
        'HLTPath_TkMu100':'HLT_TkMu100 Fired',
        }
styles = {
        'AccNoPt':{'color':R.kCyan+1,'style':22},
        'Acceptance':{'color':R.kBlue-4,'style':22},
        'RecoWrtAcc':{'color':R.kOrange+1,'style':21},
        'RecoWrtAccTrig':{'color':R.kRed-4,'style':21},
        'TotalReco':{'color':R.kBlack,'style':11},
        'TrigWrtAcc':{'color':R.kGreen+1,'style':23},
        'HLTPath_Mu27':{'color':R.kMagenta+1,'style':11},
        'HLTPath_TkMu27':{'color':R.kViolet+1,'style':11},
        'HLTPath_Mu50':{'color':R.kMagenta+1,'style':11},
        'HLTPath_TkMu50':{'color':R.kViolet+1,'style':11},
        'HLTPath_OldMu100':{'color':R.kMagenta-4,'style':11},
        'HLTPath_TkMu100':{'color':R.kViolet,'style':11},
        }

# Draw each plot individually
for cat in categories:
    for plot in plots:
        canvas = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation Preliminary')
        p = Plotter.Plot(hists[cat][plot]['Rat'],option='pe',legName=legNames[plot])
        canvas.addMainPlot(p)
        p.SetLineColor(styles[plot]['color'])
        p.SetMarkerColor(styles[plot]['color'])
        p.SetMarkerStyle(styles[plot]['style'])
        canvas.makeLegend(pos='br')
        canvas.legend.moveLegend(X=-0.5)
        canvas.firstPlot.GetYaxis().SetRangeUser(0,1.05)
        canvas.firstPlot.setTitles(X='m(#mu^{+}#mu^{#font[122]{\55}}) [GeV]',Y='Efficiency')
        canvas.mainPad.SetGrid()
        canvas.cleanup(savedir+'/'+plot+'_'+cat,extList=['.png','.pdf'])

def do_fit(cat,plot,hist):
    fit_name = plot+'_'+cat
    fitlow = R.TF1(fit_name+'_low',fit_funcs['low']['func'],fit_funcs['low']['lims'][cat][0],fit_funcs['low']['lims'][cat][1],fit_funcs['low']['lims'][cat][2])
    fithigh = R.TF1(fit_name+'_high',fit_funcs[cat]['func'],fit_funcs[cat]['lims'][0],fit_funcs[cat]['lims'][1],fit_funcs[cat]['lims'][2])
    if cat=='all': 
        fitlow.SetParameters(1.7,-0.3,90,40,-4.0,-0.2)
        fitlow.SetParLimits(0,1,2)
        fitlow.SetParLimits(1,-0.6,-0.1)
        fitlow.SetParLimits(2,80,120)
        fitlow.SetParLimits(3,30,45)
        fitlow.SetParLimits(4,-7,-2)
        fitlow.SetParLimits(5,-0.5,-0.1)
        fithigh.SetParameters(0.8,-5e8,791,-1./1.8e9)
    elif cat=='bb': 
        fitlow.SetParameters(2,-0.13,111,22,-2.4,-0.03)
        fitlow.SetParLimits(0,2,2.5)
        fitlow.SetParLimits(1,-0.2,-0.1)
        fitlow.SetParLimits(2,100,140)
        fitlow.SetParLimits(3,5,30)
        fitlow.SetParLimits(4,-4,-1)
        fitlow.SetParLimits(5,-0.05,-0.01)
        fithigh.SetParameters(5,-5.5e4,1.2e4,-2.1e-4)
    elif cat=='beee': 
        fitlow.SetParameters(14,-7,-4.8e6,-7.4e6,-108,-1.1)
        fithigh.SetParameters(0.3,0.04,1.4,-5100,713)
        fithigh.SetParLimits(0,0.2,0.4)
        fithigh.SetParLimits(1,0.01,0.05)
        fithigh.SetParLimits(2,1.0,2.0)
        fithigh.SetParLimits(3,-5500,-4800)
        fithigh.SetParLimits(4,700,1000)
    hist.Fit(fitlow,'M0R+')
    hist.Fit(fithigh,'M0R+')
    return fitlow,fithigh

def log_fit(cat,plot,graph,fitlow,fithigh):
    name = cat+'_'+plot
    lumberjack.setup_logger(name,savedir+'/combined_'+cat+'.log')
    logger = logging.getLogger(name)
    logger.info(cat+' '+plot)

    logger.info('\n'+'*'*15+'\n')
    logger.info('Low mass fit '+str(fit_funcs['low']['lims'][cat][0])+' < m < '+str(fit_funcs['low']['lims'][cat][1]))
    logger.info(fit_funcs['low']['func'])
    for p,par in enumerate([a for a in string.ascii_lowercase[:fit_funcs['low']['lims'][cat][2]]]):
        logger.info(par+' '+str(fitlow.GetParameter(p))+' +/- '+str(fitlow.GetParError(p)))
    logger.info('Chi2/ndf = '+str(fitlow.GetChisquare())+' / '+str(fitlow.GetNDF()))

    logger.info('\n'+'*'*15+'\n')
    logger.info('High mass fit '+str(fit_funcs[cat]['lims'][0])+' < m < '+str(fit_funcs[cat]['lims'][1]))
    logger.info(fit_funcs[cat]['func'])
    for p,par in enumerate([a for a in string.ascii_lowercase[:fit_funcs[cat]['lims'][2]]]):
        logger.info(par+' '+str(fithigh.GetParameter(p))+' +/- '+str(fithigh.GetParError(p)))
    logger.info('Chi2/ndf = '+str(fithigh.GetChisquare())+' / '+str(fithigh.GetNDF()))

    logger.info('\n'+'*'*15+'\n')
    logger.info('Total Reco Data')
    n = graph.GetN()
    x,y = R.Double(), R.Double()
    for i in xrange(n):
        graph.GetPoint(i, x, y)
        exl = graph.GetErrorXlow(i)
        exh = graph.GetErrorXhigh(i)
        eyl = graph.GetErrorYlow(i)
        eyh = graph.GetErrorYhigh(i)
        logger.info('%20s%10.4f%20s' % ('%.f-%.f' % (x-exl, x+exh), y, '[%5.4f, %5.4f]' % (y-eyl, y+eyh)))

    logger.info('\n'+'*'*15+'\n')


# Draw combined plot + fit
drawList = ['Acceptance','TrigWrtAcc','RecoWrtAccTrig','TotalReco']
for cat in categories:
    canvas = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation Preliminary')
    plots = {plot:Plotter.Plot(hists[cat][plot]['Rat'],option='pe',legName=legNames[plot],legType='pe') for plot in drawList}
    fitlow, fithigh = do_fit(cat,'TotalReco',hists[cat]['TotalReco']['Rat'])
    log_fit(cat,'TotalReco',hists[cat]['TotalReco']['Rat'],fitlow,fithigh)
    for plot in drawList:
        canvas.addMainPlot(plots[plot])
        plots[plot].plot.SetLineColor(styles[plot]['color'])
        plots[plot].plot.SetMarkerColor(styles[plot]['color'])
        plots[plot].plot.SetMarkerStyle(styles[plot]['style'])
    fitlow.SetLineColor(R.kRed)
    fithigh.SetLineColor(R.kRed)
    fitlow.Draw('same')
    fithigh.Draw('same')
    canvas.makeLegend(pos='br')
    canvas.legend.moveLegend(X=-0.5)
    canvas.firstPlot.GetYaxis().SetRangeUser(0,1.05)
    canvas.firstPlot.setTitles(X='m(#mu^{+}#mu^{#font[122]{\55}}) [GeV]',Y='Efficiency')
    canvas.mainPad.SetGrid()
    canvas.Update()
    canvas.cleanup(savedir+'/combined_'+cat,extList=['.png','.pdf'])
