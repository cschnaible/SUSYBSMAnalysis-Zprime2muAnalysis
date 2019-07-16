import ROOT as R
R.gROOT.SetBatch(True)
import numpy as np
import array, math, logging
import SUSYBSMAnalysis.Zprime2muAnalysis.lumberjack as lumberjack
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples# samples18, samples17, samples16
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools_chris import poisson_intervalize, clopper_pearson_poisson_means, cumulative_histogram, move_overflow_into_last_bin, binomial_divide, poisson_intervalize_ratio, clopper_pearson
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d','--tdir',default='our')
parser.add_argument('-w','--where',default='www_compare_datamc',help='Where to store plots')
parser.add_argument('-x',default='vertex_m',help='Quantity to draw on X axis')
parser.add_argument('-y','--year',default=2018,help='Which year(s) to compare to MC')
parser.add_argument('-c','--category',default='all',help='Analysis category: all, bb, beee, ee')
parser.add_argument('-s','--selection',default='vertex_m>60',help='Selection to apply in addition to Z-peak mass window')
parser.add_argument('-lx','--logx',action='store_true',default=False)
parser.add_argument('-ly','--logy',action='store_true',default=False)
parser.add_argument('-n','--name',default='h')
parser.add_argument('-nbx','--nbinsx',default=None,type=int)
parser.add_argument('--xmin',default=None,type=float)
parser.add_argument('--xmax',default=None,type=float)
args = parser.parse_args()
info = {
        2016:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/data/',
            #'file':'ana_datamc_Run2016_17Jul2018.root',
            'file':'ana_datamc_Run2016BCDEFG_23Sep2016_Run2016H_PromptReco.root',
            'lumi':36294.593964906585693,
            'ratioZ0':{'all':0.9727,'bb':0.9842,'beee':0.9610},
            'our':{
                'dir':'Our2016MuonsOppSignNtuple',
                'pre':1.,
                'FR':'mc_2016/jets_muons_2016.root',
                },
            'ourcommonpre':{
                'dir':'Our2016MuPrescaledCommonMuonsOppSignNtuple',
                'pre':320.,
                },
            'ourpre':{
                'dir':'Our2016MuPrescaledMuonsOppSignNtuple',
                'pre':146.323326629,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/mc/',
            'mc':samples[2016],
            },
        2017:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/data/',
            'file':'ana_datamc_Run2017_31Mar2018.root',
            #'file':'ana_datamc_Run2017BCDEF_20190416.root',
            'lumi':42079.880396,
            'ratioZ0':{'all':1.0282,'bb':1.0286,'beee':1.0278},
            'our':{
                'dir':'Our2018MuonsOppSignNtuple',
                'pre':1.,
                'FR':{
                    'all':'mc_2017/Data-total-jets-BB-BE-EE-pt53.root',
                    'bb':'mc_2017/Data-total-jets-BB-pt53.root',
                    'beee':'mc_2017/Data-total-jets-BEEE-pt53.root',
                    },
                },
            'ourcommonpre':{
                'dir':'Our2018MuPrescaledCommonMuonsOppSignNtuple', # 31Mar2018
                #'dir_data':'Our2017MuPrescaledMuonsPlusMuonsMinusNtuple', # BCDEF_20190416
                #'dir_MC':'Our2018MuPrescaledCommonMuonsOppSignNtuple', # 31Mar2018
                'pre':561.,
                },
            'ourpre':{
                'dir':'Our2018MuPrescaledMuonsOppSignNtuple',
                'pre':236.085072878,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/mc/',
            'mc':samples[2017],
            },
        2018:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/data/',
            'file':'ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root',
            'lumi':61298.775231718995,
            'ratioZ0':{'all':1.0062,'bb':1.0124,'beee':1.0017},
            'our':{
                'dir':'Our2018MuonsOppSignNtuple',
                'pre':1.,
                'FR':{
                    'all':'mc/Data2018-total-jets-BB-BE-EE-pt53.root',
                    'bb':'mc/Data2018-total-jets-BB-pt53.root',
                    'beee':'mc/Data2018-total-jets-BE-EE-pt53.root',
                    },
                },
            'ourcommonpre':{
                'dir':'Our2018MuPrescaledMuonsOppSignNtuple',
                'pre':500.,
                },
            'ourpre':{
                'dir':'Our2018MuPrescaledNoCommonMuonsOppSignNtuple',
                'pre':486.949643091,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/mc/',
            'mc':samples[2018],
            },
        }

