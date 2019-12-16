#!/usr/bin/env python

# (py trigeffvmass.py >! plots/out.trigeffvsmassmctruth) && (py trigeffvmass.py vbtf >! plots/out.trigeffvsmassmctruth_vbtf) && tlp plots/*trigeffvsmassmctruth*

import sys, os
from array import array
import argparse
import logging
parser = argparse.ArgumentParser()

parser.add_argument('-w','--which',default='Our2018OppSignEfficiency',
        help='Histogram directory')
parser.add_argument('-c','--category',default='all',
        help='Eta category to plot. Defaults to [bb,beee,all]')
parser.add_argument('-d','--plot-dir',default='plots',
        help='Directory to save plots')
parser.add_argument('--individual-plots',dest='make_individual_plots',action='store_true',default=False,
        help='Make individual plots')
parser.add_argument('--individual-effs',dest='make_individual_effs',action='store_true',default=False,
        help='Make individual effs')
parser.add_argument('--rebin',type=int,default=80,
        help='Rebin factor')
parser.add_argument('--do-fit',action='store_true',default=False,dest='do_fit',
        help='Parametrize efficiencies')
parser.add_argument('-xmax',default=8000,dest='xmax',type=int,
        help='X-axis maximum value')
parser.add_argument('-o','--output-name',dest='output_name',default='',
        help='Extra name to apply to histogram output')

args = parser.parse_args()


from SUSYBSMAnalysis.Zprime2muAnalysis.roottools import *
#setTDRStyle()
set_zp2mu_style()
ROOT.gStyle.SetPadTopMargin(0.02)
ROOT.gStyle.SetPadRightMargin(0.04)
ROOT.TH1.AddDirectory(0)
ROOT.gROOT.SetBatch(True)

types = ['AccNoPt', 'Acceptance', 'RecoWrtAcc', 'RecoWrtAccTrig', 'TotalReco', 'TrigWrtAcc']
doZ = True if 'AtZ' in args.which else False
zptrig = ['HLTPath_Mu50','HLTPath_OldMu100','HLTPath_TkMu100']
ztrig = ['HLTPath_Mu27']
types += ztrig if doZ else zptrig

colors =  [ROOT.kBlack,   ROOT.kRed, ROOT.kBlue, ROOT.kViolet,            8,            40,ROOT.kOrange+1, ROOT.kMagenta,   ROOT.kGreen]
samples = ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf']

mranges = [(int(x.replace('dy','').split('to')[0]) if int(x.replace('dy','').split('to')[0])!=50 else 60,int(x.replace('dy','').split('to')[1] if x.replace('dy','').split('to')[1]!='Inf' else 10000)) for x in samples if 'dy' in x]
dy = [(x,mranges[i]) for i,x in enumerate(samples) if 'dy' in x]
xtotarr = array('d',[mlo for s,(mlo,mhi) in dy]+[10000])
print dy
print xtotarr

which = args.which
plot_dir = args.plot_dir
output_name = args.output_name
rebin_factor = args.rebin
make_individual_plots = args.make_individual_plots
make_individual_effs = args.make_individual_effs
plot_categories = ['all','bb','be'] if args.category=='all' else [args.category]
categories = {'all':'','bb':'_bb','be':'_e'}

files = {}
plots = {c:{} for c in plot_categories}

samples_totals = {c:[] for c in plot_categories}

