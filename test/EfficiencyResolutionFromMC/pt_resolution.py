import ROOT as R
import os,sys,math,logging,pdb
import numpy as np
import SUSYBSMAnalysis.Zprime2muAnalysis.lumberjack as lumberjack
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples# samples18, samples17, samples16
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-w','--where',default='www_res',help='where to save output')
#parser.add_argument('--var' ,default='vertex_gen',help='which variable to compute resolution')
parser.add_argument('-t','--track',action='append',help='Which tracks to draw')
parser.add_argument('--xmin',default=0,type=float,help='Minimum variable value')
parser.add_argument('--xmax',default=3000,type=float,help='Maximum variable value')
parser.add_argument('--res-xmin',default=-1, type=float,help='minimum residual value for histogram')
parser.add_argument('--res-xmax',default= 1, type=float,help='maximum residual value for histogram')
parser.add_argument('--res-bins',default=400,type=int,help='width of residual histogram bins')
parser.add_argument('--res-func',default='dscb',help='residual fitting function')
parser.add_argument('--res-rebin',default=1,help='Rebin factor for residual histogram')
parser.add_argument('--func-xmin',default=-2.0,type=float,help='minimum residual value for fit, units in sigma of gaussian core fit')
parser.add_argument('--func-xmax',default= 1.3,  type=float,help='maximum residual value for fit, units in sigma of gaussian core fit')
#parser.add_argument('--par-func',default='pol5',help='Function to parametrize resolution fit results')
#parser.add_argument('--par-xmin',default=120,type=float,help='Minimum var value for resolution parametrization')
#parser.add_argument('--par-xmax',default=6000,type=float,help='Maximum var value for resolutin paraemetrization')
#parser.add_argument('-dy','--drell-yan',default='powheg',help='Which DY MC to use')
parser.add_argument('-y','--year',default=2018,type=int,help='Which MC year to do')
parser.add_argument('-d','--tdir',default='our',help='Which cutset to plot: our (pt>53 GeV) or ourZ (pt>30 GeV)')
parser.add_argument('-s','--selection',default='',help='Which cutset to plot: our (pt>53 GeV) or ourZ (pt>30 GeV)')
parser.add_argument('-c','--category',default='all',help='b: barrel (<1.2) or e: endcap (>1.2)')
parser.add_argument('-dy','--drell-yan',default='powheg',help='dont change this')
#parser.add_argument('--smear',default=0.0,type=float,help='Additional smearing to apply, e.g. 0.15 = 15% additional smearing')
#parser.add_argument('--syst-err',default=1.0,type=float,help='Systematic error for resolution')
args = parser.parse_args()

trackList = [t for t in args.track]
savedir = args.where+'/pt_'+str(args.year)
savedir += '_'+args.category
for t in trackList:
    savedir += '_'+t

os.system('mkdir -p '+savedir)
os.system('cp ~/public/index.php '+savedir)

R.gROOT.LoadMacro("cruijff.C+")
R.gROOT.LoadMacro('DoubleSidedCrystalBall.C+')
R.gROOT.LoadMacro('GaussExp.C+')

dyLists = {
    'powheg' : ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf'],
    }

cats = {
        'all':'(1.)',
        'bb':'(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)',
        'beee':'(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)',
        'ee':'(fabs(lep_eta[0])>1.2 && fabs(lep_eta[1])>1.2)',
        'b':'(fabs(gen_lep_eta)<=1.2)',
        'e':'(fabs(gen_lep_eta)>1.2)',
        }


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
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/mc/new/',
            'mc':samples[2018],
            },
        }

#binning = [50,100,200,400,600,800,1200,1600,2000,3000]
binning = [50,120,200,300,400,600,800,1000,1300,1600,2000,2500,3100]
#tmpbinning = np.logspace(np.log10(100),np.log10(3000),16)
#binning = [int(b) for b in tmpbinning]



nbinsx = int(args.xmax) - int(args.xmin)
hist = R.TH2D('hResVsPt','',nbinsx,args.xmin,args.xmax,int(args.res_bins),args.res_xmin,args.res_xmax)
hists = {dy:{track:{} for track in trackList} for dy in dyLists[args.drell_yan]}

