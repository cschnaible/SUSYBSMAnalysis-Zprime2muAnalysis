import ROOT as R
import numpy as np
import array, math
R.gROOT.SetBatch(True)
import argparse
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples_chris import samples17, samples18
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools_chris import poisson_intervalize, divide_bin_width, clopper_pearson_poisson_means, cumulative_histogram
parser = argparse.ArgumentParser()
parser.add_argument('-y','--year',default=2018,type=int,help='Which year to print')
parser.add_argument('-s','--sel',default='our',help='sel selection')
parser.add_argument('-c','--cut',default='')
parser.add_argument('--lumi',default=61310,type=float)
parser.add_argument('-do30','--nnpdf30',dest='nnpdf30',action='store_true')
parser.add_argument('--Z0',default=1.0,type=float)
parser.add_argument('-p','--prescale',dest='prescale',type=float,default=0.)
args = parser.parse_args()

# 42036.9393414
# 178.058438126
lumis = {
        2018:{
            'ourpre':{
                1:6.93268721899,
                148:0.147624058419,
                222:1.97545175771,
                296:2.19734009371,
                385:0.900672329177,
                445:8.90420596453,
                500:111.74380145,
                },
            'our':{
                1:6.93268721899,
                148:21.848360646,
                222:438.550290211,
                296:650.412667738,
                385:346.758846733,
                445:3962.37165422,
                500:55871.900725,
                },
            },
        2017:{
            'our':{
                59:86.8712438022,
                70:275.190535276,
                74:163.661209166,
                117:46.2436284491,
                120:4123.72145243,
                140:2413.39785073,
                148:541.983190576,
                176:860.668911332,
                210:5560.95773849,
                222:951.36024321,
                234:2050.1262438,
                280:6535.92676296,
                281:1111.61316576,
                296:1188.58563938,
                315:770.139832091,
                328:1921.36662493,
                336:1626.58354641,
                341:525.035573921,
                356:463.119019459,
                375:119.156046088,
                385:483.395320788,
                392:911.390557063,
                415:621.24955696,
                422:141.494069456,
                445:2846.99397805,
                449:752.926446731,
                458:26.4998925556,
                480:14.0916112563,
                505:2198.24925031,
                561:2704.94019996,
                },
            'ourpre':{
                59:1.47239396275,
                70:3.93129336107,
                74:2.21163796169,
                117:0.395244687597,
                120:34.364345437,
                140:17.2385560766,
                148:3.66204858499,
                176:4.89016426893,
                210:26.4807511356,
                222:4.28540650095,
                234:8.76122326406,
                280:23.3425955821,
                281:3.95591873938,
                296:4.01549202491,
                315:2.44488835583,
                328:5.85782507604,
                336:4.84102245952,
                341:1.53969376516,
                356:1.30089612208,
                375:0.317749456237,
                385:1.25557226181,
                392:2.32497591087,
                415:1.49698688423,
                422:0.335294003445,
                445:6.39773927651,
                449:1.67689631787,
                458:0.057860027413,
                480:0.029357523443,
                505:4.3529688125,
                561:4.82164028514,
                },
            },
        }
LUMI = lumis[args.sel][args.prescale] if args.prescale>0 else args.lumi


info = {
    2018:{
        'samples':samples18,
        'mcdir':'mc',
        'ddir':'data',
        'our':{
            'datafile':'ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root',
            'mcdir':'Our2018MuonsOppSignNtuple',
            'ddir' :'Our2018MuonsOppSignNtuple',
            },
        'ourpre':{
            'datafile': 'ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root',
            'mcdir': 'Our2018MuPrescaledMuonsOppSignNtuple',
            'ddir' : 'Our2018MuPrescaledNoCommonMuonsOppSignNtuple',
            },
        'ourprecommon':{
            'datafile': 'ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root',
            'mcdir': 'Our2018MuPrescaledMuonsOppSignNtuple',
            'ddir': 'Our2018MuPrescaledMuonsOppSignNtuple',
            },
        },
    2017:{
        'samples': samples17,
        'mcdir':'mc_2017',
        'ddir':'data_2017',
        'our':{
            'datafile': 'ana_datamc_Run2017BCDEF_20190416.root',
            'mcdir': 'Our2017MuonsPlusMuonsMinusNtuple',
            'ddir': 'Our2017MuonsPlusMuonsMinusNtuple',
            },
        'ourpre':{
            'datafile': 'ana_datamc_Run2017BCDEF_nocommon_20190417.root',
            'mcdir': 'Our2017MuPrescaledMuonsPlusMuonsMinusNtuple',
            'ddir': 'Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple',
            },
        'ourprecommon':{
            'datafile': 'ana_datamc_Run2017BCDEF_20190416.root',
            'mcdir': 'Our2017MuPrescaledMuonsPlusMuonsMinusNtuple',
            'ddir': 'Our2017MuPrescaledMuonsPlusMuonsMinusNtuple',
            },
        },
    }

