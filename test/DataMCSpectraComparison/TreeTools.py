import math
which = {
        'tuneP':'_',
        'picky':'_picky_',
        'dyt':'_dyt_',
        'tpfms':'_tpfms_',
        'tracker':'_tk_',
        'global':'_glb_',
        }
def cos_angle(t,track='tuneP',track0=None,track1=None):
    if track0 is None or track1 is None:
        track0=track
        track1=track
    phi0 = getattr(t,'lep'+which[track0]+'phi')[0]
    phi1 = getattr(t,'lep'+which[track1]+'phi')[1]
    eta0 = getattr(t,'lep'+which[track0]+'eta')[0]
    eta1 = getattr(t,'lep'+which[track1]+'eta')[1]
    return (math.cos(phi0)*math.cos(phi1) + math.sin(phi0)*math.sin(phi1) + math.sinh(eta0)*math.sinh(eta1))/math.cosh(eta0)/math.cosh(eta1)

def mass(t,track='tuneP',track0=None,track1=None):
    if track0 is None or track1 is None:
        track0=track
        track1=track
    pt0 = getattr(t,'lep'+which[track0]+'pt')[0]
    pt1 = getattr(t,'lep'+which[track1]+'pt')[1]
    pterr0 = getattr(t,'lep'+which[track0]+'pt_err')[0]
    pterr1 = getattr(t,'lep'+which[track1]+'pt_err')[1]
    phi0 = getattr(t,'lep'+which[track0]+'phi')[0]
    phi1 = getattr(t,'lep'+which[track1]+'phi')[1]
    eta0 = getattr(t,'lep'+which[track0]+'eta')[0]
    eta1 = getattr(t,'lep'+which[track1]+'eta')[1]
    cos = cos_angle(t,track=track,track0=track0,track1=track1)
    C = 2*math.cosh(eta0)*math.cosh(eta1)*(1-cos)
    m2 = C*pt0*pt1
    m2err = 0.25*C*( (pt1/pt0)*pow(pterr0,2)+(pt0/pt1)*pow(pterr1,2) )
    return math.sqrt(m2),math.sqrt(m2err)

class RocCorr():
    def __init__(self,t):
        self.t = t
        self.pt_minus  = self.t.lep_tk_pt[0]
        self.pt_plus   = self.t.lep_tk_pt[1]
        self.eta_minus = self.t.lep_tk_eta[0]
        self.eta_plus  = self.t.lep_tk_eta[1]
        self.phi_minus = self.t.lep_tk_phi[0]
        self.phi_plus  = self.t.lep_tk_phi[1]
        self.etabins = [-2.40,-2.10,-1.85,-1.60,-1.20,-0.80,-0.40,0.00,0.40,0.80,1.20,1.60,1.85,2.10,2.40]
        self.etabin_plus = self.getEtaBin(self.eta_plus)
        self.phibin_plus = self.getPhiBin(self.phi_plus)
        self.etabin_minus = self.getEtaBin(self.eta_minus)
        self.phibin_minus = self.getPhiBin(self.phi_minus)
        self.A = {e:{p:{} for p in range(16-1)} for e in range(len(self.etabins))}
        self.M = {e:{p:{} for p in range(16-1)} for e in range(len(self.etabins))}
        corrFile = open('corrections.txt')
        for line in corrFile:
            cols = line.strip('\n').split()
            etabin = int(cols[0])
            phibin = int(cols[1])
            A = float(cols[2])
            M = float(cols[3])
            self.A[etabin][phibin] = A
            self.M[etabin][phibin] = M

    def getEtaBin(self,eta):
        for e,ebin in enumerate(self.etabins):
            if eta < self.etabins[e+1]: return e
        return len(self.etabins)-1

    def getPhiBin(self,phi):
        pi = 3.14159
        mphi = -1*pi
        dphi = 2*pi/16.
        pbin = int((phi-mphi)/dphi)
        if pbin<0: return 0
        if pbin>=16: 15
        return pbin

    def getM(self):
        return self.M[self.etabin_minus][self.phibin_minus],self.M[self.etabin_plus][self.phibin_plus]

    def getA(self):
        return self.A[self.etabin_minus][self.phibin_minus],self.A[self.etabin_plus][self.phibin_plus]

    def getCorr(self):
        Am, Ap = self.getA()
        Mm, Mp = self.getM()
        return pow(Mm - Am*self.pt_minus,-1),pow(Mp + Ap*self.pt_plus,-1)

    def corrMuonPt(self):
        Cm, Cp = self.getCorr()
        return self.pt_minus*Cm,self.pt_plus*Cp
        #Km = -1.0/self.pt_minus + Am
        #Kp = 1.0/self.pt_plus + Ap
        #return abs(1.0/Km),abs(1.0/Kp)

    def getMass(self):
        corr_minus,corr_plus = self.corrMuonPt()
        cos = (math.cos(self.phi_minus)*math.cos(self.phi_plus) + math.sin(self.phi_minus)*math.sin(self.phi_plus) + math.sinh(self.eta_minus)*math.sinh(self.eta_plus))/math.cosh(self.eta_minus)/math.cosh(self.eta_plus)
        m2 = 2*math.cosh(self.eta_minus)*math.cosh(self.eta_plus)*corr_minus*corr_plus*(1-cos)
        return math.sqrt(m2)