var = {
#        'sa':'lep_sa_pt',
#        'tk':'lep_tk_pt',
#        'glb':'lep_glb_pt',
#        'tuneP':'lep_pt',
#        'picky':'lep_picky_pt',
#        'dyt':'lep_dyt_pt',
#        'tpfms':'lep_tpfms_pt',
        'sa':'lep_sa_p',
        'tk':'lep_tk_p',
        'glb':'lep_glb_p',
        'tuneP':'lep_p',
        'picky':'lep_picky_p',
        'dyt':'lep_dyt_p',
        'tpfms':'lep_tpfms_p',
        }

# Draw Histograms
for dy in dyLists[args.drell_yan]:
    print '*'*15
    print dy
    f = R.TFile(info[args.year]['mcpath']+'ana_datamc_'+dy+'.root')
    t = f.Get(info[args.year][args.tdir]+'/t')
    for track in trackList:
        #toDraw = '(1./'+var[track]+' - 1./gen_lep_pt) / (1./gen_lep_pt):gen_lep_pt'
        toDraw = '(1./'+var[track]+' - 1./gen_lep_p) / (1./gen_lep_p):gen_lep_p'
        hname = 'hResid_'+dy+'_'+args.category+'_'+track
        h = hist.Clone(hname)
        cuts = cats[args.category]+' && '+(args.selection if args.selection else '1.')
        print '-'*15
        print args.category 
        print cuts
        print toDraw
        t.Draw(toDraw+'>>'+hname,cuts,'')
        h.SetDirectory(0)
        hists[dy][track] = h
        hists[dy][track].SetDirectory(0)
    f.Close()

resid_hist = {track:hist.Clone('hResiduals_'+track) for track in trackList}
for track in trackList:
    for dy in dyLists[args.drell_yan]:
        resid_hist[track].Add(hists[dy][track])
    resid_hist[track].SetDirectory(0)


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
res_hists = {track:{low:{} for low in binning[:-1]} for track in trackList}
for track in trackList:
    for x,low in enumerate(binning[:-1]):
        res_hists[track][low] = R.TH1D()
        res_hists[track][low].SetDirectory(0)
        R.TH1.AddDirectory(R.kFALSE)    
        high = binning[x+1]
        xlow,xhigh = getBinRange(resid_hist[track],low,high)
        res_hists[track][low] = resid_hist[track].ProjectionY('hResid_'+track+'_'+str(low),xlow,xhigh)
        res_hists[track][low].Rebin(args.res_rebin)
        res_hists[track][low].SetDirectory(0)

parNames = {
        'dscb':["Constant","AlphaL","nL","Mean","Sigma","AlphaR","nR"],
        'cb':["Constant","Mean","Sigma","Alpha","n"],
        'gaus':['Constant','Mean','Sigma'],
        'cruijff':['Constant','Mean','Sigma','AlphaL','AlphaR'],
        'gausexp':['Constant','Mean','Sigma','AlphaL','AlphaR'],
        }

pars = {track:{par:{info:[] for info in ['xlow','xhigh','val','err']} for par in parNames[args.res_func]+['chi2']} for track in trackList}

def plot_indv_res(hist,fit,x,track):
    low = str(binning[x])
    high = str(binning[x+1])
    canv = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation Preliminary')
    plot = Plotter.Plot(hist,option='pe')
    canv.addMainPlot(plot)
    fit.SetLineWidth(2)
    fit.SetLineColor(R.kBlue)
    fit.Draw("same")
    plot.setTitles(X='(\kappa_{RECO} - \kappa_{GEN}) / \kappa_{GEN}',Y='Entries/bin')
    plot.scaleTitles(0.75)
    plot.scaleLabels(0.75)
    #fitmin = fit.GetMinimumX()
    #fitmax = fit.GetMaximumX()
    fitmin = hist.GetMean() + args.func_xmin * hist.GetRMS() # func_xmin is negative!
    fitmax = hist.GetMean() + args.func_xmax * hist.GetRMS()
    plot.GetXaxis().SetRangeUser(fitmin,fitmax)
    plot.SetStats(False)
    #canv.drawText(text=str(
    canv.cleanup(savedir+'/residual_'+track+'_'+args.category+'_'+low+'pt'+high,extList=['.png','.pdf'])

