'''
This script will be basic charge mis-ID study plotting:
    N(q_gen != q_reco) / N(all)
'''
import ROOT as R
import math,array
import Plotter
import SUSYBSMAnalysis.Zprime2muAnalysis.roottools as roottools
import argparse
parser = argparse.ArgumentParser(description='Options for charge mis-ID study')
parser.add_argument('-n','--name',default='',help='Name of input histogram ROOT file')
parser.add_argument('-mc','--mc',default='DY',help='Which MC to plot')
parser.add_argument('-o','--outname',default='',help='Additional name to add to output')
args = parser.parse_args()


histlist = ['p','pt','eta','phi','charge']#, 'mass']
numden = ['num','den']
ptypes = ['gen']
cats = ['allcat','b','em','ep','e']

if args.mc == 'DY':
    pts = ['allpt','0to300','300to450','450to800','800to1200','1200to1600','1600to2000','2000to3000']
elif args.mc == 'MuGun':
    pts = [ 'allpt', '0to100', '100to200', '200to400', '400to700',\
        '700to1000', '1000to1500', '1500to2000', '2000to2500']
charges = ['qall','qm','qp']

hists = {p:{x:{cat:{pt:{q:{} for q in charges} for pt in pts} for cat in cats} for x in ptypes} for p in numden}

OUT = '_'+args.outname if args.outname else ''

inFile = R.TFile('chargeMisIDPlots'+('_'+args.name if args.name else '')+'.root')
for p in numden:
    for x in ptypes:
        for cat in cats:
            for pt in pts:
                for q in charges:
                    for h in histlist:
                        hname = h+'_'+x+'_'+cat+'_'+pt+'_'+q+'_'+p
                        print hname
                        hists[p][x][cat][pt][q][h] = inFile.Get(hname).Clone()
                        print hists[p][x][cat][pt][q][h]


titles = {
        'eta':'muon #eta',
        'phi':'muon #phi',
        'pt':'muon p_{T} [GeV]',
        'p':'muon p [GeV]',
        'mass':'m(#mu#mu) [GeV]',
        'charge':'gen muon charge',
        }
chcolors = {'qm':R.kGreen+1,'qp':R.kMagenta}
chlegends = {'qm':'#mu^{-}','qp':'#mu^{+}'}
colors = {'b':R.kBlue, 'em':R.kRed, 'ep':R.kOrange, 'e':R.kGreen}
legends = {'b':'barrel', 'em':'endcap -', 'ep':'endcap +','e':'endcap'}
whichCats = {'esep':['b','em','ep'],'ecomb':['b','e']}

# Save num/den plots
#for x in ptypes:
#    for cat in cats:
#        for pt in pts:
#            for q in charges:
#                for hist in histlist:
#
#                    print x,cat,pt,q,hist
#                    if hists['den'][x][cat][pt][q][hist].GetEntries()==0 or hists['den'][x][cat][pt][q][hist].Integral()==0:
#                        print '*'*45
#                        print 'skipping hist'
#                        print '*'*45
#                        continue
#                    rat,r,erl,erh = roottools.binomial_divide(hists['num'][x][cat][pt][q][hist],hists['den'][x][cat][pt][q][hist])
#                    print hists['num'][x][cat][pt][q][hist],hists['den'][x][cat][pt][q][hist]
#                    for logy in [True,False]:
#                        c = Plotter.Canvas(lumi='',extra='Charge mis-ID rate',logy=logy)
#                        p = Plotter.Plot(rat,option='pe')
#                        c.addMainPlot(p)
#                        p.setTitles(Y='Charge mis-ID rate',X=titles[hist])
#                        ymin = 1e-5 if logy else 0
#                        ymax = 1. if logy else 0.04/100
#                        p.SetMinimum(ymin)
#                        p.SetMaximum(ymax)
#                        c.cleanup('plots/ratio_'+hist+'_'+x+'_'+cat+'_pt'+pt+'_'+q+('_logy' if logy else '')+OUT+'.pdf',mode='BOB')
#                    for pl in numden:
#                        for logy in [True,False]:
#                            c = Plotter.Canvas(lumi='',extra='',logy=logy)
#                            p = Plotter.Plot(hists[pl][x][cat][pt][q][hist],option='he')
#                            c.addMainPlot(p)
#                            p.setTitles(Y='N(#mu)',X=titles[hist])
#                            ymin = 1e-1 if logy else 0
#                            p.SetMinimum(ymin)
#                            c.cleanup('plots/'+pl+'_'+hist+'_'+x+'_'+cat+'_pt'+pt+'_'+q+('_logy' if logy else '')+OUT+'.pdf',mode='BOB')



