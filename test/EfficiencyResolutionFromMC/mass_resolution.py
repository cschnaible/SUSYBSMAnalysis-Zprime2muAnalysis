import ROOT as R
import os,sys,math,logging,pdb
import numpy as np
import SUSYBSMAnalysis.Zprime2muAnalysis.lumberjack as lumberjack
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples# samples18, samples17, samples16
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-w','--where',default='www_res',help='where to save output')
parser.add_argument('--var' ,default='vertex_gen',help='which variable to compute resolution')
parser.add_argument('--xmin',default=0,type=float,help='Minimum variable value')
parser.add_argument('--xmax',default=6000,type=float,help='Maximum variable value')
parser.add_argument('--res-xmin',default=-1, type=float,help='minimum residual value for histogram')
parser.add_argument('--res-xmax',default= 1, type=float,help='maximum residual value for histogram')
parser.add_argument('--res-bins',default=400,type=int,help='width of residual histogram bins')
parser.add_argument('--res-func',default='dscb',help='residual fitting function')
parser.add_argument('--res-rebin',default=1,help='Rebin factor for residual histogram')
parser.add_argument('--func-xmin',default=-2.0,type=float,help='minimum residual value for fit, units in sigma of gaussian core fit')
parser.add_argument('--func-xmax',default= 1.7,  type=float,help='maximum residual value for fit, units in sigma of gaussian core fit')
parser.add_argument('--par-func',default='pol5',help='Function to parametrize resolution fit results')
parser.add_argument('--par-xmin',default=120,type=float,help='Minimum var value for resolution parametrization')
parser.add_argument('--par-xmax',default=6000,type=float,help='Maximum var value for resolutin paraemetrization')
parser.add_argument('-dy','--drell-yan',default='powheg',help='Which DY MC to use')
parser.add_argument('-y','--year',default=2018,type=int,help='Which MC year to do')
parser.add_argument('-s','--selection',default='our',help='Which cutset to plot: our (pt>53 GeV) or ourZ (pt>30 GeV)')
#parser.add_argument('-c','--category',default='all',help='Analysis category')
parser.add_argument('--smear',default=0.0,type=float,help='Additional smearing to apply, e.g. 0.15 = 15% additional smearing')
parser.add_argument('--syst-err',default=1.0,type=float,help='Systematic error for resolution')
args = parser.parse_args()

savedir = args.where+'/'+args.var+'_'+str(args.year)
savedir += '_syst' if args.syst_err!=1.0 else '_nominal'
savedir += '_smear' if args.syst_err!=1.0 and args.smear>0.0 else ''
savedir += '_GE' if 'GE' in args.var and 'GE' in args.drell_yan else ''

os.system('mkdir -p '+savedir)
os.system('cp ~/public/index.php '+savedir)

R.gROOT.LoadMacro("cruijff.C+")
R.gROOT.LoadMacro('DoubleSidedCrystalBall.C+')
R.gROOT.LoadMacro('GaussExp.C+')

dyLists = {
    'powheg' : ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf'],
    'powheg_GE' : ['dy50to120_GE','dy120to200_GE','dy200to400_GE','dy400to800_GE','dy800to1400_GE','dy1400to2300_GE','dy2300to3500_GE','dy3500to4500_GE','dy4500to6000_GE','dy6000toInf_GE'],
    'ht' : ['dyJetsToLL_ht100to200','dyJetsToLL_ht200to400','dyJetsToLL_ht400to600','dyJetsToLL_ht600to800','dyJetsToLL_ht800to1200','dyJetsToLL_ht1200to2500','dyJetsToLL_ht2500toInf'],
    'madgraph' : ['dyInclusive50_madgraph'],
    'amcatnlo' : ['dyInclusive50_amcatnlo'],
    }

cats = {
        'all':'(1.)',
        'bb':'(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)',
        'beee':'(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)',
        'ee':'(fabs(lep_eta[0])>1.2 && fabs(lep_eta[1])>1.2)',
        }

categories = ['bb','beee']

