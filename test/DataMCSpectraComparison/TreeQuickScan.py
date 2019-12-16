import ROOT as R
R.gROOT.SetBatch(True)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-y','--year',default=2018,type=int)
parser.add_argument('-d','--dir',default='our')
parser.add_argument('-s','--selection',default='')
parser.add_argument('-c','--category',default='all',help='all,bb,beee')
parser.add_argument('-v','--var',action='append',help='Quantities to print')
parser.add_argument('-n','--name',default='',help='extra name for output')
parser.add_argument('--mc',default=None,help='Do mc and specify')
args = parser.parse_args()
info = {
        2016:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/data/',
            'file':'ana_datamc_Run2016_17Jul2018.root',
            'lumi':36294.593964906585693,
            'ratioZ0':{'all':0.9727,'bb':0.9842,'beee':0.9610},
            'our':{
                'dir':'Our2016MuonsOppSignNtuple',
                'pre':1.,
                #'lumi':36294.593964906585693,
                },
            'ourcommonpre':{
                'dir':'Our2016MuPrescaledCommonMuonsOppSignNtuple',
                'pre':320.,
                #'lumi':36285.0595135,
                },
            'ourpre':{
                'dir':'Our2016MuPrescaledMuonsOppSignNtuple',
                'pre':146.323326629,
                #'lumi':36285.0595135,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2016/mc/',
            #'mc':samples[2016],
            },
        2017:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/data/',
            'file':'ana_datamc_Run2017_31Mar2018.root',
            'lumi':42079.880396,
            'ratioZ0':{'all':1.0282,'bb':1.0286,'beee':1.0278},
            'our':{
                'dir':'Our2018MuonsOppSignNtuple',
                'pre':1.,
                #'lumi':42079.880396,
                },
            'ourcommonpre':{
                'dir':'Our2018MuPrescaledCommonMuonsOppSignNtuple',
                'pre':561.,
                #'lumi':42070.654731,
                },
            'ourpre':{
                'dir':'Our2018MuPrescaledMuonsOppSignNtuple',
                'pre':236.085072878,
                #'lumi':42070.654731,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2017/mc/',
            #'mc':samples[2017],
            },
        2018:{
            'path':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/data/',
            'file':'ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root',
            'lumi':61298.775231718995,
            'ratioZ0':{'all':1.0062,'bb':1.0124,'beee':1.0017},
            'our':{
                'dir':'Our2018MuonsOppSignNtuple',
                'pre':1.,
                #'lumi':61298.7752317,
                #'lumi':61302.3918373,
                },
            'ourcommonpre':{
                'dir':'Our2018MuPrescaledMuonsOppSignNtuple',
                'pre':500.,
                #'lumi':61291.8425445,
                #'lumi':61302.3918373,
                },
            'ourpre':{
                'dir':'Our2018MuPrescaledNoCommonMuonsOppSignNtuple',
                'pre':486.949643091,
                #'lumi':61291.8425445,
                #'lumi':61302.3918373,
                #'lumi':61298.775231718995,
                },
            'mcpath':'/eos/cms/store/user/cschnaib/ZPrime/Ana2018/mc/',
            #'mc':samples[2018],
            },
        }

if args.mc==None:
    f = R.TFile(info[args.year]['path']+info[args.year]['file'])
else:
    f = R.TFile(info[args.year]['mcpath']+'ana_datamc_'+args.mc+'.root')
t = f.Get(info[args.year][args.dir]['dir']+'/t')

cats = {
        'all':'(1.)',
        'bb':'(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)',
        'beee':'(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)',
        }
CUT = cats[args.category]+(' && '+args.selection if args.selection!='' else '')
print CUT

toPrint = args.var[0]
for var in args.var[1:]:
    toPrint += ':'+var

t.SetScanField(0)
t.GetPlayer().SetScanRedirect(True)
t.GetPlayer().SetScanFileName('event_list_'+str(args.year)+'_'+args.category+'_scan'+('_'+args.name if args.name else '')+'.txt')
t.Scan(toPrint,CUT,'colsize=10')
