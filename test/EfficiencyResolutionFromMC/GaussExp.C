#include "TMath.h"

Double_t GaussExp( Double_t *x, Double_t *par) {
    
    Double_t norm  = par[0];
    Double_t mean  = par[1];
    Double_t sigma = par[2];
    Double_t kL    = fabs((Double_t)par[3]);
    Double_t kR    = fabs((Double_t)par[4]);

    Double_t t = (x[0]-mean)/sigma;

    if (-kL < t && t <= kR) {
        return norm*exp(-0.5*t*t);
    }
    else if (t <= -kL) {
        return norm * exp(0.5*kL*kL + kL*t);
    }
    else { // (kR < t)
        return norm * exp(0.5*kR*kR - kR*t);
    }
}

