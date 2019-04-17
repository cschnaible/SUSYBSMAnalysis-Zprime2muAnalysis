import ROOT as R
import numpy as np
import array, math
R.gROOT.SetBatch(True)
import argparse
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples_chris import samples
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools_chris import poisson_intervalize, divide_bin_width, clopper_pearson_poisson_means, cumulative_histogram
parser = argparse.ArgumentParser()
#parser.add_argument('-f','--file',dest='datafile',default='data/old_datamc_20190326/ana_datamc_Run2018ABCD_inc.root')
parser.add_argument('-f','--file',dest='datafile',default='data/ana_datamc_Run2018ABCD.root')
parser.add_argument('-d','--dir',default='Our2018MuonsOppSignNtuple')
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
args = parser.parse_args()

print args

if args.do2D:
    if args.logx: 
        binsx = np.logspace(np.log10(float(args.xmin)),np.log10(float(args.xmax)),int(args.nbinsx)+1)
    else: 
        binsx = array.array('d',[args.xmin + i*(args.xmax-args.xmin)/args.nbinsx for i in range(0,args.nbinsx+1)])
    if args.logy: 
        binsy = np.logspace(np.log10(float(args.ymin)),np.log10(float(args.ymax)),int(args.nbinsy)+1)
    else: 
        binsy = array.array('d',[args.ymin + i*(args.ymax-args.ymin)/args.nbinsy for i in range(0,args.nbinsy+1)])
    hist = R.TH2D('h','',int(args.nbinsx),binsx,int(args.nbinsy),binsy)
    hname = hist.GetName()
else:
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

# Reweight to NNPDF3.0 taken from s4
# https://indico.cern.ch/event/806789/contributions/3357762/attachments/1813726/2963454/ZToMuMuComp_Min_20190318_v1.pdf
toNNPDF30 = '({a} {b}*pow(gen_dil_mass,1) {c}*pow(gen_dil_mass,2) {d}*pow(gen_dil_mass,3) {e}*pow(gen_dil_mass,4) {f}*pow(gen_dil_mass,5))'.format(a='0.9292',b='+ 5.486E-5',c='+ 6.572E-9',d='- 1.142E-11',e='+ 4.876E-15',f='- 4.117E-19')

prescale = 1.
if args.dir=='Our2018MuPrescaledMuonsOppSignNtuple': prescale *= 1./500.
elif args.dir=='Our2018MuPrescaledNoCommonMuonsOppSignNtuple': prescale *= 1./461.1316
tdir = args.dir
mu_cut = \
    "lep_isGlobalMuon[X] && "						\
    "lep_isTrackerMuon[X] && "						\
    "abs(lep_dB[X]) < 0.2 && "						\
    "lep_glb_numberOfValidTrackerLayers[X] > 5 && " \
    "lep_glb_numberOfValidPixelHits[X] >= 1 && "    \
    "(lep_glb_numberOfValidMuonHits[X] > 0"         \
    " || lep_tuneP_numberOfValidMuonHits[X] > 0) && "  \
    "lep_pt_err[X] / lep_pt[X] < 0.3 && " 			\
    "lep_sumPt[X] / lep_tk_pt[X] < 0.1 && "         \
    "(lep_numberOfMatchedStations[X] > 1"       \
    " || (lep_numberOfMatchedStations[X]==1"       \
    "  && (lep_expectedNnumberOfMatchedStations[X]==1"\
    "   || !(lep_stationMask[X]==1 || lep_stationMask[X]==16)"\
    "   || lep_numberOfMatchedRPCLayers[X]>2)))"
mu_cut_0 = mu_cut.replace('X','0')
mu_cut_1 = mu_cut.replace('X','1')
trigger_match_Mu27 = '(lep_Mu27_triggerMatchPt[0]>27 || lep_Mu27_triggerMatchPt[1]>27)'
trigger_match_Mu50 = '(lep_Mu50_triggerMatchPt[0]>50 || lep_Mu50_triggerMatchPt[1]>50)'
trigger_match_OldMu100 = '(lep_OldMu100_triggerMatchPt[0]>100 || lep_OldMu100_triggerMatchPt[1]>100)'
trigger_match_TkMu100 = '(lep_TkMu100_triggerMatchPt[0]>100 || lep_TkMu100_triggerMatchPt[1]>100)'
trigger_match_full = '('+trigger_match_Mu50+' || '+trigger_match_OldMu100+' || '+trigger_match_TkMu100+')'
fullcut = 'OppSign && extraDimuonCuts && '+mu_cut_0+' && '+mu_cut_1
if args.trig=='Mu27': 
    fullcut += ' && '+trigger_match_Mu27
    fullcut += ' && lep_pt[0]>30 && lep_pt[1]>30'
elif args.trig=='Mu50': 
    fullcut += ' && '+trigger_match_full
    fullcut += ' && lep_pt[0]>53 && lep_pt[1]>53'

cut = '('+args.cut+')' if args.cut!='' else '(1.)'
if args.dir=='SimpleMuonsAllSignsNtuple' and args.fullcut:
    cut += '*('+fullcut+')'

# Data
print 'Data'
print cut
if args.dir=='Our2018MuPrescaledNoCommonMuonsOppSignNtuple':
    f = R.TFile('data/ana_datamc_Run2018ABCD_nocommon_inc.root')
else:
    f = R.TFile(args.datafile)
t = f.Get(args.dir+'/t')
hdata = hist.Clone('hdata')
t.Draw(toDraw+'>>hdata',cut,args.style)
hdata.SetDirectory(0)
hdata.SetStats(0)
data_int = hdata.Integral()
f.Close()

# MC
print 'MC'
#print mccutweight

