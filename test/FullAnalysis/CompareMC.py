# Make 2D ratio plots comparing MC compaigns for 
# (gen-level) {leading mu pT, leading mu eta, Z pT, Z y} vs {dimuon mass}
# Example usage: python CompareMC.py
#
import ROOT as R
import os
import numpy as np
import array
import argparse
import Plotter as Plotter
from PlotsToMake import MAKEPLOTLIST
import tools
R.gROOT.SetBatch(True)

parser = argparse.ArgumentParser(description='Options for making Z-prime --> dimuon plots')
parser.add_argument('-dir','--directory',default='plots',help='Directory to save plots')
parser.add_argument('-r','--recreate',action='store_true',help='Whether or not to recreate data lists')
parser.add_argument('-norm','--normalization',type=str,default='lumi',help='How to normalize plots')
parser.add_argument('-e','--extra',type=str,default='',help='Extra save name for pdf files')
args = parser.parse_args()

print 'recreate',args.recreate

dyList = ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000']
years = ['2016','2017','2018']
dyFiles = {year:{dy:{} for dy in dyList} for year in years}
mcdata = {year:{dy:{data:{} for data in ['file','xs','nevents']} for dy in dyList} for year in years}
with open('mcdata.txt') as mcdatafile:
    for line in mcdatafile:
        if line[0]=='#': continue
        cols = line.strip('\n').split()
        year = cols[0]
        dy = cols[1]
        xs = float(cols[2])
        nevents = int(cols[3])
        if dy not in dyList: continue
        if year not in years: continue

        if year=='2016': 
            DIR = '~alfloren/public/DY_ROOT/2016/'
            t = 'SimpleNtupler/t'
            w = 'EventCounter/weights'
        elif year=='2017': 
            DIR = '~alfloren/public/DY_ROOT/2017/'
            t = 'SimpleNtupler/t'
            w = 'EventCounter/weights'
        elif year=='2018': 
            DIR = 'mc/'
            t = 'SimpleMuonsAllSignsNtuple/t'
            w = 'EventCounter/weights'

        mcdata[year][dy]['file'] = DIR+'ana_datamc_'+dy+'.root'
        mcdata[year][dy]['t'] = t
        mcdata[year][dy]['w'] = w
        mcdata[year][dy]['xs'] = xs
        mcdata[year][dy]['nevents'] = nevents


def binning(var):
    if 'log' in var:
        if var=='mass_log':
            start,end,nbins=50,6000,25
        return np.logspace(np.log10(start),np.log10(end),nbins+1)
    else:
        if var=='dil_pt':
            start,end,width = 0,3000,50.
        elif var=='dil_rap':
            start,end,width = -4,4,0.1
        elif 'mu_pt' in var:
            start,end,width = 0,4000,50.
        elif 'mu_eta' in var:
            start,end,width = -2.4,2.4,0.4
        elif var=='mass':
            start,end,width = 0,6000,200.
        nbins = int(round((end-start)/width))
        return array.array('d',[round(start+i*width,1) for i in range(nbins+1)])

def pretty(name):
    pretty = {
        'mass':'gen m(#mu#mu) [GeV]',
        'mass_log':'gen m(#mu#mu) [GeV]',
        'leading_mu_pt':'leading #mu p_{T} [GeV]',
        'leading_mu_eta':'leading #mu #eta',
        'sub_mu_pt':'sub-leading #mu p_{T} [GeV]',
        'sub_mu_eta':'sub-leading #mu #eta',
        'dil_pt':'dimuon gen p_{T} [GeV]',
        'dil_rap':'dimuon gen rapidity',
        '0m2000':'0 < m_{#mu^{+}#mu^{-}} < 2000 GeV',
        '2000m4000':'2000 < m_{#mu^{+}#mu^{-}} < 4000 GeV',
        '4000m6000':'4000 < m_{#mu^{+}#mu^{-}} < 6000 GeV',
        '2016':'80X',
        '2017':'94X',
        '2018':'102X',
        }
    return pretty[name]

def get_weight(weightHist):
    pos = weightHist.GetBinContent(2)
    neg = weightHist.GetBinContent(1)
    return int(pos-neg)

def markers(name):
    markers = {
            '2016':R.kFullCircle,
            '2017':R.kFullCircle,
            '2018':R.kFullSquare,
            }
    return markers[name]
def colors(name):
    colors = {
            '2016':R.kBlack,
            '2017':R.kRed,
            '2018':R.kBlue,
            }
    return colors[name]

