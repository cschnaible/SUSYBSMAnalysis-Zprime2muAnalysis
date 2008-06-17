#ifndef GENERALUTILITIES_H
#define GENERALUTILITIES_H

#include <iosfwd>
#include <string>

#include "TLorentzVector.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"

////////////////////////////////////////////////////////////////////
// Pretty-printing.
////////////////////////////////////////////////////////////////////

std::ostream& operator<<(std::ostream& out, const TLorentzVector& vect);
std::ostream& operator<<(std::ostream& out, const reco::Candidate& par);

////////////////////////////////////////////////////////////////////
// ROOT helpers.
////////////////////////////////////////////////////////////////////

// Build a string containing a name for a histogram -- useful inside
// loops when booking histos.
std::string nameHist(const char* s, int i, int j=-1, int k=-1,
		     int l=-1, int m=-1, bool extended=false);

void InitROOT();

////////////////////////////////////////////////////////////////////
// Lepton/dilepton acceptance
////////////////////////////////////////////////////////////////////

// Lepton location codes, used by whereIs(Di)Lepton() methods.
enum WhereLepton { W_BARREL=0, W_OVERLAP, W_CRACK=W_OVERLAP,
		   W_ENDCAP, W_OUTSIDE };
// For electrons, OVERLAP here means CRACK.
enum WhereDilepton { W_BARRELBARREL=0, W_BARRELOVERLAP,  W_BARRELENDCAP,
		     W_BARRELOUTSIDE,  W_OVERLAPOVERLAP, W_OVERLAPENDCAP, 
		     W_OVERLAPOUTSIDE, W_ENDCAPENDCAP,   W_ENDCAPOUTSIDE,
		     W_OUTSIDEOUTSIDE };
  
// Helper method to return a code (one of the W_* ones above) based
// on where the lepton is in the muon system by eta; in the barrel,
// in the overlap region, in the endcap, or outside acceptance
// (nominally 2.4).
WhereLepton whereIsLepton(const reco::CandidateBaseRef& lepton,
			  const bool isElectron);

// Helper method to return a code based on where the leptons of a
// dilepton are in the lepton system (using the above whereIsLepton method
// definitions of location).
WhereDilepton whereIsDilepton(const reco::CompositeCandidate& dil,
			      const bool areElectrons);

#endif