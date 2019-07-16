'''
Compare Data and DY MC
'''
import ROOT as R
R.gROOT.SetBatch(True)
import numpy as np
import array, math
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples18, samples17, samples16
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools_chris import poisson_intervalize, divide_bin_width, clopper_pearson_poisson_means, cumulative_histogram
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d','--tdir',default='our')
parser.add_argument('-w','--where',default='www_compare_data',help='Where to store plots')
parser.add_argument('-x',default='vertex_m',help='Quantity to draw on X axis')
parser.add_argument('-y','--year',default=2018,type=int,help='Which year(s) to compare to MC')
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
args = parser.parse_args()

dyList = ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy3500to4500','dy4500to6000','dy6000toInf']
allyears = [2016,2017,2018]
info = {
        2017:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/data/',
            'our':{
                'dir':'Our2018MuonsOppSignNtuple',
                'fn':'ana_datamc_Run2017BCDEF_20190416.root',
                'pre':1.,
                'lumi':41992.3386644,
                },
            'ourcommonpre':{
                'dir':'Our2018MuPrescaledCommonMuonsOppSignNtuple',
                'fn':'ana_datamc_Run2017BCDEF_20190416.root',
                'pre':561.,
                'lumi':41992.3386644,
                },
            'ourpre':{
                'dir':'Our2018MuPrescaledMuonsOppSignNtuple',
                'fn':'ana_datamc_Run2017BCDEF_nocommon_20190417.root',
                'pre':236.085072878,
                #'pre':224.504719239543,
                'lumi':42036.9393414,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/mc/',
            'samples':samples17,
            },
        2018:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/data/',
            'our':{
                'dir':'Our2018MuonsOppSignNtuple',
                'fn':'ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root',
                'pre':1.,
                'lumi':61302.3918373,
                },
            'ourcommonpre':{
                'dir':'Our2018MuPrescaledCommonMuonsOppSignNtuple',
                'fn':'ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root',
                'pre':500.,
                'lumi':61302.3918373,
                },
            'ourpre':{
                'dir':'Our2018MuPrescaledMuonsOppSignNtuple',
                'fn':'ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root',
                'pre':486.949643091,
                'lumi':61302.3918373/486.949643091,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/mc/',
            'samples':samples18,
            },
        2016:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/data/',
            'our':{
                'dir':'Our2016MuonsOppSignNtuple',
                'fn':'doesnotexist.root',
                'pre':1.,
                'lumi':61302.3918373,
                },
            'ourcommonpre':{
                'dir':'Our2016MuPrescaledCommonMuonsOppSignNtuple',
                'fn':'doesnotexist.root',
                'pre':500.,
                'lumi':61302.3918373,
                },
            'ourpre':{
                'dir':'Our2016MuPrescaledMuonsOppSignNtuple',
                'fn':'doesnotexist.root',
                'pre':486.949643091,
                'lumi':61302.3918373,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/mc/',
            'samples':samples16,
            }
        }

def get_sum_weights(f):
    weights = getattr(f,'EventCounter').Get('weights')
    return weights.GetBinContent(2)-weights.GetBinContent(1)
dyInfo = {year:{
    'dy50to120':{'lims':(  50,   120)},
    'dy120to200':{'lims':( 120,   200)},
    'dy200to400':{'lims':( 200,   400)},
    'dy400to800':{'lims':( 400,   800)},
    'dy800to1400':{'lims':( 800,  1400)},
    'dy1400to2300':{'lims':(1400,  2300)},
    'dy2300to3500':{'lims':(2300,  3500)},
    'dy3500to4500':{'lims':(3500,  4500)},
    'dy4500to6000':{'lims':(4500,  6000)},
    'dy6000toInf':{'lims':(6000, 10000)},
    } for year in allyears}
for year in allyears:
    for sample in info[year]['samples']:
        for dy in dyList:
            if dy!=sample.name: continue
            dyInfo[year][dy]['xs'] = sample.cross_section
            #if year==2016:
            #    dyInfo[year][dy]['nevents'] = sample.nevents
            #else:
            dyInfo[year][dy]['nevents'] = get_sum_weights(R.TFile(info[year]['mcpath']+'ana_datamc_'+dy+'.root'))