def ranges(mcut,var):
    ranges = {
            'leading_mu_eta':{
                '0m2000':(1,1E5,'Y'),
                '2000m4000':(1E-7,1E-2,'Y'),
                '4000m6000':(1E-11,1E-5,'Y'),
                },
            'leading_mu_pt':{
                '0m2000':(1E-10,1E6,'Y'),
                '2000m4000':(1E-13,1E-2,'Y'),
                '4000m6000':(1E-13,1E-6,'Y'),
                },
            'sub_mu_eta':{
                '0m2000':(1,1E5,'Y'),
                '2000m4000':(1E-7,1E-2,'Y'),
                '4000m6000':(1E-11,1E-5,'Y'),
                },
            'sub_mu_pt':{
                '0m2000':(1E-10,1E6,'Y'),
                '2000m4000':(1E-13,1E-2,'Y'),
                '4000m6000':(1E-13,1E-6,'Y'),
                },
            'dil_rap':{
                '0m2000':(1E-1,1E4,'Y'),
                '2000m4000':(1E-10,1E-2,'Y'),
                '4000m6000':(1E-13,1E-5,'Y'),
                },
            'dil_pt':{
                '0m2000':(1E-9,1E6,'Y'),
                '2000m4000':(1E-12,1E-1,'Y'),
                '4000m6000':(1E-13,1E-4,'Y'),
                },
            }
    return ranges[var][mcut]


def make2DHist(year,dy,varX,varY):
    hname = year+'_'+dy+'_'+varY+'_vs_'+varX
    htitle = pretty(varY)+' vs. '+pretty(varY)
    xax = pretty(varX)
    yax = pretty(varY)
    ybins = binning(varY)
    xbins = binning(varX)
    return R.TH2F(hname,htitle+';'+xax+';'+yax+';',len(xbins)-1,xbins,len(ybins)-1,ybins)

def makeHist(year,dy,varX,cut):
    hname = year+'_'+dy+'_'+varX+'_'+cut
    htitle = pretty(cut)
    xax = pretty(varX)
    xbins = binning(varX)
    return R.TH1F(hname,htitle+';'+xax+';XS / sum of weights;',len(xbins)-1,xbins)

varXlist = ['sub_mu_pt','leading_mu_pt','sub_mu_eta','leading_mu_eta','dil_pt','dil_rap']
varYlist = ['mass','mass_log']
mcutlist = ['0m2000','2000m4000','4000m6000']
hists = {year:{dy:{varY:{varX:{} for varX in varXlist} for varY in varYlist+mcutlist} for dy in dyList} for year in years}
if args.recreate:
    for year in years:
        for dy in dyList:
            for varX in varXlist:
                for varY in varYlist:
                    hists[year][dy][varY][varX] = make2DHist(year,dy,varX,varY)
                    hists[year][dy][varY][varX].SetDirectory(0)
                for mcut in mcutlist:
                    hists[year][dy][mcut][varX] = makeHist(year,dy,varX,mcut)
                    hists[year][dy][mcut][varX].SetDirectory(0)
    print hists

    for year in years:
        print year
        for dy in dyList:
            print dy
            f = R.TFile(mcdata[year][dy]['file'])
            t = f.Get(mcdata[year][dy]['t'])
            #mcdata[year][dy]['wsum'] = get_weight(f.Get(mcdata[year][dy]['w']))
            for e,entry in enumerate(t):
                weight = 1. # t.genWeight
                thisEvent = t.event
                if e==0: 
                    prevEvent = -1
                if thisEvent==prevEvent:
                    prevEvent = thisEvent
                    continue
                mass = t.gen_dil_mass
                dil_rap = t.gen_dil_rap
                dil_pt = t.gen_dil_pt
                leadMu = 0 if t.gen_lep_pt[0]>t.gen_lep_pt[1] else 1
                subMu = 1 if leadMu==0 else 0
                if t.lep_pt[0]<40 or t.lep_pt[1]<40: continue
                lead_mu_pt = t.gen_lep_pt[leadMu]
                lead_mu_eta = t.gen_lep_eta[leadMu]
                sub_mu_pt = t.gen_lep_pt[subMu]
                sub_mu_eta = t.gen_lep_eta[subMu]
                mcuts = {
                        '0m2000':      (0  <= mass <= 2000),
                        '2000m4000':(2000   < mass <= 4000),
                        '4000m6000':(4000   < mass <= 6000),
                        }
                for y in varYlist:
                    hists[year][dy][y]['leading_mu_pt'].Fill(lead_mu_pt,mass,weight)
                    hists[year][dy][y]['leading_mu_eta'].Fill(lead_mu_eta,mass,weight)
                    hists[year][dy][y]['sub_mu_pt'].Fill(sub_mu_pt,mass,weight)
                    hists[year][dy][y]['sub_mu_eta'].Fill(sub_mu_eta,mass,weight)
                    hists[year][dy][y]['dil_pt'].Fill(dil_pt,mass,weight)
                    hists[year][dy][y]['dil_rap'].Fill(dil_rap,mass,weight)
                    for mcut in mcuts:
                        if mcuts[mcut]:
                            hists[year][dy][mcut]['leading_mu_pt'].Fill(lead_mu_pt,weight)
                            hists[year][dy][mcut]['leading_mu_eta'].Fill(lead_mu_eta,weight)
                            hists[year][dy][mcut]['sub_mu_pt'].Fill(sub_mu_pt,weight)
                            hists[year][dy][mcut]['sub_mu_eta'].Fill(sub_mu_eta,weight)
                            hists[year][dy][mcut]['dil_rap'].Fill(dil_rap,weight)
                            hists[year][dy][mcut]['dil_pt'].Fill(dil_pt,weight)
                prevEvent = thisEvent

            f.Close()


    outFile = R.TFile('plots/mc_comparison'+('_'+args.extra if args.extra !='' else '')+'.root','recreate')
    for year in years:
        for dy in dyList:
            for varX in varXlist:
                for varY in varYlist:
                    hists[year][dy][varY][varX].Write()
                    print hists[year][dy][varY][varX].GetName()+' written'
                for mcut in mcutlist:
                    hists[year][dy][mcut][varX].Write()
                    print hists[year][dy][mcut][varX].GetName()+' written'
    outFile.Close()

