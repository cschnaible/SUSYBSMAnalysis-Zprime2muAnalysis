#!/bin/bash
#IN=ana_common_20190512
IN=20190417
OUT=nocommon_20190512
# 20190417 is for nocommon
# 20190416 is for everything else

echo "Doing Mu27"
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json \
    -u /nb --byls --hltpath HLT_Mu27_v* \
    -i json/processed_Run2017BCDEF_${IN}.json | tee lumi/processed_Run2017BCDEF_Mu27_${OUT}.lumi

echo "Doing Mu50"
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json \
    -u /nb --byls --hltpath HLT_Mu50_v* \
    -i json/processed_Run2017BCDEF_${IN}.json | tee lumi/processed_Run2017BCDEF_Mu50_${OUT}.lumi
