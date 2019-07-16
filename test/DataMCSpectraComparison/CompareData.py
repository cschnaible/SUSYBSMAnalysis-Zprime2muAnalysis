import ROOT as R
R.gROOT.SetBatch(True)
import numpy as np
import array, math
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples# samples18, samples17, samples16
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools_chris import poisson_intervalize, divide_bin_width, clopper_pearson_poisson_means, cumulative_histogram
import argparse
parser = argparse.ArgumentParser()
#parser.add_argument('-f','--file',dest='datafile',default='data/old_datamc_20190326/ana_datamc_Run2018ABCD_inc.root')
parser.add_argument('-f','--file',dest='datafile',default='data/ana_datamc_Run2018ABCD.root')
parser.add_argument('-d','--tdir',default='our')
parser.add_argument('-w','--where',default='www_compare_data',help='Where to store plots')
parser.add_argument('-x',default='vertex_m',help='Quantity to draw on X axis')
parser.add_argument('-y',default='',help='Quantity to draw on Y axis')
parser.add_argument('-c','--cut',default='')
parser.add_argument('-s','--style',default='')
parser.add_argument('-ly','--logy',action='store_true',default=False)
parser.add_argument('-lx','--logx',action='store_true',default=False)
parser.add_argument('-n','--name',default='h')
parser.add_argument('-nbx','--nbinsx',default=None,type=int)
parser.add_argument('-nby','--nbinsy',default=None,type=int)
parser.add_argument('-2D','--2D',dest='do2D',action='store_true')
parser.add_argument('--xmin',default=None,type=float)
parser.add_argument('--xmax',default=None,type=float)
parser.add_argument('--ymin',default=None,type=float)
parser.add_argument('--ymax',default=None,type=float)
parser.add_argument('--lumi',default=61310,type=float)
parser.add_argument('-bw','--bin-width',dest='bin_width',action='store_true')
parser.add_argument('-do30','--nnpdf30',dest='nnpdf30',action='store_true')
parser.add_argument('--Z0',default=1.0,type=float)
parser.add_argument('--do-stack',dest='do_stack',action='store_true')
parser.add_argument('-t','--trig',default='Mu50')
parser.add_argument('--fullcut',action='store_true')
parser.add_argument('-cum','--cumulative',action='store_true')
parser.add_argument('-dyht','--dyhtbinned',action='store_true')
parser.add_argument('-p','--prescale',dest='prescale',type=float,default=1.)
parser.add_argument('--norm',default='lumi',help='How to normalize data')
args = parser.parse_args()

years = [2016,2017,2018]
info = {
        2016:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/data/',
            'file':'ana_datamc_Run2016_17Jul2018.root',
            'our':{
                'dir':'Our2016MuonsOppSignNtuple',
                'pre':1.,
                'lumi':36294.593964906585693,
                },
            'ourcommonpre':{
                'dir':'Our2016MuPrescaledCommonMuonsOppSignNtuple',
                'pre':500.,
                'lumi':36285.0595135,
                },
            'ourpre':{
                'dir':'Our2016MuPrescaledMuonsOppSignNtuple',
                'pre':146.323326629,
                'lumi':36285.0595135,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/mc/',
            'mc':samples[2016],
            },
        2017:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/data/',
            'file':'ana_datamc_Run2017_31Mar2018.root',
            'our':{
                'dir':'Our2018MuonsOppSignNtuple',
                'pre':1.,
                'lumi':42079.880396,
                },
            'ourcommonpre':{
                'dir':'Our2018MuPrescaledCommonMuonsOppSignNtuple',
                'pre':561.,
                'lumi':42070.654731,
                },
            'ourpre':{
                'dir':'Our2018MuPrescaledMuonsOppSignNtuple',
                'pre':236.085072878,
                'lumi':42070.654731,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/mc/',
            'mc':samples[2017],
            },
        2018:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/data/',
            'file':'ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root',
            'our':{
                'dir':'Our2018MuonsOppSignNtuple',
                'pre':1.,
                'lumi':61298.7752317,
                #'lumi':61302.3918373,
                },
            'ourcommonpre':{
                'dir':'Our2018MuPrescaledMuonsOppSignNtuple',
                'pre':500.,
                'lumi':61291.8425445,
                #'lumi':61302.3918373,
                },
            'ourpre':{
                'dir':'Our2018MuPrescaledNoCommonMuonsOppSignNtuple',
                'pre':486.949643091,
                'lumi':61291.8425445,
                #'lumi':61302.3918373,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/mc/',
            'mc':samples[2018],
            },
        }

