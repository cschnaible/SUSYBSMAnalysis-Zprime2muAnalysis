import ROOT as R
R.gROOT.SetBatch(True)
import numpy as np
import array, math
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples_chris import samples18, samples17
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools_chris import poisson_intervalize, divide_bin_width, clopper_pearson_poisson_means, cumulative_histogram
import argparse
parser = argparse.ArgumentParser()
#parser.add_argument('-f','--file',dest='datafile',default='data/old_datamc_20190326/ana_datamc_Run2018ABCD_inc.root')
parser.add_argument('-f','--file',dest='datafile',default='data/ana_datamc_Run2018ABCD.root')
parser.add_argument('-d','--tdir',default='our')
parser.add_argument('-w','--which',default='test',help='Where to save plots')
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
parser.add_argument('-dc','--datacut',default='',dest='datacut')
args = parser.parse_args()

years = [2017,2018]
info = {
        2016:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/mc/',
            'samples':samples16,
            'our':'Our2016MuonsPlusMuonsMinusNtuple',
        2017:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/mc/',
            'samples':samples17,
            'our':'Our2017MuonsPlusMuonsMinusNtuple',
            'ourpre':'Our2017MuPrescaledMuonsPlusMuonsMinusNtuple',
            },
        2018:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/mc/',
            'samples':samples18,
            'our':'Our2018MuonsOppSignNtuple',
            'ourpre':'Our2018MuPrescaledMuonsOppSignNtuple',
            },
        }

if args.logx: 
    bins = np.logspace(np.log10(float(args.xmin)),np.log10(float(args.xmax)),int(args.nbinsx)+1)
else: 
    bins = array.array('d',[args.xmin + i*(args.xmax-args.xmin)/args.nbinsx for i in range(0,args.nbinsx+1)])
hist = R.TH1D('h','',int(args.nbinsx),bins)
hname = hist.GetName()

def get_sum_weights(f):
    weights = getattr(f,'EventCounter').Get('weights')
    return weights.GetBinContent(2)-weights.GetBinContent(1)

toDraw = (args.y+':' if args.y!='' else '')+args.x

print toDraw,args.cut
cut = '('+args.cut+')' if args.cut!='' else '(1.)'

# Reweight to NNPDF3.0 taken from s4
# https://indico.cern.ch/event/806789/contributions/3357762/attachments/1813726/2963454/ZToMuMuComp_Min_20190318_v1.pdf
toNNPDF30 = '({a} {b}*pow(gen_dil_mass,1) {c}*pow(gen_dil_mass,2) {d}*pow(gen_dil_mass,3) {e}*pow(gen_dil_mass,4) {f}*pow(gen_dil_mass,5))'.format(a='0.9292',b='+ 5.486E-5',c='+ 6.572E-9',d='- 1.142E-11',e='+ 4.876E-15',f='- 4.117E-19')


hists = {year:{sample.name:{} for sample in info[year]['samples']} for year in years}
nevents = {year:{sample.name:{} for sample in info[year]['samples']} for year in years}
for year in years:
    for i,sample in enumerate(info[year]['samples']):
        print sample.name
        f = R.TFile(info[year]['path']+'ana_datamc_'+sample.name+'.root')
        hmcs = hist.Clone('h'+sample.name)
        t = f.Get(info[year][args.tdir]+'/t')
        mccutweight = cut
        if args.nnpdf30 and 'dy' not in sample.name:
            mccutweight += '*1.'
        elif args.nnpdf30 and 'dy' in sample.name and 'to' in sample.name:
            mccutweight += '*'+toNNPDF30
        else:
            mccutweight += '*1.'
        mccutweight += "*genWeight"
        nevents[year][sample.name] = get_sum_weights(f)
        drawstring = toDraw+'>> h'+sample.name
        t.Draw(drawstring,mccutweight,args.style)
        hmcs.SetDirectory(0)
        print mccutweight
        print hmcs.Integral(), hmcs.GetEntries()
        hists[year][sample.name]=hmcs
        hists[year][sample.name].SetDirectory(0)
        f.Close()

print '\n','*'*15,'\n'

def mc_stuff(name):
    if 'Wjets' in name:
        return 'jets',R.kOrange+1
    if 'dy' in name and 'to' in name:
        return '#gamma/Z #rightarrow #mu^{+}#mu^{-}',R.kAzure+1
    if 'dyInclusive' in name:
        return '#gamma/Z #rightarrow #tau^{+}#tau^{-}',R.kBlue+1
    if 'ttbar' in name:
        return 't#bar{t}',R.kRed-4
    if 'tW' in name or 'tbarW' in name:
        return 'single top', R.kViolet+1
    if name in ['WW','WZ','ZZ']:
        return 'diboson', R.kGreen+1
    if 'DYJetsToLL_HT' in name:
        return '#gamma/Z #rightarrow #mu^{+}#mu^{-}',R.kAzure+1
    if '2017' in name:
        return '2017 Simulation',R.kBlue+1
    if '2018' in name:
        return '2018 Simulation',R.kOrange+1

