#!bin/bash
LUMI=60858
TAG=plots_20190328
BASE=www_datamc
#for cutset in Our2018MuPrescaled
for cutset in {Our2018,Our2018MuPrescaled,Our2018MuPrescaledNoCommon}
do
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity DileptonMass 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity DileptonMass_bb 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity DileptonMass_be 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity DimuonMassVertexConstrained 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity DimuonMassVertexConstrained_bb 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity DimuonMassVertexConstrained_be 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity DimuonMassVtxConstrainedLog 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity DimuonMassVtxConstrainedLog_bb 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity DimuonMassVtxConstrainedLog_be 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity LeptonPt 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity LeptonEta 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity DileptonPt 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity DileptonPz 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity DileptonRap 
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity RelIsoSumPt
    python draw_chris.py -d data --plot-dir-base $BASE --plot-dir-tag $TAG --luminosity $LUMI --include-cutset $cutset --include-quantity IsoSumPt
    cp ~/public/index.php $BASE/$TAG/$cutset
done

cp do_draw_chris.sh $BASE/$TAG
cp draw_chris.py $BASE/$TAG/draw_chris_${TAG}.py
cp ~/public/index.php $BASE/$TAG