if args.logx: 
    bins = np.logspace(np.log10(float(args.xmin)),np.log10(float(args.xmax)),int(args.nbinsx)+1)
else: 
    bins = array.array('d',[args.xmin + i*(args.xmax-args.xmin)/args.nbinsx for i in range(0,args.nbinsx+1)])
hist = R.TH1D('h','',int(args.nbinsx),bins)
hname = hist.GetName()

toDraw = (args.y+':' if args.y!='' else '')+args.x


hists = {year:hist.Clone('h_'+str(year)) for year in years}
nevents = {year:{} for year in years}
nzpeak = {year:{} for year in years}
for year in years:
    # Data
    print 'Data'
    data_cut = '('+args.cut+')' if args.cut!='' else '1.'
    #data_cut+=('*Mu27_prescale' if args.tdir=='ourpre' else '')
    #if args.dir=='Our2018MuPrescaledNoCommonMuonsOppSignNtuple':
    #    f = R.TFile('data/ana_datamc_Run2018ABCD_nocommon_inc.root')
    #else:
    #    f = R.TFile(args.datafile)
    f = R.TFile(info[year]['path']+info[year]['file'])
    t = f.Get(info[year][args.tdir]['dir']+'/t')
    hdata = hist.Clone('hdata')
    t.Draw(toDraw+'>>hdata',data_cut,args.style)
    hists[year] = hdata
    hists[year].SetDirectory(0)
    hists[year].SetStats(0)
    nevents[year] = hdata.Integral()
    nzpeak[year] = t.GetEntries('vertex_m > 60 && vertex_m < 120')# && '+data_cut)


raw_counts = {year:hists[year].Integral() for year in years}
print '\n','*'*30,'\n'
print args.name
print '\n','*'*15,'\n'
for year in years:
    print 'raw',year,raw_counts[year]
if args.norm=='lumi':
    scale17to18 = info[2018][args.tdir]['lumi']/info[2017][args.tdir]['lumi']
    scale17to18 *= (1./(info[2018][args.tdir]['pre']/info[2017][args.tdir]['pre']))
    hists[2017].Scale(scale17to18)
    scale16to18 = info[2018][args.tdir]['lumi']/info[2016][args.tdir]['lumi']
    scale16to18 *= (1./(info[2018][args.tdir]['pre']/info[2016][args.tdir]['pre']))
    hists[2016].Scale(scale16to18)
elif args.norm=='zpeak':
    hists[2018].Scale(1./nzpeak[2018])
    hists[2017].Scale(1./nzpeak[2017])
    hists[2016].Scale(1./nzpeak[2016])
else:
    raise ValueError(args.norm,'not a valid normalization method')
counts = {year:hists[year].Integral() for year in years}
print '\n','*'*15,'\n'
print 'Ratio 2017/2018'
r,l,h = clopper_pearson_poisson_means(counts[2017],counts[2018])
print counts[2017], counts[2018], r, (h-r + r-l)/2
tau = 1.0 # data/mc 'should' be one
p_bi = R.TMath.BetaIncomplete(1./(1+tau),counts[2017],int(counts[2018])+1)
z_bi = math.sqrt(2)*R.TMath.ErfInverse(1-2*p_bi)
print 'P-value',p_bi,'Z-value',z_bi
print '\n','*'*30,'\n'
print 'Ratio 2016/2018'
r,l,h = clopper_pearson_poisson_means(counts[2016],counts[2018])
print counts[2016], counts[2018], r, (h-r + r-l)/2
tau = 1.0 # data/mc 'should' be one
p_bi = R.TMath.BetaIncomplete(1./(1+tau),counts[2016],int(counts[2018])+1)
z_bi = math.sqrt(2)*R.TMath.ErfInverse(1-2*p_bi)
print 'P-value',p_bi,'Z-value',z_bi
print '\n','*'*30,'\n'

