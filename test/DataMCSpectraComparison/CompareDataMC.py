'''
Compare Data and MC
'''
import ROOT as R
R.gROOT.SetBatch(True)
import numpy as np
import array, math, logging
import SUSYBSMAnalysis.Zprime2muAnalysis.lumberjack as lumberjack
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples# samples18, samples17, samples16
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools_chris import poisson_intervalize, divide_bin_width, clopper_pearson_poisson_means, cumulative_histogram, move_overflow_into_last_bin
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d','--tdir',default='our')
parser.add_argument('-w','--where',default='www_compare_datamc',help='Where to store plots')
parser.add_argument('-x',default='vertex_m',help='Quantity to draw on X axis')
parser.add_argument('-y','--year',default=2018,help='Which year(s) to compare to MC')
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
parser.add_argument('--scaleZ0',action='store_true')
parser.add_argument('--do-stack',dest='do_stack',action='store_true')
parser.add_argument('-cum','--cumulative',action='store_true')
parser.add_argument('-dy','--dy-sample',default='powheg',help='Which DY MC to use: powheg, ht, madgraph, amcatnlo')
parser.add_argument('-ds','--data-sel',default='',help='Additional selection to apply to data only (e.g. prescale)')
parser.add_argument('--overflow',action='store_true',help='Draw overflow bin')
parser.add_argument('--order',default='nlo',help='Needs NNPDF30, anything other than \'nnlo\' does nothing')
parser.add_argument('--do-smear',action='store_true',help='Smear dimuon masses by 15% of resolution')
parser.add_argument('--do-fake-rate',action='store_true',help='Add data driven jets estimate')
parser.add_argument('--do-jets-mc',action='store_true',help='Add MC jets estimate')
parser.add_argument('--do-paper',action='store_true',help='Make plot in style of paper')
parser.add_argument('--do-uncert',action='store_true',help='Make uncertaity band in plot')
parser.add_argument('-pw','--prescale-weight',default='data',help='Scale data or mc')
args = parser.parse_args()

def round_to_n(x,n):
    if x>0.0:
        return round(x, -int(math.floor(math.log10(x))) + (n-1))
    else:
        return 0.0

theYear = args.year
allyears = [2016,2017,2018] if theYear in ['all','run2'] else [int(theYear)]

cols = {'dypaper':['powheg'],'nonDY':['singletop','diboson','ttbar','tautau'],'jets':['jets']}
paperDrawOrder = ['nonDY','dypaper']
paperDrawOrder = ['jets']+paperDrawOrder if args.do_fake_rate else paperDrawOrder
if args.do_jets_mc:
    mcDrawOrder = ['tautau','Wjets','singletop','diboson','ttbar','powheg']
else:
    mcDrawOrder = ['tautau','singletop','diboson','ttbar','powheg']
if args.do_fake_rate:
    mcDrawOrder = ['jets']+mcDrawOrder

dyLists = {
    'powheg' : ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf'],
    'ht' : ['dyJetsToLL_ht100to200','dyJetsToLL_ht200to400','dyJetsToLL_ht400to600','dyJetsToLL_ht600to800','dyJetsToLL_ht800to1200','dyJetsToLL_ht1200to2500','dyJetsToLL_ht2500toInf'],
    'madgraph' : ['dyInclusive50_madgraph'],
    'amcatnlo' : ['dyInclusive50_amcatnlo'],
    }
allMCs = {
        2016:{
            'powheg' : ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf'],
            'ht' : ['dyJetsToLL_ht100to200','dyJetsToLL_ht200to400','dyJetsToLL_ht400to600','dyJetsToLL_ht600to800','dyJetsToLL_ht800to1200','dyJetsToLL_ht1200to2500','dyJetsToLL_ht2500toInf'],
            'madgraph' : ['dyInclusive50_madgraph'],
            'amcatnlo' : ['dyInclusive50_amcatnlo'],
            'ttbar':['ttbar_lep_50to500','ttbar_lep_500to800','ttbar_lep_800to1200','ttbar_lep_1200to1800','ttbar_lep_1800toInf'],
            'diboson':['WW_50to200','WW_200to600','WW_600to1200','WW_1200to2500','WW_2500toInf','ZZ','WZ'],
            'singletop':['tW','tbarW'],
            'Wjets':['Wjets'],
            'tautau':['dyTauTau_madgraph'],
            'jets':['jets'],
            },
        2017:{
            'powheg' : ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf'],
            'ht' : ['dyJetsToLL_ht100to200','dyJetsToLL_ht200to400','dyJetsToLL_ht400to600','dyJetsToLL_ht600to800','dyJetsToLL_ht800to1200','dyJetsToLL_ht1200to2500','dyJetsToLL_ht2500toInf'],
            'madgraph' : ['dyInclusive50_madgraph'],
            'amcatnlo' : ['dyInclusive50_amcatnlo'],
            #'ttbar':['ttbar_lep'],
            #'diboson':['WW','ZZ','WZ'],
            #'singletop':['tW_inclusive','tbarW_inclusive'],
            'ttbar':['ttbar_lep_50to500','ttbar_lep_500to800','ttbar_lep_800to1200','ttbar_lep_1200to1800','ttbar_lep_1800toInf'],
            'diboson':['WW_50to200','WW_200to600','WW_600to1200','WW_1200to2500','WW_2500toInf','ZZTo4L','ZZTo2L2Q','ZZTo2L2Nu','WZTo3LNu','WZTo2L2Q'],
            'singletop':['tW','tbarW'],
            'Wjets':['Wjets'],
            'tautau':['dyTauTau_madgraph'],
            'jets':['jets'],
            },
        2018:{
            'powheg' : ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf'],
            'ht' : ['dyJetsToLL_ht100to200','dyJetsToLL_ht200to400','dyJetsToLL_ht400to600','dyJetsToLL_ht600to800','dyJetsToLL_ht800to1200','dyJetsToLL_ht1200to2500','dyJetsToLL_ht2500toInf'],
            'madgraph' : ['dyInclusive50_madgraph'],
            'amcatnlo' : ['dyInclusive50_amcatnlo'],
            #'ttbar':['ttbar_lep'],
            #'diboson':['WW','ZZTo4L','ZZTo2L2Q','ZZTo2L2Nu','WZTo3LNu','WZTo2L2Q'],
            'ttbar':['ttbar_lep_50to500','ttbar_lep_500to800','ttbar_lep_800to1200','ttbar_lep_1200to1800','ttbar_lep_1800toInf'],
            'diboson':['WW_50to200','WW_200to600','WW_600to1200','WW_1200to2500','WW_2500toInf','ZZTo4L','ZZTo2L2Q','ZZTo2L2Nu','WZTo3LNu','WZTo2L2Q'],
            'singletop':['tW','tbarW'],
            'Wjets':['Wjets'],
            'tautau':['dyTauTau_madgraph'],
            'jets':['jets'],
            },
        }

info = {
        2016:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/data/',
            #'file':'ana_datamc_Run2016_17Jul2018.root',
            'file':'ana_datamc_Run2016BCDEFG_23Sep2016_Run2016H_PromptReco.root',
            'lumi':36294.593964906585693,
            'ratioZ0':{'all':0.9727,'bb':0.9842,'beee':0.9610},
            'our':{
                'dir':'Our2016MuonsOppSignNtuple',
                'pre':1.,
                'FR':'mc_2016/jets_muons_2016.root',
                },
            'ourcommonpre':{
                'dir':'Our2016MuPrescaledCommonMuonsOppSignNtuple',
                'pre':320.,
                },
            'ourpre':{
                'dir':'Our2016MuPrescaledMuonsOppSignNtuple',
                'pre':146.323326629,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/mc/',
            'mc':samples[2016],
            },
        2017:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/data/',
            'file':'ana_datamc_Run2017_31Mar2018.root',
            #'file':'ana_datamc_Run2017BCDEF_20190416.root',
            'lumi':42079.880396,
            'ratioZ0':{'all':1.0282,'bb':1.0286,'beee':1.0278},
            'our':{
                'dir':'Our2018MuonsOppSignNtuple',
                'pre':1.,
                'FR':{
                    'all':'mc_2017/Data-total-jets-BB-BE-EE-pt53.root',
                    'bb':'mc_2017/Data-total-jets-BB-pt53.root',
                    'beee':'mc_2017/Data-total-jets-BEEE-pt53.root',
                    },
                },
            'ourcommonpre':{
                'dir':'Our2018MuPrescaledCommonMuonsOppSignNtuple', # 31Mar2018
                #'dir_data':'Our2017MuPrescaledMuonsPlusMuonsMinusNtuple', # BCDEF_20190416
                #'dir_MC':'Our2018MuPrescaledCommonMuonsOppSignNtuple', # 31Mar2018
                'pre':561.,
                },
            'ourpre':{
                'dir':'Our2018MuPrescaledMuonsOppSignNtuple',
                'pre':236.085072878,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/mc/',
            'mc':samples[2017],
            },
        2018:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/data/',
            'file':'ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root',
            'lumi':61298.775231718995,
            'ratioZ0':{'all':1.0062,'bb':1.0124,'beee':1.0017},
            'our':{
                'dir':'Our2018MuonsOppSignNtuple',
                'pre':1.,
                'FR':{
                    'all':'mc/Data2018-total-jets-BB-BE-EE-pt53.root',
                    'bb':'mc/Data2018-total-jets-BB-pt53.root',
                    'beee':'mc/Data2018-total-jets-BE-EE-pt53.root',
                    },
                },
            'ourcommonpre':{
                #'dir':'Our2018MuPrescaledMuonsOppSignNtuple', # dir name from duplicate file
                'dir':'Our2018MuPrescaledCommonMuonsOppSignNtuple',
                'pre':500.,
                },
            'ourpre':{
                #'dir':'Our2018MuPrescaledNoCommonMuonsOppSignNtuple', # dir name from duplicate file
                'dir':'Our2018MuPrescaledMuonsOppSignNtuple',
                'pre':486.949643091,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/mc/',
            'mc':samples[2018],
            },
        }

