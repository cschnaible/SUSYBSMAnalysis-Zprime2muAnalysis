import ROOT as R
R.gROOT.SetBatch(True)
#R.gStyle.SetOptFit(00000000)
#R.gStyle.SetOptStat(00000000)
import numpy as np
import array, math, logging
import SUSYBSMAnalysis.Zprime2muAnalysis.lumberjack as lumberjack
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools_chris import divide_bin_width, move_overflow_into_last_bin
import argparse
parser = argparse.ArgumentParser()
#parser.add_argument('-n','--numden',default='Num',help='Numerator or denominator')
#parser.add_argument('--hist',default='Acceptance',help='Histogram to use for ratio')
#parser.add_argument('-r','--rebin',default=200,type=int,help='Rebin factor')
#parser.add_argument('-c','--category',default='all',help='Analysis pseudorapidity category')
#
parser.add_argument('-x',default='res_mass',help='Quantity to draw on X axis')
parser.add_argument('-c','--category',default='all',help='Analysis category: all, bb, beee, ee')
parser.add_argument('-s','--selection',default='',help='Selection to apply in addition to Z-peak mass window')
parser.add_argument('-lx','--logx',action='store_true',default=False)
parser.add_argument('-ly','--logy',action='store_true',default=False)
parser.add_argument('-n','--name',default='')
parser.add_argument('-nbx','--nbinsx',default=None,type=int)
parser.add_argument('--xmin',default=None,type=int)
parser.add_argument('--xmax',default=None,type=int)
parser.add_argument('--fmin',default=0,type=float)
parser.add_argument('--fmax',default=6000,type=float)
parser.add_argument('--no-fit',action='store_true')
parser.add_argument('-mc','--mc',default='dy',help='Which MC to compare, dy, WW, ttbar_lep')
parser.add_argument('-bw','--bin-width',action='store_true',help='Divide by bin width')
parser.add_argument('-o','--overflow',action='store_true',help='Move overflow into last bin')
parser.add_argument('-var','--var-binning',action='store_true',help='Use variable width binning')
parser.add_argument('--fit-func',default='pol5',help='Parametrization fit function')
args = parser.parse_args()

mcList = {
    'WW':['WW_50to200','WW_200to600','WW_600to1200','WW_1200to2500','WW_2500toInf'],
    'dy':['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf'],
    'ttbar_lep':['ttbar_lep_50to500','ttbar_lep_500to800','ttbar_lep_800to1200','ttbar_lep_1200to1800','ttbar_lep_1800toInf'],
    }
info = {
        2016:{'path':'mc_2016/','dir':'Our2016OppSignEfficiency'},
        2017:{'path':'mc_2017/','dir':'Our2018OppSignEfficiency'},
        2018:{'path':'mc/','dir':'Our2018OppSignEfficiency'},
        }

categories = {
        'all':'(1.)',
        'acc':'(fabs(lep_noib_eta[0])<2.4 && fabs(lep_noib_eta[1])<2.4)',
        'bb':'(fabs(lep_noib_eta[0])<=1.2 && fabs(lep_noib_eta[1])<=1.2)',
        'beee':'((fabs(lep_noib_eta[0])>1.2 || fabs(lep_noib_eta[1])>1.2) && fabs(lep_noib_eta[0])<2.4 && fabs(lep_eta[1])<2.4)',
        'ee':'((fabs(lep_noib_eta[0])>1.2 && fabs(lep_noib_eta[1])>1.2) && fabs(lep_noib_eta[0])<2.4 && fabs(lep_eta[1])<2.4)',
        }

selection = '('+categories[args.category]+(' && '+args.selection if args.selection else '')+')'

legNames = {
        2016:'80X NNPDF3.0',
        2017:'94X NNPDF3.1',
        2018:'102X NNPDF3.1',
        }
colors = {
        2016:R.kOrange+1,
        2017:R.kBlue,
        2018:R.kRed,
        }
years = {
        'dy':[2016,2017,2018],
        'WW':[2016,2017],
        'ttbar_lep':[2016,2017],
        }