cats = {
        'all':'(1.)',
        'bb':'(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)',
        'beee':'(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)',
        'ee':'(fabs(lep_eta[0])>1.2 && fabs(lep_eta[1])>1.2)',
        'b':'(fabs(lep_eta)<1.2)',
        'e':'(fabs(lep_eta)>1.2 && fabs(lep_eta)<2.4)',
        }

sel = cats[args.category]+' && '+args.selection
#cut = 'vertex_m>120 && (lep_Mu50_triggerMatchPt[0]<50 && lep_Mu50_triggerMatchPt[1]<50) && (lep_OldMu100_triggerMatchPt[0]>100 || lep_OldMu100_triggerMatchPt[1]>100 || lep_TkMu100_triggerMatchPt[0]>100 || lep_TkMu100_triggerMatchPt[1]>100)'
numallcut = sel
numoldcut = sel+' && (lep_Mu50_triggerMatchPt[0]>50 || lep_Mu50_triggerMatchPt[1]>50 || lep_OldMu100_triggerMatchPt[0]>100 || lep_OldMu100_triggerMatchPt[1]>100)'
numtkcut = sel+' && (lep_Mu50_triggerMatchPt[0]>50 || lep_Mu50_triggerMatchPt[1]>50 || lep_TkMu100_triggerMatchPt[0]>100 || lep_TkMu100_triggerMatchPt[1]>100)'
dencut = sel+' && (lep_Mu50_triggerMatchPt[0]>50 || lep_Mu50_triggerMatchPt[1]>50)'
sels = {
        'all':sel,
        'old':numoldcut,
        'tk':numtkcut,
        'den':dencut,
        }

if args.logx: 
    hbins = np.logspace(np.log10(float(args.xmin)),np.log10(float(args.xmax)),int(args.nbinsx)+1)
    xbins = np.logspace(np.log10(float(args.xmin)),np.log10(float(args.xmax)),int(args.nbinsx)+1)
else: 
    binlist = [args.xmin + i*(args.xmax-args.xmin)/args.nbinsx for i in range(0,args.nbinsx+1)]
    hbins = array.array('d',binlist)
    xbins = np.array(binlist)
hist = R.TH1D('h','',int(args.nbinsx),hbins)

f = R.TFile(info[args.year]['path']+'/'+info[args.year]['file'])
t = f.Get(info[args.year]['our']['dir']+'/t')

hists = {name:hist.Clone(name) for name in ['all','old','tk','den']}

for name in ['all','old','tk','den']:
    t.Draw('vertex_m>>'+name,sels[name],'pe')
    hists[name].SetDirectory(0)

f.Close()

for x in range(1,hists['den'].GetNbinsX()+1):
    print x,hists['den'].GetXaxis().GetBinLowEdge(x)
    den = hists['den'].GetBinContent(x)
    a = hists['all'].GetBinContent(x)
    t = hists['tk'].GetBinContent(x)
    o = hists['old'].GetBinContent(x)
    print den,a,t,o,'\n'

#rat_all = hall.Clone('rat')
#rat_all.Divide(hden)
#g_all = R.TGraphAsymmErrors(rat_all,hden,'pois')
#g_all,yall,eylall,eyhall = binomial_divide(rat_all,hden,confint=clopper_pearson_poisson_means,force_lt_1=False)
#g_all = poisson_intervalize_ratio(rat_all,hden,include_zero_bins=True)
#g_all = binomial_divide(rat_all,hden)