nnpdf_to_rescale = {
        2017:{
            'our':['powheg','ttbar'],
            'ourpre':['powheg'],
            'ourcommonpre':['powheg'],
            },
        2018:{
            'our':['powheg','ttbar'],
            'ourpre':['powheg'],
            'ourcommonpre':['powheg'],
            },
        }
dy_nnpdf_func = '(({a}) + ({b})*pow(gen_dil_mass,1) + ({c})*pow(gen_dil_mass,2) + ({d})*pow(gen_dil_mass,3) + ({e})*pow(gen_dil_mass,4) + ({f})*pow(gen_dil_mass,5))'
WW_nnpdf_func = '(({a}) + ({b})*pow(gen_dil_mass,1) + ({c})*pow(gen_dil_mass,2) + ({d})*pow(gen_dil_mass,3) + ({e})*pow(gen_dil_mass,4))'
ttbar_nnpdf_func = '((gen_dil_mass<120)*1. + (gen_dil_mass>120 && gen_dil_mass<3000)*(({a}) + ({b})*pow(gen_dil_mass,1) + ({c})*pow(gen_dil_mass,2) + ({d})*pow(gen_dil_mass,3)) + (gen_dil_mass>3000)*(0.436005))'
zpeak_nnpdf_func = '((gen_lead_pt<30)*0.9 + (gen_lead_pt>30 && gen_lead_pt<100)*(({a}) + ({b})*pow(gen_lead_pt,1) + ({c})*pow(gen_lead_pt,2) + ({d})*pow(gen_lead_pt,3) + ({e})*pow(gen_lead_pt,4) + ({f})*pow(gen_lead_pt,5)) + (gen_lead_pt>100)*({g}))'
toNNPDF30 = {
        2017:{
            'our':{
                'powheg':{
                    #'all':dy_nnpdf_func.format(a='0.9292',b='+ 5.486E-5',c='+ 6.572E-9',d='- 1.142E-11',e='+ 4.876E-15',f='- 4.117E-19'),
                    'all': dy_nnpdf_func.format(a='0.918129',b='6.92702e-05',c='1.62175e-08',d='-2.47833e-11',e='8.75707e-15',f='-7.53019e-19'),
                    'bb':  dy_nnpdf_func.format(a='0.914053',b='7.91618e-05',c='2.19722e-08',d='-3.49212e-11',e='1.22504e-14',f='-1.07347e-18'),
                    'beee':dy_nnpdf_func.format(a='0.933214',b='3.76813e-05',c='1.95612e-08',d='-1.2688e-11', e='3.69867e-15',f='-2.62212e-19'),
                    'ee':  dy_nnpdf_func.format(a='0.952255',b='-7.67452e-05',c='1.69935e-07',d='-9.44719e-11',e='2.28419e-14',f='-1.72926e-18'),
                    },
                'ttbar':{ # same for both 2017 and 2018
                    #'all':  ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                    #'bb':   ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                    #'beee': ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                    #'all':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                    #'bb':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                    #'beee':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                    'all': ttbar_nnpdf_func.format(a='0.994078695151',b='2.64819793287e-05',c='-3.73996461024e-08',d='-1.11452866827e-11'),
                    'bb': ttbar_nnpdf_func.format(a='0.994078695151',b='2.64819793287e-05',c='-3.73996461024e-08',d='-1.11452866827e-11'),
                    'beee': ttbar_nnpdf_func.format(a='0.994078695151',b='2.64819793287e-05',c='-3.73996461024e-08',d='-1.11452866827e-11'),
                    },
                #'diboson':{
                #    'all':'(1.)',
                #    'bb':'(1.)',
                #    'beee':WW_nnpdf_func.format(a='1.0031',b='-6.30717e-05',c='-3.14538e-08',d='2.68999e-11',e='-5.66054e-15'),
                #    },
                },
            'ourcommonpre':{
                'powheg':{
                    'all':zpeak_nnpdf_func.format(a='1.8245728118',b='-0.0537728412909',c='0.000731365981935',d='7.16669312495e-06',e='-1.99723894101e-07',f='1.0112316789e-09',g='1.01849023288'),
                    'bb': zpeak_nnpdf_func.format(a='1.91383074609',b='-0.0596201865777',c='0.000811074027001',d='7.90677720686e-06',e='-2.21489848717e-07',f='1.12700571973e-09',g='1.00484010198'),
                    'beee':zpeak_nnpdf_func.format(a='1.71913319508',b='-0.0481243962238',c='0.000666286154366',d='6.45776405133e-06',e='-1.82202504311e-07',f='9.24567381899e-10',g='1.02790393101'),
                    },
                },
            },
        2018:{
            'our':{
                'powheg':{
                    'all': dy_nnpdf_func.format(a='0.919027',b='5.98337e-05', c='2.56077e-08', d='-2.82876e-11',e='9.2782e-15', f='-7.77529e-19'),
                    'bb':  dy_nnpdf_func.format(a='0.911563',b='0.000113313', c='-2.35833e-08',d='-1.44584e-11',e='8.41748e-15',f='-8.16574e-19'),
                    'beee':dy_nnpdf_func.format(a='0.934502',b='2.21259e-05', c='4.14656e-08', d='-2.26011e-11',e='5.58804e-15',f='-3.92687e-19'),
                    'ee':  dy_nnpdf_func.format(a='0.954175',b='-9.68066e-05',c='2.09278e-07', d='-1.15712e-10',e='2.77047e-14',f='-2.11731e-18'),
                    },
                'ttbar':{ # same for both 2017 and 2018
                    #'all':  ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                    #'bb':   ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                    #'beee': ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                    #'all':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                    #'bb':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                    #'beee':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                    'all': ttbar_nnpdf_func.format(a='0.994078695151',b='2.64819793287e-05',c='-3.73996461024e-08',d='-1.11452866827e-11'),
                    'bb': ttbar_nnpdf_func.format(a='0.994078695151',b='2.64819793287e-05',c='-3.73996461024e-08',d='-1.11452866827e-11'),
                    'beee': ttbar_nnpdf_func.format(a='0.994078695151',b='2.64819793287e-05',c='-3.73996461024e-08',d='-1.11452866827e-11'),
                    },
                },
            'ourcommonpre':{
                'powheg':{
                    'all':zpeak_nnpdf_func.format(a='1.69147781688',b='-0.0473286496053',c='0.000661599919558',d='6.33324308996e-06',e='-1.80459280586e-07',f='9.19632449685e-10',g='1.02344217328'),
                    'bb': zpeak_nnpdf_func.format(a='1.65477513925',b='-0.0472097707001',c='0.000681831627146',d='6.15645344304e-06',e='-1.82810037593e-07',f='9.43667804224e-10',g='1.01489199674'),
                    'beee':zpeak_nnpdf_func.format(a='1.60977951604',b='-0.0426122819079',c='0.000599273084801',d='5.88395881526e-06',e='-1.66414436738e-07',f='8.4690800397e-10',g='1.02846360871'),
                    },
                },
            },
        }

