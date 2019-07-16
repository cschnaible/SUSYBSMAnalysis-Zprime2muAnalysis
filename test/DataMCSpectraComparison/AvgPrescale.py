import ROOT as R
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
R.gROOT.SetBatch(True)
f = R.TFile('data/ana_datamc_Run2018ABC_17Sep2018_Run2018D_22Jan2019.root')
t = f.Get('Our2018MuPrescaledNoCommonMuonsOppSignNtuple/t')

h = R.TH1F('h_prescales','',600,0,600)

t.Draw('Mu27_prescale>>h_prescales','vertex_m>60&&vertex_m<120')

print 'Mean',h.GetMean()

c = Plotter.Canvas(lumi='61.31 fb^{-1} (13 TeV)',extra='Preliminary',logy=True)
p = Plotter.Plot(h,option='hist')
c.addMainPlot(p)
c.makeStatsBox(p)
c.firstPlot.setTitles(X='Prescale',Y='Events')
c.cleanup('test/Mu27_prescales.png')