info = {
        2016:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/data/',
            'file':'ana_datamc_Run2016_17Jul2018.root',
            'our':'Our2016MuonsOppSignNtuple',
            'ourcommonpre':'Our2016MuPrescaledCommonMuonsOppSignNtuple',
            'ourpre':'Our2016MuPrescaledMuonsOppSignNtuple',
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/mc/',
            'mc':samples[2016],
            },
        2017:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/data/',
            'file':'ana_datamc_Run2017_31Mar2018.root',
            'our':'Our2018MuonsOppSignNtuple',
            'ourcommonpre':'Our2018MuPrescaledCommonMuonsOppSignNtuple',
            'ourpre':'Our2018MuPrescaledMuonsOppSignNtuple',
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/mc/',
            'mc':samples[2017],
            },
        2018:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/data/',
            'file':'ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root',
            'our':'Our2018MuonsOppSignNtuple',
            'ourcommonpre':'Our2018MuPrescaledMuonsOppSignNtuple',
            'ourpre':'Our2018MuPrescaledNoCommonMuonsOppSignNtuple',
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/mc/',
            'mc':samples[2018],
            },
        }

res_info = {
        'vertex_gen':{
            'vars':{
                'gen':'gen_dil_mass',
                'reco':'vertex_m',
                },
            'bins':[120,200,300,400,600,800,1000,1300,1600,2000,2500,3100,3800,4500,5500,6500],
            },
        'dil_mass_GE_gen':{
            'vars':{
                'gen':'gen_dil_mass',
                'reco':'dil_mass',
                },
            'bins':[120,200,300,400,600,800,1000,1300,1600,2000,2500,3100,3800,4500,5500,6500],
            },
        'dil_mass_gen':{
            'vars':{
                'gen':'gen_dil_mass',
                'reco':'dil_mass',
                },
            'bins':[120,200,300,400,600,800,1000,1300,1600,2000,2500,3100,3800,4500,5500,6500],
            },
        'dil_mass_vertex':{
            'vars':{
                'gen':'dil_mass',
                'reco':'vertex_m',
                },
            'bins':[120,200,300,400,600,800,1000,1300,1600,2000,2500,3100,3800,4500,5500,6500],
            },
#        'pt':{
#            'bins':{
#                'bb':[0,40,100,150,200,300,450,800],
#                'be':[0,40,100,150,200,300,450],
#                },
#            },
        }

sigmaParam = 'gen_dil_mass*({A} + ({B})*pow(gen_dil_mass,1) + ({C})*pow(gen_dil_mass,2) + ({D})*pow(gen_dil_mass,3) + ({E})*pow(gen_dil_mass,4))'
sigma_old = {
        2018:{
            'bb':sigmaParam.format(
                A=0.00619766402942,
                B=3.2426990182e-05,
                C=-1.21732259344e-08,
                D=2.13395384051e-12,
                E=-1.31158132934e-16),
            'beee':sigmaParam.format(
                A=0.0115214484141,
                B=3.02489947633e-05,
                C=-1.05393540619e-08,
                D=1.82259948283e-12,
                E=-1.1235935836e-16),
            },
        2017:{
            'bb':sigmaParam.format(
                A=0.00583946446115,
                B=3.28449801802e-05,
                C=-1.25943053476e-08,
                D=2.28610822844e-12,
                E=-1.463716647e-16),
            'beee':sigmaParam.format(
                A=0.0114227352887,
                B=2.75680330992e-05,
                C=-7.881090642e-09,
                D=1.058825617e-12,
                E=-4.63832816511e-17),
            },
        2016:{
            'bb':sigmaParam.format(
                A=0.00619766402942,
                B=3.2426990182e-05,
                C=-1.21732259344e-08,
                D=2.13395384051e-12,
                E=-1.31158132934e-16),
            'beee':sigmaParam.format(
                A=0.0115214484141,
                B=3.02489947633e-05,
                C=-1.05393540619e-08,
                D=1.82259948283e-12,
                E=-1.1235935836e-16),
            },
        }

binning = res_info[args.var]['bins'][:] if args.year in [2017,2018] else res_info[args.var]['bins'][:-1]

nbinsx = int(args.xmax) - int(args.xmin)
hist = R.TH2D('hResVsMass','',nbinsx,args.xmin,args.xmax,int(args.res_bins),args.res_xmin,args.res_xmax)
hists = {dy:{cat:{} for cat in categories} for dy in dyLists[args.drell_yan]}