#rat_old = hold.Clone('rat')
#rat_old.Divide(hden)
#g_old = R.TGraphAsymmErrors(rat_old,hden,'pois')
#g_old,yold,eylold,eyhold = binomial_divide(rat_old,hden,confint=clopper_pearson_poisson_means,force_lt_1=False)
#g_old = poisson_intervalize_ratio(rat_old,hden,include_zero_bins=True)
#g_old = binomial_divide(rat_old,hden)

#rat_tk = htk.Clone('rat')
#rat_tk.Divide(hden)
#g_tk = R.TGraphAsymmErrors(rat_tk,hden,'pois')
#g_tk,ytk,eyltk,eyhtk = binomial_divide(rat_tk,hden,confint=clopper_pearson_poisson_means,force_lt_1=False)
#g_tk = poisson_intervalize_ratio(rat_tk,hden,include_zero_bins=True)
#g_tk = binomial_divide(rat_tk,hden)

#rat_all = hist.Clone('all')
#rat_old = hist.Clone('old')
#rat_tk  = hist.Clone('tk')

namelist = ['tk','old','all']

xlists = {name:[] for name in namelist}
exlists = {name:[] for name in namelist}
ylists = {name:[] for name in namelist}
eyhlists = {name:[] for name in namelist}
eyllists = {name:[] for name in namelist}
for i in range(1,hists['den'].GetNbinsX()+1):
    den = hists['den'].GetBinContent(i)
    xi = hists['den'].GetBinCenter(i)
    exi = 0.5*hists['den'].GetBinWidth(i)
    for name in namelist:
        c = hists[name].GetBinContent(i)
        p, eyl, eyh = clopper_pearson_poisson_means(c-den,den)
        ylists[name].append(p+1)
        eyllists[name].append(p-eyl)
        eyhlists[name].append(eyh-p)
        xlists[name].append(xi)
        exlists[name].append(exi)
        #print name,x,c,den,'inv',p,eyh,eyl,'rat',1./p,p-eyl,eyh-p

x = {name:np.array(xlists[name]) for name in namelist}
ex = {name:np.array(exlists[name]) for name in namelist}
y = {name:np.array(ylists[name]) for name in namelist}
eyh = {name:np.array(eyhlists[name]) for name in namelist}
eyl = {name:np.array(eyllists[name]) for name in namelist}
graphs = {name:R.TGraphAsymmErrors(len(x[name]),x[name],y[name],ex[name],ex[name],eyl[name],eyh[name]) for name in namelist}

legNames = {
        'all':'Mu50 || OldMu100 || TkMu100',
        'old':'Mu50 || OldMu100',
        'tk':'Mu50 || TkMu100',
        }
colors = {
        'all':R.kRed,
        'old':R.kGreen+1,
        'tk':R.kBlue,
        }

# make pretty
totLumi = info[args.year]['lumi']/1000.
lumi = '{:4.1f}'.format(totLumi)
canvas = Plotter.Canvas(extra='Preliminary',lumi=lumi+' fb^{-1} (13 TeV)',logx=args.logx)
plots = {name:Plotter.Plot(graphs[name],legName=legNames[name],legType='pe',option='pe') for name in namelist}
for name in namelist:
    canvas.addMainPlot(plots[name])
    plots[name].SetLineColor(colors[name])
    plots[name].SetMarkerColor(colors[name])
canvas.makeLegend(pos='tr')
canvas.legend.moveLegend(X=-0.4)

if args.logx: 
    canvas.firstPlot.GetXaxis().SetMoreLogLabels(True)
    canvas.firstPlot.GetXaxis().SetNoExponent(True)

canvas.firstPlot.GetYaxis().SetRangeUser(1,1.007)
canvas.firstPlot.GetYaxis().SetTitle('Ratio of trigger OR to Mu50')
canvas.firstPlot.GetXaxis().SetTitle('m(#mu^{+}#mu^{#font[122]{\55}}) [GeV]')
canvas.mainPad.SetLeftMargin(0.15)
canvas.firstPlot.GetYaxis().SetTitleOffset(1.25)
canvas.cleanup('www_misc/trigger_OR_ratio',extList=['.pdf','.png'])
