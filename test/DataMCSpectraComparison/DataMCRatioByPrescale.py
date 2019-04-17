import ROOT as R
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-r','--recreate',action='store_true',help='Recreate data counts')
args = parser.parse_args()

masslist = ['60m120','m120','all']
catlist = ['all','bb','beee']
prescalelist = [1,148,222,296,385,445,500]
plumi = {
        1:7.,
        148:22.,
        222:438.,
        296:647.,
        385:345.,
        445:3963.,
        500:53692.+782,
        }

def get_sum_weights(f):
    weights = getattr(f,'EventCounter').Get('weights')
    return weights.GetBinContent(2)-weights.GetBinContent(1)

if args.recreate:
    f = R.TFile('data/ana_datamc_Run2018ABCD_nocommon_inc.root')
    t = f.Get('Our2018MuPrescaledNoCommonMuonsOppSignNtuple/t')
    from RunPrescaleDict import RunPrescaleDict

    hists = {mass:{cat:{pre:R.TH1F('h_'+mass+'_'+cat+'_'+str(int(pre)),'',5000,0,5000) for pre in prescalelist} for cat in catlist} for mass in masslist}
    counts = {mass:{cat:{pre:0. for pre in prescalelist} for cat in catlist} for mass in masslist}

    for e,event in enumerate(t):
        if e%100000==0: print e
        masses = {
                '60m120':60 <= t.vertex_m < 120,
                'm120': t.vertex_m >= 120,
                'all': t.vertex_m >= 60,
                }
        cats = {
                'all':True,
                'bb':abs(t.lep_eta[0])<1.2 and abs(t.lep_eta[1])<1.2,
                'beee':abs(t.lep_eta[0])>=1.2 or abs(t.lep_eta[1])>=1.2,
                }
        if t.run == 315366:
            prescale = 222 if t.lumi < 3 else 296
        elif t.run == 315365:
            prescale = 222 if t.lumi < 16 else 296
        else:
            prescale = RunPrescaleDict[t.run]
        for mass in masses:
            for cat in cats:
                if cats[cat] and masses[mass]:
                    hists[mass][cat][prescale].Fill(t.vertex_m)
                    counts[mass][cat][prescale] += 1

    outF = R.TFile('Z0NormalizationByPrescale_Run2018ABCD_inc.root','recreate')
    for mass in masslist:
        for cat in catlist:
            for pre in prescalelist:
                hists[mass][cat][prescale].Write()
    print counts
