#include "TMath.h"

Double_t DoubleSidedCrystalBall( Double_t *x, Double_t *par) {

    Double_t norm      = par[0];
    Double_t absAlphaL = fabs((Double_t)par[1]);
    Double_t nL        = par[2];
    Double_t mean      = par[3];
    Double_t sigma     = par[4];
    Double_t absAlphaR = fabs((Double_t)par[5]);
    Double_t nR        = par[6];

    Double_t t = (x[0]-mean)/sigma;

    if(t>=-1*absAlphaL && t<=absAlphaR){
        return norm*exp(-0.5*t*t);
    }else if(t<-1*absAlphaL){
        Double_t A1 = TMath::Power(nL/absAlphaL,nL)*exp(-absAlphaL*absAlphaL/2);
        Double_t B1 = nL/absAlphaL-absAlphaL;
        return norm*A1/TMath::Power(B1-t,nL);
    }else {// if(t>absAlphaR){
        Double_t A2 = TMath::Power(nR/absAlphaR,nR)*exp(-absAlphaR*absAlphaR/2);
        Double_t B2 = nR/absAlphaR-absAlphaR;
        return norm*A2/TMath::Power(B2+t,nR);
    }
}
