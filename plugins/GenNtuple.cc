#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "TTree.h"
#include "TMath.h"


class GenNtuple : public edm::EDAnalyzer {
 public:
  explicit GenNtuple(const edm::ParameterSet&);

 private:
 virtual bool analyze(edm::Event&, const edm::EventSetup&);

  edm::InputTag src;

  double eventWeight;
  bool useMadgraphWeight;
  double madgraphWeight;

  TTree* tree;

  TH2F* Weight_Zmass;
  TH2F* Zpt_Zmass;
  TH2F* Zeta_Zmass;
  TH2F* Zy_Zmass;
  TH2F* Zphi_Zmass;
  TH2F* pt_Zmass;
  TH2F* eta_Zmass;
  TH2F* phi_Zmass;

  TH2F* Weight_Zmass_;
  TH2F* Zpt_Zmass_;
  TH2F* Zeta_Zmass_;
  TH2F* Zy_Zmass_;
  TH2F* Zphi_Zmass_;
  TH2F* pt_Zmass_;
  TH2F* eta_Zmass_;
  TH2F* phi_Zmass_;
  struct tree_t {
      // stuff
      unsigned run,lumi,event;
      float genWeight;
      // ib
      float gen_dil_mass;
      float gen_dil_rap;
      float gen_dil_eta;
      float gen_dil_pt;
      float gen_dil_pz;
      float gen_dil_phi;
      float gen_lep_p[2];
      float gen_lep_pt[2];
      float gen_lep_pz[2];
      float gen_lep_E[2];
      float gen_lep_eta[2];
      float gen_lep_phi[2];
      // noib
      float gen_res_mass;
      float gen_res_rap;
      float gen_res_eta;
      float gen_res_pt;
      float gen_res_pz;
      float gen_res_phi;
      float gen_lep_noib_p[2];
      float gen_lep_noib_pt[2];
      float gen_lep_noib_pz[2];
      float gen_lep_noib_E[2];
      float gen_lep_noib_eta[2];
      float gen_lep_noib_phi[2];
  };


};


GenNtuple::GenNtuple(const edm::ParameterSet& cfg)
  : src(cfg.getParameter<edm::InputTag>("src")),
    eventWeight(1.0),
    useMadgraphWeight(cfg.getParameter<bool>("useMadgraphWeight")),
    madgraphWeight(1.0)
{
  consumes<reco::GenParticleCollection>(src);
  mayConsume<GenEventInfoProduct>(edm::InputTag("generator"));

  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t","");
  // stuff
  tree->Branch("run",&t.run,"run/i");
  tree->Branch("lumi",&t.lumi,"lumi/i");
  tree->Branch("event",&t.event,"event/i");
  tree->Branch("genWeight",&t.genWeight,"genWeight/F");
  // ib
  tree->Branch("gen_dil_mass",&t.gen_dil_mass,"gen_dil_mass/F");
  tree->Branch("gen_dil_pt",&t.gen_dil_pt,"gen_dil_pt/F");
  tree->Branch("gen_dil_pz",&t.gen_dil_pz,"gen_dil_pz/F");
  tree->Branch("gen_dil_rap",&t.gen_dil_rap,"gen_dil_rap/F");
  tree->Branch("gen_dil_eta",&t.gen_dil_eta,"gen_dil_eta/F");
  tree->Branch("gen_dil_phi",&t.gen_dil_phi,"gen_dil_phi/F");
  tree->Branch("gen_lep_p",t.gen_lep_p,"gen_lep_p[2]/F");
  tree->Branch("gen_lep_pt",t.gen_lep_pt,"gen_lep_pt[2]/F");
  tree->Branch("gen_lep_pz",t.gen_lep_pz,"gen_lep_pz[2]/F");
  tree->Branch("gen_lep_eta",t.gen_lep_eta,"gen_lep_eta[2]/F");
  tree->Branch("gen_lep_E",t.gen_lep_E,"gen_lep_E[2]/F");
  tree->Branch("gen_lep_phi",t.gen_lep_phi,"gen_lep_phi[2]/F");
  // noib
  tree->Branch("gen_res_mass",&t.gen_res_mass,"gen_res_mass/F");
  tree->Branch("gen_res_pt",&t.gen_res_pt,"gen_res_pt/F");
  tree->Branch("gen_res_pz",&t.gen_res_pz,"gen_res_pz/F");
  tree->Branch("gen_res_rap",&t.gen_res_rap,"gen_res_rap/F");
  tree->Branch("gen_res_eta",&t.gen_res_eta,"gen_res_eta/F");
  tree->Branch("gen_res_phi",&t.gen_res_phi,"gen_res_phi/F");
  tree->Branch("gen_lep_noib_p",t.gen_lep_noib_p,"gen_lep_noib_p[2]/F");
  tree->Branch("gen_lep_noib_pt",t.gen_lep_noib_pt,"gen_lep_noib_pt[2]/F");
  tree->Branch("gen_lep_noib_pz",t.gen_lep_noib_pz,"gen_lep_noib_pz[2]/F");
  tree->Branch("gen_lep_noib_eta",t.gen_lep_noib_eta,"gen_lep_noib_eta[2]/F");
  tree->Branch("gen_lep_noib_E",t.gen_lep_noib_E,"gen_lep_noib_E[2]/F");
  tree->Branch("gen_lep_noib_phi",t.gen_lep_noib_phi,"gen_lep_noib_phi[2]/F");

}

