'''
The purpose of this script is to draw N-1 efficiency vs quantities that don't work well
with the other draw script. Namely, it's impossible to do any N-1 efficiencies vs N(PV) 
due to the way that histogram gets filled. Also allows for some interactive-ness.
'''
import ROOT as R
import Selection as Sel
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools import poisson_interval, poisson_intervalize, binomial_divide, clopper_pearson, cumulative_histogram, get_integral, plot_saver
import array,math,argparse
import numpy as np
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples_chris import samples
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter

parser = argparse.ArgumentParser()
parser.add_argument('-nm1','--nminus1',default=None,help='Which cut to remove from the selection')
parser.add_argument('-x',default='vertex_m',help='Quantity to plot on x-axis')
parser.add_argument('-y',default='',help='Quantity to draw on Y axis')
parser.add_argument('-f','--file',dest='datafile',default='data/ana_datamc_Run2018ABCD.root')
#parser.add_argument('-d','--dir',default='Our2018MuonsOppSignNtuple')
parser.add_argument('-d','--dir',default='SimpleMuonsAllSignsNtuple')
parser.add_argument('-c','--cut',default='',help='Extra selections to apply')
parser.add_argument('-s','--style',default='')
parser.add_argument('-ly','--logy',action='store_true',default=False)
parser.add_argument('-lx','--logx',action='store_true',default=False)
parser.add_argument('-n','--name',default='h')
parser.add_argument('-nbx','--nbinsx',default=None,type=int)
parser.add_argument('--xmin',default=None,type=float)
parser.add_argument('--xmax',default=None,type=float)
parser.add_argument('--lumi',default=61310,type=float)
#parser.add_argument('-bw','--bin-width',dest='bin_width',action='store_true')
parser.add_argument('-do30','--nnpdf30',dest='nnpdf30',action='store_true')
#parser.add_argument('--Z0',default=1.0,type=float)
#parser.add_argument('--do-stack',dest='do_stack',action='store_true')
#parser.add_argument('-t','--trig',default='Mu50')
#parser.add_argument('--fullcut',action='store_true')
args = parser.parse_args()
print args
print

fullSelList = Sel.Sel[2018]
print fullSelList
print
fullSel = Sel.GetSelection(2018,fullSelList)
print fullSel
print
nm1Sel = Sel.Nminus1(2018,args.nminus1)
print nm1Sel
#print nm1SelList
#nm1Sel = Sel.GetSelection(2018,nm1SelList)
print args.cut

fullSel += ' && '+args.cut
nm1Sel += ' && '+args.cut

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

# Reweight to NNPDF3.0 taken from s4
# https://indico.cern.ch/event/806789/contributions/3357762/attachments/1813726/2963454/ZToMuMuComp_Min_20190318_v1.pdf
toNNPDF30 = '({a} {b}*pow(gen_dil_mass,1) {c}*pow(gen_dil_mass,2) {d}*pow(gen_dil_mass,3) {e}*pow(gen_dil_mass,4) {f}*pow(gen_dil_mass,5))'.format(a='0.9292',b='+ 5.486E-5',c='+ 6.572E-9',d='- 1.142E-11',e='+ 4.876E-15',f='- 4.117E-19')

print toDraw,args.cut

###################################################################

# Data
print 'Data'
f = R.TFile(args.datafile)
t = f.Get(args.dir+'/t')
hdata = {
        'num':hist.Clone('hdata_num'),
        'den':hist.Clone('hdata_den'),
        }
t.Draw(toDraw+'>>hdata_num',fullSel,args.style)
t.Draw(toDraw+'>>hdata_den',nm1Sel,args.style)
for nd in hdata.keys():
    hdata[nd].SetDirectory(0)
    hdata[nd].SetStats(0)
data_int = {nd:hdata[nd].Integral() for nd in hdata.keys()}
f.Close()

hdata_eff,y,eyl,eyh = binomial_divide(hdata['num'],hdata['den'])

###################################################################

# MC
print 'MC'
#print mccutweight
#hists = {sample.name:{} for sample in samples}
nevents = {sample.name:{} for sample in samples}
for i,sample in enumerate(samples):
    print sample.name
    f = R.TFile('mc/ana_datamc_'+sample.name+'.root')
    t = f.Get(args.dir+'/t')
    sample.sumofweights = get_sum_weights(f)
    sample.histogram_eff_num = hist.Clone('h'+sample.name+'_num')
    sample.histogram_eff_den = hist.Clone('h'+sample.name+'_den')
    mccutweight = ''
    if args.nnpdf30 and 'dy' in sample.name and 'to' in sample.name:
        mccutweight += toNNPDF30
    else:
        mccutweight += '1.'
    mccutweight += "*genWeight"
    t.Draw(toDraw+'>>h'+sample.name+'_num',mccutweight+'*('+fullSel+')',args.style)
    t.Draw(toDraw+'>>h'+sample.name+'_den',mccutweight+'*('+nm1Sel+')',args.style)
    sample.histogram_eff_num.SetDirectory(0)
    sample.histogram_eff_den.SetDirectory(0)
    print mccutweight
    f.Close()