#pi_func =  '({a} {b}*pow(gen_dil_mass,1) {c}*pow(gen_dil_mass,2) {d}*pow(gen_dil_mass,3))'.format(a='1.067',b='- 0.000112',c='+ 3.176e-8',d='- 4.068e-12')
#k_func_high = '({a} {b}*pow(gen_dil_mass-400.0,1) {c}*pow(gen_dil_mass-400.0,2) {d}*pow(gen_dil_mass-400.0,3))'
#k_func_low  = '({a} {b}*pow(gen_dil_mass-130.0,1) {c}*pow(gen_dil_mass-130.0,2) {d}*pow(gen_dil_mass-130.0,3))'
kfunc = '(({a}) + ({b})*pow(gen_res_mass,1) + ({c})*pow(gen_res_mass,2) + ({d})*pow(gen_res_mass,3))'
kFunction = {
        'our':{ # m > 150 GeV
            'all' :kfunc.format(a='1.053',b='-0.0001552',c='5.661e-08',d='-8.382e-12'),
            'bb'  :kfunc.format(a='1.032',b='-0.000138', c='4.827e-08',d='-7.321e-12'),
            'beee':kfunc.format(a='1.064',b='-0.0001674',c='6.599e-08',d='-9.657e-12'),
            },
        #'our':{ # pt > 53 GeV and m > 120
        #    #'all': k_func_high.format(a='1.067',b='- 0.000112',c='+ 3.176e-8',d='- 4.068e-12'),
        #    'all': k_func_high.format(a='1.047',b='- 0.000143', c='+ 5.167e-8',d='- 7.84e-12'),
        #    'bb' : k_func_high.format(a='1.036',b='- 0.0001441',c='+ 5.068e-8',d='- 7.581e-12'),
        #    'beee':k_func_high.format(a='1.052',b='- 0.0001471',c='+ 5.903e-8',d='- 9.037e-12'),
        #    },
        #'ourpre':{ # pt > 30 and m < 170
        #    'all': k_func_low.format(a='1.067',b='- 0.000112',c='+ 3.176e-8',d='- 4.068e-12'),
        #    'bb' : k_func_low.format(a='1.036',b='- 0.0001441',c='+ 5.058e-8',d='- 7.581e-12'),
        #    'beee':k_func_low.format(a='1.052',b='- 0.0001471',c='+ 5.903e-8',d='- 9.037e-12'),
        #    },
        #'ourcommonpre':{
        #    'all': k_func_high.format(a='1.067',b='- 0.000112',c='+ 3.176e-8',d='- 4.068e-12'),
        #    'bb' : k_func_high.format(a='1.036',b='- 0.0001441',c='+ 5.058e-8',d='- 7.581e-12'),
        #    'beee':k_func_high.format(a='1.052',b='- 0.0001471',c='+ 5.903e-8',d='- 9.037e-12'),
        #    },
        }

resFunc = '({a} + ({b})*pow(gen_res_mass,1) + ({c})*pow(gen_res_mass,2) + ({d})*pow(gen_res_mass,3) + ({e})*pow(gen_res_mass,4))'
resMass = {
        2018:{
            'bb':resFunc.format(a='0.00608',b='3.42e-05',c='-1.34e-08',d='2.4e-12',e='-1.5e-16'),
            'beee':resFunc.format(a='0.0135',b='2.83e-05',c='-9.71e-09',d='1.71e-12',e='-1.09e-16'),
            },
        2017:{
            'bb':resFunc.format(a='0.00606',b='3.41e-05',c='-1.33e-08',d='2.39e-12',e='-1.5e-16'),
            'beee':resFunc.format(a='0.0108',b='3.25e-05',c='-1.18e-08',d='2.11e-12',e='-1.35e-16'),
            },
        2016:{
            'bb':resFunc.format(a='0.00701',b='3.32e-05',c='-1.29e-08',d='2.73e-12',e='-2.05e-16'),
            'beee':resFunc.format(a='0.0124',b='3.75e-05',c='-1.52e-08',d='3.44e-12',e='-2.85e-16'),
            }
        }

def get_sum_weights(f):
    weights = getattr(f,'EventCounter').Get('weights')
    return weights.GetBinContent(2)-weights.GetBinContent(1)

if args.logx: 
    hbins = np.logspace(np.log10(float(args.xmin)),np.log10(float(args.xmax)),int(args.nbinsx)+1)
    xbins = np.logspace(np.log10(float(args.xmin)),np.log10(float(args.xmax)),int(args.nbinsx)+1)
else: 
    binlist = [args.xmin + i*(args.xmax-args.xmin)/args.nbinsx for i in range(0,args.nbinsx+1)]
    hbins = array.array('d',binlist)
    xbins = np.array(binlist)
hist = R.TH1D('h','',int(args.nbinsx),hbins)

def mc_draw(year):
    if args.x=='vertex_m' and args.do_smear:
        gRand = 'sin(2.0*pi*rndm)*sqrt(-2.0*log(rndm))'
        smear = {
                # 10% for bb 20% for beee
                2016:{'bb':'sqrt(pow(1.10,2)-1)','beee':'sqrt(pow(1.20,2)-1)'},
                # no smearing for bb 15% for beee
                2017:{'bb':'sqrt(pow(1.0,2)-1)','beee':'sqrt(pow(1.15,2)-1)'},
                2018:{'bb':'sqrt(pow(1.0,2)-1)','beee':'sqrt(pow(1.15,2)-1)'},
                }
        # Smear mass = reco mass + reco mass * rand->gaus(0,res(gen mass)*extraSmear)
        if args.category=='all':
            drawThis = 'vertex_m + vertex_m*'+gRand+'*('+\
                    cats['bb']  +'*'+smear[year]['bb']  +'*'+resMass[year]['bb']+' + '+\
                    cats['beee']+'*'+smear[year]['beee']+'*'+resMass[year]['beee']+')'
        elif args.category=='bb':
            drawThis = 'vertex_m + vertex_m*'+gRand+'*'+smear[year]['bb']+'*'+resMass[year]['bb']
        elif args.category=='beee':
            drawThis = 'vertex_m + vertex_m*'+gRand+'*'+smear[year]['beee']+'*'+resMass[year]['beee']
    else:
        if args.x=='lead_pt':
            drawThis = '(lep_pt[0]>lep_pt[1])*lep_pt[0] + (lep_pt[1]>lep_pt[0])*lep_pt[1]'
        elif args.x=='lead_pt_b':
            drawThis = '(lep_pt[0]>lep_pt[1])*(fabs(lep_eta[0])<1.2)*lep_pt[0] + (lep_pt[1]>lep_pt[0])*(fabs(lep_eta[1])<1.2)*lep_pt[1]'
        elif args.x=='lead_pt_e':
            drawThis = '(lep_pt[0]>lep_pt[1])*(fabs(lep_eta[0])>1.2)*lep_pt[0] + (lep_pt[1]>lep_pt[0])*(fabs(lep_eta[1])>1.2)*lep_pt[1]'
        elif args.x=='sub_pt':
            drawThis = '(lep_pt[0]<lep_pt[1])*lep_pt[0] + (lep_pt[1]<lep_pt[0])*lep_pt[1]'
        elif args.x=='sub_pt_b':
            drawThis = '(lep_pt[0]<lep_pt[1])*(fabs(lep_eta[0])<1.2)*lep_pt[0] + (lep_pt[1]<lep_pt[0])*(fabs(lep_eta[1])<1.2)*lep_pt[1]'
        elif args.x=='sub_pt_e':
            drawThis = '(lep_pt[0]<lep_pt[1])*(fabs(lep_eta[0])>1.2)*lep_pt[0] + (lep_pt[1]<lep_pt[0])*(fabs(lep_eta[1])>1.2)*lep_pt[1]'
        elif args.x=='dil_pt_diff':
            drawThis = 'fabs(lep_pt[0]-lep_pt[1])'
        elif args.x=='rel_iso':
            drawThis = 'lep_sumPt / lep_tk_pt'
        elif args.x=='lep_pt':
            drawThis = 'lep_pt[0]'
        else:
            drawThis = args.x
    return drawThis

cats = {
        'all':'(1.)',
        'bb':'(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)',
        'beee':'(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)',
        'ee':'(fabs(lep_eta[0])>1.2 && fabs(lep_eta[1])>1.2)',
        'b':'(fabs(lep_eta)<1.2)',
        'e':'(fabs(lep_eta)>1.2 && fabs(lep_eta)<2.4)',
        }
if args.category=='all':
    sel = args.selection
else:
    sel = cats[args.category]+' && '+args.selection

if args.x=='lead_pt':
    dataDraw = '(lep_pt[0]>lep_pt[1])*lep_pt[0] + (lep_pt[1]>lep_pt[0])*lep_pt[1]'
elif args.x=='lead_pt_b':
    dataDraw = '(lep_pt[0]>lep_pt[1])*(fabs(lep_eta[0])<1.2)*lep_pt[0] + (lep_pt[1]>lep_pt[0])*(fabs(lep_eta[1])<1.2)*lep_pt[1]'
elif args.x=='lead_pt_e':
    dataDraw = '(lep_pt[0]>lep_pt[1])*(fabs(lep_eta[0])>1.2)*lep_pt[0] + (lep_pt[1]>lep_pt[0])*(fabs(lep_eta[1])>1.2)*lep_pt[1]'
elif args.x=='sub_pt':
    dataDraw = '(lep_pt[0]<lep_pt[1])*lep_pt[0] + (lep_pt[1]<lep_pt[0])*lep_pt[1]'
