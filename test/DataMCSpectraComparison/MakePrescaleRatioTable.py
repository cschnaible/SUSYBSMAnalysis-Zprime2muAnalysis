import math

prescales_lumi = {
    #1:6.93268721899,
    148:21.848360646,
    222:438.550290211,
    296:650.412667738,
    385:346.758846733,
    445:3962.37165422,
    500:55871.900725,
    }

totLumi = 0.
nums = {'all':0.,'bb':0.,'beee':0.}
dens = {'all':0.,'bb':0.,'beee':0.}

text = r'''
\begin{table}[]
\begin{tabular}{|c|c|c|c|c|}
\hline
Prescale factor & Int. Lumi pb$^{-1}$ & All & BB & BE+EE \\ \hline \hline
'''
for ip,p in enumerate(sorted(prescales_lumi.keys())):
    thisLine = '{prescale} & {lumi:.1f}'.format(prescale=str(p),lumi=(round(prescales_lumi[p],1)))
    totLumi += float(prescales_lumi[p])
    if ip==len(prescales_lumi.keys())-1: last = True
    else: last = False
    for cat in ['all','bb','beee']:
        #thisFile = open('test/vertex_m_mu27_pre'+str(p)+'_'+cat+'.log')
        thisFile = open('www_ratios/z_peak_ratio_'+cat+'_'+str(p)+'.txt')
        thisFileLines = thisFile.readlines()
        lineWithData = thisFileLines[-2]
        colsWithData = lineWithData.split()
        #num = float(colsWithData[0])
        #den = float(colsWithData[1])
        #rat = float(colsWithData[2])
        #err = float(colsWithData[3])
        rat = float(colsWithData[4])
        err = float(colsWithData[5])
        thisLine += r' & {rat:.3f} $\pm$ {err:.3f}'.format(**locals())
        nums[cat] += rat/pow(err,2)
        dens[cat] += 1./pow(err,2)
    thisLine += r'\\ \hline'
    if last: thisLine += r' \hline'
    thisLine += '\n'
    text += thisLine

totLumi = round(totLumi)
meanall = round(nums['all']/dens['all'],3)
errall = round(math.sqrt(1./dens['all']),3)
meanbb = round(nums['bb']/dens['bb'],3)
errbb = round(math.sqrt(1./dens['bb']),3)
meanbeee = round(nums['beee']/dens['beee'],3)
errbeee = round(math.sqrt(1./dens['beee']),3)
text += 'Combined & {totLumi} & {meanall} $\pm$ {errall} & {meanbb} $\pm$ {errbb} & {meanbeee} $\pm$ {errbeee} \\\ \hline\n'.format(**locals())

text += \
r'''\end{tabular}
\end{table}'''

print text


