import ROOT as R
import SUSYBSMAnalysis.Zprime2muAnalysis.Plotter as Plotter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s','--scale',default='mc',help='what to scale, data/mc or mc/mc')
args = parser.parse_args()

data_vars_to_compare = ['lead_pt','sub_pt','dil_pt']
mc_vars_to_compare = ['gen_lead_pt','gen_sub_pt','gen_dil_pt']#,'gen_dil_rap']
rels = ['80X','94X','102X']
years = [2016,2017,2018]
relYearMap = {year:rel for year,rel in zip(rels,years)}
categories = {
        'lead_pt':['all','b','e'],
        'sub_pt':['all','b','e'],
        'gen_lead_pt':['all','b','e'],
        'gen_sub_pt':['all','b','e'],
        'dil_pt':['all','bb','beee'],
        'gen_dil_pt':['all','bb','beee'],
        }
xlist = ['log','lin']
#rescaleFile = R.TFile('rescale/rescale_histograms_20190522.root')
rescaleFile = R.TFile('rescale/rescale_histograms.root')

if args.scale=='mc': # scale to mc
    hname = 'mcRat'
    nums = rels
    dens = rels
    vars_to_compare = data_vars_to_compare + mc_vars_to_compare
elif args.scale=='data': # scale to data
    hname = 'dataRat'
    nums = years
    dens = rels
    vars_to_compare = data_vars_to_compare

ratHists = {num:{den:{var:{cat:{x:{} for x in xlist} for cat in categories[var]} for var in vars_to_compare} for den in dens} for num in nums}
for num in nums:
    for den in dens:
        if num==den: continue
        for var in vars_to_compare:
            for cat in categories[var]:
                for x in xlist:
                    thehname = hname+'_'+num+'_'+den+'_'+var+'_'+cat+'_'+x
                    print thehname
                    ratHists[num][den][var][cat][x] = rescaleFile.Get(thehname).Clone()
                    ratHists[num][den][var][cat][x].SetDirectory(0)


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
        'dil_pz':'p_{Z}(#mu#mu) [GeV]',
        'gen_dil_pt':'GEN p_{T}(#mu#mu) [GeV]',
        'gen_dil_pz':'GEN p_{Z}(#mu#mu) [GeV]',
        'gen_dil_rap':'GEN y(#mu#mu)',
        }

center = 1.0
pm = 0.5
for den in dens:
    for var in vars_to_compare:
        for cat in categories[var]:
            for x in xlist:
                logx = True if x=='log' else False
                canvas = Plotter.Canvas(extra='Preliminary',lumi='(13 TeV)',logx=logx)
                plots = {}
                for num in nums:
                    if num==den:continue
                    plots[num]=Plotter.Plot(ratHists[num][den][var][cat][x],legName=legNames[num],legType='pe',option='pe')
                    canvas.addMainPlot(plots[num])
                for num in nums:
                    if num==den:continue
                    plots[num].SetLineColor(colors[num])
                    plots[num].SetMarkerColor(colors[num])
                canvas.firstPlot.GetYaxis().SetRangeUser(center-pm,center+pm)
                line = R.TLine(canvas.firstPlot.GetXaxis().GetXmin(),1,canvas.firstPlot.GetXaxis().GetXmax(),1)
                line.Draw()
                canvas.makeLegend(pos='tr')
                canvas.legend.moveLegend(X=-0.1)
                canvas.firstPlot.setTitles(X=titles[var],Y='Ratio to '+str(den))
                if logx: 
                    canvas.mainPad.SetLogx()
                canvas.Update()
                canvas.cleanup('www_nnpdf/ratio_'+args.scale+'_'+den+'_'+var+'_'+cat+'_'+x+'.png')