def log_indv_res(hist,gfunc,ffunc,x,track):
    low = str(binning[x])
    high = str(binning[x+1])
    name = 'residual_'+track+'_'+args.category+'_'+low+'pt'+high
    lumberjack.setup_logger(name,savedir+'/'+name+'.log')
    logger = logging.getLogger(name)
    logger.info(low+' < m < '+high+', '+track+', '+hist.GetName())
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


for track in trackList:
    for x,low in enumerate(binning[:-1]):
        high = binning[x+1]
        fitmin = res_hists[track][low].GetMean() + args.func_xmin * res_hists[track][low].GetRMS() # func_xmin is negative!
        fitmax = res_hists[track][low].GetMean() + args.func_xmax * res_hists[track][low].GetRMS()
        # Gaussian function to initialize fit
        init_name = 'gaus_'+str(low)+'_'+track
        gfunc = R.TF1(init_name,'gaus',fitmin,fitmax)
        gfunc.SetParameters(0,res_hists[track][low].GetMean(),res_hists[track][low].GetRMS())
        gfunc.SetParNames('Constant','Mean','Sigma')
        res_hists[track][low].Fit(init_name,"M0R+")

        fit_name = 'resid_fit_'+str(low)+'_'+track
        if args.res_func=='dscb':
            fit_funct = R.TF1(fit_name,R.DoubleSidedCrystalBall,fitmin,fitmax,7)
            #fit_funct.SetParameters(res_hists[track][low].GetEntries(),1.4,1.0,gfunc.GetParameter(1),gfunc.GetParameter(2),1.4,1.0)
            fit_funct.SetParameters(res_hists[track][low].GetEntries(),1.4,1.0,res_hists[track][low].GetMean(),res_hists[track][low].GetRMS(),1.4,1.0)
            if args.year in [2017,2018]:
                fit_funct.SetParLimits(4,0,3.25*res_hists[track][low].GetRMS()) # sigma
            else:
                fit_funct.SetParLimits(4,0,3.5*res_hists[track][low].GetRMS()) # sigma
            fit_funct.SetParLimits(1,0.05,5.) # alphaL
            fit_funct.SetParLimits(5,0.05,5.) # alphaR
            fit_funct.SetParLimits(2,10.,25.) # nL
            fit_funct.SetParLimits(6,10.,25.) # nR
            fit_funct.SetParNames("Constant","AlphaL","nL","Mean","Sigma","AlphaR","nR")
        elif args.res_func=='gaus':
            #fit_funct = R.TF1(fit_name,'gaus',fitmin,fitmax)
            fit_funct = R.TF1(fit_name,'gaus',
                    #fitmin,
                    #fitmax)
                    gfunc.GetParameter(1)+args.func_xmin*gfunc.GetParameter(2),
                    gfunc.GetParameter(1)+args.func_xmax*gfunc.GetParameter(2))
            #fit_funct.SetParameters(0,gfunc.GetParameter(1),gfunc.GetParameter(2))
            fit_funct.SetParameters(0,res_hists[track][low].GetMean(),res_hists[track][low].GetRMS())

        res_hists[track][low].Fit(fit_name,'M0R+')
        
        plot_indv_res(res_hists[track][low], fit_funct, x, track)#, fit_name)
        log_indv_res(res_hists[track][low],gfunc,fit_funct,x,track)
        
        for p,par in enumerate(parNames[args.res_func]):
            pars[track][par]['xlow'].append(float(low))
            pars[track][par]['xhigh'].append(float(high))
            val = float(fit_funct.GetParameter(p))
            pars[track][par]['val'].append(val)
            perr = float(fit_funct.GetParError(p))
            serr = 0.# (args.syst_err-1.0)*val
            err = math.sqrt(pow(perr,2)+pow(serr,2))
            pars[track][par]['err'].append(err)

        pars[track]['chi2']['xlow'].append(float(low))
        pars[track]['chi2']['xhigh'].append(float(high))
        pars[track]['chi2']['val'].append(float(fit_funct.GetChisquare()))
        pars[track]['chi2']['err'].append(0.)

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
    name = 'pt_Sigma'
    lumberjack.setup_logger(name,savedir+'/'+name+'.log')
    logger = logging.getLogger(name)
    logger.info('\n'+'*'*30+'\n')
    logger.info('Resolution Parametrization Results')
    for track in trackList:
        logger.info('\n'+'*'*15+'\n')
        logger.info(track)
        for i in range(fits[track].GetNpar()):
            logger.info(str(i)+' '+str(fits[track].GetParName(i))+' '+str(fits[track].GetParameter(i))+' +/- '+str(fits[track].GetParError(i)))
        logger.info('Chi2/ndof = '+str(fits[track].GetChisquare())+' / '+str(fits[track].GetNDF()))
    logger.info('\n'+'*'*30+'\n')
    logger.info('Raw Resolution Data')
    for track in trackList:
        logger.info('\n'+'*'*15+'\n')
        logger.info(track)
        x,y = R.Double(), R.Double()
        for i in range(graphs[track].GetN()):
            graphs[track].GetPoint(i,x,y)
            xerr = graphs[track].GetErrorX(i)
            yerr = graphs[track].GetErrorY(i)
            data = '{i} {x} {xerr} {y} {yerr}'.format(**locals())
            logger.info(data)
    logger.info('\n'+'*'*15+'\n')