if args.var_binning:
    if args.mc=='ttbar_lep': 
        bins = array.array('d',[i*100 for i in range(11)]+[1200,1400,1700,2000,2400,3000]) # ttbar
    elif args.mc=='WW': 
        bins = array.array('d',[i*200 for i in range(8)]+[1800,2200,3000]) # WW
    elif args.mc=='dy':
        if args.x=='lead_pt':
            bins = array.array('d',[30+i*5 for i in range(11)]+[90,100,110,125,150,175,200,250,300,400,600])
elif args.logx: 
    bins = np.logspace(np.log10(float(args.xmin)),np.log10(float(args.xmax)),int(args.nbinsx)+1)
else: 
    bins = array.array('d',[args.xmin + i*(args.xmax-args.xmin)/args.nbinsx for i in range(0,args.nbinsx+1)])

hist = R.TH1D('h','',int(len(bins))-1,bins)

# Make Histograms
def get_sum_weights(t):
    if hasattr(t,'genWeight'):
        return float(t.GetEntries('genWeight>0'))-t.GetEntries('genWeight<0')
    else:
        return t.GetEntries()

plotVars = {
        'res_mass':'res_mass',
        'lead_pt':'( lep_noib_pt[0]*(lep_noib_pt[0]>lep_noib_pt[1]) + lep_noib_pt[1]*(lep_noib_pt[1]>lep_noib_pt[0]) )',
        }
xtitles = {
        'res_mass':'GEN m(#mu^{+}#mu^{-}) [GeV]',
        'lead_pt':'GEN leading #mu p_{T} [GeV]',
        }

hists = {year:{mc:{} for mc in mcList[args.mc]+['all']} for year in years[args.mc]}
for year in years[args.mc]:
    hists[year]['all'] = hist.Clone('h'+str(year))
    hists[year]['all'].SetDirectory(0)
    for mc in mcList[args.mc]:
        fname = info[year]['path']+'ana_genmc_'+mc+'.root'
        f = R.TFile(fname)
        h = hist.Clone(str(year)+'_'+mc)
        t = f.Get('hardInteractionNtuple/t')
        theselection = '(res_mass>50 && '+selection+')'+('*genWeight' if year!=2016 else '')
        #theselection = selection if year==2016 else selection+'*genWeight'
        t.Draw(plotVars[args.x]+'>>'+str(year)+'_'+mc,theselection,'pe')
        h.SetDirectory(0)
        hists[year][mc] = h
        hists[year][mc].SetDirectory(0)
        scale_by = samples[year][mc].cross_section/get_sum_weights(t)
        hists[year][mc].Scale(scale_by)
        print mc,samples[year][mc].cross_section,get_sum_weights(t),samples[year][mc].cross_section/get_sum_weights(t),hists[year][mc].Integral(),hists[year][mc].GetEntries()
        hists[year]['all'].Add(hists[year][mc])
        hists[year]['all'].SetDirectory(0)
        f.Close()

for year in years[args.mc]:
    if args.overflow:
        move_overflow_into_last_bin(hists[year]['all'])
    if args.bin_width:
        divide_bin_width(hists[year]['all'])

xlines = {
        'WW':[50,200,600,1200,2500],
        'ttbar_lep':[50,500,800,1200,1800],
        'dy':[50,120,200,400,800,1400,2300,3500,4500,6000],
        }

canvas = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation Preliminary',logy=True)
plots = {year:Plotter.Plot(hists[year]['all'],legName=legNames[year],legType='l',option='hist') for year in years[args.mc]}
for year in years[args.mc]:
    canvas.addMainPlot(plots[year])
    plots[year].SetLineColor(colors[year])
    plots[year].SetLineWidth(2)
hmin = min([hists[year]['all'].GetMinimum() for year in years[args.mc] if hists[year]['all'].GetMinimum()>0.])/10.
hmax = max([hists[year]['all'].GetMaximum() for year in years[args.mc]])*10
canvas.firstPlot.GetYaxis().SetRangeUser(hmin,hmax)
line = {}
if args.x=='res_mass':
    for x in xlines[args.mc]:
        line[x] = R.TLine(x,hmin,x,hmax)
        line[x].Draw('same')
