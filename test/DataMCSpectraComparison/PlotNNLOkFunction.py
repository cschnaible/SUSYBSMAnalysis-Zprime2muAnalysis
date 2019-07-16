import ROOT as R
R.gROOT.SetBatch(True)
#R.gStyle.SetOptFit(00000000)
#R.gStyle.SetOptStat(00000000)
import numpy as np
import array, math, logging
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples
import SUSYBSMAnalysis.Zprime2muAnalysis.lumberjack as lumberjack
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-c','--category',default='all',help='Analysis category: all, bb, beee, ee')
parser.add_argument('-s','--selection',default='high',help='Low-mass or high-mass acceptance selection')
parser.add_argument('-lx','--logx',action='store_true',default=False)
parser.add_argument('-n','--name',default='')
#parser.add_argument('--xmin',default=60,type=float)
#parser.add_argument('--xmax',default=6000,type=float)
parser.add_argument('--fmin',default=60,type=float)
parser.add_argument('--fmax',default=6000,type=float)
args = parser.parse_args()

params = {
        'high':{
            'func':'{a} + pow(x-400,1)*({b}) + pow(x-400,2)*({c}) + pow(x-400,3)*({d})',
            'pars':{
                'all' :{'a':1.047,'b':-0.000143, 'c':5.167e-8,'d':-7.84e-12},
                'bb'  :{'a':1.036,'b':-0.0001441,'c':5.068e-8,'d':-7.581e-12},
                'beee':{'a':1.052,'b':-0.0001471,'c':5.903e-8,'d':-9.037e-12},
                },
            },
        'low':{
            #'func':'{a} + pow(x-130,1)*({b}) + pow(x-130,2)*({c}) + pow(x-130,3)*({d}) + pow(x-130,4)*({e}) + pow(x-130,5)*({f})',
            #'func':'{a} + pow(x-400,1)*({b}) + pow(x-400,2)*({c}) + pow(x-400,3)*({d}) + pow(x-400,4)*({e}) + pow(x-400,5)*({f})',
            #'func':'{a} + pow(x,1)*({b}) + pow(x,2)*({c}) + pow(x,3)*({d}) + pow(x,4)*({e}) + pow(x,5)*({f})',
            'func':'{a} + pow(x-130,1)*({b}) + pow(x-130,2)*({c}) + pow(x-130,3)*({d})',
            'pars':{
                #'all' :{'a':1.051,'b':-0.0001516,'c':-1.592e-6,'d':-1.531e-9,'e':5.515e-8,'f':-8.22e-12},
                #'bb'  :{'a':1.027,'b':-0.0001262,'c': 2.184e-8,'d': 2.644e-9,'e':4.338e-8,'f':-6.778e-12},
                #'beee':{'a':1.066,'b':-0.0001755,'c':-2.624e-6,'d':-4.108e-9,'e':7.057e-8,'f':-1.03e-11},
                'bb'  :{'a':1.003,'b':-0.0002904,'c':-3.281e-6,'d':5.258e-9},
                'beee':{'a':1.012,'b':-0.001607, 'c': 8.796e-6,'d':1.401e-6},
                },
            },
        }

lumberjack.setup_logger(args.name,'www_run2/'+args.name+'.log')
logger = logging.getLogger(args.name)


canvas = R.TCanvas()

func = R.TF1('kFunc_'+args.category+'_'+args.selection,\
        params[args.selection]['func'].format(**params[args.selection]['pars'][args.category]),\
        args.fmin,args.fmax)
func.Draw()

if args.logx: 
    canvas.SetLogx()
    func.GetXaxis().SetMoreLogLabels(True)
    func.GetXaxis().SetNoExponent(True)

func.GetXaxis().SetTitle('Dimuon Mass [GeV]')
#func.GetXaxis().SetRangeUser(args.fmin,args.fmax)

func.GetYaxis().SetTitle('FEWZ(LUXqed) / POWHEG(NNPDF3.0)')
func.GetYaxis().SetRangeUser(0.3,1.4)

logger.info(args)
logger.info('\n'+'*'*15+'\n')
logger.info(params[args.selection]['func'].format(**params[args.selection]['pars'][args.category]))

canvas.SaveAs('www_run2/'+args.name+'.png')
