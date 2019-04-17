#!/bin/bash 

echo $1
brilcalc lumi --normtag  /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb  -i $1