canvas.makeLegend(pos='tr')
canvas.legend.moveLegend(X=-0.1)
canvas.firstPlot.setTitles(X=xtitles[args.x],Y='XS / sum of weights'+(' / GeV' if args.bin_width else ''))
plotname = args.mc+'_'+args.x+'_'+args.category+'_compare'+('_'+args.name if args.name else '')+('' if args.no_fit else '_fit')
canvas.cleanup('www_nnpdf/'+plotname,extList=['.png','.pdf'])
        

rats = {
        2017:hists[2016]['all'].Clone('rat_80X_94X_'+args.x),
        2018:hists[2016]['all'].Clone('rat_80X_102X_'+args.x),
        }
for year in years[args.mc][1:]:
    print rats[year], hists[year]['all']
    rats[year].Divide(hists[year]['all'])

canvas = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation Preliminary')
plots = {year:Plotter.Plot(rats[year],legName=legNames[year],legType='pe',option='pe') for year in years[args.mc][1:]}
for year in years[args.mc][1:]:
    canvas.addMainPlot(plots[year])
    plots[year].SetMarkerColor(colors[year])
    plots[year].SetLineColor(colors[year])

if args.x=='lead_pt':
    func = '(x<100)*([0] + [1]*pow(x,1) + [2]*pow(x,2) + [3]*pow(x,3) + [4]*pow(x,4) + [5]*pow(x,5)) + (x>100)*[6]'
else:
    func = args.fit_func
if not args.no_fit:
    fits = {
            2017:R.TF1('f_'+args.x+'_80X_94X',func,args.fmin,args.fmax),
            2018:R.TF1('f_'+args.x+'_80X_102X',func,args.fmin,args.fmax),
            }
    print '\n','*'*30,'\n','80X / 94X',func,args.fmin,args.fmax,'\n'
    rats[2017].Fit(fits[2017].GetName(),'R')
    rats[2017].SetStats(False)
    fits[2017].SetLineColor(colors[2017])
    fits[2017].Draw('same')
    if args.mc=='dy':
        print '\n','*'*30,'\n','80X / 102X',func,args.fmin,args.fmax,'\n'
        rats[2018].Fit(fits[2018].GetName(),'R')
        rats[2018].SetStats(False)
        fits[2018].SetLineColor(colors[2018])
        fits[2018].Draw('same')

canvas.Update()
if args.mc=='dy':
    if args.x=='res_mass':
        hmin,hmax=0.5,3.5
    elif args.x=='lead_pt':
        hmin,hmax=0.5,1.5
elif args.mc=='WW':
    hmin,hmax = 0,2
elif args.mc=='ttbar_lep':
    hmin,hmax = 0,2
canvas.firstPlot.GetYaxis().SetRangeUser(hmin,hmax)
line = {}
if args.x=='res_mass':
    for x in xlines[args.mc]:
        line[x] = R.TLine(x,hmin,x,hmax)
        line[x].Draw('same')
l1 = R.TLine(bins[0],1,bins[-1],1)
l1.Draw('same')
canvas.firstPlot.setTitles(X=xtitles[args.x],Y='NNPDF3.0 / NNPDF3.1')
plotname = args.mc+'_'+args.x+'_'+args.category+'_ratio'+('_'+args.name if args.name else '')+('' if args.no_fit else '_fit')
canvas.cleanup('www_nnpdf/'+plotname,extList=['.png','.pdf'])


lumberjack.setup_logger(plotname,'www_nnpdf/'+plotname+'.log')
logger = logging.getLogger(plotname)
logger.info(args)
logger.info('\n'+'*'*15+'\n')
logger.info(args.x+' '+args.category+' '+args.selection)
logger.info('\n'+'*'*15+'\n')
logger.info('Binning')
if args.nbinsx!=None: logger.info(int(args.nbinsx))
logger.info(bins)
logger.info('\n'+'*'*15+'\n')
logger.info('Fit Results')
for year in years[args.mc][1:]:
    logger.info(str(year))
    for p in range(fits[year].GetNpar()):
        logger.info(str(p)+' '+str(fits[year].GetParameter(p))+' +/- '+str(fits[year].GetParError(p)))
logger.info('\n'+'*'*15+'\n')

