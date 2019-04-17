'''
Combine MC samples and parameterize shape
'''
import os
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools_chris import *
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples_chris import *
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-l','--luminosity',dest='int_lumi',default=59090,type=float,
        help='Integrated luminosity in /pb')
parser.add_argument('-d','--output-dir',dest='output_dir',default='www_bckgshape',
        help='Output directory name')
parser.add_argument('-t','--output-tag',dest='output_tag',default='',
        help='Output tagectory name')
parser.add_argument('--dy-only',dest='dy_only',action='store_true',
        help='Only combine Drell-Yan MC')

args = parser.parse_args()

set_zp2mu_style()
cutset = 'Our2018'
dilepton = 'MuonsPlusMuonsMinus'
quantities = ['DimuonMassVertexConstrained'+cat for cat in ['','_bb','be']]
mc_dir = os.path.join('mc')

def rebin_histogram(hist,cutset,dilepton,quantity):
    rebin = 1
    if 'DimuonMassVertexConstrained' in quantity:
        rebin = 10
    if 'DileptonMass' in quantity:
        rebin = 10
    if quantity in ['DileptonPt','DileptonPz','LeptonPt','LeptonPz','LeptonP']:
        rebin = 10
    if quantity in ['RelCombIso', 'RelIsoSumPt']:
        rebin = 5
    if quantity in ['DileptonPhi', 'DileptonRap', 'LeptonPhi', 'LeptonEta']:
        rebin = 5
    if 'Log' in quantity:
        rebin = 10
    hist.Rebin(rebin)

def add_hists(cutset,dilepton,quantity):
    total = ROOT.TH1D()
    for s,sample in enumerate(samples):
        if args.dy_only and 'dy' in sample.name: continue
        mc_fn = os.path.join(mc_dir, 'ana_datamc_%s.root' % sample.name)
        f = ROOT.TFile(mc_fn)
        sample.histogram = getattr(f, self.get_dir_name(cutset, dilepton)).Get(quantity).Clone()
        sample.scaled_by = args.int_lumi * sample.partial_weight_eff
        rebin_histogram(sample.histogram, cutset, dilepton, quantity_to_compare)
        sample.histogram.Scale(sample.scaled_by)
        if s==0:
            total = sample.histogram.Clone()
        else:
            total.Add(sample.histogram)
    return total


for quantity in quantities:
    total = add_hists(samples,cutset,dilepton,quantity)





