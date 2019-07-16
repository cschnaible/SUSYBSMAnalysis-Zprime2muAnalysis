#include "GeneralizedEndpoint.h"
#include <iostream>
#include "TRandom.h"
#include <math.h>
using std::cout;
using std::cerr;
using std::endl;

GeneralizedEndpoint::GeneralizedEndpoint(int GEyear){
    if (GEyear==2016){
        /*
        // https://indico.cern.ch/event/693825/sessions/262876/attachments/1582867/2501533/GE_Method_muonScale_15Jan2018.pdf
      //Corrections from 2D matrix in MuonPOG presentation in c/TeV.
      //[-2.4, -2.1]
      _Correction[0][0] = -0.388122; _CorrectionError[0][0] = 0.045881; //-180,-60
      _Correction[0][1] =  0.376061; _CorrectionError[0][1] = 0.090062; //-60,60
      _Correction[0][2] =  -0.153950; _CorrectionError[0][2] = 0.063053; //60,180
      //[-2.1, -1.2]                                                                                           
      _Correction[1][0] =  -0.039346; _CorrectionError[1][0] = 0.031655;
      _Correction[1][1] =  0.041069;  _CorrectionError[1][1] = 0.030070;
      _Correction[1][2] =  -0.113320; _CorrectionError[1][2] = 0.028683;
      //[-1.2, 0.]
      _Correction[2][0] =  0.0;      _CorrectionError[2][0] = 0.03;
      _Correction[2][1] =  0.0;      _CorrectionError[2][1] = 0.03;
      _Correction[2][2] =  0.0;      _CorrectionError[2][2] = 0.03;
      //[-0., 1.2]
      _Correction[3][0] =  0.0;      _CorrectionError[3][0] = 0.03;
      _Correction[3][1] =  0.0;      _CorrectionError[3][1] = 0.03;
      _Correction[3][2] =  0.0;      _CorrectionError[3][2] = 0.03;
      //[1.2, 2.1]
      _Correction[4][0] =  0.005114; _CorrectionError[4][0] = 0.033115;
      _Correction[4][1] =  0.035573; _CorrectionError[4][1] = 0.038574;
      _Correction[4][2] =  0.070002; _CorrectionError[4][2] = 0.035002;
      //[2.1, 2.4]
      _Correction[5][0] =  -0.235470; _CorrectionError[5][0] = 0.077534;
      _Correction[5][1] =  -0.122719; _CorrectionError[5][1] = 0.061283;
      _Correction[5][2] =  0.091502;  _CorrectionError[5][2] = 0.074502;
      */
      //Corrections from 2D matrix in c/TeV from AN-18-008.
      //[-2.4, -2.1]
      _Correction[0][0] = -0.032;  _CorrectionError[0][0] = 0.11; //-180,-60
      _Correction[0][1] =  0.11;   _CorrectionError[0][1] = 0.064; //-60,60
      _Correction[0][2] =  -0.10;  _CorrectionError[0][2] = 0.082; //60,180
      //[-2.1, -1.2]                                                                                           
      _Correction[1][0] =   0.04;  _CorrectionError[1][0] = 0.059;
      _Correction[1][1] =  -0.051; _CorrectionError[1][1] = 0.043;
      _Correction[1][2] =  -0.068; _CorrectionError[1][2] = 0.10;
      //[-1.2, 0.]
      _Correction[2][0] =  -0.017; _CorrectionError[2][0] = 0.032;
      _Correction[2][1] =  0.081;  _CorrectionError[2][1] = 0.045;
      _Correction[2][2] =  0.029;  _CorrectionError[2][2] = 0.05;
      //[-0., 1.2]
      _Correction[3][0] =  0.014;  _CorrectionError[3][0] = 0.054;
      _Correction[3][1] =  0.09;   _CorrectionError[3][1] = 0.048;
      _Correction[3][2] =  -0.085; _CorrectionError[3][2] = 0.049;
      //[1.2, 2.1]
      _Correction[4][0] =  -0.1;   _CorrectionError[4][0] = 0.046;
      _Correction[4][1] =  0.012;  _CorrectionError[4][1] = 0.061;
      _Correction[4][2] =  0.0066; _CorrectionError[4][2] = 0.029;
      //[2.1, 2.4]
      _Correction[5][0] =  0.14;   _CorrectionError[5][0] = 0.17;
      _Correction[5][1] =  0.084;  _CorrectionError[5][1] = 0.08;
      _Correction[5][2] =  0.11;   _CorrectionError[5][2] = 0.058;
    }
    else if (GEyear==2017) {
      //Corrections from 2D matrix in c/TeV from AN-18-008.
      //[-2.4, -2.1]
      _Correction[0][0] =   0.05;   _CorrectionError[0][0] = 0.042; //-180,-60
      _Correction[0][1] =  -0.15;   _CorrectionError[0][1] = 0.06; //-60,60
      _Correction[0][2] =  -0.0046; _CorrectionError[0][2] = 0.013; //60,180
      //[-2.1, -1.2]                                                                                          
      _Correction[1][0] =  -0.012;  _CorrectionError[1][0] = 0.07;
      _Correction[1][1] =   0.061;  _CorrectionError[1][1] = 0.073;
      _Correction[1][2] =  -0.032;  _CorrectionError[1][2] = 0.052;
      //[-1.2, 0.]
      _Correction[2][0] =   0.029;  _CorrectionError[2][0] = 0.045;
      _Correction[2][1] =  -0.032;  _CorrectionError[2][1] = 0.05;
      _Correction[2][2] =  -0.035;  _CorrectionError[2][2] = 0.04;
      //[-0., 1.2]
      _Correction[3][0] =  -0.058;  _CorrectionError[3][0] = 0.08;
      _Correction[3][1] =  -0.017;  _CorrectionError[3][1] = 0.037;
      _Correction[3][2] =   0.011;  _CorrectionError[3][2] = 0.049;
      //[1.2, 2.1]
      _Correction[4][0] =  -0.078;  _CorrectionError[4][0] = 0.051;
      _Correction[4][1] =  -0.03;   _CorrectionError[4][1] = 0.065;
      _Correction[4][2] =  -0.12;   _CorrectionError[4][2] = 0.046;
      //[2.1, 2.4]
      _Correction[5][0] =  -0.12;   _CorrectionError[5][0] = 0.029;
      _Correction[5][1] =  -0.47;   _CorrectionError[5][1] = 0.12;
      _Correction[5][2] =  -0.029;  _CorrectionError[5][2] = 0.037;
    }
    else if (GEyear==2018) {
      //Corrections from 2D matrix in MuonPOG presentation in c/TeV.
      // https://indico.cern.ch/event/823654/contributions/3445416/attachments/1851389/3039433/highpT_27May.pdf
      //[-2.4, -2.1] // pt > 110 GeV 
      _Correction[0][0] = -0.065; _CorrectionError[0][0] = 0.04; //-180,-60
      _Correction[0][1] =  0.0076; _CorrectionError[0][1] = 0.042; //-60,60
      _Correction[0][2] =  0.04; _CorrectionError[0][2] = 0.036; //60,180
      //[-2.1, -1.2]                                                                                           
      _Correction[1][0] =  0.028; _CorrectionError[1][0] = 0.027;
      _Correction[1][1] =  0.012; _CorrectionError[1][1] = 0.031;
      _Correction[1][2] =  0.021; _CorrectionError[1][2] = 0.034;
      //[-1.2, 0.]
      _Correction[2][0] = -0.036;  _CorrectionError[2][0] = 0.022;
      _Correction[2][1] =  0.0055; _CorrectionError[2][1] = 0.022;
      _Correction[2][2] = -0.033;  _CorrectionError[2][2] = 0.021;
      //[-0., 1.2]
      _Correction[3][0] =  0.037;  _CorrectionError[3][0] = 0.02;
      _Correction[3][1] =  0.042;  _CorrectionError[3][1] = 0.023;
      _Correction[3][2] =  0.0052;  _CorrectionError[3][2] = 0.021;
      //[1.2, 2.1]
      _Correction[4][0] =  0.018;  _CorrectionError[4][0] = 0.029;
      _Correction[4][1] = -0.0066; _CorrectionError[4][1] = 0.034;
      _Correction[4][2] = -0.022;  _CorrectionError[4][2] = 0.027;
      //[2.1, 2.4] // pt > 110 GeV
      _Correction[5][0] =  0.027;   _CorrectionError[5][0] = 0.044;
      _Correction[5][1] = -0.13;   _CorrectionError[5][1] = 0.038;
      _Correction[5][2] = -0.075;  _CorrectionError[5][2] = 0.05;
    }


};

