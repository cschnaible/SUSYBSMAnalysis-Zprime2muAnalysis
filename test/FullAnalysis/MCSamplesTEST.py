import numpy,os,glob
import ROOT as R

PATH = 'mc/'

class MCSubSample(object):
    def __init__(self,name,xs,nevents):
        self.subname = name # 
        self.xs = xs # in pb^-1
        self.nevents = nevents
        self.partialWeight = float(xs)/float(nevents)
        self.path = PATH+'zp2mu_histos_'+name+'.root'

    def __str__(self):
        print self.subname
        print self.xs
        print self.nevents
        print self.partialWeight
        print self.path


class MCSample(object):
    def __init__(self,nicename,color,subSampleList):
        self.nicename = nicename
        self.color = color
        self.subSampleList = subSampleList

    def __str__(self):
        print self.nicename
        for subSample in self.subSampleList:
            print subSample

    def get_histos(self,toPlotList):
        self.histos = {toPlot:{} for toPlot in toPlotList}
        self.subhistos = {}
        for s,subSample in enumerate(self.subSampleList):
            self.subhistos[subSample.name] = {}
            f = R.TFile(subSample.path)
            self.histos[
            for toPlot in toPlotList:
                self.subhistos[subSample.name][toPlot] = f.Get(toPlot).Clone()
                self.subhistos[subSample.name][toPlot].Scale(subSample.partialWeight)
                if s==0:
                    self.histos[toPlot] = self.subhistos[subSample.name][toPlot].Clone()
                else:
                    self.histos[toPlot].Add(self.subhistos[subSample.name][toPlot])
        return self.histos


            

 
if __name__=='__main__':
    dy50to120    = MCSubSample('dy50to120',   2.112905E3,2961000)
    dy120to200   = MCSubSample('dy120to200',  2.0553E1,   100000)
    dy200to400   = MCSubSample('dy200to400',  2.8861E0,   100000)
    dy400to800   = MCSubSample('dy400to800',  2.5126E-1,  100000)
    dy800to1400  = MCSubSample('dy800to1400', 1.7075E-2,  100000)
    dy1400to2300 = MCSubSample('dy1400to2300',1.333E-3,   100000)
    dy2300to3500 = MCSubSample('dy2300to3500',8.178E-5,   100000)
    dy3500to4500 = MCSubSample('dy3500to4500',3.191E-6,   100000)
    dy4500to6000 = MCSubSample('dy4500to6000',2.787E-7,   100000)
    dy6000toInf  = MCSubSample('dy4500toInf', 9.569E-9,   100000)
    DrellYanList = [dy50to120,dy120to200,dy200to400,dy400to800,\
                    dy800to1400,dy1400to2300,dy2300to3500,\
                    dy3500to4500,dy4500to600,dy600toInf]

    DrellYan = MCSample('Drell-Yan',R.kGreen+1,DrellYanList)
    print DrellYan