elif args.x=='sub_pt_b':
    dataDraw = '(lep_pt[0]<lep_pt[1])*(fabs(lep_eta[0])<1.2)*lep_pt[0] + (lep_pt[1]<lep_pt[0])*(fabs(lep_eta[1])<1.2)*lep_pt[1]'
elif args.x=='sub_pt_e':
    dataDraw = '(lep_pt[0]<lep_pt[1])*(fabs(lep_eta[0])>1.2)*lep_pt[0] + (lep_pt[1]<lep_pt[0])*(fabs(lep_eta[1])>1.2)*lep_pt[1]'
elif args.x=='dil_pt_diff':
    dataDraw = 'fabs(lep_pt[0]-lep_pt[1])'
elif args.x=='rel_iso':
    dataDraw = 'lep_sumPt / lep_tk_pt'
elif args.x=='lep_pt':
    dataDraw = 'lep_pt[0]'
else:
    dataDraw = args.x

# Make Data histograms
totData = hist.Clone('totData')
dataHists = {year:{} for year in allyears}
for year in allyears:
    #data_sel = sel+(' && '+args.data_sel if args.data_sel else '')
    if args.tdir=='our':
        #data_sel = '(vertex_m>120 && '+sel+(' && '+args.data_sel if args.data_sel else '')+')'
        data_sel = '('+sel+(' && '+args.data_sel if args.data_sel else '')+')'
    elif args.tdir=='ourcommonpre':
        if args.prescale_weight=='mc':
            data_sel = '(vertex_m<120 && '+sel+(' && '+args.data_sel if args.data_sel else '')+')'
        elif args.prescale_weight=='data':
            if year==2016:
                data_sel = '(vertex_m<120 && '+sel+(' && '+args.data_sel if args.data_sel else '')+')*320'
            elif year==2017:
                data_sel = '(vertex_m<120 && '+sel+(' && '+args.data_sel if args.data_sel else '')+')*561'
            elif year==2018:
                data_sel = '(vertex_m<120 && '+sel+(' && '+args.data_sel if args.data_sel else '')+')*500'
    f = R.TFile(info[year]['path']+info[year]['file'])
    t = f.Get(info[year][args.tdir]['dir']+'/t')
    hdata = hist.Clone('hdata')
    t.Draw(dataDraw+'>>hdata',data_sel,'pe')
    hdata.SetDirectory(0)
    dataHists[year] = hdata
    dataHists[year].SetDirectory(0)
    f.Close()
    # Combine into a total
    totData.SetDirectory(0)
    totData.Add(dataHists[year])

# Make MC histograms
# Combine MC histograms
def mc_cut_weight(year,name):
    mcCutWeight = '('+sel+')'
    if year!=2016 and args.nnpdf30 and name in nnpdf_to_rescale[year][args.tdir]:
        if args.tdir=='our':
            mcCutWeight += '*('+toNNPDF30[year][args.tdir][name][args.category]+'*(gen_res_mass>120)+(gen_res_mass<120)*(1.))'
        elif args.tdir=='ourcommonpre' or args.tdir=='ourpre':
            mcCutWeight += '*('+toNNPDF30[year][args.tdir][name][args.category]+')'
    if args.order=='nnlo' and args.nnpdf30 and name=='powheg':
        # relies on the nnpdf3.0 reweight for 2017 and 2018 MC
        if args.tdir=='our':
            mcCutWeight += '*('+kFunction[args.tdir][args.category]+'*(gen_res_mass>120)+(gen_res_mass<120)*(1.))'
        elif args.tdir=='ourcommonpre' or args.tdir=='ourpre':
            mcCutWeight += '*(1.)'
    mcCutWeight += '*genWeight'
    return mcCutWeight

mc_int_sum = 0.
mc_ent_sum = 0.
mc_err2_sum = 0.
totMC = hist.Clone('totMC')
#hist_sums = {year:hist.Clone('hmc_'+str(year)) for year in allyears}
hist_sums = {name:hist.Clone(name) for name in mcDrawOrder}
hists = {year:{name:{mc:{} for mc in allMCs[year][name]} for name in mcDrawOrder} for year in allyears}
for name in mcDrawOrder:
    # Do Jets separately
    if name=='jets': continue
    # Draw and scale MC
    for year in allyears:
        for mc in allMCs[year][name]:
            mcFile = R.TFile(info[year]['mcpath']+'ana_datamc_'+mc+'.root')
            hmcname = 'h'+str(year)+'_'+mc
            hmc = hist.Clone(hmcname)
            if year==2018:
                if name in ['amcatnlo','madgraph']:
                    mcTree = mcFile.Get(info[2017][args.tdir]['dir']+'/t')
                else:
                    dirname = 'Our2018MuPrescaledMuonsOppSignNtuple' if args.tdir=='ourcommonpre' else 'Our2018MuonsOppSignNtuple'
                    mcTree = mcFile.Get(dirname+'/t')
            else:
                mcTree = mcFile.Get(info[year][args.tdir]['dir']+'/t')
            mcTree.SetAlias('gen_lead_pt','(gen_lep_pt[0]*(gen_lep_pt[0]>gen_lep_pt[1]) + gen_lep_pt[1]*(gen_lep_pt[1]>gen_lep_pt[0]))')
            mcTree.Draw(mc_draw(year)+'>>'+hmcname,mc_cut_weight(year,name),'')
            hmc.SetDirectory(0)
            hists[year][name][mc] = hmc
            hists[year][name][mc].SetDirectory(0)
            info[year]['mc'][mc].sum_weights = get_sum_weights(mcFile)
            mcFile.Close()
            # Scale by (cross section / sum weights) * lumi * RZ0
            # Combine into a total
            scale_by = info[year]['mc'][mc].cross_section / float(info[year]['mc'][mc].sum_weights)
            scale_by *= info[year]['lumi']# / info[year][args.tdir]['pre']
            # If desired, scale MC to prescale found in data
            scale_by *= (1./info[year][args.tdir]['pre']) if args.prescale_weight=='mc' else 1.0
            if args.scaleZ0: scale_by *= info[year]['ratioZ0'][args.category]
            hists[year][name][mc].Scale(scale_by)
            hist_sums[name].SetDirectory(0)
            hist_sums[name].Add(hists[year][name][mc])
    totMC.SetDirectory(0)
    totMC.Add(hist_sums[name])

# Make Fake-Rate histograms
if args.do_fake_rate:
    for year in allyears:
        if year!=2016:
            frfile = R.TFile(info[year][args.tdir]['FR'][args.category])
            frhist_orig = frfile.Get('TotalJets').Clone()
        else:
            frfile = R.TFile(info[year][args.tdir]['FR'])
            jetname = 'jets'
            if args.category=='bb': jetname = jetname+'BB'
            elif args.category=='beee': jetname = jetname+'BE'
            frhist_orig = frfile.Get(jetname)
        frhist = hist.Clone('FakeRate_'+args.category)
        for ibin in range(1,frhist.GetNbinsX()+1):
            start = frhist_orig.FindBin(frhist.GetBinLowEdge(ibin))
            end = frhist_orig.FindBin(frhist.GetBinLowEdge(ibin+1))
            isum = 0.
            for jbin in range(start,end):
                isum += frhist_orig.GetBinContent(jbin)
            frhist.SetBinContent(ibin,isum)
        frhist.SetDirectory(0)
        hists[year]['jets']['jets'] = frhist
        hists[year]['jets']['jets'].SetDirectory(0)
        hist_sums['jets'].Add(hists[year]['jets']['jets'])
        hist_sums['jets'].SetDirectory(0)
        frfile.Close()
        totMC.Add(hists[year]['jets']['jets'])
        totMC.SetDirectory(0)

#############################
## Calculate uncertainties ##
#############################

