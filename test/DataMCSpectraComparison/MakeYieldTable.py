import logging
import SUSYBSMAnalysis.Zprime2muAnalysis.lumberjack as lumberjack
#logDir = '/afs/cern.ch/user/c/cschnaib/www/private/ZPrime/2018/DataMC/plots_PreApp/edit/extra/'
#logDir = '/afs/cern.ch/user/c/cschnaib/www/private/ZPrime/2018/test/'
#logDir = 'www_yields_20190628/'
#logDir = 'www_yields_20190701/'
#logDir = 'www_yields_20190701_withJets/'
#logDir = 'www_yields_20190702_forApproval/'
logDir = 'www_yields_20190713/'
cats = ['all','bb','beee']
years = ['run2','2018','2017','2016']
pyears = {'2016':'2016','2017':'2017','2018':'2018','all':'Run2','run2':'Run2'}
pcats = {'bb':'barrel-barrel','beee':'barrel-endcap + endcap-endcap','all':'inclusive'}
masses = ['60_120','120_400','400_600','600_900','900_1300','1300_1800','1800_4000']
pmasses = {'60_120':'$60-120$','120_400':'$120-400$', '400_600':'$400-600$', '600_900':'$600-900$', '900_1300':'$900-1300$', '1300_1800':'$1300-1800$', '1800_4000':'$>1800$'}
data = {year:{cat:{mass:{} for mass in masses} for cat in cats} for year in years}
for year in years:
    for cat in cats:
        for mass in masses:
            #fname = 'mass_'+year+'_'+cat+'_nnpdf30_nnlo_bw_'+mass+'.log'
            fname = 'mass_'+year+'_'+cat+'_nnpdf30_nnlo_'+mass+'.log'
            f = open(logDir+fname)
            with open(logDir+fname) as f:
                lines = f.read().splitlines()
            #p=' & '.join([lines[-11].split()[0].strip('.00')]+[x for x in lines[-11].split()[1:] if x!='|'][:3])+' \\\\'
            p = ' '.join(lines[-1].split()[1:])
            p = pmasses[mass]+' & '+p
            data[year][cat][mass] = p
            #data[year][mass] = lines[-9]

lumberjack.setup_logger('yield_tables',logDir+'/yield_tables.txt')
logger = logging.getLogger('yield_tables')

tableBegin = r'''
\begin{table*}[htb!]
  \centering
\begin{tabular}{c@{\hspace{6pt}}c@{\hspace{6pt}}r@{\hspace{1.5pt}}c@{\hspace{1.5pt}}l@{\hspace{6pt}}|r@{\hspace{1.5pt}}c@{\hspace{1.5pt}}l@{\hspace{10pt}}r@{\hspace{1.5pt}}c@{\hspace{1.5pt}}l@{\hspace{2.5pt}}r@{\hspace{1.5pt}}c@{\hspace{1.5pt}}l}
\multicolumn{1}{c}{$m_{\MM}$ range} & Observed    & \multicolumn{3}{c}{Total}             & \multicolumn{3}{c}{$\cPZg$}           & \multicolumn{3}{c}{$\ttbar$ + other}    &   \multicolumn{3}{c}{Jet mis-}       \\
\multicolumn{1}{c}{[{GeV}]}         & yield       & \multicolumn{3}{c}{background}        & \multicolumn{3}{c}{}                  & \multicolumn{3}{c}{backgrounds}         &   \multicolumn{3}{c}{reconstruction} \\ \hline'''
tableEnd = \
'''  \end{tabular}
  \caption{The number of dimuon events for %s in the %s category for selected dimuon mass ranges. The total background is the sum of all simulated SM processes considered. The yields from SM simulation are normalized to the expected cross section, the number of events generated, the NNPDF and NNLO correction factors, and normalized to the observed yield using the number of events in the mass window $60-120\GeV$, acquired using a prescaled low threshold trigger. Uncertainties include both statistical and systematic components, summed in quadrature.}
  \label{tab:yield_%s_%s}
\end{table*}
'''

for year in years:
    for cat in cats:
        logger.info(tableBegin)
        for mass in masses:
            logger.info(data[year][cat][mass])
        logger.info(tableEnd%(pyears[year],pcats[cat],year,cat))
#print '*'*15

# \begin{table*}[htb!]
# \centering
# \topcaption{
# The number of dimuon events in various invariant mass ranges.
# The total background is the sum of the events for the SM processes listed.
# The yields from simulation are normalized relative to the expected cross sections, and overall the simulation is normalized to the observed yield using the number of events in the mass window 60--120\GeV , acquired using a prescaled low threshold trigger.
# Uncertainties include both statistical and systematic components, summed in quadrature.
# }
# \begin{tabular}{c@{\hspace{6pt}}c@{\hspace{6pt}}r@{\hspace{1.5pt}}c@{\hspace{1.5pt}}l@{\hspace{6pt}}|r@{\hspace{1.5pt}}c@{\hspace{1.5pt}}l@{\hspace{10pt}}r@{\hspace{1.5pt}}c@{\hspace{1.5pt}}l@{\hspace{0pt}}r@{\hspace{1.5pt}}c@{\hspace{1.5pt}}l}
# \multicolumn{1}{c}{$m_{\MM}$ range} & Observed    & \multicolumn{3}{c}{Total}             & \multicolumn{3}{c}{$\cPZg$}           & \multicolumn{3}{c}{$\ttbar$ + other}    &   \multicolumn{3}{c}{Jet mis-}       \\
# \multicolumn{1}{c}{[{GeV}]}         & yield       & \multicolumn{3}{c}{background}        & \multicolumn{3}{c}{}                  & \multicolumn{3}{c}{backgrounds}         &   \multicolumn{3}{c}{reconstruction} \\ \hline
# 120--400   & $244\,277$ & $260\,000$ & $\pm$ & $14\,000$ & $218\,000$ & $\pm$ & $11\,000$ & $40\,900$ & $\pm$ & $3\,500$ & \hspace{10pt} 800 & $\pm$ & 400   \\
# 400--600   &     5912   & 6290       & $\pm$ & 350       & 4340       & $\pm$ & 230       & 1900      & $\pm$ & 160      & 50  & $\pm$ & 25    \\
# 600--900   &     1311   & 1430       & $\pm$ & 80        & 1070       & $\pm$ & 60        & 340       & $\pm$ & 30       & 20  & $\pm$ & 10    \\
# 900--1300  &      244   & 268        & $\pm$ & 15        & 220        & $\pm$ & 12        & 41        & $\pm$ & 4        & 7   & $\pm$ & 4      \\
# 1300--1800 &       41   & 50         & $\pm$ & 3         & 42.6       & $\pm$ & 2.5       & 5.4       & $\pm$ & 0.9      & 2.1   & $\pm$ & 1.1   \\
# $>$1800    &        8   & 12.1       & $\pm$ & 1.5       & 9.8        & $\pm$ & 0.7       & 1.1       & $\pm$ & 0.4      & 1.2 & $\pm$ & 0.6   \\
# \end{tabular}
# \label{tab:event_yieldmumu}
# \end{table*}
