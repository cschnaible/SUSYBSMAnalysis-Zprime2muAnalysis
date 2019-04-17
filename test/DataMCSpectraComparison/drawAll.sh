#!/bin/bash

LUMI=61608
HDIR=data # directory with data
TAG=20190227 
for plot in {DimuonMassVertexConstrained,DimuonMassVtxConstrainedLog,DileptonMass}
do
    for cat in {_bb,_be,""}
    do
        for cut in {Our2018,Our2018Prescaled}
        do
            echo $plot $cat $cut 
            python draw.py --histo-dir $HDIR --luminosity $LUMI --include-quantity $plot$cat --include-cutset $cut --plot-dir-tag $TAG
        done
    done
done

for plot in {LeptonPt,LeptonEta,DileptonRap,DileptonPt,DimuonMassVtx_chi2,DimuonMassVtx_prob}
do
    for cut in {Our2018,Our2018Prescaled}
    do
        echo $plot $cut 
        python draw.py --histo-dir $HDIR --luminosity $LUMI --include-quantity $plot --include-cutset $cut --plot-dir-tag $TAG
    done
done