#legNames = {'bb':'BB','beee':'BE+EE'}
#colors = {'bb':R.kRed,'beee':R.kGreen+1}
legNames = {
        'tk':'Tracker Tracks',
        'glb':'Global Tracks',
        'sa':'Stand-Alone Tracks',
        'picky':'Picky Tracks',
        'dyt':'DYT Tracks',
        'tpfms':'TPFMS Tracks',
        'tuneP':'TuneP Tracks',
        }
colors = {
        'tk':R.kRed-4,
        'glb':R.kGreen-3,
        'sa':R.kViolet+1,
        'picky':R.kBlue-4,
        'dyt':R.kOrange+1,
        'tpfms':R.kMagenta+1,
        'tuneP':R.kBlack,
        }
npoints = len(binning)
x = np.array([0.5*(binning[i]+binning[i+1]) for i in range(npoints-1)])
xerr = np.array([0.5*(binning[i+1]-binning[i]) for i in range(npoints-1)])
for p,par in enumerate(parNames[args.res_func]+['chi2']):
    y,yerr = {},{}
    plots,graphs = {},{}
    params = {}
    canv = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation Preliminary')#,logy=True)#,logx=True)
    for track in trackList:
        y[track] = np.array(pars[track][par]['val'])
        yerr[track] = np.array(pars[track][par]['err'])
        graphs[track] = R.TGraphErrors(npoints,x,y[track],xerr,yerr[track])
        plots[track] = Plotter.Plot(graphs[track],legName=legNames[track],legType='pe',option='pe')
        # Draw + options
        canv.addMainPlot(plots[track])
        plots[track].SetLineColor(colors[track])
        plots[track].SetMarkerColor(colors[track])
    # Fit parametrization
#    if par=='Sigma':
#        for track in trackList:
#            param_name = 'param_'+track+'_'+par
#            params[track] = R.TF1(param_name,'pol4',120.0,6500.0)
#            params[track].SetParNames('A','B','C','D','E')
#            for i in range(params[track].GetNpar()):
#                params[track].ReleaseParameter(i)
#                params[track].SetParameter(i,0.)
#            params[track].SetParameters(0.0,3E-5,-1.E-8,2E-12,-1.5E-16)
#            params[track].SetParLimits(1,1E-6,1E-4)
#            params[track].SetParLimits(2,-1E-7,-1E-9)
#            params[track].SetLineColor(colors[track])
#            params[track].SetLineWidth(1)
#            graphs[track].Fit(param_name,'M+')
#        log_full_res(graphs,params)
    #canv.firstPlot.setTitles(X='m(#mu^{+}#mu^{#font[122]{\55}}) [GeV]',Y='Dimuon Mass Resolution')
    canv.firstPlot.setTitles(X='p [GeV]',Y='\Deltap/p')
    #canv.firstPlot.GetYaxis().SetRangeUser(*lims[par])
    canv.firstPlot.GetYaxis().SetRangeUser(0,0.125)
    canv.firstPlot.GetXaxis().SetRangeUser(binning[0],binning[-1])
    canv.makeLegend(pos='tl')
    #canv.legend.moveLegend(X=-0.2)
    #canv.mainPad.SetGrid()
    canv.firstPlot.GetXaxis().SetMoreLogLabels(True)
    canv.firstPlot.GetXaxis().SetNoExponent(True)
    canv.Update()
    canv.cleanup(savedir+'/pt_'+par,extList=['.png','.pdf'])


