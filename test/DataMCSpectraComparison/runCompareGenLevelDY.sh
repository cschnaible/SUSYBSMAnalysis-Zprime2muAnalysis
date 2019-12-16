#!/bin/bash

name=20190728

#python CompareGenLevelDY.py -x res_pt --nbinsx 30 --xmin 0 --xmax 300 --logy -s "res_mass>60 && res_mass<120" -n gen_res_pt_all
#python CompareGenLevelDY.py -x res_pt --nbinsx 30 --xmin 0 --xmax 300 --logy -s "res_mass>60 && res_mass<120" -n gen_res_pt_acc -c acc
#python CompareGenLevelDY.py -x res_pt --nbinsx 30 --xmin 0 --xmax 300 --logy -s "res_mass>60 && res_mass<120 && lep_noib_pt[0]>30 && lep_noib_pt[1]>30" -n gen_res_pt_acc_pt -c acc
#
#python CompareGenLevelDY.py -x res_rap --nbinsx 30 --xmin -5 --xmax 5 --logy -s "res_mass>60 && res_mass<120" -n gen_res_rap_all
#python CompareGenLevelDY.py -x res_rap --nbinsx 30 --xmin -5 --xmax 5 --logy -s "res_mass>60 && res_mass<120" -n gen_res_rap_acc -c acc
#python CompareGenLevelDY.py -x res_rap --nbinsx 30 --xmin -5 --xmax 5 --logy -s "res_mass>60 && res_mass<120 && lep_noib_pt[0]>30 && lep_noib_pt[1]>30" -n gen_res_rap_acc_pt -c acc

python CompareGenLevelDY.py -x res_rap --nbinsx 80 --xmin -4 --xmax 4 --logy -s "res_mass>5000" -n gen_res_rap_5000m_all_${name}
python CompareGenLevelDY.py -x res_rap --nbinsx 80 --xmin -4 --xmax 4 --logy -s "res_mass>5000" -n gen_res_rap_5000m_acc_${name} -c acc
python CompareGenLevelDY.py -x res_rap --nbinsx 80 --xmin -4 --xmax 4 --logy -s "res_mass>5000" -n gen_res_rap_5000m_bb_${name} -c bb
python CompareGenLevelDY.py -x res_rap --nbinsx 80 --xmin -4 --xmax 4 --logy -s "res_mass>5000" -n gen_res_rap_5000m_beee_${name} -c beee
