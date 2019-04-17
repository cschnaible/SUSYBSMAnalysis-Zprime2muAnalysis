import ROOT as R
import numpy as np
R.gROOT.SetBatch(True)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',default='data/ana_datamc_data_Run2018_inc.root')
parser.add_argument('-d','--dir',default='Our2018MuonsPlusMuonsMinusNtuple')
parser.add_argument('-x',default='vertex_m',help='Quantity to draw on X axis')
parser.add_argument('-y',default='',help='Quantity to draw on Y axis')
parser.add_argument('-c','--cut',default='')
parser.add_argument('-s','--style',default='')
parser.add_argument('-ly','--logy',action='store_true',default=False)
parser.add_argument('-lx','--logx',action='store_true',default=False)
parser.add_argument('-n','--name',default='h')
parser.add_argument('-nb','--nbins',default=None)
parser.add_argument('--xmin',default=None)
parser.add_argument('--xmax',default=None)
parser.add_argument('--ymin',default=None)
parser.add_argument('--ymax',default=None)
args = parser.parse_args()

f = R.TFile(args.file)
tprescaled = f.Get('Our2018MuPrescaledMuonsPlusMuonsMinusNtuple/t')
tsimple = f.Get('SimpleMuonsAllSignsNtuple/t')

print args.logx,args.nbins,args.xmin,args.xmax

if (args.logx==False) and (args.nbins!=None or args.xmax!=None or args.xmin!=None):
    hist = R.TH1D('h','',int(args.nbins),float(args.xmin),float(args.xmax))
    hname = hist.GetName()
elif args.logx and (args.nbins!=None or args.xmin!=None or args.xmax!=None):
    hist = R.TH1D('h','',int(args.nbins),np.logspace(np.log10(float(args.xmin)),np.log10(float(args.xmax)),int(args.nbins)+1))
    hname = hist.GetName()
else:
    hname = 'h'

histprescaled = hist.Clone('hPrescaled')
histsimple= hist.Clone('hSimple')

CUT = 'lep_id[0]*lep_id[1]<0 && lep_isGlobalMuon[0] && lep_isTrackerMuon[0] && fabs(lep_eta[0]) < 2.4 && abs(lep_dB[0]) < 0.2 && lep_sumPt[0] / lep_tk_pt[0] < 0.10 && lep_glb_numberOfValidTrackerLayers[0] > 5 && lep_glb_numberOfValidPixelHits[0] >= 1 && ( (lep_glb_numberOfValidMuonHits[0] > 0) || (lep_tuneP_numberOfValidMuonHits[0] > 0) ) && lep_numberOfMatchedStations[0]>1 && lep_pt_err[0] / lep_pt[0] < 0.3 && lep_isGlobalMuon[1] && lep_isTrackerMuon[1] && fabs(lep_eta[1]) < 2.4 && abs(lep_dB[1]) < 0.2 && lep_sumPt[1] / lep_tk_pt[1] < 0.10 && lep_glb_numberOfValidTrackerLayers[1] > 5 && lep_glb_numberOfValidPixelHits[1] >= 1 && ( (lep_glb_numberOfValidMuonHits[1] > 0) || (lep_tuneP_numberOfValidMuonHits[1] > 0) ) && lep_numberOfMatchedStations[1]>1 && lep_pt_err[1] / lep_pt[1] < 0.3 && vertex_chi2 < 20 && cos_angle>-0.9998 && lep_pt[0]>53 && lep_pt[1]>53'

toDraw = (args.y+':' if args.y!='' else '')+args.x
tprescaled.Draw(toDraw+'>>hPrescaled','lep_pt[0]>53 && lep_pt[1]>53',args.style)
tsimple.Draw(toDraw+'>>hSimple',CUT,args.style)

hnum = f.Get('hPrescaled').Clone()
hnum.SetDirectory(0)
hden = f.Get('hSimple').Clone()
hden.SetDirectory(0)
f.Close()
outF = R.TFile(args.name+'.root','recreate')
hnum.Write()
hden.Write()
outF.Close()

#c = R.TCanvas()
#hnum.Scale(500)
#hnum.Divide(hden)
#hnum.Draw(args.style)
#hnum.GetYaxis().SetRangeUser(0,1)
#if args.logy: c.SetLogy()
#if args.logx: c.SetLogx()
#c.SaveAs('test/'+args.name+'.root')
