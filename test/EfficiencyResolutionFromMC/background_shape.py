import ROOT as R
import os,sys,math,logging,pdb
import numpy as np
import SUSYBSMAnalysis.Zprime2muAnalysis.lumberjack as lumberjack
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples# samples18, samples17, samples16
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-y','--year',default=2018,type=int,help='Year')
parser.add_argument('--nnpdf30',action='store_true',help='scale 2017 and 2018 dy and ttbar to 2016')
parser.add_argument('-bw','--bin-width',default=20,type=int,help='Bin width')
parser.add_argument('-w','--where',default='www_bckgshape',help='Save destination')
parser.add_argument('-n','--name',default='',help='Extra name')
args = parser.parse_args()

savedir = args.where+'/'
nbins = 8000/args.bin_width
hist = R.TH1D('h','',int(nbins),0,8000)
fit_funcs = {
        'low':{
            'func':'exp([0]+[1]*x+[2]*pow(x,2))*pow(x,[3])',
            'lims':[120,500,4],
            'par':['aL','bL','cL','kL'],
            },
        'high':{
            'lims':[500,6000,5],
            'func':'exp([0]+[1]*x+[2]*pow(x,2)+[3]*pow(x,3))*pow(x,[4])',
            'par':['aH','bH','cH','dH','kH'],
            #'func':'exp([0]+[1]*x+[2]*pow(x,2)+[3]*pow(x,3)+[4]*pow(x,4))*pow(x,[5])',
            #'par':['aH','bH','cH','dH','eH','kH'],
            },
        }

info = {
        2016:{
            'dir':'Our2016MuonsOppSignNtuple',
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/mc/',
            'mc':samples[2016],
            'FR':'mc_2016/jets_muons_2016.root',
            },
        2017:{
            'dir':'Our2018MuonsOppSignNtuple',
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/mc/',
            'mc':samples[2017],
            'FR':{
                'all':'mc_2017/Data-total-jets-BB-BE-EE-pt53.root',
                'bb':'mc_2017/Data-total-jets-BB-pt53.root',
                'beee':'mc_2017/Data-total-jets-BEEE-pt53.root',
                },
            },
        2018:{
            'dir':'Our2018MuonsOppSignNtuple',
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/mc/',
            'mc':samples[2018],
            'FR':{
                'all':'mc/Data2018-total-jets-BB-BE-EE-pt53.root',
                'bb':'mc/Data2018-total-jets-BB-pt53.root',
                'beee':'mc/Data2018-total-jets-BE-EE-pt53.root',
                },
            },
        }