plot_dir_base = os.path.join(plot_dir,output_name)
print '%30s%30s%30s%30s%30s' % ('sample', 'type', 'num', 'den', 'eff')
for sample,(mlo,mhi) in dy:
    f = files[sample] = ROOT.TFile('mc/ana_effres_%s.root' % sample)
    d = f.Get(which)
    if make_individual_plots or make_individual_effs:
        ps = plot_saver(os.path.join(plot_dir_base,'samples',sample), pdf=True, C=True,log=False)

    for c in plot_categories:
        cat = categories[c]
        for t in types:
            num = d.Get('Num' + t + cat).Clone()
            den = d.Get('Den' + t + cat).Clone()

            # Get cumulative numbers before changing axes ranges and rebinning
            cnum = get_integral(num,mlo,mhi,integral_only=True)
            cden = get_integral(den,mlo,mhi,integral_only=True)
            print '%30s%30s%30f%30f%30f' % (sample, t+'_'+c, cnum, cden, cnum/cden)
            sys.stdout.flush()
            samples_totals[c].append((sample, t, cnum, cden, mlo, mhi))

            num.SetAxisRange(0,args.xmax,'X')
            den.SetAxisRange(0,args.xmax,'X')
            num.Rebin(rebin_factor)
            den.Rebin(rebin_factor)

            if make_individual_plots:
                num.Draw()
                ps.save(t + 'Num' + cat,log=False)
                den.Draw()
                ps.save(t + 'Den' + cat,log=False)

                num.SetLineColor(ROOT.kRed)
                den.SetLineColor(ROOT.kBlack)
                den.Draw()
                num.Draw('same')
                ps.save(t + 'Both' + cat,log=False)

            if make_individual_effs:
                eff,y,eyl,eyh = binomial_divide(num, den)
                eff.Draw('AP')
                if t not in ['AccNoPt', 'Acceptance']:
                    eff.GetYaxis().SetRangeUser(0., 1.01)
                else:
                    eff.GetYaxis().SetRangeUser(0., 1.05)
                ps.save(t, log=False)
            else:
                eff = None

            plots[c][(sample, t)] = (num, den, eff)


ps = plot_saver(plot_dir_base, pdf=True,log=False)

ps.set_plot_dir(os.path.join(plot_dir_base,'totals'))
totals_histos = {c:{t:{} for t in types} for c in plot_categories}
for c in plot_categories:
    for t in types:
        name = t+'_totals_'+c+'_'
        totals_histos[c][t] = [ROOT.TH1F(name+h,'',int(len(xtotarr)-1),xtotarr) for h in ['num','den']]

    for sample, t, cnum, cden, mlo, mhi in samples_totals[c]:
        hnum, hden = totals_histos[c][t]
        mass = hden.FindBin(mlo)
        hnum.SetBinContent(mass, cnum)
        hden.SetBinContent(mass, cden)

    for t in types:#sorted(totals_histos.iterkeys()):
        hnum,hden = totals_histos[c][t]
        eff,y,eyl,eyh = binomial_divide(hnum,hden)
        totals_histos[c][t+'_eff'] = eff
        if t.startswith('Acc'):
            eff.GetYaxis().SetRangeUser(0., 1.01)
        elif 'Reco' in t:
            eff.GetYaxis().SetRangeUser(0., 1.01)
        else:
            eff.GetYaxis().SetRangeUser(0., 1.01)
        eff.Draw('AP')
        ps.save(t+'_totals_'+c, log=False)

def do_overlay(name, samples, which, c):
    if not samples:
        return
    x = 'AP'
    for i, ((sample, (mlo,mhi)), color) in enumerate(zip(samples, colors)):
        g = plots[c][(sample, which)][-1]
        g.SetLineColor(color)
        g.Draw(x)
        g.GetXaxis().SetRangeUser(0, args.xmax)
        if which not in ['AccNoPt', 'Acceptance']:
            g.GetYaxis().SetRangeUser(0.0, 1.05)
        else:
            g.GetYaxis().SetRangeUser(0.0, 1.05)
        x = 'P same'
    ps.save('%s_%s_overlay_%s' % (name, which, c),log=False)

ps.set_plot_dir(os.path.join(plot_dir_base,'overlay'))
if make_individual_effs:
    for c in plot_categories:
        for t in types:
            do_overlay('dy',dy,t,c)

