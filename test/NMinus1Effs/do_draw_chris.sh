#!/bin/bash

#LUMI=61035
LUMI=60825 # A+B+C+D
TAG=plots_20190320_data
BASE=www_nm1

#for DRAW in NoPt NoPtMuPrescaledPt27 NoDB NoIso NoMuHits NoMuMatch NoPxHits NoTkLayers NoTrgMtch NoTrgMtchMuPrescaledPt53 NoTrgMtchMuPrescaledPt27 NoB2B NoVtxProb NoDptPt NoCosm
for DRAW in NoIso
do
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --no-lumi-rescale --nm1-name $DRAW --exclude-sample dyInclusive50_madgraph
done
cp ~/public/index.php $BASE/$TAG
cp do_draw_chris.sh $BASE/$TAG
cp draw_chris.py $BASE/$TAG/draw_chris_${TAG}.py