# Comparison of ratios for eta categories
for x in ptypes:
    for pt in pts:
        for hist in histlist:
            for q in charges:
                for whichCat in whichCats:
                    for logy in [True,False]:
                        plots = {}
                        c = Plotter.Canvas(lumi='',extra='Charge mis-ID rate',logy=logy)
                        skipped = []
                        for cat in whichCats[whichCat]:
                            if hists['den'][x][cat][pt][q][hist].GetEntries()==0 or hists['den'][x][cat][pt][q][hist].Integral()==0:
                                print '*'*45
                                print 'skipping hist'
                                print '*'*45
                                skipped.append(cat)
                                continue
                            num = hists['num'][x][cat][pt][q][hist].Clone()
                            den = hists['den'][x][cat][pt][q][hist].Clone()
                            rat,r,erl,erh = roottools.binomial_divide(num,den)
                            plots[cat] = Plotter.Plot(rat,option='pe',legName=legends[cat],legType='pe')
                        for cat in whichCats[whichCat]: 
                            if cat in skipped: continue
                            c.addMainPlot(plots[cat])
                        for cat in whichCats[whichCat]:
                            if cat in skipped: continue
                            plots[cat].SetLineColor(colors[cat])
                            plots[cat].SetMarkerColor(colors[cat])
                        if c.firstPlot is None: continue
                        c.firstPlot.setTitles(Y='Charge mis-ID rate',X=titles[hist])
                        ymin = 1e-6 if logy else 0
                        ymax = 1. if logy else 0.006
                        c.firstPlot.SetMinimum(ymin)
                        c.firstPlot.SetMaximum(ymax)
                        c.makeLegend()
                        c.cleanup('plots/ratio_'+hist+'_'+x+'_'+whichCat+'_pt'+pt+'_'+q+('_logy' if logy else '')+OUT+'.pdf',mode='BOB')

# Comparison of ratios for charges
for x in ptypes:
    for pt in pts:
        for hist in ['eta']:#histlist:
            for cat in cats:
                for logy in [True,False]:
                    plots = {}
                    c = Plotter.Canvas(lumi='',extra='Charge mis-ID rate',logy=logy)
                    skipped = []
                    for q in ['qm','qp']:
                        num = hists['num'][x][cat][pt][q][hist].Clone()
                        if hist=='eta':num.Rebin(2)
                        den = hists['den'][x][cat][pt][q][hist].Clone()
                        if hist=='eta':den.Rebin(2)
                        if den.Integral()==0 or den.GetEntries()==0: 
                            skipped.append(q)
                            continue
                        rat,r,erl,erh = roottools.binomial_divide(num,den)
                        plots[q] = Plotter.Plot(rat,option='pe',legName=chlegends[q],legType='pe')
                    for q in ['qm','qp']: 
                        if q in skipped: continue
                        c.addMainPlot(plots[q])
                    for q in ['qm','qp']:
                        if q in skipped: continue
                        plots[q].SetLineColor(chcolors[q])
                        plots[q].SetMarkerColor(chcolors[q])
                    if len(plots.keys())==0: continue
                    c.firstPlot.setTitles(Y='Charge mis-ID rate',X=titles[hist])
                    ymin = 1e-6 if logy else 0
                    ymax = 1. if logy else 0.006
                    c.firstPlot.SetMinimum(ymin)
                    c.firstPlot.SetMaximum(ymax)
                    c.makeLegend()
                    c.cleanup('plots/ratio_'+hist+'_'+x+'_'+cat+'_pt'+pt+'_qcomp'+('_logy' if logy else '')+OUT+'.pdf',mode='BOB')

# Comparison of num and den plots for charges
# Save num/den plots
for x in ptypes:
    for cat in cats:
        for pt in pts:
            for hist in ['eta']:#histlist:
                for pl in ['num']:#numden:
                    for logy in [True,False]:
                        ratF = 1./3 if hist=='eta' else 0
                        c = Plotter.Canvas(lumi='',ratioFactor=ratF,extra='',logy=logy)

                        hm = hists[pl][x][cat][pt]['qm'][hist].Clone()
                        if hist=='eta':hm.Rebin(5)
                        pm = Plotter.Plot(hm,legName=chlegends['qm'],option='pe')

                        hp = hists[pl][x][cat][pt]['qp'][hist].Clone()
                        if hist=='eta':hp.Rebin(5)
                        pp = Plotter.Plot(hp,legName=chlegends['qp'],option='pe')

                        c.addMainPlot(pm)
                        c.addMainPlot(pp)
                        pm.SetLineColor(chcolors['qm'])
                        pm.SetMarkerColor(chcolors['qm'])
                        pp.SetLineColor(chcolors['qp'])
                        pp.SetMarkerColor(chcolors['qp'])
                        c.firstPlot.setTitles(Y='N(#mu)',X=titles[hist])
                        ymin = 1e-1 if logy else 0
                        c.firstPlot.SetMinimum(ymin)
                        c.setMaximum(recompute=True,use_error_bars=True)
                        c.makeLegend()
                        if hist=='eta':
                            c.addRatioPlot(pm,pp,ytit='#mu^{-} / #mu^{+}',xtit=titles[hist],option='pe',plusminus=1.)
                        c.cleanup('plots/'+pl+'_'+hist+'_'+x+'_'+cat+'_pt'+pt+'_qcomp'+('_logy' if logy else '')+OUT+'.pdf',mode='BOB')
