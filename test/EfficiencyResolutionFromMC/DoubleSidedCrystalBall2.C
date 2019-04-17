Double_t DoubleSidedCrystalBall2( Double_t *x, Double_t *par) {
    // double sided crystal ball

    double norm = par[0];
    double alphaL = par[1];
    //double nL = par[2];
    int nL = par[2];
    double mean = par[3];
    double sigma = par[4];
    double alphaR = par[5];
    //double nR = par[6];
    int nR = par[6];

    if (x[0] < alphaL) {
        return norm * pow(nL/alphaL,nL) * exp(-0.5*pow(alphaL,2)) / pow(nL/alphaL - alphaL - x[0],nL);
    }
    else if (-1*alphaL <= x[0] && x[0] <= alphaR) {
        return norm * exp(-0.5*pow(x[0]-mean,2)/pow(sigma,2));
    }
    else if (alphaR < x[0]) {
        return norm * pow(nR/alphaR,nR) * exp(-0.5*pow(alphaR,2)) / pow(nR/alphaR - alphaR - x[0],nR);
    }
    else {
        return 99;
    }
}