if args.do_uncert:
    #mass_scale_func = 'fabs(-0.001792 + 2.484e-6 * x - 4.795e-9 * x * x)'
    #mass_scale = R.TF1('mass_scale',mass_scale_func,60,6000)
    dy_pdf_func = '6.68537e-3 + 2.54218e-5 * pow(x,1) - 1.09503e-8 * pow(x,2) + 1.97141e-12 * pow(x,3)'
    dy_pdf = R.TF1('dy_pdf',dy_pdf_func,60,6000)

    tot_sums = {name:0. for name in mcDrawOrder+['total']}
    uncert_sums = {name:0. for name in mcDrawOrder+['total']}
    h = hist.Clone('mc_uncert')
    xlist = []
    ylist = []
    xerrlist = []
    yerrlist = []
    if args.overflow:
        nbins= h.GetNbinsX()+2
    else:
        nbins= h.GetNbinsX()+1
    for ibin in range(1,nbins):
        ix = hist.GetXaxis().GetBinCenter(ibin)
        bw = hist.GetBinWidth(ibin)
        xlist.append(ix)
        ylist.append(0.)
        xerrlist.append(hist.GetXaxis().GetBinWidth(ibin))
        #allerr2 = pow(mass_scale.Eval(ix),2)   + pow(0.05,2)          + pow(0.01,2)  + pow(0.03,2) 
        #allerr2 = pow(0.01,2) + pow(0.05,2) + pow(0.01,2) + pow(0.01,2) + pow(0.02,2)
        # ************
        # These uncertainties are for purely illustrative purposes in the ratio panel of the mass
        # plot and for reasonable-enough looking numbers in the yield tables. Their accuracy should
        # be taken with a grain of salt. 
        # ************
        # Uncertainties:
        # ************
        # * DY PDF:
        #   * Function
        #   * Correlated for all three years
        # * Non-DY cross sections:
        #   * +/- 7%
        #   * Correlated for all three years
        # * Jet Background
        #   * +/- 50% for 2016, +/- 100% for 2017+2018
        #   * Correlated for all three years
        # * Mass scale: 
        #   * +/- 1% for all three years
        #   * 2017+2018 correlated and uncorrelated with 2016
        #   * Caveats: this is actually a one-sided shift in the mass, not an up/down shift in the yield. 
        #              I'm simplifying things to a single +/- 1% uncertainty because the largest shifts 
        #              are at > 6 TeV and the bulk of events are < 3 TeV where the scale uncertainty is 
        #              negligible. For details see Min's study: 
        #              https://indico.cern.ch/event/829944/#2-reconstruction-selection-and
        #              Also, assuming 1% is valid for < 4 TeV in 2016 which is really isn't.
        # * Z-normalization: 
        #   * +/- 5% for all three years
        #   * Correlated for all three years
        # * ID efficiency: 
        #   # +/- 1% for all three years
        #   * Correlated for all three years
        # * Trigger efficiency: 
        #   * +/- 1% for all three years
        #   * Correlated for all three years
        # * Reco efficiency: 
        #   * +/- 1% BB, +/- 2% BEEE, +/- 2% All
        #   * Correlated for all three years
        #   * Caveats: This is also a one-sided uncertainty that I'm simplifying to a symmetric one.
        #              This uncertainty is also uncorrelated between BB and BE+EE categories but I 
        #              ignore that for now. Accounting for the correlations/uncorrelations for this 
        #              uncertainty introduces negligible corrections compared to the 5% Z-norm, 
        #              7% non-DY yield, and DY PDF contributions. 
        # ************
        # For uncorrelated uncertainties between 16 and 17+18 we use the luminosity ratio for simplicity
        # * (2017+2018) / (2016+2017+2018) = (42.1+61.3)/(139.7) = 0.740 ~= 3/4
        # * 2016 / (2016+2017+2018) = 36.3 / 139.7 = 0.260 ~= 1/4
        # * Assuming, err(16) = err(17+18)
        # * rel err = sqrt( pow(1/4,2)*err(16)^2 + pow(3/4,2)*err(17+18)^2 + (3/4)*(1/4)*err(16)*err(17+18) )
        #           = err * sqrt( 13/16 ) 
        # ************
        corrErr2 = pow(0.05,2) + pow(0.01,2) + pow(0.01,2) + pow(0.02,2)
        uncorrErr2 = (13/16)*pow(0.01,2)
        allerr2 = corrErr2 + uncorrErr2
        # Drell-Yan errors (additional PDF uncertainties with DY)
        dybin = hist_sums['powheg'].GetBinContent(ibin)
        if dybin<0:
            print ix,dybin
        reldyerr2 = pow(dy_pdf.Eval(ix),2)
        idyerr = dybin*math.sqrt( reldyerr2 )
        uncert_sums['powheg'] += math.sqrt( pow(idyerr,2) + pow(dybin,2)*allerr2 )
        tot_sums['powheg'] += math.sqrt( pow(idyerr,2) )
        # non-DY errors (additional 7% on non-DY estimate)
        nondysum = 0.
        relnondyerr2 = pow(0.07,2)
        for nondy in cols['nonDY']:
            thisbin = hist_sums[nondy].GetBinContent(ibin)
            if thisbin<0: 
                #print '*'*15,ix,nondy,thisbin
                thisbin = 0.
            nondysum += thisbin
            uncert_sums[nondy] += thisbin*math.sqrt(relnondyerr2 + allerr2 )
            tot_sums[nondy] += thisbin*math.sqrt(relnondyerr2)
        inonerr = nondysum*math.sqrt( relnondyerr2 )
        # Jets errors
        if args.do_fake_rate:
            jetbin = hist_sums['jets'].GetBinContent(ibin)
            if year==2017 and ix==1712.5 and args.category=='bb':
                jeterr = 0
            else:
                # 0.88 = (0.5*36.3 + 42.1 + 63.1) / 140
                jeterr = 0.88*jetbin
            uncert_sums['jets'] += jeterr
            tot_sums['jets'] += jeterr
        else:
            jeterr = 0.
        # Total err
        #print ix,(dybin,idyerr),(nondysum,inonerr),(jetbin,jeterr)
        # Include jet contribution to uncertainty
        total = sum([hist_sums[name].GetBinContent(ibin) for name in mcDrawOrder if hist_sums[name].GetBinContent(ibin)>0])
        if total<=0:
            print '*'*15,ix,total,dybin,nondysum,jetbin
        toterr = math.sqrt(pow(idyerr,2) + pow(inonerr,2) + pow(jeterr,2) + pow(total,2)*allerr2 )
        #print ibin,ix,(total,toterr),(dybin,idyerr),(nondysum,inonerr),(jetbin,jeterr)
        # Remove jet contribution to uncertainty
        #total = sum([hist_sums[name].GetBinContent(ibin) for name in mcDrawOrder if name!='jets']) # this total is only used to compute relative uncertainty
        #toterr = math.sqrt(pow(idyerr,2) + pow(inonerr,2) + pow(total,2)*allerr2 )
        uncert_sums['total'] += toterr
        reltoterr = toterr/total
        yerrlist.append(reltoterr)
    x = np.array(xlist)
    y = np.array(ylist)
    xerr = np.array(xerrlist)
    yerr = np.array(yerrlist)
    total_uncert = R.TGraphErrors(len(x),x,y,xerr,yerr)

#####################################################################
## Do logging before dividing by bin width, making cumulative, etc ##
#####################################################################

lumberjack.setup_logger(args.name,args.where+'/'+args.name+'.log')
logger = logging.getLogger(args.name)
logger.info(args)
logger.info('\n'+'*'*15+'\n')
logger.info(args.x+' '+args.category+' '+args.selection)
logger.info('\n'+'*'*15+'\n')
logger.info('Binning')
logger.info(int(args.nbinsx))
logger.info(xbins)
for year in allyears:
    logger.info('\n'+'*'*15+'\n')
    logger.info(str(year)+' Data Integral '+str(dataHists[year].Integral()))
logger.info('\n'+'*'*15+'\n')
logger.info('MC')
logger.info('\n'+'*'*15+'\n')
if args.do_smear:logger.info('Additional dimuon mass resolution mearing applied to all MC')
for year in allyears:
    logger.info(str(year)+'\n'+mc_draw(year))
logger.info('\n'+'*'*15+'\n')
stats = {name:0. for name in mcDrawOrder+['other']}
for name in mcDrawOrder:
    logger.info('\n'+'*'*30+'\n')
    logger.info(name)
    logger.info('*'*15)
    if not args.do_fake_rate: logger.info(mc_cut_weight(year,name))
    if args.order=='nnlo' and args.nnpdf30 and name=='powheg' and args.tdir=='our':
        #logger.info('\n'+'*'*15+'\n')
        logger.info('*'*15)
        logger.info('NNLO k-function')
        logger.info(kFunction[args.tdir][args.category])
        #logger.info('\n'+'*'*15+'\n')
    thisTotal = 0.
    for year in allyears:
        logger.info('*'*15)
        if name=='jets':
            stats[name] += hists[year][name][name].Integral()
            logger.info(str(year)+' Data-Driven Jets '+str(hists[year][name][name].Integral()))
        else:
            if year!=2016 and name in toNNPDF30[year][args.tdir].keys() and args.nnpdf30:
                logger.info('NNPDF30 scaling')
                logger.info(toNNPDF30[year][args.tdir][name][args.category])
            txt = '{:4} {:21} {:17} {:10} {:10}'.format('Year','MC Sample','Yield','XS','Sum Weights')
            logger.info(txt)
            for mc in allMCs[year][name]:
                txt = '{:4} {:21} {:17} {:10} {:10}'.format(str(year),mc,str(hists[year][name][mc].Integral()),str(info[year]['mc'][mc].cross_section),str(info[year]['mc'][mc].sum_weights))
                logger.info(txt)
                if args.overflow:
                    stats[name] += hists[year][name][mc].Integral(1,hists[year][name][mc].GetNbinsX()+1)
                else:
                    stats[name] += hists[year][name][mc].Integral()
                if name in ['ttbar','diboson','tautau','singletop']:
                    if args.overflow:
                        stats['other'] += hists[year][name][mc].Integral()
                    else:
                        stats['other'] += hists[year][name][mc].Integral()
    logger.info('*'*15)
    logger.info('Total '+name+' Yield '+str(stats[name]))
    if args.do_uncert: logger.info('Total '+name+' Uncert '+str(uncert_sums[name]))
