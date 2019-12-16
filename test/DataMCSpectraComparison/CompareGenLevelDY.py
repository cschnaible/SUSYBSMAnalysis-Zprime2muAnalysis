import ROOT as R
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples# samples18, samples17, samples16
import array,math
import numpy as np
import argparse
parser = argparse.ArgumentParser('')
parser.add_argument('-w','--where',default='www_nnpdf',help='Where to store plots')
parser.add_argument('-x',default='res_mass',help='Quantity to draw on X axis')
parser.add_argument('-c','--category',default='all',help='Analysis category: all, bb, beee, ee')
parser.add_argument('-s','--selection',default='',help='Selection to apply in addition to Z-peak mass window')
parser.add_argument('-lx','--logx',action='store_true',default=False)
parser.add_argument('-ly','--logy',action='store_true',default=False)
parser.add_argument('-n','--name',default='h')
parser.add_argument('-nbx','--nbinsx',default=None,type=int)
parser.add_argument('--xmin',default=None,type=float)
parser.add_argument('--xmax',default=None,type=float)
parser.add_argument('-bw','--bin-width',dest='bin_width',action='store_true')
parser.add_argument('-do30','--nnpdf30',dest='nnpdf30',action='store_true')
parser.add_argument('--Z0',default=1.0,type=float)
parser.add_argument('--do-stack',dest='do_stack',action='store_true')
parser.add_argument('-cum','--cumulative',action='store_true')
parser.add_argument('-dy','--dy-sample',default='powheg',help='Which DY MC to use: powheg, ht, madgraph, amcatnlo')
parser.add_argument('-ds','--data-sel',default='',help='Additional selection to apply to data only (e.g. prescale)')
parser.add_argument('--overflow',action='store_true',help='Draw overflow bin')
args = parser.parse_args()

def get_sum_weights(t):
    weight = t.GetEntries("genWeight>0") - float(t.GetEntries("genWeight<0"))
    return weight
if args.logx: 
    bins = np.logspace(np.log10(float(args.xmin)),np.log10(float(args.xmax)),int(args.nbinsx)+1)
else: 
    bins = array.array('d',[args.xmin + i*(args.xmax-args.xmin)/args.nbinsx for i in range(0,args.nbinsx+1)])
hist = R.TH1D('h','',int(args.nbinsx),bins)

legNames = {
        '80X':'80X NNPDF3.0',
        '94X':'94X NNPDF3.1',
        '102X':'102X NNPDF3.1',
        }
colors = {
        '80X':R.kRed-4,
        '94X':R.kViolet+1,
        '102X':R.kAzure+1,
        }
titles = {
        'lead_pt':'leading p_{T}(#mu) [GeV]',
        'sub_pt':'sub-leading p_{T}(#mu) [GeV]',
        'gen_lead_pt':'leading GEN p_{T}(#mu) [GeV]',
        'gen_sub_pt':'sub-leading GEN p_{T}(#mu) [GeV]',
        'dil_pt':'p_{T}(#mu#mu) [GeV]',
        'gen_dil_pt':'GEN p_{T}(#mu#mu) [GeV]',
        }

dyList = ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf']
rels = ['80X','94X','102X']

info = {
        '80X':{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/mc/',
            'ntuple':'hardInteractionNtuple/t',
            'mc':samples[2016],
            },
        '94X':{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/mc/',
            'ntuple':'hardInteractionNtuple/t',
            'mc':samples[2017],
            },
        '102X':{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/mc/',
            'ntuple':'hardInteractionNtuple/t',
            'mc':samples[2018],
            },
        }

toDraw = args.x
cats = {
        'all':'(1.)',
        'acc':'(fabs(lep_noib_eta[0])<2.4 && fabs(lep_noib_eta[1])<2.4)',
        'bb':'(fabs(lep_noib_eta[0])<=1.2 && fabs(lep_noib_eta[1]<=1.2))',
        'beee':'(fabs(lep_noib_eta[0])>1.2 || fabs(lep_noib_eta[1]>1.2))',
        'ee':'(fabs(lep_noib_eta[0])>1.2 && fabs(lep_noib_eta[1]>1.2))',
        }