if args.logx: 
    bins = np.logspace(np.log10(float(args.xmin)),np.log10(float(args.xmax)),int(args.nbinsx)+1)
else: 
    bins = array.array('d',[args.xmin + i*(args.xmax-args.xmin)/args.nbinsx for i in range(0,args.nbinsx+1)])
hist = R.TH1D('h','',int(args.nbinsx),bins)

toDraw = args.x


# Make Data histograms
# Data
data_cut = '('+args.cut+')' if args.cut!='' else '1.'
f = R.TFile(info[args.year]['path']+info[args.year][args.tdir]['fn'])
t = f.Get(info[args.year][args.tdir]['dir']+'/t')
hdata = hist.Clone('hdata')
t.Draw(toDraw+'>>hdata',data_cut,args.style)
hdata.SetDirectory(0)
nevents = hdata.Integral()
#nzpeak = t.GetEntries('vertex_m > 60 && vertex_m < 120 && '+data_cut)

# Make DY histograms
#norms = {year:{dy:{} for dy in dyList} for year in allyears}
hists = {year:{dy:{} for dy in dyList} for year in allyears}
for year in allyears:
    for dy in dyList:
        dyFile = R.TFile(info[year]['mcpath']+'ana_datamc_'+dy+'.root')
        hname = str(year)+'_'+dy
        hdy = hist.Clone(hname)
        dyTree = dyFile.Get(info[year][args.tdir]['dir']+'/t')
        dyTree.Draw(toDraw+'>>'+hname,data_cut)
        hdy.SetDirectory(0)
        hists[year][dy] = hdy
        hists[year][dy].SetDirectory(0)
        #norms[year][dy] = get_sum_weights(dyFile)
        dyFile.Close()


# Combine DY histograms
hmc = {year:hist.Clone('hmc_'+str(year)) for year in allyears}
for year in allyears:
    for dy in dyList:
        scale_by = dyInfo[year][dy]['xs'] * args.lumi / float(dyInfo[year][dy]['nevents'])
        hists[year][dy].Scale(scale_by)
        hmc[year].Add(hists[year][dy])

# pretty stuff
mcPretty = {
        2016:['80X NNPDF3.0',R.kRed-4],
        2017:['94X NNPDF3.1',R.kViolet+1],
        2018:['102X NNPDF3.1',R.kAzure+1],
        }
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

# 
lumi = '{:5.2f}'.format(args.lumi/1000.)
canvas = Plotter.Canvas(lumi='{lumi}'.format(lumi=lumi)+' fb^{-1} (13 TeV)',extra='Preliminary',ratioFactor=1./3,logy=args.logy)
pmc = {year:Plotter.Plot(hmc[year],legName=mcPretty[year][0],legType='l',option='hist') for year in allyears}
for year in allyears:
    canvas.addMainPlot(pmc[year])
    pmc[year].SetLineColor(mcPretty[year][1])
pdata = Plotter.Plot(hdata,legName=str(args.year)+' Data',legType='pe',option='pe')
canvas.addMainPlot(pdata)
canvas.makeLegend(pos='tr')
canvas.legend.moveLegend(X=-0.1)
xtit = pretty(args.x)
canvas.firstPlot.setTitles(X=xtit,Y='Events'+(' / GeV' if args.bin_width else ''))
for year in allyears:
    canvas.addRatioPlot(hdata,hmc[year],ytit='Data / MC',xtit=xtit,plusminus=0.5,option='hist',color=mcPretty[year][1])
hmax = max([hmc[year].GetMaximum()]+[hdata.GetMaximum()])
hmin = min([hmc[year].GetMinimum()]+[hdata.GetMinimum()])
if hmin==0. and args.logy: hmin=0.1
hmin = hmin/10 if args.logy else 0.
hmax = hmax*10 if args.logy else hmax*1.2
canvas.firstPlot.GetYaxis().SetRangeUser(hmin,hmax)
if args.logx: 
    canvas.mainPad.SetLogx()
    canvas.ratPad.SetLogx()
    canvas.ratList[0].GetXaxis().SetMoreLogLabels(True)
    canvas.ratList[0].GetXaxis().SetNoExponent(True)
canvas.Update()
print args.where+'/'+args.name+'.png'
canvas.cleanup(args.where+'/'+args.name+'.png')
f.Close()

