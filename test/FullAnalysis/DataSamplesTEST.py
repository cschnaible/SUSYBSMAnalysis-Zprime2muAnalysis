# Helper class for data
# General philosophy is to make a class dedicated to a year of data taking
# - Methods for accessing 
#   - ROOT file containing histos and ttree
#   - Histograms and ttree from ROOT file
#   - integrated luminosity
#   - styling options for histograms
#   - analysis category definitions used for ttree
# - Methods for creating
#   - Histos from PlotsToMake.py
#   - Event list for data to make plots
# - Method for printing general info
import numpy,os,glob
import ROOT as R

PATH = '/afs/cern.ch/work/c/cschnaib/Zprime2muAnalysis/'
PATHroot = '/eos/cms/store/user/cschnaib/ZPrime/'
SELECTION = ''


class DataSample(object):
    def __init__(self,nicename,year,era='All',version='',reco='',color=R.kBlack,style=R.kFullCircle,openROOT=True):
        self.nicename = nicename
        self.year = year
        self.era = era
        self.version = version
        self.reco = reco
        self.color = color
        self.style = style
        self.norm = {}
        self.histos = {}

        self.name = 'data_Run'+str(self.year)+'_'+str(self.era)+\
                ('_'+str(self.reco) if self.reco else '')+\
                ('_v'+str(self.version) if self.version else '')
        self.path = PATHroot+'Ana'+str(self.year)+'/data/'+\
                'zp2mu_histos_Run'+str(self.year)+'_'+str(self.era)+\
                ('_'+str(reco) if reco else '')+\
                ('_v'+str(version) if version else '')+\
                '.root'
        if openROOT:
            self.f = R.TFile(self.path)
            self.t = self.f.Get('SimpleNtupler/t')

        self.runranges = {
                2016:{
                    'A':[271036,271658],
                    'B':[272007,275376],
                    'C':[275657,276283],
                    'D':[276315,276811],
                    'E':[276831,277420],
                    'F':[277772,278808],
                    'G':[278820,280385],
                    'H':[280919,284044],
                    'All': [271036,284044],
                    },
                2017:{
                    'B':[297020,299329],
                    'C':[299337,302029],
                    'D':[302030,303434],
                    'E':[303435,304826],
                    'F':[304911,306462],
                    'All': [297020,306462],
                    },
                2018:{
                    'A':[315252,316995],
                    'B':[316998,319312],
                    #'C':[319313,],
                    'All': [315252,325175],
                    },
                }

        self.dataset = {
                2018:{
                    'A-06Jun2018-1':{
                        'dataset':'/SingleMuon/Run2018A-06Jun2018-v1/MINIAOD',
                        'runs':[315257,316505],
                        },
                    #'A-22May2018-1':{
                    #    'dataset':'/SingleMuon/Run2018A-22May2018-v1/MINIAOD',
                    #    'runs':[315267,315267],
                    #    },
                    #'A-PromptReco-1':{
                    #    'dataset':'/SingleMuon/Run2018A-PromptReco-v1/MINIAOD',
                    #    'runs':[315252,316219],
                    #    },
                    #'A-PromptReco-2':{
                    #    'dataset':'/SingleMuon/Run2018A-PromptReco-v2/MINIAOD',
                    #    'runs':[316239,316944],
                    #    },
                    'A-PromptReco-3':{
                        'dataset':'/SingleMuon/Run2018A-PromptReco-v3/MINIAOD',
                        'runs':[316569,316995],
                        },
                    'B-PromptReco-1':{
                        'dataset':'/SingleMuon/Run2018B-PromptReco-v1/MINIAOD',
                        'runs':[317080,317696],
                        },
                    'B-PromptReco-2':{
                        'dataset':'/SingleMuon/Run2018B-PromptReco-v2/MINIAOD',
                        'runs':[318070,319310],
                        },
                    'C-PromptReco-1':{
                        'dataset':'/SingleMuon/Run2018C-PromptReco-v1/MINIAOD',
                        'runs':[319337,319349],
                        },
                    'C-PromptReco-2':{
                        'dataset':'/SingleMuon/Run2018C-PromptReco-v2/MINIAOD',
                        'runs':[319449,319756],
                        },
                    'C-PromptReco-3':{
                        'dataset':'/SingleMuon/Run2018C-PromptReco-v3/MINIAOD',
                        'runs':[319833,320191],
                        },
                    'D-PromptReco-2':{
                        'dataset':'/SingleMuon/Run2018D-PromptReco-v2/MINIAOD',
                        'runs':[320500,322430],
                        },
                    },
                2017:{
                    'B-17Nov2017-1':{
                        'dataset':'/SingleMuon/Run2017B-17Nov2017-v1/MINIAOD',
                        'runs':[297047,299329],
                        },
                    'C-17Nov2017-1':{
                        'dataset':'/SingleMuon/Run2017C-17Nov2017-v1/MINIAOD',
                        'runs':[299368,302029],
                        },
                    'D-17Nov2017-1':{
                        'dataset':'/SingleMuon/Run2017D-17Nov2017-v1/MINIAOD',
                        'runs':[302031,302663],
                        },
                    'E-17Nov2017-1':{
                        'dataset':'/SingleMuon/Run2017E-17Nov2017-v1/MINIAOD',
                        'runs':[303824,304797],
                        },
                    'F-17Nov2017-1':{
                        'dataset':'/SingleMuon/Run2017F-17Nov2017-v1/MINIAOD',
                        'runs':[305040,306462],
                        },
                    'G-17Nov2017-1':{
                        'dataset':'/SingleMuon/Run2017G-17Nov2017-v1/MINIAOD',
                        'runs':[306546,306826],
                        },
                    'H-17Nov2017-1':{
                        'dataset':'/SingleMuon/Run2017H-17Nov2017-v1/MINIAOD',
                        'runs':[306896,307082],
                        },
                    'H-17Nov2017-2':{
                        'dataset':'/SingleMuon/Run2017H-17Nov2017-v2/MINIAOD',
                        'runs':[306896,307082],
                        },
                    },
                2016:{
                    'B-07Aug17_ver1':{
                        'dataset':'/SingleMuon/Run2016B-07Aug17_ver1-v1/MINIAOD',
                        'runs':[272760,273017],
                        },
                    'B-07Aug17_ver2':{
                        'dataset':'/SingleMuon/Run2016B-07Aug17_ver2-v1/MINIAOD',
                        'runs':[273150,275376],
                        },
                    'C-07Aug17-1':{
                        'dataset':'/SingleMuon/Run2016C-07Aug17-v1/MINIAOD',
                        'runs':[275656,276283],
                        },
                    'D-07Aug17-1':{
                        'dataset':'/SingleMuon/Run2016D-07Aug17-v1/MINIAOD',
                        'runs':[276315,276811],
                        },
                    'E-07Aug17-1':{
                        'dataset':'/SingleMuon/Run2016E-07Aug17-v1/MINIAOD',
                        'runs':[276831],
                        },
                    'F-07Aug17-1':{
                        'dataset':'/SingleMuon/Run2016F-07Aug17-v1/MINIAOD',
                        'runs':[277932,278808],
                        },
                    'G-07Aug17-1':{
                        'dataset':'/SingleMuon/Run2016G-07Aug17-v1/MINIAOD',
                        'runs':[278820,280385],
                        },
                    'H-07Aug17-1':{
                        'dataset':'/SingleMuon/Run2016H-07Aug17-v1/MINIAOD',
                        'runs':[281613,284044],
                        },
                    },
                }


    def get_histos(self,toPlotDir,toPlotList):
        for toPlot in toPlotList:
            try:
                self.histos[toPlot] = self.f.Get(toPlotDir+'/'+toPlot).Clone()
            except:
                raise ValueError(toPlotDir+'/'+toPlot)

    def get_lumi(self):
        lumis = open(PATH+'Ana'+str(self.year)+'/lumi/Run_'+str(self.year)+'_All_'+str(self.reco)+'.lumi')
        lumi = 0.
        for l,line in enumerate(lumis):
            if l==0: continue
            cols = line.strip('\n').split()
            if '#' in cols[0]: break
            if int(cols[0]) >= self.runranges[self.year][self.era][0] and\
               int(cols[0]) <= self.runranges[self.year][self.era][1]:
                lumi += float(cols[-1])
        return float(lumi)

    def set_norm(self,selection,nevts,mlow=0,mhigh=10000):
        self.norm['lumi'] = self.get_lumi()
        if nevts:
            self.norm['nevts']=self.get_entries(selection,mlow,mhigh)

    def get_entries(self,selection,mlow=50,mhigh=10000):
        sel = 'vertex_m >= {mlow} && vertex_m <= {mhigh}'.format(**locals())
        sel += ' && '+selection
        return float(self.t.Draw('vertex_m>>histtmp',sel,'goff'))

    def setup(self,recreate,selection,norm='lumi',mlow=0,mhigh=10000):
        if recreate: self.make_event_list_old(selection)
        nevts = True if norm=='nevts' else False
        self.set_norm(selection,nevts,mlow,mhigh)

    def get_dataset(self,run):
        cmd = 'dasgoclient -query=\"dataset run={run} dataset=/SingleMuon/Run{year}*{reco}*/MINIAOD\"'
        dataset = os.popen(cmd.format(year=self.year,run=run,reco=self.reco)).read()
        return dataset.strip('\n')

    def make_hist_from_list(self,plotdict,plot,year,category):
        toprint = ['vertex_m','run','lumi','event','sumpt','eta1','eta2','pt1','pt2']
        index = {val:i for i,val in enumerate(toprint)}
        cleaned_dils = open('lists/'+self.name+'_list.txt')
        histname = plot+('_'+category if category else '')+'_'+str(year)
        hist = R.TH1F(histname,plotdict['titles'],*plotdict['bins'])
        for line in cleaned_dils:
            dil = line.strip('\n').split()
            catsel = {
                    '':True,
                    'bb':(float(dil[index['eta1']]) <= 1.2 and float(dil[index['eta2']]) <= 1.2 \
                            and float(dil[index['eta1']]) >= -1.2 and float(dil[index['eta2']]) >= -1.2),
                    'be':(float(dil[index['eta1']]) > 1.2 or float(dil[index['eta2']]) > 1.2 \
                            or float(dil[index['eta1']]) < -1.2 or float(dil[index['eta2']]) < -1.2),
                    'ee':((float(dil[index['eta1']]) > 1.2 or float(dil[index['eta1']]) < -1.2) and\
                            (float(dil[index['eta2']]) > 1.2 or float(dil[index['eta2']]) < -1.2)),
                    }
            if catsel[category]:
                hist.Fill(float(dil[index[plotdict['var']]]))
        return hist

    def make_hist_test(self,plotdict,plot,selection,year,category,name=''):
        histname = plot+('_'+category if category else '')+'_'+str(year)+('_'+name if name else '')
        var = plotdict['var']
        hist = R.TH1F(histname,plotdict['titles'],*plotdict['bins'])
        todraw = '{var}>>{histname}'.format(var=var,histname=histname)
        print todraw
        self.t.Draw(todraw,selection)
        return hist
    def make_event_list(self,selection,extra):
        self.t.GetPlayer().SetScanRedirect(True)
        list_name = self.name+('_'+extra if extra!='' else '')+'_tmp.txt'
        self.t.GetPlayer().SetScanFileName('lists/'+list_name)
        #- colsize=10 is needed in order not to currupt the event number
        branch_spec = 'vertex_m:run:lumi:event:(lep_pt[0]+lep_pt[1]):lep_eta[0]:lep_eta[1]'
        toprint = ['vertex_m','run','lumi','event','sumpt','eta1','eta2']
        self.t.Scan(branch_spec, selection, "colsize=10 precision=10")
        self.t.GetPlayer().SetScanRedirect(False)
        dils = [line.split(' *')[1:] for line in open('lists/'+list_name).readlines() if ' * ' in line and 'Row' not in line]
        nice_dils = []
        for dil in dils:
            newline = '{mass}\t{run}\t{lumi}\t{event}\t{sumpt}\t{eta1}\t{eta2}'
            mass = float(dil[0].strip())
            run = int(dil[1].strip())
            lumi = int(dil[2].strip())
            event = int(dil[3].strip())
            sumpt = float(dil[4].strip())
            eta1 = float(dil[5].strip())
            eta2 = float(dil[6].strip())
            nice_dils.append(newline.format(**locals()))
        dataListName= 'lists/'+self.name+('_'+extra if extra!='' else '')+'.txt'
        open(dataListName, 'wt').write('\n'.join(nice_dils))
            


    def make_event_list_old(self,selection):
        self.t.GetPlayer().SetScanRedirect(True)
        full_list_name = self.name+'_full.txt'
        self.t.GetPlayer().SetScanFileName('lists/'+full_list_name)
        #- colsize=10 is needed in order not to currupt the event number
        branch_spec = 'vertex_m:run:lumi:event:(lep_pt[0]+lep_pt[1]):lep_eta[0]:lep_eta[1]'#:lep_pt[0]:lep_pt[1]'
        toprint = ['vertex_m','run','lumi','event','sumpt','eta1','eta2']#,'pt1','pt2']
        self.t.Scan(branch_spec, selection, "colsize=10 precision=10")
        self.t.GetPlayer().SetScanRedirect(False)
        dils = [line.split(' *')[1:] for line in open('lists/'+full_list_name).readlines() if ' * ' in line and 'Row' not in line]
        #- This loop is to keep only the first (highest-rank) dimuon in an event
        cleaned_dils = []
        passed,passed_mass = 0,0
        # 'this' is the set of info for the current _dimuon_
        this = {} 
        # 'the' is the best dimuon for the _event_
        the = {}
        # 'prev' is the set of info for the previous _dimuon_
        prev = {}
        for dil in dils:
            cleaned_dil = []
            # set 'this' info from current dimuon
            this['vertex_m'] = float(dil[0].strip())
            this['run'] = int(dil[1].strip())
            this['lumi'] = int(dil[2].strip())
            this['event'] = int(dil[3].strip())
            this['sumpt'] = float(dil[4].strip())
            this['eta1'] = float(dil[5].strip())
            this['eta2'] = float(dil[6].strip())
            #this['pt1'] = float(dil[7].strip())
            #this['pt2'] = float(dil[8].strip())

            if len(prev.keys())==0:
                # First dimuon
                prev = this.copy()
                the = this.copy()
            elif this['run']!=prev['run'] or this['lumi']!=prev['lumi'] or this['event']!=prev['event']:
                # 'this' is a dimuon from a new event
                # Save 'the' best dimuon from previous event
                passed += 1
                for a in toprint:
                    cleaned_dil.append(the[a])
                cleaned_dils.append(cleaned_dil)
                # reset 'this' dimuon as 'the' best dimuon since 'this' is from a new event
                the = this.copy()
            else:
                # 'this' dimon is from same event as previous dimuon
                # check to see if it is better
                if this['sumpt']>the['sumpt']:
                    # 'this' dimuon is better than the current best choice
                    the = this.copy()
            # set 'prev' as 'this' for the next entry
            prev = this.copy()
        else:
            # Don't forget to save 'the' best from the last event!
            # Putting this in an else block is technically unnecessary 
            # since this code will always run when the for loop finishes
            # I put it in a for-else just for clarity sake that it is a 
            # part of the loop to find selected dimuons
            passed += 1
            for a in toprint:
                cleaned_dil.append(the[a])
            cleaned_dils.append(cleaned_dil)
        cleaned_dils_txt = ['\t'.join(str(y) for y in x) for x in cleaned_dils]
        dataListName = 'lists/'+self.name+'_list.txt'
        open(dataListName, 'wt').write('\n'.join(cleaned_dils_txt))


    def __str__(self):
        toPrint = 'Run{self.year}{self.era} {self.reco} {self.version}'
        toPrint += '\nLuminosity = {:6.3f} fb^-1'.format(self.get_lumi())
        toPrint += '\n{self.path}'
        return toPrint.format(**locals())

