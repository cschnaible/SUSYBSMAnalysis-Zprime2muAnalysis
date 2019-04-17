#!/bin/bash
pushd test/DataMCSpectraComparison/
bash setup.sh
popd

pushd test/NMinus1Effs
bash setup.sh
popd

pushd test/EfficiencyResolutionFromMC
bash setup.sh
popd

pushd test/FullAnalysis
bash setup.sh
popd
