#!/bin/bash

python QuickDrawDataMC.py -x lep_pt --nbinsx 30 --xmin 0 --xmax 1500 --logy --do-stack -c "fabs(lep_eta)<1.2 && dil_pt>100 && dil_pt<=200" -n lep_pt_barrel_dyht_100zpt200
python QuickDrawDataMC.py -x lep_pt --nbinsx 30 --xmin 0 --xmax 1500 --logy --do-stack -c "fabs(lep_eta)>=1.2 && dil_pt>100 && dil_pt<=200" -n lep_pt_endcap_dyht_100zpt200

python QuickDrawDataMC.py -x lep_pt --nbinsx 30 --xmin 0 --xmax 1500 --logy --do-stack -c "fabs(lep_eta)<1.2 && dil_pt>200 && dil_pt<=400" -n lep_pt_barrel_dyht_200zpt400
python QuickDrawDataMC.py -x lep_pt --nbinsx 30 --xmin 0 --xmax 1500 --logy --do-stack -c "fabs(lep_eta)>=1.2 && dil_pt>200 && dil_pt<=400" -n lep_pt_endcap_dyht_200zpt400

#python QuickDrawDataMC.py -x lep_pt --nbinsx 30 --xmin 0 --xmax 1500 --logy --do-stack -c "fabs(lep_eta)<1.2 && dil_pt>400 && dil_pt<=600" -n lep_pt_barrel_dyht_400zpt600
#python QuickDrawDataMC.py -x lep_pt --nbinsx 30 --xmin 0 --xmax 1500 --logy --do-stack -c "fabs(lep_eta)>=1.2 && dil_pt>400 && dil_pt<=600" -n lep_pt_endcap_dyht_400zpt600

python QuickDrawDataMC.py -x lep_pt --nbinsx 30 --xmin 0 --xmax 1500 --logy --do-stack -c "fabs(lep_eta)<1.2 && dil_pt>400" -n lep_pt_barrel_dyht_400zpt
python QuickDrawDataMC.py -x lep_pt --nbinsx 30 --xmin 0 --xmax 1500 --logy --do-stack -c "fabs(lep_eta)>=1.2 && dil_pt>400" -n lep_pt_endcap_dyht_400zpt