def pretty(arg):
    ret = {
        'vertex_m':'m(#mu^{+}#mu^{-}) [GeV]',
        'cos_angle':'cos(#alpha)',
        'dil_pt':'p_{T}(#mu^{+}#mu^{-}) [GeV]',
        'lep_pt':'p_{T}(#mu) [GeV]',
        'n_dils':'N(#mu^{+}#mu^{-}) passing selection',
        'nvertices':'N(primary vertices)',
        'lep_Mu27_triggerMatchPt':'Mu27 trigger match p_{T}(#mu) [GeV]',
        }
    for val in ret.keys():
        if val in arg: return ret[val]

def nice(name):
    if '2016' in name:
        return '2016 Data',R.kGreen+1
    if '2017' in name:
        return '2017 Data',R.kBlue+1
    if '2018' in name:
        return '2018 Data',R.kOrange+1

for year in years:
    if args.bin_width:
        divide_bin_width(hists[year])
    elif args.cumulative:
        hists[year] = cumulative_histogram(hists[year])

lumi = '{:5.2f}'.format(args.lumi/1000.)
canvas = Plotter.Canvas(lumi='{lumi}'.format(lumi=lumi)+' fb^{-1} (13 TeV)',extra='Preliminary',ratioFactor=1./3,logy=args.logy)
pdata16 =   Plotter.Plot(hists[2016],  legName='2016 Data',legType='l',option='hist')
pdata17 =   Plotter.Plot(hists[2017],  legName='2017 Data',legType='l',option='hist')
pdata18 =   Plotter.Plot(hists[2018],  legName='2018 Data',legType='l',option='hist')
canvas.addMainPlot(pdata16)
canvas.addMainPlot(pdata17)
canvas.addMainPlot(pdata18)
pdata16.SetLineColor(nice('2016')[1])
pdata17.SetLineColor(nice('2017')[1])
pdata18.SetLineColor(nice('2018')[1])
canvas.makeLegend(pos='tr')
xtit = pretty(args.x)
canvas.firstPlot.setTitles(X=xtit,Y='Events'+(' / GeV' if args.bin_width else ''))
canvas.addRatioPlot(hists[2017],hists[2018],ytit='201X / 2018',xtit=xtit,plusminus=0.5,color=nice('2017')[1])
canvas.addRatioPlot(hists[2016],hists[2018],ytit='201X / 2018',xtit=xtit,plusminus=0.5,color=nice('2016')[1])
hmax = max([hists[year].GetMaximum() for year in years])
hmin = min([hists[year].GetMinimum() for year in years])
if hmin==0. and args.logy: hmin=1E-1
hmin = hmin/10 if args.logy else 0.
hmax = hmax*10 if args.logy else hmax*1.2
pdata17.GetXaxis().SetTitleSize(0)
pdata17.GetXaxis().SetLabelSize(0)
if args.do_stack:
    canvas.firstPlot.SetMinimum(hmin)
    canvas.firstPlot.SetMaximum(hmax)
else:
    canvas.firstPlot.GetYaxis().SetRangeUser(hmin,hmax)
if args.logx: 
    canvas.mainPad.SetLogx()
    canvas.ratPad.SetLogx()
    canvas.ratList[0].GetXaxis().SetMoreLogLabels(True)
    canvas.ratList[0].GetXaxis().SetNoExponent(True)
canvas.Update()
canvas.cleanup(args.where+'/'+args.name+'.png')
f.Close()

