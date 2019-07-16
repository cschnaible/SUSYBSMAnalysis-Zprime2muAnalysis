#!/bin/bash

#python CompareDataDY.py -x lep_pt --logy --xmin 50 --xmax 120 --nbinsx 15 -w www_nnpdf -c "vertex_m>60" -n lep_pt_our_data_mc_nnpdf_all 
#python CompareDataDY.py -x lep_pt --logy --xmin 50 --xmax 120 --nbinsx 15 -w www_nnpdf -c "vertex_m>60 && fabs(lep_eta)<1.2" -n lep_pt_our_data_mc_nnpdf_b
#python CompareDataDY.py -x lep_pt --logy --xmin 50 --xmax 120 --nbinsx 15 -w www_nnpdf -c "vertex_m>60 && fabs(lep_eta)>0.9 && fabs(lep_eta)<1.2" -n lep_pt_our_data_mc_nnpdf_o
#python CompareDataDY.py -x lep_pt --logy --xmin 50 --xmax 120 --nbinsx 15 -w www_nnpdf -c "vertex_m>60 && fabs(lep_eta)>1.2" -n lep_pt_our_data_mc_nnpdf_e
#python CompareDataDY.py -x lep_pt --logy --xmin 50 --xmax 120 --nbinsx 15 -w www_nnpdf -c "vertex_m>60 && fabs(lep_eta)>2.1" -n lep_pt_our_data_mc_nnpdf_efwd

python CompareDataDY.py -d ourpre -x lep_pt --logy --xmin 30 --xmax 120 --nbinsx 15 -w www_nnpdf -c "vertex_m>60" -n lep_pt_ourpre_data_mc_nnpdf_all  --lumi 125.89
python CompareDataDY.py -d ourpre -x lep_pt --logy --xmin 30 --xmax 120 --nbinsx 15 -w www_nnpdf -c "vertex_m>60 && fabs(lep_eta)<1.2" -n lep_pt_ourpre_data_mc_nnpdf_b --lumi 125.89
python CompareDataDY.py -d ourpre -x lep_pt --logy --xmin 30 --xmax 120 --nbinsx 15 -w www_nnpdf -c "vertex_m>60 && fabs(lep_eta)>0.9 && fabs(lep_eta)<1.2" -n lep_pt_ourpre_data_mc_nnpdf_o --lumi 125.89
python CompareDataDY.py -d ourpre -x lep_pt --logy --xmin 30 --xmax 120 --nbinsx 15 -w www_nnpdf -c "vertex_m>60 && fabs(lep_eta)>1.2" -n lep_pt_ourpre_data_mc_nnpdf_e --lumi 125.89
python CompareDataDY.py -d ourpre -x lep_pt --logy --xmin 30 --xmax 120 --nbinsx 15 -w www_nnpdf -c "vertex_m>60 && fabs(lep_eta)>2.1" -n lep_pt_ourpre_data_mc_nnpdf_efwd --lumi 125.89
