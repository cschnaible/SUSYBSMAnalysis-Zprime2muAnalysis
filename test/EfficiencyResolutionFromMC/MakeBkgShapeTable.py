logDir = '/afs/cern.ch/user/c/cschnaib/www/private/ZPrime/2018/BackgroundShape/'
cats = ['all','bb','beee']
#years = ['2016','2017','2018','all']
years = ['2017','2018']#,'all']
pyears = {'2016':'2016','2017':'2017','2018':'2018','all':'Run2'}
pcats = {'bb':'barrel-barrel','beee':'barrel-endcap + endcap-endcap','all':'inclusive'}
highparams = ['aH','bH','cH','dH','kH']
lowparams = ['aL','bL','cL','kL']
data = {year:{cat:{p:{} for p in lowparams+highparams} for cat in cats} for year in years}
for year in years:
    for cat in cats:
        fname = 'powheg_nnpdf30_nnlo_'+cat+'_'+year+'.log'
        with open(logDir+fname) as f:
            lines = f.read().splitlines()
        for line in lines:
            dat = line.split()
            if len(dat)<2: continue
            if dat[1] in lowparams+highparams:
                data[year][cat][dat[1]] = '{:7.3e}'.format(float(dat[2]))


tableBegin = r'''
\begin{table}
  \centering
  \begin{tabular}{c|cccc}
    Category & $\gamma_0$ & $\gamma_1$ & $\gamma_2$ & $\mu$ \\ \hline'''
tableMiddle = '''\
  \end{tabular}
  \\begin{tabular}{c|ccccc}
    Category & $\delta_0$ & $\delta_1$ & $\delta_2$ & $\delta_3$ & $\\nu$ \\\\ \hline'''
tableEnd = \
r'''  \end{tabular}
  \caption{Background pdf fit results for each analysis category for %s.}
  \label{tab:BkgFitResults_%s}
\end{table}
'''

for year in years:
    print tableBegin
    for cat in cats:
        l = ' & '.join([data[year][cat][d] for d in lowparams])
        l = cat+' & '+l+' \\\\'
        print l
    print tableMiddle
    for cat in cats:
        l = ' & '.join([data[year][cat][d] for d in highparams])
        l = cat+' & '+l+' \\\\'
        print l
    print tableEnd%(year,year)
print '*'*15
