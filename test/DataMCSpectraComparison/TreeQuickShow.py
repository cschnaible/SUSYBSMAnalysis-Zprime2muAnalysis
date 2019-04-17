import ROOT as R
R.gROOT.SetBatch(True)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',default='data/ana_datamc_Run2018ABCD.root')
parser.add_argument('-d','--dir',default='Our2018MuonsOppSignNtuple')
parser.add_argument('-e','--entry',default=0,type=int)
args = parser.parse_args()

f = R.TFile(args.file)
t = f.Get(args.dir+'/t')

t.Show(args.entry)