dy_nnpdf_func = '(({a}) + ({b})*pow(gen_dil_mass,1) + ({c})*pow(gen_dil_mass,2) + ({d})*pow(gen_dil_mass,3) + ({e})*pow(gen_dil_mass,4) + ({f})*pow(gen_dil_mass,5))'
WW_nnpdf_func = '(({a}) + ({b})*pow(gen_dil_mass,1) + ({c})*pow(gen_dil_mass,2) + ({d})*pow(gen_dil_mass,3) + ({e})*pow(gen_dil_mass,4))'
ttbar_nnpdf_func = '(({a}) + ({b})*pow(gen_dil_mass,1) + ({c})*pow(gen_dil_mass,2) + ({d})*pow(gen_dil_mass,3))'
toNNPDF30 = {
        2017:{
            'powheg_nnpdf30':{
                #'all':dy_nnpdf_func.format(a='0.9292',b='+ 5.486E-5',c='+ 6.572E-9',d='- 1.142E-11',e='+ 4.876E-15',f='- 4.117E-19'),
                'all': dy_nnpdf_func.format(a='0.918129',b='6.92702e-05',c='1.62175e-08',d='-2.47833e-11',e='8.75707e-15',f='-7.53019e-19'),
                'bb':  dy_nnpdf_func.format(a='0.914053',b='7.91618e-05',c='2.19722e-08',d='-3.49212e-11',e='1.22504e-14',f='-1.07347e-18'),
                'beee':dy_nnpdf_func.format(a='0.933214',b='3.76813e-05',c='1.95612e-08',d='-1.2688e-11', e='3.69867e-15',f='-2.62212e-19'),
                'ee':  dy_nnpdf_func.format(a='0.952255',b='-7.67452e-05',c='1.69935e-07',d='-9.44719e-11',e='2.28419e-14',f='-1.72926e-18'),
                },
            'powheg_nnpdf30_nnlo':{
                #'all':dy_nnpdf_func.format(a='0.9292',b='+ 5.486E-5',c='+ 6.572E-9',d='- 1.142E-11',e='+ 4.876E-15',f='- 4.117E-19'),
                'all': dy_nnpdf_func.format(a='0.918129',b='6.92702e-05',c='1.62175e-08',d='-2.47833e-11',e='8.75707e-15',f='-7.53019e-19'),
                'bb':  dy_nnpdf_func.format(a='0.914053',b='7.91618e-05',c='2.19722e-08',d='-3.49212e-11',e='1.22504e-14',f='-1.07347e-18'),
                'beee':dy_nnpdf_func.format(a='0.933214',b='3.76813e-05',c='1.95612e-08',d='-1.2688e-11', e='3.69867e-15',f='-2.62212e-19'),
                'ee':  dy_nnpdf_func.format(a='0.952255',b='-7.67452e-05',c='1.69935e-07',d='-9.44719e-11',e='2.28419e-14',f='-1.72926e-18'),
                },
            'ttbar':{
                #'all':  ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                #'bb':   ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                #'beee': ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                'all':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                'bb':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                'beee':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                },
            #'diboson':{
            #    'all':'(1.)',
            #    'bb':'(1.)',
            #    'beee':WW_nnpdf_func.format(a='1.0031',b='-6.30717e-05',c='-3.14538e-08',d='2.68999e-11',e='-5.66054e-15'),
            #    },
            },
        2018:{
            'powheg_nnpdf30':{
                'all': dy_nnpdf_func.format(a='0.919027',b='5.98337e-05', c='2.56077e-08', d='-2.82876e-11',e='9.2782e-15', f='-7.77529e-19'),
                'bb':  dy_nnpdf_func.format(a='0.911563',b='0.000113313', c='-2.35833e-08',d='-1.44584e-11',e='8.41748e-15',f='-8.16574e-19'),
                'beee':dy_nnpdf_func.format(a='0.934502',b='2.21259e-05', c='4.14656e-08', d='-2.26011e-11',e='5.58804e-15',f='-3.92687e-19'),
                'ee':  dy_nnpdf_func.format(a='0.954175',b='-9.68066e-05',c='2.09278e-07', d='-1.15712e-10',e='2.77047e-14',f='-2.11731e-18'),
                },
            'powheg_nnpdf30_nnlo':{
                'all': dy_nnpdf_func.format(a='0.919027',b='5.98337e-05', c='2.56077e-08', d='-2.82876e-11',e='9.2782e-15', f='-7.77529e-19'),
                'bb':  dy_nnpdf_func.format(a='0.911563',b='0.000113313', c='-2.35833e-08',d='-1.44584e-11',e='8.41748e-15',f='-8.16574e-19'),
                'beee':dy_nnpdf_func.format(a='0.934502',b='2.21259e-05', c='4.14656e-08', d='-2.26011e-11',e='5.58804e-15',f='-3.92687e-19'),
                'ee':  dy_nnpdf_func.format(a='0.954175',b='-9.68066e-05',c='2.09278e-07', d='-1.15712e-10',e='2.77047e-14',f='-2.11731e-18'),
                },
            'ttbar':{
                #'all':  ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                #'bb':   ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                #'beee': ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                'all':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                'bb':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                'beee':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                },
            }
        }

kfunc = '(({a}) + ({b})*pow(gen_res_mass,1) + ({c})*pow(gen_res_mass,2) + ({d})*pow(gen_res_mass,3))'
kFunction = {
        'our':{ # m > 150 GeV
            'all' :kfunc.format(a='1.053',b='-0.0001552',c='5.661e-08',d='-8.382e-12'),
            'bb'  :kfunc.format(a='1.032',b='-0.000138', c='4.827e-08',d='-7.321e-12'),
            'beee':kfunc.format(a='1.064',b='-0.0001674',c='6.599e-08',d='-9.657e-12'),
            },
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

dyLists = {
    'powheg' : ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf'],
    #'powheg_GE' : ['dy50to120_GE','dy120to200_GE','dy200to400_GE','dy400to800_GE','dy800to1400_GE','dy1400to2300_GE','dy2300to3500_GE','dy3500to4500_GE','dy4500to6000_GE','dy6000toInf_GE'],
    'ht' : ['dyJetsToLL_ht100to200','dyJetsToLL_ht200to400','dyJetsToLL_ht400to600','dyJetsToLL_ht600to800','dyJetsToLL_ht800to1200','dyJetsToLL_ht1200to2500','dyJetsToLL_ht2500toInf'],
    'madgraph' : ['dyInclusive50_madgraph'],
    'amcatnlo' : ['dyInclusive50_amcatnlo'],
    }
allMCs = {
        2016:{
            'powheg' : dyLists['powheg'],
            'powheg_nnlo' : dyLists['powheg'],
            #'powheg_GE' : dyLists['powheg_GE'],
            #'powheg_GE_nnlo' : dyLists['powheg_GE'],
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
            'powheg' : dyLists['powheg'],
            'powheg_nnpdf30' : dyLists['powheg'],
            'powheg_nnpdf30_nnlo' : dyLists['powheg'],
            #'powheg_GE' : dyLists['powheg_GE'],
            #'powheg_GE_nnpdf30' : dyLists['powheg_GE'],
            #'powheg_GE_nnpdf30_nnlo' : dyLists['powheg_GE'],
            'ht' : ['dyJetsToLL_ht100to200','dyJetsToLL_ht200to400','dyJetsToLL_ht400to600','dyJetsToLL_ht600to800','dyJetsToLL_ht800to1200','dyJetsToLL_ht1200to2500','dyJetsToLL_ht2500toInf'],
            'madgraph' : ['dyInclusive50_madgraph'],
            'amcatnlo' : ['dyInclusive50_amcatnlo'],
            #'ttbar':['ttbar_lep'],
            #'ttbar':['ttbar_lep_50to500','ttbar_lep_500to800','ttbar_lep_800to1200','ttbar_lep_1200to1800','ttbar_lep_1800toInf'],
            'ttbar':['ttbar_lep_50to500','ttbar_lep_500to800','ttbar_lep_800to1200','ttbar_lep_1200to1800','ttbar_lep_1800toInf'],
            #'diboson':['WW','ZZ','WZ'],
            'diboson':['WW_50to200','WW_200to600','WW_600to1200','WW_1200to2500','WW_2500toInf','ZZTo4L','ZZTo2L2Q','ZZTo2L2Nu','WZTo3LNu','WZTo2L2Q'],
            'singletop':['tW','tbarW'],
            'Wjets':['Wjets'],
            'tautau':['dyTauTau_madgraph'],
            'jets':['jets'],
            },
        2018:{
            'powheg' : dyLists['powheg'],
            'powheg_nnpdf30' : dyLists['powheg'],
            'powheg_nnpdf30_nnlo' : dyLists['powheg'],
            #'powheg_GE' : dyLists['powheg_GE'],
            #'powheg_GE_nnpdf30' : dyLists['powheg_GE'],
            #'powheg_GE_nnpdf30_nnlo' : dyLists['powheg_GE'],
            'ht' : ['dyJetsToLL_ht100to200','dyJetsToLL_ht200to400','dyJetsToLL_ht400to600','dyJetsToLL_ht600to800','dyJetsToLL_ht800to1200','dyJetsToLL_ht1200to2500','dyJetsToLL_ht2500toInf'],
            'madgraph' : ['dyInclusive50_madgraph'],
            'amcatnlo' : ['dyInclusive50_amcatnlo'],
            #'ttbar':['ttbar_lep'],
            #'diboson':['WW','ZZ','WZ'],
            #'diboson':['WW','ZZTo4L','ZZTo2L2Q','ZZTo2L2Nu','WZTo3LNu','WZTo2L2Q'],
            'ttbar':['ttbar_lep_50to500','ttbar_lep_500to800','ttbar_lep_800to1200','ttbar_lep_1200to1800','ttbar_lep_1800toInf'],
            'diboson':['WW_50to200','WW_200to600','WW_600to1200','WW_1200to2500','WW_2500toInf','ZZTo4L','ZZTo2L2Q','ZZTo2L2Nu','WZTo3LNu','WZTo2L2Q'],
            'singletop':['tW','tbarW'],
            'Wjets':['Wjets'],
            'tautau':['dyTauTau_madgraph'],
            'jets':['jets'],
            },
        }

#nonDYmc = ['ttbar','diboson','singletop','Wjets','tautau']
nonDYmc = ['ttbar','diboson','singletop','tautau']
dyMC = {
        2016:['powheg','powheg_nnlo'],#,'powheg_GE','powheg_GE_nnlo'],
        2017:['powheg','powheg_nnpdf30','powheg_nnpdf30_nnlo'],#,'powheg_GE','powheg_GE_nnpdf30','powheg_GE_nnpdf30_nnlo'],
        2018:['powheg','powheg_nnpdf30','powheg_nnpdf30_nnlo'],#,'powheg_GE','powheg_GE_nnpdf30','powheg_GE_nnpdf30_nnlo'],
        }
mcList = nonDYmc + dyMC[args.year] +['jets']


categories = ['all','bb','beee']
cats = {
        'all':'(1.)',
        'bb':'(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)',
        'beee':'(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)',
        #'ee':'(fabs(lep_eta[0])>1.2 && fabs(lep_eta[1])>1.2)',
        }

def get_sum_weights(f):
    weights = getattr(f,'EventCounter').Get('weights')
    return weights.GetBinContent(2)-weights.GetBinContent(1)
def mc_draw(year,mc,cat):
    gRand = 'sin(2.0*pi*rndm)*sqrt(-2.0*log(rndm))'
    smear = {
            # 10% for bb 20% for beee
            2016:{'bb':'sqrt(pow(1.10,2)-1)','beee':'sqrt(pow(1.20,2)-1)'},
            # no smearing for bb 15% for beee
            2017:{'bb':'sqrt(pow(1.0,2)-1)','beee':'sqrt(pow(1.15,2)-1)'},
            2018:{'bb':'sqrt(pow(1.0,2)-1)','beee':'sqrt(pow(1.15,2)-1)'},
            }
    # Smear mass = reco mass + reco mass * rand->gaus(0,res(gen mass)*extraSmear)
    if cat=='all':
        drawThis = 'vertex_m + vertex_m*'+gRand+'*('+\
                cats['bb']  +'*'+smear[year]['bb']  +'*'+resMass[year]['bb']+' + '+\
                cats['beee']+'*'+smear[year]['beee']+'*'+resMass[year]['beee']+')'
    elif cat=='bb':
        drawThis = 'vertex_m + vertex_m*'+gRand+'*'+smear[year]['bb']+'*'+resMass[year]['bb']
    elif cat=='beee':
        drawThis = 'vertex_m + vertex_m*'+gRand+'*'+smear[year]['beee']+'*'+resMass[year]['beee']

    return drawThis

# Make MC histograms
hists = {cat:{name:{mc:{} for mc in allMCs[args.year][name]+['jets']} for name in mcList} for cat in categories}
for name in mcList:
    if name=='jets': continue
    for mc in allMCs[args.year][name]:
        mcFile = R.TFile(info[args.year]['mcpath']+'ana_datamc_'+mc+'.root')
        sum_weights = get_sum_weights(mcFile)
        print name,mc
        if args.year==2018 and name in ['amcatnlo','madgraph']:
            mcTree = mcFile.Get(info[2017]['dir']+'/t')
        else:
            mcTree = mcFile.Get(info[args.year]['dir']+'/t')
        for cat in categories:
            hmcname = 'h_'+mc+'_'+cat
            hmc = hist.Clone(hmcname)

            mcCutWeight = '('+cats[cat]+')'
            if args.year!=2016 and name in toNNPDF30[args.year].keys():
                mcCutWeight += '*'+toNNPDF30[args.year][name][cat]
            if 'nnlo' in name and 'nnpdf30' in name and 'powheg' in name:
                mcCutWeight += '*'+kFunction['our'][cat]
            mcCutWeight += '*genWeight'
            print mc_draw(args.year,mc,cat)
            print mcCutWeight
            print
            mcTree.Draw(mc_draw(args.year,mc,cat)+'>>'+hmcname,mcCutWeight,'')

            hmc.SetDirectory(0)
            hists[cat][name][mc] = hmc
            hists[cat][name][mc].SetDirectory(0)
            scale_by = info[args.year]['mc'][mc].cross_section / float(sum_weights)
            hists[cat][name][mc].Scale(scale_by)
        mcFile.Close()

# Make non-DY MC sum
nonDYhists = {cat:hist.Clone('nonDY_'+cat) for cat in categories}
for cat in categories:
    for name in nonDYmc:
        for mc in allMCs[args.year][name]:
            nonDYhists[cat].Add(hists[cat][name][mc])

#for cat in categories:
#    if args.year!=2016:
#        frfile = R.TFile(info[args.year]['FR'][cat])
#        frhist_orig = frfile.Get('TotalJets').Clone()
#    else:
#        frfile = R.TFile(info[args.year]['FR'])
#        jetname = 'jets'
#        if cat=='bb': jetname = jetname+'BB'
#        elif cat=='beee': jetname = jetname+'BE'
#        frhist_orig = frfile.Get(jetname)
#    frhist = hist.Clone('FakeRate_'+cat)
#    for ibin in range(1,frhist.GetNbinsX()+1):
#        start = frhist_orig.FindBin(frhist.GetBinLowEdge(ibin))
#        end = frhist_orig.FindBin(frhist.GetBinLowEdge(ibin+1))
#        isum = 0.
#        for jbin in range(start,end):
#            isum += frhist_orig.GetBinContent(jbin)
#        frhist.SetBinContent(ibin,isum)
#    frhist.SetDirectory(0)
#    hists[cat]['jets']['jets'] = frhist
#    hists[cat]['jets']['jets'].SetDirectory(0)
#    frfile.Close()
#    nonDYhists[cat].SetDirectory(0)
#    nonDYhists[cat].Add(hists[cat]['jets']['jets'])

print nonDYhists

# Make MC sum histograms
# First clone non-DY hists then add in the DY
sumHists = {cat:{dy:nonDYhists[cat].Clone('hSum_'+dy) for dy in dyMC[args.year]} for cat in categories}
print sumHists
print 'asdfasdf'
for cat in categories:
    for dy in dyMC[args.year]:
        for mc in allMCs[args.year][dy]:
            print cat,dy,mc,hists[cat][dy][mc]
            sumHists[cat][dy].Add(hists[cat][dy][mc])

legNames = {
        'all':'All #eta',
        'bb':'Barrel-Barrel',
        'beee':'Barrel-Endcap + Endcap+Endcap',
        'powheg':'Nominal Fit to MC',
        'powheg_nnpdf30':' + Scaled to NNPDF3.0 (NLO)',
        'powheg_nnpdf30_nnlo':' + NNLO k-function applied',
        'powheg_nnlo':' + NNLO k-function applied',
        }

# Do fits
fits = {cat:{dy:{mass:{} for mass in ['low','high']} for dy in dyMC[args.year]} for cat in categories}
for cat in categories:
    for dy in dyMC[args.year]:
        for mass in ['low','high']:
            fitname = 'fit_'+dy+'_'+cat+'_'+mass
            fits[cat][dy][mass] = R.TF1(fitname,fit_funcs[mass]['func'],fit_funcs[mass]['lims'][0],fit_funcs[mass]['lims'][1],fit_funcs[mass]['lims'][2])
            if mass=='low':
                fits[cat][dy][mass].SetParameters(10,-0.015,5e-6,-2)        # Starting values
                #fits[cat][dy][mass].SetParLimits(0,1,40)                    # aL
                #fits[cat][dy][mass].SetParLimits(1,-1e-1,-1e-4)             # bL
                #fits[cat][dy][mass].SetParLimits(2,1e-7,1e-5)               # cL
                #fits[cat][dy][mass].SetParLimits(3,-4,-1)                   # kL
            elif mass=='high':
                fits[cat][dy][mass].SetParameters(20,-5e-4,-2e-8,-1e-12,-4)  # Starting values
                #fits[cat][dy][mass].SetParLimits(0,1,40)                    # aH
                #fits[cat][dy][mass].SetParLimits(1,-1e-1,-1e-7)             # bH
                #fits[cat][dy][mass].SetParLimits(2,-1e-5,-1e-11)            # cH
                #fits[cat][dy][mass].SetParLimits(3,1e-18,1e-9)              # dH
                #fits[cat][dy][mass].SetParLimits(4,-5,-3)                   # kH
            print '\n','*'*30,'\n'
            print cat,dy,mass
            sumHists[cat][dy].Fit(fits[cat][dy][mass],'ME0R+')

colors = {
        'all':R.kBlack,
        'bb':R.kOrange+1,
        'beee':R.kAzure+1,
        'powheg':R.kBlack,
        'powheg_nnpdf30':R.kGreen+1,
        'powheg_nnpdf30_nnlo':R.kViolet+1,
        'powheg_nnlo':R.kViolet+1,
        }

def do_fit_log(cat,dy,fits,hist):
    name = dy+'_'+cat+'_'+str(args.year)+('_'+args.name if args.name else '')
    lumberjack.setup_logger(name,savedir+'/'+name+'.log')
    logger = logging.getLogger(name)
    logger.info('\n'+'*'*30+'\n')
    logger.info('Background Shape Parametrization')
    logger.info('\n'+'*'*30+'\n')
    logger.info(dy+' '+cat+' '+str(args.year))
    for mass in ['low','high']:
        logger.info('\n'+'*'*15+'\n')
        logger.info(mass)
        logger.info(fit_funcs[mass]['func'])
        logger.info(str(fit_funcs[mass]['lims'][0])+' -- '+str(fit_funcs[mass]['lims'][1]))
        for i in range(fits[mass].GetNpar()):
            logger.info(str(i)+' '+fit_funcs[mass]['par'][i]+' '+str(fits[mass].GetParameter(i))+' +/- '+str(fits[mass].GetParError(i))+'\t\tRelative Uncertainty '+str(abs(fits[mass].GetParError(i)/fits[mass].GetParameter(i))))
        logger.info('Chi2/ndof = '+str(fits[mass].GetChisquare())+' / '+str(fits[mass].GetNDF()))
    logger.info('\n'+'*'*30+'\n')

# Draw histograms+fits and residual
for cat in categories:
    for dy in dyMC[args.year]:
        canvas = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation Preliminary',logy=True)
        plot = Plotter.Plot(sumHists[cat][dy],legName=legNames[cat],legType='l',option='hist')
        canvas.addMainPlot(plot)
        for mass in ['low','high']:
            fits[cat][dy][mass].SetLineColor(R.kRed)
            fits[cat][dy][mass].Draw('same')
        canvas.firstPlot.setTitles(X='m(#mu^{+}#mu^{#font[122]{\55}}) [GeV]',Y='XS / Sum of Weights')
        canvas.firstPlot.GetXaxis().SetRangeUser(0,6500)
        canvas.firstPlot.GetYaxis().SetRangeUser(1e-11,10)
        #res = make_residual_plot(fits[cat][dy],sumHists[cat][dy])
        #canvas.ratPad.cd()
        #res.Draw()
        do_fit_log(cat,dy,fits[cat][dy],sumHists[cat][dy])
        canvas.cleanup(savedir+dy+'_'+cat+'_'+str(args.year)+('_'+args.name if args.name else ''),extList=['.png','.pdf'])

       
# Draw fits for each category together    
for dy in dyMC[args.year]:
    canvas = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation Preliminary',logy=True)
    plots = {cat:{mass:Plotter.Plot(fits[cat][dy][mass],legName=legNames[cat],legType='l',option='l') for mass in ['low','high']} for cat in categories}
    p = Plotter.Plot(R.TH1D('tmp_'+dy,'',1,0,6000))
    canvas.addMainPlot(p,addToPlotList=False)
    for c,cat in enumerate(categories):
        canvas.addMainPlot(plots[cat]['low'])
        canvas.addMainPlot(plots[cat]['high'],addToPlotList=False)
        fits[cat][dy]['low'].SetLineColor(colors[cat])
        fits[cat][dy]['high'].SetLineColor(colors[cat])
    canvas.firstPlot.GetYaxis().SetRangeUser(1e-11,10)
    canvas.firstPlot.GetXaxis().SetRangeUser(120,6000)
    canvas.firstPlot.setTitles(X='m(#mu^{+}#mu^{#font[122]{\55}}) [GeV]',Y='XS / Sum of Weights')
    canvas.makeLegend(pos='tr')
    canvas.legend.moveLegend(X=-0.3)
    canvas.cleanup(savedir+dy+'_'+str(args.year)+('_'+args.name if args.name else ''),extList=['.png','.pdf'])

# Draw fits for single eta category but compare orders of correction
for cat in categories:
    canvas = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation Preliminary',logy=True)
    plots = {dy:{mass:Plotter.Plot(fits[cat][dy][mass],legName=legNames[dy],legType='l',option='l') for mass in ['low','high']} for dy in dyMC[args.year]}
    p = Plotter.Plot(R.TH1D('tmp_'+cat,'',1,0,6000))
    canvas.addMainPlot(p,addToPlotList=False)
    for i,dy in enumerate(dyMC[args.year]):
        canvas.addMainPlot(plots[dy]['low'])
        canvas.addMainPlot(plots[dy]['high'],addToPlotList=False)
        fits[cat][dy]['low'].SetLineColor(colors[dy])
        fits[cat][dy]['high'].SetLineColor(colors[dy])
    canvas.firstPlot.GetYaxis().SetRangeUser(1e-11,10)
    canvas.firstPlot.GetXaxis().SetRangeUser(120,6000)
    canvas.firstPlot.setTitles(X='m(#mu^{+}#mu^{#font[122]{\55}}) [GeV]',Y='XS / Sum of Weights')
    canvas.makeLegend(pos='tr')
    canvas.legend.moveLegend(X=-0.3)
    canvas.cleanup(savedir+cat+'_'+str(args.year)+('_'+args.name if args.name else ''),extList=['.png','.pdf'])