logger.info('\n'+'*'*30+'\n')
logger.info('Integrated Luminosity')
for year in allyears:
    logger.info(str(year)+' : '+str(info[year]['lumi']))
if args.scaleZ0:
    logger.info('\nZ-peak Data / MC Ratio')
    for year in allyears:
        logger.info(str(year)+' : '+str(info[year]['ratioZ0']))

data_int = totData.Integral()
mc_int = totMC.Integral()

if args.do_uncert:
    logger.info('\n'+'*'*30+'\n')
    logger.info('Background Yield Uncertainties')
    logger.info('*'*15)
    logger.info('Uncertainties for all MC')
    logger.info('3% for acc x eff, 1% for Z-normalization, 1% for trigger')
    #logger.info('Mass resolution & scale function : '+mass_scale_func)
    logger.info('*'*15)
    logger.info('Uncertainties for DY MC')
    logger.info('PDF uncertainty : '+dy_pdf_func)
    logger.info('*'*15)
    logger.info('Uncertainties for non-DY MC (prompt)')
    logger.info('7% for all prompt MC')
    logger.info('50% for data-driven Jets')
    logger.info('*'*15)
    logger.info('(Mass dependent uncertainties evaluated at bin center)')
    logger.info('*'*15)
    logger.info('Relative Uncertainty vs Mass')
    logger.info('\n'.join(['{:7.2f}\t{:6.4f}'.format(b,y) for i,(b,y) in enumerate(zip(xbins,yerr))]))

logger.info('\n'+'*'*30+'\n')
if args.do_fake_rate:
    logger.info('{data:>9} {mc:>9} | {dy:>9} {oth:>9} {jets:>9} | {tt:>9} {dib:>9} {st:>9} {tau:>9}'.format(data='Data',mc='MC Total',dy='Drell-Yan',oth='Non-DY',jets='Jets',tt='t-tbar',dib='Diboson',st='Single-Top',tau='tau-tau'))
    txtdat = '{data:>9.2f} {mc:>9.2f} | {dy:>9.2f} {oth:9.2f} {jets:9.2f} | {tt:>9.2f} {dib:>9.2f} {st:>9.2f} {tau:>9.2f}'
    logger.info(txtdat.format(data=totData.Integral(),mc=totMC.Integral(),dy=stats['powheg'],oth=stats['other'],jets=stats['jets'],tt=stats['ttbar'],dib=stats['diboson'],st=stats['singletop'],tau=stats['tautau']))
    #txtdattable = 'XXXX {data:>9.2f} & {mc:>9.2f} & $\pm$ & {mcunc:>5.0f} & {dy:>9.2f} & $\pm$ & {dyunc:>5.0f} & {oth:9.2f} & $\pm$ & {othunc:9.2f} & {jets:9.2f} & $\pm$ & {jetunc:>5.0f} \\\\'
    txtdattable = 'XXXX {data:>9} & {mc:>9} & $\pm$ & {mcunc:>5} & {dy:>9} & $\pm$ & {dyunc:>5} & {oth:>9} & $\pm$ & {othunc:>9} & {jets:>4} & $\pm$ & {jetunc:>4} \\\\'
elif '60_120' in args.name:
    txtdattable = 'XXXX {data:>9} & {mc:>9} & $\pm$ & {mcunc:>5} & {dy:>9} & $\pm$ & {dyunc:>5} & {oth:>9} & $\pm$ & {othunc:>9} & {jets:>4} & $/$ & {jetunc:>4} \\\\'
else:
    logger.info('{data:>9} {mc:>9} | {dy:>9} {oth:>9} | {tt:>9} {dib:>9} {st:>9} {tau:>9}'.format(data='Data',mc='MC Total',dy='Drell-Yan',oth='Non-DY',tt='t-tbar',dib='Diboson',st='Single-Top',tau='tau-tau'))
    logger.info('{data:>9.2f} {mc:>9.2f} | {dy:>9.2f} {oth:9.2f} | {tt:>9.2f} {dib:>9.2f} {st:>9.2f} {tau:>9.2f}'.format(data=totData.Integral(),mc=totMC.Integral(),dy=stats['powheg'],oth=stats['other'],tt=stats['ttbar'],dib=stats['diboson'],st=stats['singletop'],tau=stats['tautau']))
    logger.info('{data:>9.2f} {mc:>9.2f} | {dy:>9.2f} {oth:9.2f} | {tt:>9.2f} {dib:>9.2f} {st:>9.2f} {tau:>9.2f}'.format(data=totData.Integral(),mc=totMC.Integral(),dy=stats['powheg'],oth=stats['other'],tt=stats['ttbar'],dib=stats['diboson'],st=stats['singletop'],tau=stats['tautau']))
    txtdattable = ''

if args.do_uncert:
    logger.info('Total uncertainty '+str(uncert_sums['total']))

logger.info('\n'+'*'*15+'\n')
r,l,h = clopper_pearson_poisson_means(data_int,mc_int)
logger.info('Data / MC')
logger.info('{d} / {mc} = {rat}'.format(d=data_int, mc=mc_int, rat=r))#, err1=err1, err2=(h-r + r-l)/2))
tau = 1.0 # data/mc 'should' be one
p_bi = R.TMath.BetaIncomplete(1./(1+tau),data_int,int(mc_int)+1)
z_bi = math.sqrt(2)*R.TMath.ErfInverse(1-2*p_bi)
logger.info('P-value : '+str(p_bi)+'\nZ-value : '+str(z_bi))
logger.info('\n'+'*'*15+'\n')
if args.do_uncert:
    if '1800_4000' in args.name:
        totalunc = math.sqrt(sum([pow(tot_sums[m],2) for m in ['powheg','ttbar','diboson','singletop','tautau','jets']])+pow(totMC.Integral(1,hists[year][name][mc].GetNbinsX()+1),2)*allerr2)
    else:
        if args.do_fake_rate:
            totalunc = math.sqrt(sum([pow(tot_sums[m],2) for m in ['powheg','ttbar','diboson','singletop','tautau','jets']])+pow(totMC.Integral(),2)*allerr2)
        else:
            totalunc = math.sqrt(sum([pow(tot_sums[m],2) for m in ['powheg','ttbar','diboson','singletop','tautau']])+pow(totMC.Integral(),2)*allerr2)
    if '60_120' in args.name: logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),3),mcunc=round_to_n(totalunc,3),dy=round_to_n(stats['powheg'],3),dyunc=round_to_n(uncert_sums['powheg'],2),oth=round_to_n(stats['other'],3),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),2),jets='',jetunc=''))
    elif '120_400' in args.name:
        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),3),mcunc=round_to_n(totalunc,3),dy=round_to_n(stats['powheg'],3),dyunc=round_to_n(uncert_sums['powheg'],2),oth=round_to_n(stats['other'],3),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),2),jets=round_to_n(stats['jets'],3),jetunc=round_to_n(uncert_sums['jets'],2)))
    elif '400_600' in args.name:
        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),3),mcunc=round_to_n(totalunc,3),dy=round_to_n(stats['powheg'],3),dyunc=round_to_n(uncert_sums['powheg'],2),oth=round_to_n(stats['other'],3),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),2),jets=round_to_n(stats['jets'],3),jetunc=round_to_n(uncert_sums['jets'],2)))
    elif '600_900' in args.name:
        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),3),mcunc=round_to_n(totalunc,3),dy=round_to_n(stats['powheg'],3),dyunc=round_to_n(uncert_sums['powheg'],2),oth=round_to_n(stats['other'],3),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),2),jets=round_to_n(stats['jets'],3),jetunc=round_to_n(uncert_sums['jets'],2)))
    elif '900_1300' in args.name:
        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),3),mcunc=round_to_n(totalunc,3),dy=round_to_n(stats['powheg'],3),dyunc=round_to_n(uncert_sums['powheg'],2),oth=round_to_n(stats['other'],3),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),2),jets=round_to_n(stats['jets'],3),jetunc=round_to_n(uncert_sums['jets'],2)))
    elif '1300_1800' in args.name:
        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),3),mcunc=round_to_n(totalunc,3),dy=round_to_n(stats['powheg'],3),dyunc=round_to_n(uncert_sums['powheg'],2),oth=round_to_n(stats['other'],3),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),2),jets=round_to_n(stats['jets'],3),jetunc=round_to_n(uncert_sums['jets'],2)))
    elif '1800_4000' in args.name:
        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(1,hists[year][name][mc].GetNbinsX()+1),3),mcunc=round_to_n(totalunc,3),dy=round_to_n(stats['powheg'],3),dyunc=round_to_n(uncert_sums['powheg'],2),oth=round_to_n(stats['other'],3),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),2),jets=round_to_n(stats['jets'],3),jetunc=round_to_n(uncert_sums['jets'],2)))
