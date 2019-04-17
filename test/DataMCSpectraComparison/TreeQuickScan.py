import ROOT as R
R.gROOT.SetBatch(True)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',default='data/ana_datamc_Run2018ABCD.root')
parser.add_argument('-d','--dir',default='Our2018MuonsOppSignNtuple')
parser.add_argument('-c','--cut',default='')
parser.add_argument('-v','--var',action='append',help='Quantities to print')
args = parser.parse_args()

f = R.TFile(args.file)
t = f.Get(args.dir+'/t')

toPrint = args.var[0]
for var in args.var[1:]:
    toPrint += ':'+var

t.SetScanField(0)
t.Scan(toPrint,args.cut,'colsize=10')