def do_replace_or_add(name, c, samples, which, add=False):
    if not samples:
        return
    num = plots[c][(samples[0][0], which)][0].Clone('%s_numtot' % name)
    den = plots[c][(samples[0][0], which)][1].Clone('%s_dentot' % name)
    num.SetAxisRange(0,args.xmax,'X')
    den.SetAxisRange(0,args.xmax,'X')
    assert(num.GetNbinsX() == den.GetNbinsX())
    for i in xrange(1, len(samples)):
        n = plots[c][(samples[i][0], which)][0]
        d = plots[c][(samples[i][0], which)][1]
        n.SetAxisRange(0,args.xmax,'X')
        d.SetAxisRange(0,args.xmax,'X')
        assert(n.GetNbinsX() == d.GetNbinsX() and n.GetNbinsX() == num.GetNbinsX())
        for j in xrange(0, n.GetNbinsX()+1):
            if add:
                num.SetBinContent(j, num.GetBinContent(j) + n.GetBinContent(j))
                den.SetBinContent(j, den.GetBinContent(j) + d.GetBinContent(j))
            else: # replace
                if d.GetBinContent(j):
                    num.SetBinContent(j, n.GetBinContent(j))
                    den.SetBinContent(j, d.GetBinContent(j))

    num.SetLineColor(ROOT.kRed)
    den.SetLineColor(ROOT.kBlack)
    den.Draw('hist')
    num.Draw('hist same')
    ps.save('%s_%s_%s_%s_both' % (name, which, c, 'add' if add else 'replace'))

    eff,y,eyl,eyh = binomial_divide(num, den)
    eff.Draw('AP')
    eff.GetXaxis().SetRangeUser(50, args.xmax)
    if which.startswith('Acc'):
        eff.GetYaxis().SetRangeUser(0., 1.01)
    elif 'Reco' in which:
        eff.GetYaxis().SetRangeUser(0., 1.01)
    else:
        eff.GetYaxis().SetRangeUser(0., 1.01)
        
    eff.SetTitle('')
    eff.GetXaxis().SetTitle('m(#mu^{+}#mu^{-}) [GeV]')
    eff.GetYaxis().SetTitleOffset(1.2);
    eff.GetYaxis().SetTitle('Acceptance' if which in ['AccNoPt', 'Acceptance'] else 'Efficiency')
    ps.save('%s_%s_%s_%s' % (name, which, c, 'add' if add else 'replace'), log=False)
    return eff

ps.set_plot_dir(os.path.join(plot_dir_base,'add'))
final_plots = {c:{} for c in plot_categories}
for c in plot_categories:
    for t in types:
        final_plots[c][t] = do_replace_or_add('dy', c, dy, t, add=True)

#for c in plot_categories:
#    for x,y in final_plots[c].iteritems():
#        do = '%s_%s = y' % (x,c)
#        exec do
   
ps.set_plot_dir(os.path.join(plot_dir_base,'summary'))
# Compare efficiency for all eta categories
pretty_eta = {
        'all':{'color':ROOT.kBlack,    'style':20, 'leg':'All'},
        'bb': {'color':ROOT.kOrange+2, 'style':21, 'leg':'BB'}, 
        'be': {'color':ROOT.kBlue,     'style':22, 'leg':'BE+EE'},
        }
for t in types:
    plots = {}
    lg = ROOT.TLegend(0.16, 0.23, 0.47, 0.40)
    draw = 'AP'
    for c in plot_categories:
        plots[c] = final_plots[c][t]
        plots[c].SetMarkerStyle(pretty_eta[c]['style'])
        plots[c].SetMarkerColor(pretty_eta[c]['color'])
        plots[c].SetMarkerSize(1.2)
        plots[c].SetLineColor(pretty_eta[c]['color'])
        lg.AddEntry(plots[c], pretty_eta[c]['leg'], 'LPE')
        plots[c].Draw(draw)
        draw = 'P same'
        plots[c].GetXaxis().SetRangeUser(0, args.xmax)
        plots[c].GetYaxis().SetRangeUser(0.0, 1.0)
    lg.Draw()
    tex = ROOT.TPaveLabel(0.50, 0.84, 0.90, 0.94, 'CMS Simulation   #sqrt{s} = 13 TeV', 'brNDC')
    tex.SetTextFont(42)
    tex.SetTextSize(0.39)
    tex.SetBorderSize(0)
    tex.SetFillColor(0)
    tex.SetFillStyle(0)
    tex.Draw()                                        
    ps.save(t+'_eta_summary', log=False)