if args.category=='':
    sel = args.selection
else:
    sel = cats[args.category]+' && '+args.selection

hists = {rel:{dy:{} for dy in dyList} for rel in rels}
for rel in rels:
    for dy in dyList:
        f = R.TFile(info[rel]['path']+'ana_genmc_'+dy+'.root')
        t = f.Get(info[rel]['ntuple'])
        h = hist.Clone(rel+'_'+dy)
        theSel = '('+sel+')'+('*genWeight' if rel!='80X' else '')
        t.Draw(toDraw+'>>'+rel+'_'+dy,theSel,'')
        h.SetDirectory(0)
        hists[rel][dy] = h
        hists[rel][dy].SetDirectory(0)
        info[rel]['mc'][dy].sum_weights = get_sum_weights(t) if rel!='80X' else t.GetEntries()
        f.Close()

# Combine MC histograms
mc_int_sum = 0.
mc_ent_sum = 0.
mc_err2_sum = 0.
hmc = hist.Clone('hmc_sum')
histSums = {rel:hist.Clone(rel) for rel in rels}
for rel in rels:
    for mc in reversed(dyList):
        scale_by = info[rel]['mc'][mc].cross_section / float(info[rel]['mc'][mc].sum_weights)
        hists[rel][mc].Scale(scale_by)
        print mc,hists[rel][mc].Integral()
        mc_int_sum += hists[rel][mc].Integral()
        mc_err2_sum += 1./math.sqrt(hists[rel][mc].GetEntries()) if hists[rel][mc].GetEntries()>0 else 0.
        mc_ent_sum += hists[rel][mc].GetEntries()
        histSums[rel].Add(hists[rel][mc])

def pretty(arg):
    ret = {
        'res_pt':'GEN p_{T}(#mu^{+}#mu^{-}) [GeV]',
        'res_mass':'GEN m(#mu^{+}#mu^{-}) [GeV]',
        'res_rap':'GEN y(#mu^{+}#mu^{-})',
        }
    for val in ret.keys():
        if val in arg: return ret[val]

def plusminus(arg):
    ret = {
        'res_pt':0.25,
        'res_rap':1.,
        }
    for val in ret.keys():
        if val in arg: return ret[val]

canvas = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation',logy=True,ratioFactor=1./4,cWidth=1000,cHeight=1000)
canvas.mainPad.SetFillStyle(4000)
plots = {rel:Plotter.Plot(histSums[rel],legName=legNames[rel],legType='l',option='hist') for rel in rels}
for rel in rels:
    canvas.addMainPlot(plots[rel])
    plots[rel].SetLineColor(colors[rel])
canvas.makeLegend(pos='tr')
canvas.legend.moveLegend(X=-0.15)
xtit = pretty(args.x)
canvas.firstPlot.setTitles(X=xtit,Y='XS / Sum weights')
hmax = max([histSums[rel].GetMaximum() for rel in rels])
hmin = min([histSums[rel].GetMinimum() for rel in rels])
if hmin==0. and args.logy: hmin=0.1
hmin = hmin/10 if args.logy else 0.
hmax = hmax*10 if args.logy else hmax*1.2
canvas.firstPlot.GetXaxis().SetTitleSize(0)
canvas.firstPlot.GetXaxis().SetLabelSize(0)
canvas.addRatioPlot(histSums['94X'], histSums['80X'],ytit='3.1 / 3.0',xtit=xtit,plusminus=plusminus(args.x),color=colors['94X'],div='normal',option='pe')
canvas.addRatioPlot(histSums['102X'],histSums['80X'],ytit='3.1 / 3.0',xtit=xtit,plusminus=plusminus(args.x),color=colors['102X'],div='normal',option='pe')
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
canvas.firstPlot.GetYaxis().SetRangeUser(1E-12,1E-6)
canvas.Update()
canvas.ratPad.RedrawAxis()
canvas.cleanup(args.where+'/'+args.name+'.png',extrascale=1.5)