smearSigma = math.sqrt(pow(args.smear,2)-1) if args.smear>0.0 else 0.0 # smearSigma is a relative percentage
gausRndm = {cat:sigma_old[args.year][cat]+'*'+str(smearSigma)+'*sin(2.0*pi*rndm)*sqrt(-2.0*log(rndm))' for cat in categories}
var = {cat:res_info[args.var]['vars']['reco']+(' + '+gausRndm[cat] if args.smear>0.0 else '') for cat in categories}
toDraw = {cat:'('+var[cat]+' - '+res_info[args.var]['vars']['gen']+') / '+res_info[args.var]['vars']['gen']+':'+res_info[args.var]['vars']['gen'] for cat in categories}

# Draw Histograms
for dy in dyLists[args.drell_yan]:
    print '*'*15
    print dy
    f = R.TFile(info[args.year]['mcpath']+'ana_datamc_'+dy+'.root')
    t = f.Get(info[args.year][args.selection]+'/t')
    for cat in categories:
        hname = 'hResid_'+dy+'_'+cat
        h = hist.Clone(hname)
        cuts = cats[cat]
        print '-'*15
        print cat
        print cuts
        print toDraw[cat]
        t.Draw(toDraw[cat]+'>>'+hname,cuts,'')
        h.SetDirectory(0)
        hists[dy][cat] = h
        hists[dy][cat].SetDirectory(0)
    f.Close()

resid_hist = {cat:hist.Clone('hResiduals_'+cat) for cat in categories}
for cat in categories:
    for dy in dyLists[args.drell_yan]:
        resid_hist[cat].Add(hists[dy][cat])
    resid_hist[cat].SetDirectory(0)


def getBinRange(histo,mlow,mhigh):
    xmin =  0
    xmax = -1
    nbins = histo.GetNbinsX()
    for bin in range(nbins):
        if mlow==histo.GetXaxis().GetBinLowEdge(bin): 
            xmin = bin
        if mhigh==histo.GetXaxis().GetBinUpEdge(bin):
            xmax = bin
    return xmin,xmax

# Slice Histograms
res_hists = {cat:{low:{} for low in binning[:-1]} for cat in categories}
for cat in categories:
    for x,low in enumerate(binning[:-1]):
        res_hists[cat][low] = R.TH1D()
        res_hists[cat][low].SetDirectory(0)
        R.TH1.AddDirectory(R.kFALSE)    
        high = binning[x+1]
        xlow,xhigh = getBinRange(resid_hist[cat],low,high)
        res_hists[cat][low] = resid_hist[cat].ProjectionY('hResid_'+cat+'_'+str(low),xlow,xhigh)
        res_hists[cat][low].Rebin(args.res_rebin)
        res_hists[cat][low].SetDirectory(0)

parNames = {
        'dscb':["Constant","AlphaL","nL","Mean","Sigma","AlphaR","nR"],
        'cb':["Constant","Mean","Sigma","Alpha","n"],
        'gaus':['Constant','Mean','Sigma'],
        'cruijff':['Constant','Mean','Sigma','AlphaL','AlphaR'],
        'gausexp':['Constant','Mean','Sigma','AlphaL','AlphaR'],
        }

pars = {cat:{par:{info:[] for info in ['xlow','xhigh','val','err']} for par in parNames[args.res_func]+['chi2']} for cat in categories}

def plot_indv_res(hist,fit,x,cat):
    low = str(binning[x])
    high = str(binning[x+1])
    canv = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation')
    plot = Plotter.Plot(hist,option='pe')
    canv.addMainPlot(plot)
    fit.SetLineWidth(2)
    fit.SetLineColor(R.kBlue)
    fit.Draw("same")
    plot.setTitles(X='(m_{RECO} - m_{GEN}) / m_{GEN}',Y='Entries/bin')
    plot.scaleTitles(0.75)
    plot.scaleLabels(0.75)
    fitmin = hist.GetMean() + args.func_xmin * hist.GetRMS() # func_xmin is negative!
    fitmax = hist.GetMean() + args.func_xmax * hist.GetRMS()
    plot.GetXaxis().SetRangeUser(fitmin,fitmax)
    plot.SetStats(False)
    #canv.drawText(text=str(
    canv.cleanup(savedir+'/residual_'+cat+'_'+low+'m'+high,extList=['.png','.pdf'])