if __name__=='__main__':
    from Selection import Selection, SelectionFull, Categories
    import argparse
    parser = argparse.ArgumentParser(description='Options for using DataSamples class directly')
    parser.add_argument('-data',action='append',type=str,help='Which year of data to plot')
    parser.add_argument('-sel','--selection',default='2016',help='Which set of selections for dimuons to draw')
    parser.add_argument('-cats','--categories',action='append',help='Which analysis categories to draw')
    parser.add_argument('-t','--test',action='store_true',help='Only do the testing module')
    parser.add_argument('-ml','--make_list',action='store_true',help='Make event lists, requires selection and year options also')
    args = parser.parse_args()

    if args.test:
        print 'Testing'
        Data2016 = DataSample('Data 2016',2016,reco='07Aug2017')
        print Data2016
        Data2017 = DataSample('Data 2017',2017,reco='17Nov2017')
        print Data2017
        Data2018 = DataSample('Data 2018',2018,reco='PromptReco')
        print Data2018
        exit()

    datalist = [int(year) for year in args.data]
    print datalist
    if not args.categories:
        categorylist = ['','bb','be','ee']
    else:
        categorylist = [cat for cat in args.categories]
    print categorylist

    bestReco = {
            2016:'07Aug2017',
            2017:'17Nov2017',
            2018:'PromptReco',
            }
    data = {year:DataSample('Data '+str(year),year,reco=bestReco[year]) for year in datalist}


    if args.make_list:
        for year in data:
            sel = SelectionFull[year]+' && vertex_m > 50'# && run==3166826 && lumi==826 && event==1174619365'
            data[year].make_event_list(sel,'test')

