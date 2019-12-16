import math

prescales_lumi = {
    59:86.8712438022,
    70:275.190535276,
    74:163.661209166,
    117:46.2436284491,
    120:4123.72145243,
    140:2413.39785073,
    148:541.983190576,
    176:860.668911332,
    210:5560.95773849,
    222:951.36024321,
    234:2050.1262438,
    280:6535.92676296,
    281:1111.61316576,
    296:1188.58563938,
    315:770.139832091,
    328:1921.36662493,
    336:1626.58354641,
    341:525.035573921,
    356:463.119019459,
    375:119.156046088,
    385:483.395320788,
    392:911.390557063,
    415:621.24955696,
    422:141.494069456,
    445:2846.99397805,
    449:752.926446731,
    458:26.4998925556,
    480:14.0916112563,
    505:2198.24925031,
    561:2704.94019996,
    }

totLumi = 0.
nums = {'all':0.,'bb':0.,'beee':0.}
dens = {'all':0.,'bb':0.,'beee':0.}

text = r'''
\begin{table}[]
\begin{tabular}{|c|c|c|c|c|}
\hline
Prescale factor & Int. Lumi pb$^{-1}$ & All & BB & BE+EE \\ \hline\hline
'''
for p in sorted(prescales_lumi.keys()):
    thisLine = '{prescale} & {lumi:.1f}'.format(prescale=str(p),lumi=(round(prescales_lumi[p],1)))
    totLumi += float(prescales_lumi[p])
    for cat in ['all','bb','beee']:
        thisFile = open('test/vertex_m_mu27_pre'+str(p)+'_'+cat+'.log')
        thisFileLines = thisFile.readlines()
        print thisFile
        lineWithData = thisFileLines[-2]
        colsWithData = lineWithData.split()
        num = float(colsWithData[0])
        den = float(colsWithData[1])
        rat = float(colsWithData[2])
        err = float(colsWithData[3])
        thisLine += r' & {rat:.3f} $\pm$ {err:.3f}'.format(**locals())
        nums[cat] += rat/pow(err,2)
        dens[cat] += 1./pow(err,2)
    thisLine += r'\\ \hline'+('\hline' if p==561 else '')
    thisLine += '\n'
    text += thisLine

totLumi = round(totLumi)
meanall = round(nums['all']/dens['all'],3)
errall = round(math.sqrt(1./dens['all']),3)
meanbb = round(nums['bb']/dens['bb'],3)
errbb = round(math.sqrt(1./dens['bb']),3)
meanbeee = round(nums['beee']/dens['beee'],3)
errbeee = round(math.sqrt(1./dens['beee']),3)
text += 'Combined & {totLumi} & {meanall} $\pm$ {errall} & {meanbb} $\pm$ {errbb} & {meanbeee} $\pm$ {errbeee}\\\ \hline\n'.format(**locals())

text += \
r'''\end{tabular}
\end{table}'''

print text