hists = {sample.name:{} for sample in samples}
nevents = {sample.name:{} for sample in samples}
for i,sample in enumerate(samples):
    print sample.name
    f = R.TFile('mc/ana_datamc_'+sample.name+'.root')
    hmcs = hist.Clone('h'+sample.name)
    t = f.Get(tdir+'/t')
    mccutweight = cut
    if args.nnpdf30 and 'dy' not in sample.name:
        mccutweight += '*1.'
    elif args.nnpdf30 and 'dy' in sample.name and 'to' in sample.name:
        mccutweight += '*'+toNNPDF30
    else:
        mccutweight += '*1.'
    mccutweight += "*genWeight"
    nevents[sample.name] = get_sum_weights(f)
    drawstring = toDraw+'>> h'+sample.name
    t.Draw(drawstring,mccutweight,args.style)
    hmcs.SetDirectory(0)
    print mccutweight
    print hmcs.Integral(), hmcs.GetEntries()
    hists[sample.name]=hmcs
    hists[sample.name].SetDirectory(0)
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

mc_int = 0.
hmc = hist.Clone('hmc')
for sample in samples:
    scale_by = args.Z0 * prescale * sample.cross_section * args.lumi / float(nevents[sample.name])
    hists[sample.name].Scale(scale_by)
    print sample.name,hists[sample.name].Integral()
    mc_int += hists[sample.name].Integral()
    hmc.Add(hists[sample.name])

if args.do_stack:
    s = R.THStack('s','')
    for sample in samples:
        hists[sample.name].SetLineWidth(0)
        hists[sample.name].SetMarkerStyle(0)
        hists[sample.name].SetFillColor(mc_stuff(sample.name)[1])
        if args.bin_width: divide_bin_width(hists[sample.name])
        elif args.cumulative: hists[sample.name] = cumulative_histogram(hists[sample.name])
        s.Add(hists[sample.name])

print '\n','*'*15,'\n'
r,l,h = clopper_pearson_poisson_means(data_int,mc_int)
print data_int, mc_int, r, (h-r + r-l)/2
tau = 1.0 # data/mc 'should' be one
p_bi = R.TMath.BetaIncomplete(1./(1+tau),data_int,int(mc_int)+1)
z_bi = math.sqrt(2)*R.TMath.ErfInverse(1-2*p_bi)
print 'P-value',p_bi,'Z-value',z_bi


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

if args.bin_width:
    gdata = poisson_intervalize(hdata,bin_width=args.bin_width,zero_ex=True)
    divide_bin_width(hmc)
    divide_bin_width(hdata)
elif args.cumulative:
    hmc = cumulative_histogram(hmc)
    hdata = cumulative_histogram(hdata)
    gdata = poisson_intervalize(hdata,bin_width=False,zero_ex=True)
else:
    gdata = poisson_intervalize(hdata,bin_width=False,zero_ex=True)


lumi = '{:5.2f}'.format(args.lumi/1000.)
canvas = Plotter.Canvas(lumi='{lumi}'.format(lumi=lumi)+' fb^{-1} (13 TeV)',extra='Preliminary',ratioFactor=1./3,logy=args.logy)
pdata = Plotter.Plot(gdata,legName='Data',           legType='pe',  option='pe')
if args.do_stack:
    pmc = Plotter.Plot(s,legName='',legType='',option='hist')
    pdy    = Plotter.Plot(hists['dy50to120'],legName=mc_stuff('dy50to120')[0],legType='F')
    #pdy    = Plotter.Plot(hists['DYJetsToLL_HT_100to200'],legName=mc_stuff('DYJetsToLL_HT_100to200')[0],legType='F')
    ptt    = Plotter.Plot(hists['ttbar_lep'],legName=mc_stuff('ttbar_lep')[0],legType='F')
    ptW    = Plotter.Plot(hists['tW_full'],legName=mc_stuff('tW_full')[0],legType='F')
    pdib   = Plotter.Plot(hists['WW'],legName=mc_stuff('WW')[0],legType='F')
    pwjets = Plotter.Plot(hists['Wjets'],legName=mc_stuff('Wjets')[0],legType='F')
    ptau   = Plotter.Plot(hists['dyInclusive50_madgraph'],legName=mc_stuff('dyInclusive50_madgraph')[0],legType='F')
else:
    pmc =   Plotter.Plot(hmc,  legName='102X simulation',legType='hist',option='hist')
canvas.addMainPlot(pmc,addToPlotList=False)
canvas.addMainPlot(pdata)
canvas.makeLegend(pos='tr')
if args.do_stack:
    canvas.legend.addLegendEntry(pdy)
    canvas.legend.addLegendEntry(ptt)
    canvas.legend.addLegendEntry(ptW)
    canvas.legend.addLegendEntry(pdib)
    canvas.legend.addLegendEntry(pwjets)
    canvas.legend.addLegendEntry(ptau)
    canvas.legend.resizeHeight(1.1)
xtit = pretty(args.x)
canvas.firstPlot.setTitles(X=xtit,Y='Events'+(' / GeV' if args.bin_width else ''))
canvas.addRatioPlot(hdata,hmc,ytit='Data / MC',xtit=xtit,plusminus=1.)
hmax = max([hmc.GetMaximum(),hdata.GetMaximum()])
hmin = min([hmc.GetMinimum(),hdata.GetMinimum()])
if hmin==0. and args.logy: hmin=0.1
hmin = hmin/10 if args.logy else 0.
hmax = hmax*10 if args.logy else hmax*1.2
pmc.GetXaxis().SetTitleSize(0)
pmc.GetXaxis().SetLabelSize(0)
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
canvas.cleanup('test/'+args.name+'.png',extrascale=1.5)
f.Close()

