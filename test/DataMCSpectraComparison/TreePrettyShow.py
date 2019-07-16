import ROOT as R
R.gROOT.SetBatch(True)
import math
import argparse
from TreeTools import *
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',default='data/ana_datamc_Run2018ABCD.root')
parser.add_argument('-d','--dir',default='Our2018MuonsOppSignNtuple')
parser.add_argument('-e','--entry',default=0,type=int)
args = parser.parse_args()

f = R.TFile(args.file)
t = f.Get(args.dir+'/t')

t.GetEntry(args.entry)
print t.run, t.lumi, t.event

dil_mass,dil_mass_err = mass(t,track='tuneP')
trk_mass,trk_mass_err = mass(t,track='tracker')
cos3D = cos_angle(t,track='tuneP')

rc = RocCorr(t)
Am,Ap = rc.getA()
Mm,Mp = rc.getM()
Cm,Cp = rc.getCorr()
tk_corr_minus,tk_corr_plus = rc.corrMuonPt()
trk_corr_mass = rc.getMass()
trk_corr_mass_err = 0.

massPrint = '''\
{vertex_m:7.2f} {vertex_m_err:6.2f} GeV tuneP vertex constrained mass
{dil_mass:7.2f} {dil_mass_err:6.2f} GeV tuneP invariant mass
{trk_mass:7.2f} {trk_mass_err:6.2f} GeV tracker invariant mass
{trk_corr_mass:7.2f} {trk_corr_mass_err:6.2f} GeV tracker invariant mass with additive Rochester Correction
vertex fit chi2/ndof = {vtx_chi2:<5.2f}
dilepton pT = {dil_pt:<6.2f} GeV
dilepton phi = {dil_phi:<7.4f}
dilepton y = {dil_rap:<7.4f}
dilepton dR = {dil_dR:<7.4f}
dilepton dPhi = {dil_dPhi:<7.4f}
cos(3D angle) = {cos_angle:7.4f}
MET = {MET:<6.2f} GeV
phi(MET) = {MET_phi:<4.2f}
n(jets) = {njets:<2}\
'''.format(vertex_m=t.vertex_m,vertex_m_err=t.vertex_m_err,
        dil_mass=dil_mass,dil_mass_err=dil_mass_err,
        trk_mass=trk_mass,trk_mass_err=trk_mass_err,
        trk_corr_mass=trk_corr_mass,trk_corr_mass_err=trk_corr_mass_err,
        vtx_chi2=t.vertex_chi2,cos_angle=cos3D,dil_pt=t.dil_pt,
        dil_phi=t.dil_phi,dil_rap=t.dil_rap,dil_dR=t.dil_dR,dil_dPhi=t.dil_dPhi,
        MET=t.met_pt,MET_phi=t.met_phi,njets=int(t.nJets))
print massPrint
# always 4 jets listed :(
for i in range(t.nJets):
    if t.jet_pt[i]<0: continue
    print 'jet',i+1,'{jet_pt:6.2f} GeV ({jet_eta:>4.2f},{jet_phi:>4.2f})'.format(jet_pt=t.jet_pt[i],jet_eta=t.jet_eta[i],jet_phi=t.jet_phi[i])