fit_fncs = {c:{x:{} for x in ['low','high']} for c in plot_categories}
fit_windows = {
    'all':{'low':[120,800],'high':[800,6000]},
    'bb':{'low':[120,600],'high':[600,6000]},
    'be':{'low':[120,450],'high':[450,6000]},
    }
for c in plot_categories:
    fit_fncs[c]['low']['f'] = ROOT.TF1(c+'_low','[0]+[1]*exp(-1*(x-[2])/[3])+[4]*pow(x,[5])',*fit_windows[c]['low'])
    fit_fncs[c]['low']['f'].SetParameters(5,1,0,0,-10,0)
    fit_fncs[c]['low']['pretty'] = 'a + b*e^{-#frac{(m-c)}{d}} + e*m^{f}'
    if c=='all':
        fit_fncs[c]['high']['f'] = ROOT.TF1(c+'_high','[0]+[1]/(pow((x+[2]),3))+[3]*x*x',*fit_windows[c]['high'])
        #fit_fncs[c]['high']['f'].SetParameters()
        fit_fncs[c]['high']['pretty'] = 'a + #frac{b}{(m+c)^{3}} + d*x^{2}'
    elif c=='bb':
        fit_fncs[c]['high']['f'] = ROOT.TF1(c+'_high','[0]+[1]/(x+[2])+[3]*x',*fit_windows[c]['high'])
        fit_fncs[c]['high']['pretty'] = 'a + #frac{b}{(m+c)} + d*x'
    elif c=='be':
        fit_fncs[c]['high']['f'] = ROOT.TF1(c+'_high','[0]+[1]*pow(x,[2])*exp(-(x-[3])/[4])',*fit_windows[c]['high'])
        fit_fncs[c]['high']['pretty'] = 'a + b*m^{2}*e^{-#frac{m-d}{e}}'
    else:
        print c,'stop'
        exit()

# Compare Reco efficiencies wrt acc+trig, acc, and total
for c in plot_categories:
    for h,col,m in [(final_plots[c]['RecoWrtAccTrig'], ROOT.kRed, 20), (final_plots[c]['RecoWrtAcc'], ROOT.kGreen+2, 21), (final_plots[c]['TotalReco'], ROOT.kBlue, 22)]:
        h.SetMarkerStyle(m)
        h.SetMarkerColor(col)
        h.SetMarkerSize(1.2)
        h.SetLineColor(col)
    lg = ROOT.TLegend(0.20, 0.16, 0.92, 0.36)
    lg.AddEntry(final_plots[c]['RecoWrtAccTrig'], 'w.r.t. triggered events in acceptance', 'LPE')
    lg.AddEntry(final_plots[c]['RecoWrtAcc'], 'w.r.t. events in acceptance', 'LPE')
    lg.AddEntry(final_plots[c]['TotalReco'], 'total', 'LPE')
    final_plots[c]['RecoWrtAccTrig'].GetXaxis().SetRangeUser(0, args.xmax)
    final_plots[c]['RecoWrtAccTrig'].GetYaxis().SetRangeUser(0., 1.)
    final_plots[c]['RecoWrtAccTrig'].GetYaxis().SetTitleOffset(1.0);
    final_plots[c]['RecoWrtAccTrig'].Draw('AP')
    final_plots[c]['RecoWrtAcc'].Draw('P same')
    final_plots[c]['TotalReco'].Draw('P same')
    if args.do_fit:
        fcn.SetParLimits(1,-9e6,-1.e4)
        fcn.SetParLimits(2,1e7,1.e14)
        fcn.SetParNames("a", "b", "c")
        fcn.SetLineColor(TotalReco.GetLineColor())
        lg.AddEntry(fcn, 'fit to a + b/pow(m, 3) + m^2/d for m in 200-3500 GeV', 'L')
    lg.SetTextFont(42)
    lg.Draw()

    if args.do_fit:
        ROOT.gStyle.SetOptFit(1111)
        for x in ['low','high']:
            final_plots[c]['TotalReco'].Fit(fit_fncs[c][x]['f'], 'VR')
            fit_fncs[c][x]['f'].SetLineColor(final_plots[c]['TotalReco'].GetLineColor())
    ps.c.Update()
    #s = TotalReco.GetListOfFunctions().FindObject('stats')
    ##s = RecoWrtAcc.GetListOfFunctions().FindObject('stats')
    #s.SetFitFormat('5.3g')
    #s.SetX1NDC(0.49)
    #s.SetY1NDC(0.37)
    #s.SetX2NDC(0.92)
    #s.SetY2NDC(0.61)
    t = ROOT.TPaveLabel(0.58, 0.60, 0.86, 0.70, 'CMS Simulation   #sqrt{s} = 13 TeV', 'brNDC')
    #t.SetTextFont(42)
    t.SetTextSize(0.38)
    t.SetBorderSize(0)
    t.SetFillColor(0)
    t.SetFillStyle(0)
    t.Draw()                                        
    ps.save('summary_recoeff_'+c, log=False)