mc_int = 0.
hmc = {year:hist.Clone('hmc_'+str(year)) for year in years}
for year in years:
    print year
    for sample in info[year]['samples']:
        scale_by = sample.cross_section * args.lumi / float(nevents[year][sample.name])
        hists[year][sample.name].Scale(scale_by)
        print sample.name,hists[year][sample.name].Integral()
        mc_int += hists[year][sample.name].Integral()
        hmc[year].Add(hists[year][sample.name])
    print 

def pretty(arg):
    ret = {
        'vertex_m':'m(#mu^{+}#mu^{-}) [GeV]',
        'cos_angle':'cos(#alpha)',
        'dil_pt':'p_{T}(#mu^{+}#mu^{-}) [GeV]',
        'gen_dil_pt':'GEN p_{T}(#mu^{+}#mu^{-}) [GeV]',
        'gen_dil_rap':'GEN y(#mu^{+}#mu^{-})',
        'lep_pt':'p_{T}(#mu) [GeV]',
        'n_dils':'N(#mu^{+}#mu^{-}) passing selection',
        'nvertices':'N(primary vertices)',
        'lep_Mu27_triggerMatchPt':'Mu27 trigger match p_{T}(#mu) [GeV]',
        }
    for val in ret.keys():
        if val in arg: return ret[val]

mc_2017_raw = hmc[2017].Integral()
mc_2018_raw = hmc[2018].Integral()
print '\n','*'*30,'\n'
print args.name
print '\n','*'*15,'\n'
print 'raw',mc_2017_raw,mc_2018_raw
#scale = info[2018][args.tdir]['lumi']/info[2017][args.tdir]['lumi']
#scale *= (1./(info[2018][args.tdir]['pre']/info[2017][args.tdir]['pre']))
#scale = 60434./42001.
#scale *= 1./(487.254/237.798)
#hmc[2017].Scale(scale)
#hmc[2018].Scale(1./nzpeak[2018])
#hmc[2017].Scale(1./nzpeak[2017])
mc_2017 = hmc[2017].Integral()
mc_2018 = hmc[2018].Integral()
print '\n','*'*15,'\n'
r,l,h = clopper_pearson_poisson_means(mc_2017,mc_2018)
print mc_2017, mc_2018, r, (h-r + r-l)/2
tau = 1.0 # data/mc 'should' be one
p_bi = R.TMath.BetaIncomplete(1./(1+tau),mc_2017,int(mc_2018)+1)
z_bi = math.sqrt(2)*R.TMath.ErfInverse(1-2*p_bi)
print 'P-value',p_bi,'Z-value',z_bi
print '\n','*'*30,'\n'

for year in years:
    if args.bin_width:
        divide_bin_width(hmc[year])
    elif args.cumulative:
        hmc[year] = cumulative_histogram(hmc[year])

lumi = '{:5.2f}'.format(args.lumi/1000.)
canvas = Plotter.Canvas(lumi='{lumi}'.format(lumi=lumi)+' fb^{-1} (13 TeV)',extra='Preliminary',ratioFactor=1./3,logy=args.logy)
pmc17 =   Plotter.Plot(hmc[2017],  legName='2017 simulation',legType='l',option='hist')
pmc18 =   Plotter.Plot(hmc[2018],  legName='2018 simulation',legType='l',option='hist')
canvas.addMainPlot(pmc17)
canvas.addMainPlot(pmc18)
pmc17.SetLineColor(mc_stuff('2017')[1])
pmc18.SetLineColor(mc_stuff('2018')[1])
canvas.makeLegend(pos='tr')
xtit = pretty(args.x)
canvas.firstPlot.setTitles(X=xtit,Y='Events'+(' / GeV' if args.bin_width else ''))
canvas.addRatioPlot(hmc[2017],hmc[2018],ytit='2017 / 2018',xtit=xtit,plusminus=0.25)
hmax = max([hmc[2017].GetMaximum(),hmc[2018].GetMaximum()])
hmin = min([hmc[2017].GetMinimum(),hmc[2018].GetMinimum()])
if hmin==0. and args.logy: hmin=0.1
hmin = hmin/10 if args.logy else 0.
hmax = hmax*10 if args.logy else hmax*1.2
pmc17.GetXaxis().SetTitleSize(0)
pmc17.GetXaxis().SetLabelSize(0)
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
canvas.cleanup(args.which+'/'+args.name+'.png')
f.Close()

