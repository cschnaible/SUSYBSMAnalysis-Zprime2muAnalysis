import ROOT as R
import numpy as np
import array 
R.gROOT.SetBatch(True)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',default='data/old/ana_datamc_data_Run2018_inc.root')
parser.add_argument('-d','--dir',default='Our2018MuonsPlusMuonsMinusNtuple')
#parser.add_argument('-d','--dir',default='Our2018MuonsOppSignNtuple')
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
args = parser.parse_args()

f = R.TFile(args.file)
t = f.Get(args.dir+'/t')

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


toDraw = (args.y+':' if args.y!='' else '')+args.x
t.Draw(toDraw+'>>'+hname,args.cut,args.style)
h = f.Get('h')
c = R.TCanvas()
h.Draw(args.style)
if args.logy: c.SetLogy()
if args.logx: c.SetLogx()
c.SaveAs('test/'+args.name+'.png')
f.Close()