#    if '60_120' in args.name: logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),7),mcunc=round_to_n(totalunc,5),dy=round_to_n(stats['powheg'],6),dyunc=round_to_n(uncert_sums['powheg'],5),oth=round_to_n(stats['other'],6),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),5),jets=round_to_n(stats['jets'],4),jetunc=round_to_n(uncert_sums['jets'],4)))
#    elif '120_400' in args.name:
#        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),7),mcunc=round_to_n(totalunc,5),dy=round_to_n(stats['powheg'],6),dyunc=round_to_n(uncert_sums['powheg'],5),oth=round_to_n(stats['other'],6),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),5),jets=round_to_n(stats['jets'],4),jetunc=round_to_n(uncert_sums['jets'],4)))
#    elif '400_600' in args.name:
#        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),5),mcunc=round_to_n(totalunc,4),dy=round_to_n(stats['powheg'],5),dyunc=round_to_n(uncert_sums['powheg'],4),oth=round_to_n(stats['other'],5),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),4),jets=round_to_n(stats['jets'],3),jetunc=round_to_n(uncert_sums['jets'],3)))
#    elif '600_900' in args.name:
#        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),4),mcunc=round_to_n(totalunc,3),dy=round_to_n(stats['powheg'],4),dyunc=round_to_n(uncert_sums['powheg'],3),oth=round_to_n(stats['other'],4),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),3),jets=round_to_n(stats['jets'],3),jetunc=round_to_n(uncert_sums['jets'],3)))
#    elif '900_1300' in args.name:
#        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),4),mcunc=round_to_n(totalunc,3),dy=round_to_n(stats['powheg'],4),dyunc=round_to_n(uncert_sums['powheg'],3),oth=round_to_n(stats['other'],4),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),3),jets=round_to_n(stats['jets'],3),jetunc=round_to_n(uncert_sums['jets'],3)))
#    elif '1300_1800' in args.name:
#        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),3),mcunc=round_to_n(totalunc,3),dy=round_to_n(stats['powheg'],3),dyunc=round_to_n(uncert_sums['powheg'],3),oth=round_to_n(stats['other'],3),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),3),jets=round_to_n(stats['jets'],2),jetunc=round_to_n(uncert_sums['jets'],2)))
#    elif '1800_4000' in args.name:
#        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(1,hists[year][name][mc].GetNbinsX()+1),3),mcunc=round_to_n(totalunc,3),dy=round_to_n(stats['powheg'],3),dyunc=round_to_n(uncert_sums['powheg'],3),oth=round_to_n(stats['other'],3),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),3),jets=round_to_n(stats['jets'],2),jetunc=round_to_n(uncert_sums['jets'],2)))
#    if '120_400' in args.name:
#        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),7),mcunc=round_to_n(uncert_sums['total'],5),dy=round_to_n(stats['powheg'],6),dyunc=round_to_n(uncert_sums['powheg'],5),oth=round_to_n(stats['other'],6),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),5),jets=round_to_n(stats['jets'],4),jetunc=round_to_n(2*stats['jets'],4)))
#    elif '400_600' in args.name:
#        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),5),mcunc=round_to_n(uncert_sums['total'],4),dy=round_to_n(stats['powheg'],5),dyunc=round_to_n(uncert_sums['powheg'],4),oth=round_to_n(stats['other'],5),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),4),jets=round_to_n(stats['jets'],3),jetunc=round_to_n(2*stats['jets'],3)))
#    elif '600_900' in args.name:
#        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),4),mcunc=round_to_n(uncert_sums['total'],3),dy=round_to_n(stats['powheg'],4),dyunc=round_to_n(uncert_sums['powheg'],3),oth=round_to_n(stats['other'],4),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),3),jets=round_to_n(stats['jets'],3),jetunc=round_to_n(2*stats['jets'],3)))
#    elif '900_1300' in args.name:
#        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),4),mcunc=round_to_n(uncert_sums['total'],3),dy=round_to_n(stats['powheg'],4),dyunc=round_to_n(uncert_sums['powheg'],3),oth=round_to_n(stats['other'],4),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),3),jets=round_to_n(stats['jets'],3),jetunc=round_to_n(2*stats['jets'],3)))
#    elif '1300_1800' in args.name:
#        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(),3),mcunc=round_to_n(uncert_sums['total'],3),dy=round_to_n(stats['powheg'],3),dyunc=round_to_n(uncert_sums['powheg'],3),oth=round_to_n(stats['other'],3),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),3),jets=round_to_n(stats['jets'],2),jetunc=round_to_n(2*stats['jets'],2)))
#    elif '1800_4000' in args.name:
#        logger.info(txtdattable.format(data=int(totData.Integral()),mc=round_to_n(totMC.Integral(1,hists[year][name][mc].GetNbinsX()+1),3),mcunc=round_to_n(uncert_sums['total'],3),dy=round_to_n(stats['powheg'],3),dyunc=round_to_n(uncert_sums['powheg'],3),oth=round_to_n(stats['other'],3),othunc=round_to_n(sum([uncert_sums[a] for a in ['ttbar','diboson','singletop','tautau']]),3),jets=round_to_n(stats['jets'],2),jetunc=round_to_n(2*stats['jets'],2)))

##############################
## Plotter pretty functions ##
##############################

def pretty(arg):
    ret = {
        'vertex_m':'m(#mu^{+}#mu^{#font[122]{\55}}) [GeV]',
        'cos_angle':'cos(#alpha)',
        'dil_pt':'p_{T}(#mu^{+}#mu^{#font[122]{\55}}) [GeV]',
        'lead_pt':'leading muon p_{T} [GeV]',
        'sub_pt':'sub-leading muon p_{T} [GeV]',
        'dil_rap':'y (#mu^{+}#mu^{#font[122]{\55}})',
        'lep_pt':'p_{T}(#mu) [GeV]',
        'n_dils':'N(#mu^{+}#mu^{#font[122]{\55}}) passing selection',
        'nvertices':'N(primary vertices)',
        'lep_Mu27_triggerMatchPt':'Mu27 trigger match p_{T}(#mu) [GeV]',
        'lep_pz':'p_{Z}(#mu) [GeV]',
        'lep_eta':'#eta(#mu)',
        'lep_phi':'#phi(#mu)',
        'rel_iso':'rel. trk. iso.',
        'dil_pt_diff':'|#Delta p_{T}(#mu)|',
        }
    return ret[arg]
    #for val in ret.keys():
    #    if val in arg: return ret[val]

def mc_stuff(name):
    # My style
    if 'powheg'==name:
        #return '#gamma/Z #rightarrow #mu^{+}#mu^{-} (POWHEG)',R.kAzure+1
        return '#gamma*/Z #rightarrow #mu^{#plus}#mu#lower[-0.4]{^{#minus}}',R.kAzure+1,R.TColor.GetColor('#99ccff')
    if 'madgraph'==name:
        return '#gamma/Z #rightarrow #mu^{+}#mu^{#font[122]{\55}} (MadGraph MLM)',R.kAzure+1
    if 'amcatnlo'==name:
        return '#gamma/Z #rightarrow #mu^{+}#mu^{#font[122]{\55}} (aMC@NLO FxFx)',R.kAzure+1
    if 'ht'==name:
        return '#gamma/Z #rightarrow #mu^{+}#mu^{#font[122]{\55}} (HT-bin MADGRAPH)',R.kAzure+1
    if 'ttbar'==name:
        return 't#bar{t}',R.kRed-4
    if 'singletop'==name:
        return 'single top', R.kViolet+1
    if 'diboson'==name:
        return 'diboson', R.kGreen+1
    if 'Wjets'==name:
        return 'Jets',R.kOrange+1
    if 'tautau'== name:
        return '#gamma/Z #rightarrow #tau^{+}#tau^{#font[122]{\55}}',R.kBlue+1
    # Paper style
    if 'dypaper'==name:
        return '#gamma*/Z #rightarrow #mu^{#plus}#mu#lower[-0.4]{^{#minus}}',R.TColor.GetColor('#99ccff')
    if 'nonDY'==name:
        return 't#bar{t}, tW, WW, WZ, ZZ, #tau#tau',R.TColor.GetColor('#ff6666')
    if 'jets'==name:
        return 'Jets',R.TColor.GetColor('#ffff66')
    # other
    if name==2016:
        return '80X Simulation', R.kRed-4
    if name==2017:
        return '94X Simulation', R.kViolet+1
    if name==2018:
        return '102X Simulation', R.kAzure+1