binerrors = array.array('d',[]) # append once for each bin error
for i,sample in enumerate(samples):
    # Get unweighted uncertainties
    binerrorstmp = array.array('d',[])
    for j,ibin in enumerate(range(1,sample.histogram_eff_den.GetNbinsX()+1)):
        # Bins with zero counts get p=0,err=0
        if sample.histogram_eff_num.GetBinContent(ibin) == sample.histogram_eff_den.GetBinContent(ibin) == 0:
            p_ibin=0.
            err2_ibin=0.
        else:
            if sample.histogram_eff_den.GetBinContent(ibin)==0:
                p_ibin=0.
                err2_ibin=0.
            else:
                p_ibin = sample.histogram_eff_num.GetBinContent(ibin) / sample.histogram_eff_den.GetBinContent(ibin)
                err2_ibin = p_ibin*(1-p_ibin)/sample.histogram_eff_den.GetBinContent(ibin)
        # Force when a bin has a negative probability (due to negative weights)
        # p_ibin = 0 and err2_ibin = 0
        if p_ibin<0 or err2_ibin<0:
            p_ibin=0.
            err2_ibin=0.

        binerrorstmp.append(err2_ibin)

    sample.scaled_by = args.lumi * sample.cross_section / sample.sumofweights
    sample.histogram_eff_num.Scale(sample.scaled_by)
    sample.histogram_eff_den.Scale(sample.scaled_by)

    # Each bin gets weighted by the number in the denominator for this sample
    for j,ibin in enumerate(range(1,sample.histogram_eff_den.GetNbinsX()+1)):
        den2 = pow(sample.histogram_eff_den.GetBinContent(ibin),2)
        if i==0:
            binerrors.append(binerrorstmp[j]*den2)
        else:
            binerrors[j] += binerrorstmp[j]*den2


for i,sample in enumerate(samples):
    if i==0:
        mc_eff = sample.histogram_eff_num.Clone()
        mc_eff_den = sample.histogram_eff_den.Clone()
    else:
        mc_eff.Add(sample.histogram_eff_num)
        mc_eff_den.Add(sample.histogram_eff_den)

mc_eff.Divide(mc_eff_den)
for j,ibin in enumerate(range(1,mc_eff.GetNbinsX()+1)):
    if mc_eff.GetBinContent(ibin)==1.:
        mc_eff.SetBinError(ibin,0.)
    else:
        # Divide by the weighted errors by the total mc prediction for that bin
        err = math.sqrt(binerrors[j]/pow(mc_eff_den.GetBinContent(ibin),2))
        #print ibin,mc_eff.GetXaxis().GetBinCenter(ibin),mc_eff.GetBinContent(ibin),err
        mc_eff.SetBinError(ibin,err)

###################################################################

pretty = {
        'vertex_m':'m(#mu^{+}#mu^{-}) [GeV]',
        'cos_angle':'cos(#alpha)',
        'dil_pt':'p_{T}(#mu^{+}#mu^{-}) [GeV]',
        'lep_pt':'p_{T}(#mu) [GeV]',
        'n_dils':'N(#mu^{+}#mu^{-}) passing selection',
        'nvertices':'N(primary vertices)',
        'lep_Mu27_triggerMatchPt':'Mu27 trigger match p_{T}(#mu) [GeV]',
        }

lumi = '{:5.2f}'.format(args.lumi/1000.)
canvas = Plotter.Canvas(lumi='{lumi}'.format(lumi=lumi)+' fb^{-1} (13 TeV)',extra='Preliminary',logx=args.logx)
pdata = Plotter.Plot(hdata_eff,legName='Data',legType='pe',option='pe')
pmc   = Plotter.Plot(mc_eff,legName='102X Simulation',legType='F',option='e2')
canvas.addMainPlot(pmc)
canvas.addMainPlot(pdata)
pmc.SetMarkerStyle(0)
pmc.SetFillStyle(1001)
pmc.SetFillColor(R.kAzure+1)
pmc.SetLineWidth(0)
canvas.firstPlot.GetYaxis().SetRangeUser(0.5,1.1)
canvas.firstPlot.setTitles(X=pretty[args.x],Y='N-1 Efficiency')
canvas.makeLegend(pos='br')
canvas.legend.moveLegend(X=-0.2)
canvas.cleanup('www_nm1/test/'+args.name+'.png')
