#!/bin/bash

python CompareGenLevelDY.py -x res_pt --nbinsx 30 --xmin 0 --xmax 300 --logy -s "res_mass>60 && res_mass<120" -n gen_res_pt_all
python CompareGenLevelDY.py -x res_pt --nbinsx 30 --xmin 0 --xmax 300 --logy -s "res_mass>60 && res_mass<120" -n gen_res_pt_acc -c acc
python CompareGenLevelDY.py -x res_pt --nbinsx 30 --xmin 0 --xmax 300 --logy -s "res_mass>60 && res_mass<120 && lep_noib_pt[0]>30 && lep_noib_pt[1]>30" -n gen_res_pt_acc_pt -c acc

python CompareGenLevelDY.py -x res_rap --nbinsx 30 --xmin -5 --xmax 5 --logy -s "res_mass>60 && res_mass<120" -n gen_res_rap_all
python CompareGenLevelDY.py -x res_rap --nbinsx 30 --xmin -5 --xmax 5 --logy -s "res_mass>60 && res_mass<120" -n gen_res_rap_acc -c acc
python CompareGenLevelDY.py -x res_rap --nbinsx 30 --xmin -5 --xmax 5 --logy -s "res_mass>60 && res_mass<120 && lep_noib_pt[0]>30 && lep_noib_pt[1]>30" -n gen_res_rap_acc_pt -c acc