def get_sum_weights(f):
    weights = getattr(f,'EventCounter').Get('weights')
    return weights.GetBinContent(2)-weights.GetBinContent(1)

mcEventYields = {sample.name:{} for sample in info[args.year]['samples']}
for i,sample in enumerate(info[args.year]['samples']):
    #print sample.name
    f = R.TFile(info[args.year]['mcdir']+'/ana_datamc_'+sample.name+'.root')
    t = f.Get(info[args.year][args.sel]['mcdir']+'/t')
    #mccutweight = cut
    #if args.nnpdf30 and 'dy' not in sample.name:
    #    mccutweight += '*1.'
    #elif args.nnpdf30 and 'dy' in sample.name and 'to' in sample.name:
    #    mccutweight += '*'+toNNPDF30
    #else:
    #    mccutweight += '*1.'
    #mccutweight += "*genWeight"
    mcEventYields[sample.name]['name'] = sample.name
    mcEventYields[sample.name]['pos'] = t.GetEntries('genWeight>0'+(' && '+args.cut if args.cut else ''))
    mcEventYields[sample.name]['neg'] = t.GetEntries('genWeight<0'+(' && '+args.cut if args.cut else ''))
    mcEventYields[sample.name]['pn'] = mcEventYields[sample.name]['pos'] - mcEventYields[sample.name]['neg']
    mcEventYields[sample.name]['xs']  = sample.cross_section
    mcEventYields[sample.name]['nevents'] = get_sum_weights(f)
    mcEventYields[sample.name]['weight'] = mcEventYields[sample.name]['xs']/mcEventYields[sample.name]['nevents']
    mcEventYields[sample.name]['total'] = (mcEventYields[sample.name]['pos']-mcEventYields[sample.name]['neg'])*mcEventYields[sample.name]['weight']*LUMI
    f.Close()

print '\n','*'*30,'\n'
print 'Cuts : ',args.cut
print 'Prescale : ',args.prescale
print 'Luminosity : ',LUMI,'[pb]'
print '\n{name:<25} {pos:>10} {neg:>10} {pn:>10} {xs:>9} {nevents:>11} {weight:>13} {total:>11}'.format(name='MC Name',pos='Pos Events',neg='Neg Events',pn='Pos-Neg',xs='XS [pb]',nevents='N MC events',weight='xs/nevts',total='total')
toPrint = '{name:<25} {pos:>10} {neg:>10} {pn:>10} {xs:>9.3e} {nevents:>11} {weight:>9.7e} {total:>11.5f}'
for sample in info[args.year]['samples']:
    print toPrint.format(**mcEventYields[sample.name])


names = ['dy','ttbar','diboson','singletop','Wjets','tautau']
combine = {
        2018:{
            'dy':['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf'],
            'ttbar':['ttbar_lep'],
            'diboson':['WW','WZ','ZZ'],
            'singletop':['tW_full','tbarW_full'],
            'Wjets':['Wjets'],
            'tautau':['dyTauTau_madgraph'],
            },
        2017: {
            'dy':['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf'],
            'ttbar':['ttbar_lep'],
            'diboson':['WW_v2','WZ','ZZ'],
            'singletop':['tW','tbarW'],
            'Wjets':['Wjets'],
            'tautau':['dyInclusive50_amcatnlo'],
            },
        }
mc_int = 0.
mc_ints = {sample:0. for sample in ['dy','ttbar','diboson','singletop','Wjets','tautau']}
for proc in names:
    for iproc in combine[args.year][proc]:
        mc_ints[proc] += mcEventYields[iproc]['total']
    mc_int += mc_ints[proc]

print
toPrint = '{proc:<10} {total:>15.3f}'
for proc in names:
    print toPrint.format(proc=proc,total=mc_ints[proc])
print '-'*15
print toPrint.format(proc='Total MC',total=mc_int)

f = R.TFile(info[args.year]['ddir']+'/'+info[args.year][args.sel]['datafile'])
t = f.Get(info[args.year][args.sel]['ddir']+'/t')
data_int = t.GetEntries(args.cut+(' && Mu27_prescale=='+str(args.prescale) if args.prescale>1. else ''))
f.Close()
print toPrint.format(proc='Data',total=data_int)

print '\n','*'*15,'\n'
r,l,h = clopper_pearson_poisson_means(data_int,mc_int)
print 'Data / MC =', r, (h-r + r-l)/2, h-r, r-l
tau = 1.0 # data/mc 'should' be one
p_bi = R.TMath.BetaIncomplete(1./(1+tau),data_int,int(mc_int)+1)
z_bi = math.sqrt(2)*R.TMath.ErfInverse(1-2*p_bi)
print 'P-value',p_bi,'Z-value',z_bi