for year in years:
    for dy in dyList:
        f = R.TFile(mcdata[year][dy]['file'])
        mcdata[year][dy]['wsum'] = get_weight(f.Get(mcdata[year][dy]['w']))
        f.Close()
histFile = R.TFile('plots/mc_comparison'+('_'+args.extra if args.extra !='' else '')+'.root')
for year in years:
    for dy in dyList:
        for varX in varXlist:
            for varY in varYlist:
                hists[year][dy][varY][varX] = histFile.Get(year+'_'+dy+'_'+varY+'_vs_'+varX)
                hists[year][dy][varY][varX].SetDirectory(0)
            for mcut in mcutlist:
                hists[year][dy][mcut][varX] = histFile.Get(year+'_'+dy+'_'+varX+'_'+mcut)
                hists[year][dy][mcut][varX].SetDirectory(0)
histFile.Close()

rats = [['2016','2017'],['2016','2018'],['2017','2018']]
histFile = R.TFile('plots/mc_comparison_pretty'+('_'+args.extra if args.extra !='' else '')+'.root','recreate')

print 'Making plots'
# sum numerator and denominators
sums = {year:{dy:{varY:{varX:{} for varX in varXlist} for varY in varYlist+mcutlist} for dy in dyList+['all']} for year in years}
for varY in varYlist+mcutlist:
    for varX in varXlist:
        for year in years:
            for i,dy in enumerate(dyList):
                print varY,varX,year,dy
                #norm = float(mcdata[year][dy]['xs']) / mcdata[year][dy]['wsum']
                norm = float(mcdata[year][dy]['xs']) / mcdata[year][dy]['nevents']
                sums[year][dy][varY][varX] = hists[year][dy][varY][varX].Clone(varY+'_vs_'+varX+'_'+year+'_'+dy)
                sums[year][dy][varY][varX].Scale(norm)
                if i==0:
                    sums[year]['all'][varY][varX] = sums[year][dy][varY][varX].Clone(varY+'_vs_'+varX+'_'+year+'_all')
                else:
                    sums[year]['all'][varY][varX].Add(sums[year][dy][varY][varX])
                sums[year][dy][varY][varX].Write()
            sums[year]['all'][varY][varX].Write()



# Make plots
for varY in varYlist:
    for varX in varXlist:
        logy = True if 'log' in varY else False
        logx = True if 'log' in varX else False
        for denYear,numYear in rats:
            rat = sums[numYear]['all'][varY][varX].Clone(varY+'_vs_'+varX+'_rat_'+numYear+'_'+denYear)
            den = sums[denYear]['all'][varY][varX].Clone()
            rat.Divide(den)
            c = Plotter.Canvas(lumi=pretty(numYear)+' / '+pretty(denYear),logy=logy,logx=logx)
            plot = Plotter.Plot(rat,option='colz')
            c.addMainPlot(plot)
            plot.SetAxisRange(0.,2.,'Z')
            if 'log' in varX:
                c.firstPlot.GetXaxis().SetMoreLogLabels(True)
            rat.Write()
            c.cleanup('plots/'+rat.GetName()+('_'+args.extra if args.extra!='' else '')+'.pdf',mode='BOB')
for mcut in mcutlist:
    for varX in varXlist:
        c = Plotter.Canvas(cWidth=800,cHeight=800,lumi=pretty(mcut),logy=True, ratioFactor=1./3)
        plots = {}
        plotname = varX+'_'+mcut
        for year in years:
            plots[year] = Plotter.Plot(sums[year]['all'][mcut][varX].Clone(),option='pe',legType='pe',legName=pretty(year))
            c.addMainPlot(plots[year])
            plots[year].SetMarkerColor(colors(year))
            plots[year].SetMarkerStyle(markers(year))
            plots[year].SetLineColor(colors(year))
            plotname += '_'+year
        c.firstPlot.SetAxisRange(*ranges(mcut,varX))
        c.makeLegend(pos='tl')
        for r,numYear in enumerate(['2017','2018']):
            c.addRatioPlot(plots[numYear],plots['2016'],color=colors(numYear),ytit='later/'+pretty('2016'),option='pe',plusminus=1.)
            c.ratList[r].Write(varX+'_'+mcut+'_'+numYear+'_2016')
        plotname += ('_'+args.extra if args.extra!='' else '')
        c.cleanup('plots/'+plotname+'.pdf',mode='BOB')