GeneralizedEndpoint::~GeneralizedEndpoint()
{
};

float GeneralizedEndpoint::GeneralizedEndpointPt(float MuonPt, int MuonCharge, float MuonEta, float MuonPhi, int Mode, int verbose){

  //Check the input format.
  if (fabs(MuonEta)>2.4) {
    cerr<<"ERROR: MuonEta = "<< MuonEta << ", outisde valide range = [-2.4,2.4] "<<endl;
    return 0;
  }
  if (fabs(MuonPhi)>180) {
    cerr<<"ERROR: MuonPhi = "<< MuonPhi << ", outisde valide range = [-180,180] "<<endl;
    return 0;
  }
  if (MuonCharge != 1 && MuonCharge != -1) {
    cerr<<"ERROR: Invalide Muon Charge = "<< MuonCharge << endl;
    return 0;
  }
  if (Mode != 0 && Mode != 1 && Mode != 2 && Mode != -1 && Mode != -2 && Mode != -3) {
    cerr<<"ERROR: Invalide Mode = "<< Mode << endl;
    cerr<<"\t: Valid modes: 0 = Nominal, 1 = SystematicUp and 2 = SystematicDown "<< endl;
    cerr<<"\t: Experimental mode: -1 = Nominal for Data, -2 = SystematicUp and -3 = SystematicDown "<< endl;
    return 0;
  }

  // Eta Binning
  unsigned int etaBINS = 6;
  unsigned int kEtaBin = etaBINS;
  double EtaBin[etaBINS+1];
  EtaBin[0]=-2.4; EtaBin[1]=-2.1; EtaBin[2]=-1.2; EtaBin[3]=0.;
  EtaBin[4]=1.2; EtaBin[5]=2.1; EtaBin[6]=2.4;  

  // Phi Binning.
  unsigned int phiBINS =3;
  unsigned int kPhiBin = phiBINS;
  double PhiBin[phiBINS+1];
  PhiBin[0]=-180.; PhiBin[1]=-60.; PhiBin[2]=60.; PhiBin[3]=180.;
  

  for (unsigned int kbin=0; kbin<=etaBINS; ++kbin) {
    if (MuonEta<EtaBin[kbin+1]) {
      kEtaBin = kbin;
      break;
    }
  }

  for (unsigned int kbin=0; kbin<=phiBINS; ++kbin) {
    if (MuonPhi<PhiBin[kbin+1]) {
      kPhiBin = kbin;
      break;
    }
  }

  float KappaBias=_Correction[kEtaBin][kPhiBin];
  float KappaBiasError=_CorrectionError[kEtaBin][kPhiBin];
  
  float rnd = KappaBias+99*KappaBiasError;
  while (abs(KappaBias-rnd) > KappaBiasError)
    rnd = gRandom->Gaus(KappaBias,KappaBiasError);

  KappaBias = rnd;
  // if ((KappaBias-KappaBiasError)/KappaBias > 0.70) return MuonPt;
  //  if (abs(KappaBiasError/KappaBias) > 0.70) return MuonPt; // ignore the bias if the error on the estimation is too big... 
  

  if (Mode==1) KappaBias = KappaBias+KappaBiasError; //Take bias + UpSystematic.
  if (Mode==2) KappaBias = KappaBias-KappaBiasError; //Takes bias - DownSystematic.

  /// Experimental ///
  if (Mode==-1) KappaBias = -1*KappaBias; //Reverse the sign to use it with data as first approximation. (this option has some non-trivial assumptions).
  if (Mode==-2) KappaBias = -1*(KappaBias+KappaBiasError); //Reverse the sign to use it with data as first approximation. (this option has some non-trivial assumptions).
  if (Mode==-3) KappaBias = -1*(KappaBias-KappaBiasError); //Reverse the sign to use it with data as first approximation. (this option has some non-trivial assumptions).
  //////

  if (verbose ==1) printf("eta bin %i, phi bin %i Correction %f +- %f pt %f\n", kEtaBin, kPhiBin, _Correction[kEtaBin][kPhiBin], KappaBiasError,MuonPt);

  MuonPt = MuonPt/1000.; //GeV to TeV.
  MuonPt = MuonCharge*fabs(MuonPt); //Signed Pt.
  MuonPt = 1/MuonPt; //Convert to Curvature.
  MuonPt = MuonPt + KappaBias; //Apply the bias.
  if (fabs(MuonPt) < 0.14 && verbose ==1)  printf("WARNING: Very small curvature after correction!(is this expected?) eta = %.2f, phi = %.2f \n", MuonEta, MuonPhi);
  if (fabs(MuonPt) < 0.14) MuonPt = KappaBiasError; //To avoid a division by set the curvature to its error if after the correction the pt is larger than 7 TeV.
  MuonPt = 1/MuonPt;//Return to Pt.
  MuonPt = fabs(MuonPt);//returns unsigned Pt, any possible sign flip due to the curvature is absorbed here.
  MuonPt = MuonPt*1000.;//Return to Pt in GeV.

  if (verbose ==1) printf("NEW pt %f\n", MuonPt);

  return MuonPt;
};