lines = [
        ('','-','+'),
        ('eta',t.lep_eta[0],'',t.lep_eta[1],''),
        ('phi',t.lep_phi[0],'',t.lep_phi[1],''),
        ('tuneP',t.lep_pt[0],t.lep_pt_err[0],t.lep_pt[1],t.lep_pt_err[1]),
        ('picky',t.lep_picky_pt[0],t.lep_picky_pt_err[0],t.lep_picky_pt[1],t.lep_picky_pt_err[1]),
        ('dyt',t.lep_dyt_pt[0],t.lep_dyt_pt_err[0],t.lep_dyt_pt[1],t.lep_dyt_pt_err[1]),
        ('tpfms',t.lep_tpfms_pt[0],t.lep_tpfms_pt_err[0],t.lep_tpfms_pt[1],t.lep_tpfms_pt_err[1]),
        ('trk',t.lep_tk_pt[0],t.lep_tk_pt_err[0],t.lep_tk_pt[1],t.lep_tk_pt_err[1]),
        ('global',t.lep_glb_pt[0],t.lep_glb_pt_err[0],t.lep_glb_pt[1],t.lep_glb_pt_err[1]),
        ('Mu50',t.lep_Mu50_triggerMatchPt[0],'',t.lep_Mu50_triggerMatchPt[1],''),
        ('OldMu100',t.lep_OldMu100_triggerMatchPt[0],'',t.lep_OldMu100_triggerMatchPt[1],''),
        ('TkMu100',t.lep_TkMu100_triggerMatchPt[0],'',t.lep_TkMu100_triggerMatchPt[1],''),
        ('dB(PV)',t.lep_dB[0],'',t.lep_dB[1],''),
        ('rel iso',t.lep_sumPt[0]/t.lep_tk_pt[0],'',t.lep_sumPt[1]/t.lep_tk_pt[1],''),
        ('vmh(tP)',t.lep_tuneP_numberOfValidMuonHits[0],'',t.lep_tuneP_numberOfValidMuonHits[1],''),
        ('vmh(glb)',t.lep_glb_numberOfValidMuonHits[0],'',t.lep_glb_numberOfValidMuonHits[1],''),
        ('vpxh(glb)',t.lep_glb_numberOfValidPixelHits[0],'',t.lep_glb_numberOfValidPixelHits[1],''),
        ('vtl(glb)',t.lep_glb_numberOfValidTrackerLayers[0],'',t.lep_glb_numberOfValidTrackerLayers[1],''),
        ('match st',t.lep_numberOfMatchedStations[0],'',t.lep_numberOfMatchedStations[1],''),
        #('exp match st',t.lep_expectedNnumberOfMatchedStations[0],'',t.lep_expectedNnumberOfMatchedStations[1],''),
        ('match rpc',t.lep_numberOfMatchedRPCLayers[0],'',t.lep_numberOfMatchedRPCLayers[1],''),
        ('st mask',t.lep_stationMask[0],'',t.lep_stationMask[1],''),
        ('RC A',Am,'',Ap,''),
        ('RC M',Mm,'',Mp,''),
        ('RC corr',Cm,'',Cp,''),
        ('trk corr',tk_corr_minus,'',tk_corr_plus,''),
        ]
for l,line in enumerate(lines):
    if l==0: 
        print '{a:9} {b:>18} {c:>18}'.format(a=line[0],b=line[1],c=line[2])
    elif l==1 or l==2 or l==9 or l==10 or l==11 or (l>11 and 'RC' not in line[0]):
        toPrint = '{name:<9} | {col1:>16.2f} | {col2:>16.2f}'
        print toPrint.format(name=line[0],col1=float(line[1]),col2=float(line[3]))
    elif 'RC' not in line[0]:
        toPrint = '{name:<9} | {col1:>9.2f} {col2:>6.2f} | {col3:>9.2f} {col4:>6.2f}'
        print toPrint.format(name=line[0],col1=float(line[1]),col2=float(line[2]),col3=float(line[3]),col4=float(line[4]))
    elif 'RC A'==line[0]:
        toPrint = '{name:<9} | {col1:>16e} | {col2:>16e}'
        print toPrint.format(name=line[0],col1=float(line[1]),col2=float(line[3]))
    elif 'RC M'==line[0]:
        toPrint = '{name:<9} | {col1:>16.5f} | {col2:>16.5f}'
        print toPrint.format(name=line[0],col1=float(line[1]),col2=float(line[3]))
    elif 'RC corr'==line[0]:
        toPrint = '{name:<9} | {col1:>16.5f} | {col2:>16.5f}'
        print toPrint.format(name=line[0],col1=float(line[1]),col2=float(line[3]))