bool GenNtuple::analyze(edm::Event& event, const edm::EventSetup&) {

  eventWeight = 1.0;
  madgraphWeight = 1.0;

  if (useMadgraphWeight) {
    edm::Handle<GenEventInfoProduct> gen_ev_info;
    event.getByLabel(edm::InputTag("generator"), gen_ev_info);
    if (gen_ev_info.isValid() ){
      eventWeight = gen_ev_info->weight();
      madgraphWeight = ( eventWeight > 0.0 ) ? 1.0 : -1.0;
    }
  }
  else {
    eventWeight = 1.0;
    madgraphWeight = 1.0;
  }

  edm::Handle<reco::GenParticleCollection> genParticles;
  event.getByLabel(src, genParticles);

  reco::GenParticleCollection::const_iterator genp = genParticles->begin();

  bool isFind1 = false;
  bool isFind2 = false;

  const reco::Candidate *mu1 = 0;
  const reco::Candidate *mu2 = 0;
  reco::Particle::LorentzVector Z;


  bool isFind1_ = false;
  bool isFind2_ = false;

  const reco::Candidate *mu1_ = 0;
  const reco::Candidate *mu2_ = 0;
  reco::Particle::LorentzVector Z_;


  for (; genp != genParticles->end(); genp++) {

    if( (genp->pdgId() == 13) && (genp->isHardProcess()) ){
      isFind1 = true;
      mu1 = &*genp;
    }

    if( (genp->pdgId() == -13) && (genp->isHardProcess()) ){
      isFind2 = true;
      mu2 = &*genp;
    }

    if( (genp->pdgId() == 13) && (genp->status() == 1) ){

      const reco::Candidate* m = genp->mother();
      bool ok = false;
      while (m) {
        if( m->pdgId() == 32 || m->pdgId() == 23 || m->pdgId() == 39 || m->pdgId() == 5000039 ) {
          ok = true;
          break;
        }
        m = m->mother();
      }

      if(ok) {
        isFind1_ = true;
        mu1_ = &*genp;
      }
    }

    if( (genp->pdgId() == -13) && (genp->status() == 1) ){

      const reco::Candidate* m = genp->mother();
      bool ok = false;
      while (m) {
        if( m->pdgId() == 32 || m->pdgId() == 23 || m->pdgId() == 39 || m->pdgId() == 5000039 ) {
          ok = true;
          break;
        }
        m = m->mother();
      }

      if(ok) {
        isFind2_ = true;
        mu2_ = &*genp;
      }
    }

  }


  if( isFind1 && isFind2 && isFind1_ && isFind2_ ){

    Z  = mu1->p4() + mu2->p4();
    Z_ = mu1_->p4() + mu2_->p4();

    // if(Z_.mass() < 200) {
    //   std::cout << std::endl;
    //   std::cout << "M: " << Z.mass() << std::endl;
    //   std::cout << "\t M: " << Z_.mass() << std::endl;
    //   std::cout << "p+: " << mu1->p4() << std::endl;
    //   std::cout << "\t p+: " << mu1_->p4() << std::endl;
    //   std::cout << "p-: " << mu2->p4() << std::endl;
    //   std::cout << "\t p-: " << mu2_->p4() << std::endl;
    //   std::cout << "p4: " << (mu1->p4()+mu2->p4()) << std::endl;
    //   std::cout << "\t p4: " << (mu1_->p4()+mu2_->p4()) << std::endl;
    // }
    //

    t.gen_res_mass = 

    float l_pt   = mu1_->pt() > mu2_->pt() ? mu1->pt()  : mu2->pt();
    float l_eta  = mu1_->pt() > mu2_->pt() ? mu1->eta() : mu2->eta();
    float l_phi  = mu1_->pt() > mu2_->pt() ? mu1->phi() : mu2->phi();

    float l_pt_   = mu1_->pt() > mu2_->pt() ? mu1_->pt()  : mu2_->pt();
    float l_eta_  = mu1_->pt() > mu2_->pt() ? mu1_->eta() : mu2_->eta();
    float l_phi_  = mu1_->pt() > mu2_->pt() ? mu1_->phi() : mu2_->phi();

    Weight_Zmass->Fill( Z.mass(), madgraphWeight );
    Zpt_Zmass->Fill(    Z.mass(), Z.pt(),  madgraphWeight );
    Zeta_Zmass->Fill(   Z.mass(), Z.eta(), madgraphWeight );
    Zy_Zmass->Fill(     Z.mass(), Z.Rapidity(),   madgraphWeight );
    Zphi_Zmass->Fill(   Z.mass(), Z.phi(), madgraphWeight );
    pt_Zmass->Fill(     Z.mass(), l_pt,    madgraphWeight );
    eta_Zmass->Fill(    Z.mass(), l_eta,   madgraphWeight );
    phi_Zmass->Fill(    Z.mass(), l_phi,   madgraphWeight );

    Weight_Zmass_->Fill( Z_.mass(), madgraphWeight );
    Zpt_Zmass_->Fill(    Z_.mass(), Z_.pt(),  madgraphWeight );
    Zeta_Zmass_->Fill(   Z_.mass(), Z_.eta(), madgraphWeight );
    Zy_Zmass_->Fill(     Z_.mass(), Z_.Rapidity(),   madgraphWeight );
    Zphi_Zmass_->Fill(   Z_.mass(), Z_.phi(), madgraphWeight );
    pt_Zmass_->Fill(     Z_.mass(), l_pt_,    madgraphWeight );
    eta_Zmass_->Fill(    Z_.mass(), l_eta_,   madgraphWeight );
    phi_Zmass_->Fill(    Z_.mass(), l_phi_,   madgraphWeight );

  }

  return
    isFind1 && isFind2 && isFind1_ && isFind2_;
}


DEFINE_FWK_MODULE(GenNtuple);