#    residuals = TotalReco.Clone('residuals')
#    x,y = ROOT.Double(), ROOT.Double()
#    for i in xrange(TotalReco.GetN()):
#        TotalReco.GetPoint(i, x, y)
#        f = fcn.Eval(x)
#        residuals.SetPoint(i, x, f/y-1)
#    residuals.GetXaxis().SetRangeUser(0, 6000)
#    residuals.SetTitle(';dimuon invariant mass (GeV);relative residual f/h-1')
#    residuals.Draw('AP')
#    residuals.Fit('pol1', 'VR', '', *fitwindow)
#    fcn = residuals.GetFunction('pol1')
#    fcn.SetParNames('a', 'b')
#    ps.c.Update()
#    residuals.GetYaxis().SetRangeUser(-0.1, 0.1)
#    residuals.GetYaxis().SetTitleOffset(1.2)
#    lg = ROOT.TLegend(0.14, 0.32, 0.44, 0.39)
#    lg.AddEntry(fcn, 'Fit to a + bx', 'L')
#    lg.Draw()
#    s = residuals.GetListOfFunctions().FindObject('stats')
#    s.SetX1NDC(0.14)
#    s.SetY1NDC(0.14)
#    s.SetX2NDC(0.54)
#    s.SetY2NDC(0.31)
#    ps.save('totalreco_fit_residuals', log=False)

# Dump the values of the total reconstruction curve.  Also print effs.
# for 60-120 and 120-200 GeV bins from the total counts.
print '\nTotal efficiencies (acceptance times trigger+reconstruction+selection efficiencies)'
for cat in plot_categories:
    print '\n',cat
    print '%20s%10s%20s' % ('mass range', 'eff', '68%CL interval')
    x,y = ROOT.Double(), ROOT.Double()
    g = totals_histos[cat]['TotalReco_eff']
    g.GetPoint(0, x, y)
    print '%20s%10.4f%20s' % ( '60-120', y, '[%5.4f, %5.4f]' % (y-g.GetErrorYlow(0), y+g.GetErrorYhigh(0)))
    g = final_plots[c]['TotalReco']
    n = g.GetN()
    for i in xrange(n):
        g.GetPoint(i, x, y)
        exl = g.GetErrorXlow(i)
        exh = g.GetErrorXhigh(i)
        eyl = g.GetErrorYlow(i)
        eyh = g.GetErrorYhigh(i)
        print '%20s%10.4f%20s' % ('%.f-%.f' % (x-exl, x+exh), y, '[%5.4f, %5.4f]' % (y-eyl, y+eyh))
