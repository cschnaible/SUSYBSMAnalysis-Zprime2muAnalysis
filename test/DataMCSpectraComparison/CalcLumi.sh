#!/bin/bash

echo "Doing Mu27 2018"
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json \
    -u /ub --byls --hltpath HLT_Mu27_v* \
    -i json/processed_Run2018ABCD_17Sep2018_Run2018D_22Jan2019_20190502.json | tee lumi/processed_Mu27_Run2018ABCD_17Sep2018_Run2018D_22Jan2019_20190502.lumi

echo "Doing Mu50 2018"
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json \
    -u /ub --byls --hltpath HLT_Mu50_v* \
    -i json/processed_Run2018ABCD_17Sep2018_Run2018D_22Jan2019_20190502.json | tee lumi/processed_Mu50_Run2018ABCD_17Sep2018_Run2018D_22Jan2019_20190502.lumi

echo "Doing Mu27 2017"
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json \
    -u /ub --byls --hltpath HLT_Mu27_v* \
    -i json/processed_Run2017_31Mar2018.json | tee lumi/processed_Mu27_Run2017_31Mar2018.lumi

echo "Doing Mu50 2017"
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json \
    -u /ub --byls --hltpath HLT_Mu50_v* \
    -i json/processed_Run2017_31Mar2018.json | tee lumi/processed_Mu50_Run2017_31Mar2018.lumi

echo "Doing Mu27 2016"
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PUBLICPLOTS.json \
    -u /ub --byls --hltpath HLT_Mu27_v* \
    -i json/processed_Run2016_17Jul2018.json | tee lumi/processed_Mu27_Run2016_17Jul2018.lumi

echo "Doing Mu50 2016"
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PUBLICPLOTS.json \
    -u /ub --byls --hltpath HLT_Mu50_v* \
    -i json/processed_Run2016_17Jul2018.json | tee lumi/processed_Mu50_Run2016_17Jul2018.lumi