def get_color(name):
    # paper style
    if name=='nonDY':
        return mc_stuff('nonDY')[1]
    elif name=='dypaper':
        return mc_stuff('dypaper')[1]
    elif name=='jets':
        return mc_stuff('jets')[1]
    else: # My style
        return mc_stuff(name)[1]

################################
## Make stacked mc histograms ##
################################

if args.do_stack:
    s = R.THStack('s','')
    if args.do_paper:
        paper_sums = {col:hist.Clone(col+'_paper') for col in paperDrawOrder}
        for col in paperDrawOrder:
            for name in cols[col]:
                paper_sums[col].Add(hist_sums[name])
            paper_sums[col].SetLineWidth(1)
            paper_sums[col].SetMarkerStyle(0)
            paper_sums[col].SetFillColor(get_color(col))
            paper_sums[col].SetLineColor(R.kBlack)
            if args.overflow: move_overflow_into_last_bin(paper_sums[col])
            if args.bin_width: divide_bin_width(paper_sums[col])
            elif args.cumulative: paper_sums[col] = cumulative_histogram(paper_sums[col],overflow=args.overflow)
            s.Add(paper_sums[col])
    else:
        for name in mcDrawOrder:
            hist_sums[name].SetLineWidth(1)
            hist_sums[name].SetMarkerStyle(0)
            hist_sums[name].SetFillColor(get_color(name))
            hist_sums[name].SetLineColor(get_color(name))
            if args.overflow: move_overflow_into_last_bin(hist_sums[name])
            if args.bin_width: divide_bin_width(hist_sums[name])
            elif args.cumulative: hist_sums[name] = cumulative_histogram(hist_sums[name],overflow=args.overflow)
            s.Add(hist_sums[name])

#################################################
## Divide by bin width, making cumulative, etc ##
#################################################

if args.overflow and not args.bin_width:
    move_overflow_into_last_bin(totMC)
    move_overflow_into_last_bin(totData)
#gdata = poisson_intervalize(totData,bin_width=False,zero_ex=True)
if args.bin_width:
    if args.overflow:
        move_overflow_into_last_bin(totMC)
        move_overflow_into_last_bin(totData)
    gdata = poisson_intervalize(totData,bin_width=args.bin_width,zero_ex=True)
elif args.cumulative:
    totMC = cumulative_histogram(totMC,noerr=True,overflow=args.overflow)
    totData = cumulative_histogram(totData,overflow=args.overflow)
    gdata = poisson_intervalize(totData,bin_width=False,zero_ex=True)
else:
    gdata = poisson_intervalize(totData,bin_width=False,zero_ex=True)
if args.do_paper: gdata.SetMarkerSize(0.9)

##################################
## Finally draw the final plots ##
##################################

# Make Canvas
totLumi = sum([info[year]['lumi']/1000. for year in allyears])
lumi = '{:4.1f}'.format(totLumi) if len(allyears)==1 else '{:3.0f}'.format(totLumi)
if args.do_paper:
    canvas = Plotter.Canvas(lumi='{lumi}'.format(lumi=lumi)+' fb^{-1} (13 TeV)',extra='Preliminary',ratioFactor=0.23,logy=args.logy,cWidth=1000,cHeight=1000,cmsPaper=True)
else:
    canvas = Plotter.Canvas(lumi='{lumi}'.format(lumi=lumi)+' fb^{-1} (13 TeV)',extra='Preliminary',ratioFactor=1./4,logy=args.logy,cWidth=800,cHeight=600)
    #canvas = Plotter.Canvas(lumi='{lumi}'.format(lumi=lumi)+' fb^{-1} (13 TeV)',extra='Preliminary',ratioFactor=1./3,logy=args.logy,cWidth=800,cHeight=600)

# Make and Draw Plots
pdata = Plotter.Plot(gdata,legName='Data',legType='pez',option='pez')
if args.do_stack:
    pmcstack = Plotter.Plot(s,legName='',legType='',option='hist')
    if args.do_paper:
        pmcs = {col:Plotter.Plot(paper_sums[col].Clone(),legName=mc_stuff(col)[0],legType='F') for col in paperDrawOrder}
    else:
        pmcs = {name:Plotter.Plot(hists[allyears[0]][name][allMCs[allyears[0]][name][0]],legName=mc_stuff(name)[0],legType='F') for name in mcDrawOrder}
else:
    pmcstack = Plotter.Plot(totMC,  legName=mc_stuff(year),legType='hist',option='hist')
canvas.addMainPlot(Plotter.Plot(hist.Clone('tmp')),addToPlotList=False)
canvas.firstPlot.GetXaxis().SetLabelSize(0)
canvas.addMainPlot(pmcstack,addToPlotList=False)
canvas.addMainPlot(pdata)

# Make and Draw Legend
canvas.makeLegend(pos='tr')
if args.do_stack:
    if args.do_paper:
        for col in reversed(paperDrawOrder):
            pmcs[col].SetFillColor(get_color(col))
            canvas.legend.addLegendEntry(pmcs[col])
        canvas.legend.moveLegend(-0.1)
    else:
        for name in reversed(mcDrawOrder):
            pmcs[name].SetFillColor(get_color(name))
            pmcs[name].SetLineWidth(0)
            canvas.legend.addLegendEntry(pmcs[name])
        canvas.legend.resizeHeight(1.1)
        canvas.legend.moveLegend(X=-0.1)

# Set Axes
xtit = pretty(args.x)
canvas.firstPlot.setTitles(X=xtit,Y='Events'+(' / GeV' if args.bin_width else '')+(' #geq m(#mu^{+}#mu^{#font[122]{\55}})' if args.cumulative else '')+(' / '+str(int(hist.GetBinWidth(1)))+' GeV' if not args.logx and not args.bin_width and not args.cumulative else ''))
#R.gStyle.SetErrorX(0)
#R.gStyle.SetEndErrorSize(0)
if args.do_paper and args.do_uncert:
    include_zero_bins=False
    canvas.addRatioPlot(totData,totMC,ytit='(Data #minus Bkg) / Bkg',xtit=xtit,plusminus=1.,zeroed=True,option='pe0z',include_zero_bins=include_zero_bins)
    if args.tdir=='our':
        if args.cumulative:
            hmin,hmax = 1E-2,1E8
        else:
            hmin,hmax = 1E-5,3E6
    elif args.tdir=='ourcommonpre' or args.tdir=='ourpre':
        hmin,hmax=1E-1,3E8
    canvas.ratPad.cd()
    total_uncert.Draw('4same')
    total_uncert.SetFillColor(R.TColor.GetColor("#b4ccdb"))
    total_uncert.SetFillStyle(1001)
    #total_uncert.SetLineWidth(2)
    #total_uncert.SetLineStyle(2)
    for rat in canvas.ratList:
        rat.Draw('pezsame0')
    #canvas.addRatioPlot(totData,totMC,ytit='(Data #minus Bkg) / Bkg',xtit=xtit,plusminus=1.,zeroed=True,option='pe0')
    canvas.ratPad.RedrawAxis()
    ratLine = R.TLine(args.xmin,0,args.xmax,0)
    ratLine.SetLineStyle(3)
    ratLine.SetLineWidth(1)
    ratLine.Draw()
else:
    include_zero_bins=False
    #canvas.addRatioPlot(totData,totMC,ytit='Data / Bkg',xtit=xtit,plusminus=1.,option='pe0')
    canvas.addRatioPlot(totData,totMC,ytit='(Data #minus Bkg) / Bkg',xtit=xtit,plusminus=1.,zeroed=True,option='pe0z',include_zero_bins=include_zero_bins)
    #canvas.addRatioPlot(totData,totMC,ytit='Data / MC',xtit=xtit,plusminus=1.,option='pe0')
    hmin = min([s.GetStack().Last().GetMinimum(),gdata.GetHistogram().GetMinimum()])
    hmax = max([s.GetStack().Last().GetMaximum(),gdata.GetHistogram().GetMaximum()])
    if hmin==0. and args.logy: hmin=0.01
    hmin = hmin/10 if args.logy else 0.
    hmax = hmax*10 if args.logy else hmax*1.2
    if 'zpeak' in args.name:
        hmin,hmax = 1, 1E7
    elif 'dil_rap' in args.name:
        hmin,hmax = 1E2,1E6
    elif 'lep_pz' in args.name:
        hmin,hmax = 1E-1,1E5
canvas.firstPlot.GetXaxis().SetTitleSize(0)
canvas.firstPlot.GetXaxis().SetLabelSize(0)
canvas.firstPlot.GetYaxis().SetRangeUser(hmin,hmax)
if args.logx: 
    canvas.mainPad.SetLogx()
    canvas.ratPad.SetLogx()
    canvas.ratList[0].GetXaxis().SetMoreLogLabels(True)
    canvas.ratList[0].GetXaxis().SetNoExponent(True)

# Finish
canvas.Update()
canvas.cleanup(args.where+'/'+args.name,extList=['.png','.pdf','.C','.root'],extrascale=1.5)