else:
    from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples_chris import samples
    from SUSYBSMAnalysis.Zprime2muAnalysis.roottools import clopper_pearson_poisson_means
    #ndata = {'60m120': {'all': {1: 3711.0, 385: 183874.0, 296: 338741.0, 148: 11600.0, 500: 29426053.0, 445: 2085979.0, 222: 226254.0}, 'beee': {1: 2202.0, 385: 107068.0, 296: 195751.0, 148: 6766.0, 500: 17148543.0, 445: 1210696.0, 222: 130721.0}, 'bb': {1: 1509.0, 385: 76806.0, 296: 142990.0, 148: 4834.0, 500: 12277510.0, 445: 875283.0, 222: 95533.0}}, 'all': {'all': {1: 3818.0, 385: 187880.0, 296: 346027.0, 148: 11877.0, 500: 30064543.0, 445: 2130932.0, 222: 231210.0}, 'beee': {1: 2282.0, 385: 109655.0, 296: 200515.0, 148: 6929.0, 500: 17558452.0, 445: 1239286.0, 222: 133848.0}, 'bb': {1: 1536.0, 385: 78225.0, 296: 145512.0, 148: 4948.0, 500: 12506091.0, 445: 891646.0, 222: 97362.0}}, 'm120': {'all': {1: 107.0, 385: 4006.0, 296: 7286.0, 148: 277.0, 500: 638490.0, 445: 44953.0, 222: 4956.0}, 'beee': {1: 80.0, 385: 2587.0, 296: 4764.0, 148: 163.0, 500: 409909.0, 445: 28590.0, 222: 3127.0}, 'bb': {1: 27.0, 385: 1419.0, 296: 2522.0, 148: 114.0, 500: 228581.0, 445: 16363.0, 222: 1829.0}}}
    ndata = {'60m120': {'all': {1: 6.0, 385: 441.0, 296: 1125.0, 148: 78.0, 500: 58028.0, 445: 4711.0, 222: 1003.0}, 'beee': {1: 3.0, 385: 260.0, 296: 647.0, 148: 48.0, 500: 33753.0, 445: 2727.0, 222: 555.0}, 'bb': {1: 3.0, 385: 181.0, 296: 478.0, 148: 30.0, 500: 24275.0, 445: 1984.0, 222: 448.0}}, 'all': {'all': {1: 6.0, 385: 455.0, 296: 1148.0, 148: 80.0, 500: 59247.0, 445: 4824.0, 222: 1017.0}, 'beee': {1: 3.0, 385: 268.0, 296: 663.0, 148: 50.0, 500: 34534.0, 445: 2814.0, 222: 565.0}, 'bb': {1: 3.0, 385: 187.0, 296: 485.0, 148: 30.0, 500: 24713.0, 445: 2010.0, 222: 452.0}}, 'm120': {'all': {1: 0.0, 385: 14.0, 296: 23.0, 148: 2.0, 500: 1219.0, 445: 113.0, 222: 14.0}, 'beee': {1: 0.0, 385: 8.0, 296: 16.0, 148: 2.0, 500: 781.0, 445: 87.0, 222: 10.0}, 'bb': {1: 0.0, 385: 6.0, 296: 7.0, 148: 0.0, 500: 438.0, 445: 26.0, 222: 4.0}}}
    #inF = R.TFile('Z0NormalizationByPrescale_Run2018ABCD_inc.root')
    #print inF
    #inF.ls()
    #hists = {mass:{cat:{pre:{} for pre in prescalelist} for cat in catlist} for mass in masslist}
    #for mass in masslist:
    #    for cat in catlist:
    #        for pre in prescalelist:
    #            name = 'h_'+mass+'_'+cat+'_'+str(int(pre))
    #            print name
    #            hists[mass][cat][pre] = inF.Get(name)
    #print hists
    #mchists = {sample.name:{} for sample in samples}
    #nevents = {sample.name:{} for sample in samples}
    nraw = {sample.name:{mass:{cat:{} for cat in catlist} for mass in masslist} for sample in samples}
    tdir = 'Our2018MuPrescaledMuonsOppSignNtuple'
    for i,sample in enumerate(samples):
        print sample.name
        f = R.TFile('mc/ana_datamc_'+sample.name+'.root')
        t = f.Get(tdir+'/t')
        #hmcs = hist.Clone('h'+sample.name)
        #drawstring = toDraw+'>> h'+sample.name
        #t.Draw(drawstring,mccutweight,args.style)
        #hmcs.SetDirectory(0)
        #mchists[sample.name]=hmcs
        #mchists[sample.name].SetDirectory(0)
        #nevents[sample.name] = get_sum_weights(f)
        nevents = get_sum_weights(f)
        masses = {
                '60m120':'(60 <= vertex_m  && vertex_m < 120)',
                'm120': '(vertex_m >= 120)',
                'all': '(vertex_m >= 60)',
                }
        cats = {
                'all':'1.',
                'bb':'(abs(lep_eta[0])<1.2 && abs(lep_eta[1])<1.2)',
                'beee':'(abs(lep_eta[0])>=1.2 || abs(lep_eta[1])>=1.2)',
                }
        for pre in prescalelist:
            for mass in masses:
                for cat in cats:
                    cut = masses[mass]+' && '+cats[cat]
                    n = float(t.GetEntries(cut+' && genWeight>0'))-float(t.GetEntries(cut+' && genWeight<0'))
                    nraw[sample.name][mass][cat] = n * sample.cross_section / float(nevents)
        f.Close()
    print nraw

    mctot = {mass:{cat:{pre:0. for pre in prescalelist} for cat in catlist} for mass in masslist}
    for mass in masslist:
        for cat in catlist:
            for pre in prescalelist:
                prescale = 1./pre
                scale_by = prescale * plumi[pre]
                for sample in samples:
                    mctot[mass][cat][pre] += (nraw[sample.name][mass][cat])
                mctot[mass][cat][pre] *= scale_by

    print mctot 
    for mass in masslist:
        for cat in catlist:
            for pre in prescalelist:
                print mass,cat,pre
                #r,h,l = clopper_pearson_poisson_means(hists[mass][cat][pre].GetEntries(),mctot[mass][cat][pre])
                r,l,h = clopper_pearson_poisson_means(ndata[mass][cat][pre],mctot[mass][cat][pre])
                print r,r-l,h-r,(h-r+r-l)/2.

