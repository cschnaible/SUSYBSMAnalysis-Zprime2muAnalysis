import ROOT as R
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--draw-data',action='store_true',help='draw data on top of mc')
parser.add_argument('--rescale-name',default='',help='name for rescale histogram file')
args = parser.parse_args()

data_vars_to_compare = ['lead_pt','sub_pt','dil_pt','dil_rap']
vars_to_compare = data_vars_to_compare# + ['gen_lead_pt','gen_sub_pt','gen_dil_pt']
rels = ['80X','94X','102X']
years = [2016,2017,2018]
relYearMap = {year:rel for year,rel in zip(rels,years)}
categories = {
        'lead_pt':{'cats':['all','b','e'],'x':['lin','log']},
        'sub_pt':{'cats':['all','b','e'],'x':['lin','log']},
        'gen_lead_pt':{'cats':['all','b','e'],'x':['lin','log']},
        'gen_sub_pt':{'cats':['all','b','e'],'x':['lin','log']},
        'dil_pt':{'cats':['all','bb','beee'],'x':['lin','log']},
        'gen_dil_pt':{'cats':['all','bb','beee'],'x':['lin','log']},
        'dil_rap':{'cats':['all','bb','beee'],'x':['lin']},
        'gen_dil_rap':{'cats':['all','bb','beee'],'x':['lin']},
        }
#rescaleFile = R.TFile('rescale/rescale_histograms_20190522.root')
rescale_name = '_'+args.rescale_name if args.rescale_name else ''
rescaleFile = R.TFile('rescale/rescale_histograms'+rescale_name+'.root')

dataHists = {year:{var:{cat:{x:rescaleFile.Get('hdata_'+str(year)+'_'+var+'_'+cat+'_'+x).Clone() for x in categories[var]['x']} for cat in categories[var]['cats']} for var in data_vars_to_compare} for year in years}
mcHists = {rel:{var:{cat:{x:rescaleFile.Get('hmc_'+rel+'_'+var+'_'+cat+'_'+x).Clone() for x in categories[var]['x']} for cat in categories[var]['cats']} for var in vars_to_compare} for rel in rels}


legNames = {
        '80X':'80X NNPDF3.0',
        '94X':'94X NNPDF3.1',
        '102X':'102X NNPDF3.1',
        2016:'2016 Data',
        2017:'2017 Data',
        2018:'2018 Data',
        }
colors = {
        '80X':R.kRed-4,
        '94X':R.kViolet+1,
        '102X':R.kAzure+1,
        }
titles = {
        'lead_pt':'leading p_{T}(#mu) [GeV]',
        'sub_pt':'sub-leading p_{T}(#mu) [GeV]',
        'gen_lead_pt':'leading GEN p_{T}(#mu) [GeV]',
        'gen_sub_pt':'sub-leading GEN p_{T}(#mu) [GeV]',
        'dil_pt':'p_{T}(#mu#mu) [GeV]',
        'gen_dil_pt':'GEN p_{T}(#mu#mu) [GeV]',
        'dil_rap':'y(#mu#mu)',
        'gen_dil_rap':'GEN y(#mu#mu)',
        }
scales = {
        'ourpre':{
            2016:36294.5939649/146.32332663,
            2017:42079.880396/236.0850729,
            2018:61298.7752317/486.949643,
            },
        'ourcommonpre':{
            2016:36294.5939649/320,
            2017:42079.880396/561,
            2018:61298.7752317/500,
            },
        }

for var in vars_to_compare:
    for cat in categories[var]['cats']:
        for x in categories[var]['x']:
            logx = True if x=='log' else False
            for year in years:
                canvas = Plotter.Canvas(extra='Preliminary',lumi='(13 TeV)',logx=logx,logy=True,ratioFactor=1./3)
                hists = {rel:mcHists[rel][var][cat][x].Clone() for rel in rels}
                for rel in rels:
                    hists[rel].Scale(scales[args.rescale_name][year])
                mcPlots = {rel:Plotter.Plot(hists[rel],legName=legNames[rel],legType='l',option='hist') for rel in rels}
                dataHist = dataHists[year][var][cat][x].Clone()
                for rel in rels:
                    canvas.addMainPlot(mcPlots[rel])
                    mcPlots[rel].SetLineColor(colors[rel])
                canvas.makeLegend(pos='tr')
                canvas.legend.moveLegend(X=-0.1)
                canvas.firstPlot.setTitles(X=titles[var],Y='Events')
                canvas.addRatioPlot(hists['102X'],hists['80X'],xtit=titles[var],ytit='Ratio to 80X',option='hist',color=colors['102X'])
                canvas.addRatioPlot(hists['94X'],hists['80X'],xtit=titles[var],ytit='Ratio to 80X',option='hist',color=colors['94X'])
                if args.draw_data:
                    dataPlot = Plotter.Plot(dataHist,legName=legNames[year],legType='pe',option='pe')
                    canvas.addMainPlot(dataPlot)
                    canvas.addRatioPlot(dataHist,hists['80X'],xtit=titles[var],ytit='Ratio to 80X',option='pe')
                if logx: 
                    canvas.mainPad.SetLogx()
                    canvas.ratPad.SetLogx()
                    canvas.ratList[0].GetXaxis().SetMoreLogLabels(True)
                    canvas.ratList[0].GetXaxis().SetNoExponent(True)
                canvas.Update()
                if args.draw_data:
                    canvas.cleanup('www_nnpdf/'+var+'_data_'+str(year)+'_'+cat+'_'+x+rescale_name+'.png')
                else:
                    canvas.cleanup('www_nnpdf/'+var+'_mc_'+cat+'_'+x+rescale_name+'.png')