def log_indv_res(hist,gfunc,ffunc,x,cat):
    low = str(binning[x])
    high = str(binning[x+1])
    name = 'residual_'+cat+'_'+low+'m'+high
    lumberjack.setup_logger(name,savedir+'/'+name+'.log')
    logger = logging.getLogger(name)
    logger.info(low+' < m < '+high+', '+cat+', '+hist.GetName())
    logger.info('\n'+'*'*15+'\n')
    logger.info('Histogram Data')
    for dat in ['Entries','Mean','RMS']:
        logger.info(dat+' '+str(getattr(hist,'Get'+dat)()))
    logger.info('\n'+'*'*15+'\n')
    logger.info('Gaussian fit')
    for n in range(gfunc.GetNpar()):
        logger.info(str(n)+' '+str(gfunc.GetParName(n))+' '+str(gfunc.GetParameter(n))+' +/- '+str(gfunc.GetParError(n)))
    logger.info('Chi2/ndf = '+str(gfunc.GetChisquare())+' / '+str(gfunc.GetNDF()))
    logger.info('\n'+'*'*15+'\n')
    logger.info(args.res_func)
    for n in range(ffunc.GetNpar()):
        logger.info(str(n)+' '+str(ffunc.GetParName(n))+' '+str(ffunc.GetParameter(n))+' +/- '+str(ffunc.GetParError(n)))
    logger.info('Chi2/ndf = '+str(ffunc.GetChisquare())+' / '+str(ffunc.GetNDF()))
    logger.info('\n'+'*'*15+'\n')


for cat in categories:
    for x,low in enumerate(binning[:-1]):
        high = binning[x+1]
        fitmin = res_hists[cat][low].GetMean() + args.func_xmin * res_hists[cat][low].GetRMS() # func_xmin is negative!
        fitmax = res_hists[cat][low].GetMean() + args.func_xmax * res_hists[cat][low].GetRMS()
        # Gaussian function to initialize fit
        gfunc = R.TF1('gaus_'+str(low)+'_'+cat,'gaus',fitmin,fitmax)
        gfunc.SetParameters(0,res_hists[cat][low].GetMean(),res_hists[cat][low].GetRMS())
        gfunc.SetParNames('Constant','Mean','Sigma')
        res_hists[cat][low].Fit("gaus","M0R+")

        fit_name = 'resid_fit_'+str(low)+'_'+cat
        if args.res_func=='dscb':
            fit_funct = R.TF1(fit_name,R.DoubleSidedCrystalBall,fitmin,fitmax,7)
            fit_funct.SetParameters(res_hists[cat][low].GetEntries(),1.4,1.5,gfunc.GetParameter(1),gfunc.GetParameter(2),1.4,1.5)
            if args.year in [2017,2018]:
                fit_funct.SetParLimits(4,0,3.25*res_hists[cat][low].GetRMS()) # sigma
            else:
                fit_funct.SetParLimits(4,0,3.5*res_hists[cat][low].GetRMS()) # sigma
            fit_funct.SetParLimits(1,0.5,4.) # alphaL
            fit_funct.SetParLimits(5,0.5,5.) # alphaR
            fit_funct.SetParLimits(2,0.,25.) # nL
            fit_funct.SetParLimits(6,0.,25.) # nR
            fit_funct.SetParNames("Constant","AlphaL","nL","Mean","Sigma","AlphaR","nR")
        res_hists[cat][low].Fit(fit_name,'M0R+')
        
        plot_indv_res(res_hists[cat][low], fit_funct, x, cat)#, fit_name)
        log_indv_res(res_hists[cat][low],gfunc,fit_funct,x,cat)
        
        for p,par in enumerate(parNames[args.res_func]):
            pars[cat][par]['xlow'].append(float(low))
            pars[cat][par]['xhigh'].append(float(high))
            val = float(fit_funct.GetParameter(p))
            pars[cat][par]['val'].append(val)
            perr = float(fit_funct.GetParError(p))
            serr = (args.syst_err-1.0)*val
            err = math.sqrt(pow(perr,2)+pow(serr,2))
            pars[cat][par]['err'].append(err)

        pars[cat]['chi2']['xlow'].append(float(low))
        pars[cat]['chi2']['xhigh'].append(float(high))
        pars[cat]['chi2']['val'].append(float(fit_funct.GetChisquare()))
        pars[cat]['chi2']['err'].append(0.)

