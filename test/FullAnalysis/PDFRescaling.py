import ROOT as R
import numpy as np
import Plotter as Plotter

dataFile = open('data_PDFRescaling.txt','read')
info = {
        'labels':[],
        'units':[],
        }
data = {}
for l,line in enumerate(dataFile):
    cols = line.strip('\n').split()
    if cols[0]=='#':
        if l==0:
            for label in cols[1:]:
                info['labels'].append(label)
                data[label] = np.array([])
            data['mmid'] = np.array([])
        elif l==1:
            for unit in cols[1:]:
                info['units'].append(unit.strip('[').strip(']'))
        else: continue
    else:
        for d,label in enumerate(info['labels']):
            data[label] = np.append(data[label],float(cols[d]))
        data['mmid'] = np.append(data['mmid'],(float(cols[0])+float(cols[1]))/2)

xs_colors = {
        'CT14':R.kBlue,
        'NNPDF30':R.kRed,
        'NNPDF31':R.kGreen+1,
        }

# plot cross sections
graphs = {
        'CT14':R.TGraphAsymmErrors(len(data['mmid']),
            data['mmid'],data['sCT14nlowlo']/(data['mhi']-data['mlo']),
            data['mmid']-data['mlo'],data['mhi']-data['mmid'],
            data['emCT14nlo']/(data['mhi']-data['mlo']),data['epCT14nlo']/(data['mhi']-data['mlo'])),
        'NNPDF30':R.TGraphAsymmErrors(len(data['mmid']),
            data['mmid'],data['sNNPDF30nlo']/(data['mhi']-data['mlo']),
            data['mmid']-data['mlo'],data['mhi']-data['mmid'],
            data['eNNPDF30nlo']/(data['mhi']-data['mlo']),data['eNNPDF30nlo']/(data['mhi']-data['mlo'])),
        'NNPDF31':R.TGraphAsymmErrors(len(data['mmid']),
            data['mmid'],data['sNNPDF31nlo']/(data['mhi']-data['mlo']),
            data['mmid']-data['mlo'],data['mhi']-data['mmid'],
            data['eNNPDF31nlo']/(data['mhi']-data['mlo']),data['eNNPDF31nlo']/(data['mhi']-data['mlo'])),
        }

canvas = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation',logy=True)
xs_plots = {plot:Plotter.Plot(graphs[plot],legName=plot,legType='pe',option='pe') for plot in graphs.keys()}
canvas.addMainPlot(xs_plots['CT14'])
canvas.addMainPlot(xs_plots['NNPDF30'])
canvas.addMainPlot(xs_plots['NNPDF31'])
for plot in xs_plots.keys():
    xs_plots[plot].SetLineColor(xs_colors[plot])
    xs_plots[plot].SetMarkerColor(xs_colors[plot])
canvas.firstPlot.setTitles(X='mass [GeV]',Y='d#sigma/dm [pb/GeV]')
canvas.firstPlot.GetYaxis().SetRangeUser(1e-12,1E1)
canvas.makeLegend(pos='tr')
canvas.legend.moveLegend(X=-0.1)
canvas.cleanup('hists/pdf/compareCrossSections_vs_mass.pdf')

# make ratio plots in loop
# CT14 / NNPDF31
# NNPDF30 / NNPDF31
ratios = {
        'CT14/NNPDF31':R.TGraph(len(data['mmid']),
            data['mmid'],data['sCT14nlowlo']/data['sNNPDF31nlo']),
        'NNPDF30/NNPDF31':R.TGraph(len(data['mmid']),
            data['mmid'],data['sNNPDF30nlo']/data['sNNPDF31nlo']),
        'CT14/NNPDF30':R.TGraph(len(data['mmid']),
            data['mmid'],data['sCT14nlowlo']/data['sNNPDF30nlo']),

        }
rat_fits = {
        'CT14/NNPDF31':R.TF1('rat_CT14_NNPDF31','pol5',150,5000),
        'NNPDF30/NNPDF31':R.TF1('rat_NNPDF30_NNPDF31','pol5',120,5000),
        'CT14/NNPDF30':R.TF1('rat_CT14_NNPDF30','pol5',150,5000),
        }
rat_colors = {
        'CT14/NNPDF31':R.kBlue,
        'NNPDF30/NNPDF31':R.kRed,
        'CT14/NNPDF30':R.kViolet+1,
        }
rat_plots = {plot:Plotter.Plot(ratios[plot],legType='pe',option='p') for plot in ratios.keys()}
for plot in ratios.keys():
    canvas = Plotter.Canvas(lumi='(13 TeV)',extra='Simulation')
    canvas.addMainPlot(rat_plots[plot])
    num,den = plot.split('/')
    rat_plots[plot].SetLineColor(rat_colors[plot])
    rat_plots[plot].SetMarkerColor(rat_colors[plot])
    rat_plots[plot].Fit(rat_fits[plot],'FR')
    pos = 'tr' if den=='NNPDF30' else 'tl'
    canvas.setFitBoxStyle(rat_plots[plot],pos=pos,lHeight=0.25)
    canvas.firstPlot.setTitles(X='mass [GeV]',Y=num+' / '+den)
    canvas.cleanup('hists/pdf/crossSectionRatios_'+num+'_'+den+'.pdf')