lims = {
        'Sigma':[0,0.1],
        'Mean':[-0.015,0],
        'nL':[0,4],
        'nR':[-5,55],
        'AlphaL':[0,3],
        'AlphaR':[0,3],
        'Constant':[0,3500],
        'chi2':[0,150],
        }

def log_full_res(graphs,fits):
    name = 'mass_Sigma'
    lumberjack.setup_logger(name,savedir+'/'+name+'.log')
    logger = logging.getLogger(name)
    logger.info('\n'+'*'*30+'\n')
    logger.info('Resolution Parametrization Results')
    for cat in categories:
        logger.info('\n'+'*'*15+'\n')
        logger.info(cat)
        for i in range(fits[cat].GetNpar()):
            logger.info(str(i)+' '+str(fits[cat].GetParName(i))+' '+str(fits[cat].GetParameter(i))+' +/- '+str(fits[cat].GetParError(i)))
        logger.info('Chi2/ndof = '+str(fits[cat].GetChisquare())+' / '+str(fits[cat].GetNDF()))
    logger.info('\n'+'*'*30+'\n')
    logger.info('Raw Resolution Data')
    for cat in categories:
        logger.info('\n'+'*'*15+'\n')
        logger.info(cat)
        x,y = R.Double(), R.Double()
        for i in range(graphs[cat].GetN()):
            graphs[cat].GetPoint(i,x,y)
            xerr = graphs[cat].GetErrorX(i)
            yerr = graphs[cat].GetErrorY(i)
            data = '{i} {x} {xerr} {y} {yerr}'.format(**locals())
            logger.info(data)
    logger.info('\n'+'*'*15+'\n')


legNames = {'bb':'BB','beee':'BE+EE'}
colors = {'bb':R.kRed,'beee':R.kGreen+1}
npoints = len(binning)
x = np.array([0.5*(binning[i]+binning[i+1]) for i in range(npoints-1)])
xerr = np.array([0.5*(binning[i+1]-binning[i]) for i in range(npoints-1)])
for p,par in enumerate(parNames[args.res_func]+['chi2']):
    y,yerr = {},{}
    plots,graphs = {},{}
    params = {}
    canv = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation Preliminary')
    for cat in categories:
        y[cat] = np.array(pars[cat][par]['val'])
        yerr[cat] = np.array(pars[cat][par]['err'])
        graphs[cat] = R.TGraphErrors(npoints,x,y[cat],xerr,yerr[cat])
        plots[cat] = Plotter.Plot(graphs[cat],legName=legNames[cat],legType='pe',option='pe')
        # Draw + options
        canv.addMainPlot(plots[cat])
        plots[cat].SetLineColor(colors[cat])
        plots[cat].SetMarkerColor(colors[cat])
    # Fit parametrization
    if par=='Sigma':
        for cat in categories:
            param_name = 'param_'+cat+'_'+par
            params[cat] = R.TF1(param_name,'pol4',120.0,6500.0)
            params[cat].SetParNames('A','B','C','D','E')
            for i in range(params[cat].GetNpar()):
                params[cat].ReleaseParameter(i)
                params[cat].SetParameter(i,0.)
            params[cat].SetParameters(0.0,3E-5,-1.E-8,2E-12,-1.5E-16)
            params[cat].SetParLimits(1,1E-6,1E-4)
            params[cat].SetParLimits(2,-1E-7,-1E-9)
            params[cat].SetLineColor(colors[cat])
            params[cat].SetLineWidth(1)
            graphs[cat].Fit(param_name,'M+')
        log_full_res(graphs,params)
    canv.firstPlot.setTitles(X='m(#mu^{+}#mu^{#font[122]{\55}}) [GeV]',Y='Dimuon Mass Resolution')
    canv.firstPlot.GetYaxis().SetRangeUser(*lims[par])
    canv.firstPlot.GetXaxis().SetRangeUser(120,6500)
    canv.mainPad.SetGrid()
    canv.Update()
    canv.cleanup(savedir+'/mass_'+par,extList=['.png','.pdf'])


