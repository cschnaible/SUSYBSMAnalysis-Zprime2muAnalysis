#!/bin/bash

python CompareData.py -x nvertices --logy --nbinsx 45 --xmin 0 --xmax 90 -n data_comparison_luminorm_2017_2018_zpeak_nvertices -c "vertex_m>60 && vertex_m<120"
python CompareData.py -x nvertices --logy --nbinsx 45 --xmin 0 --xmax 90 -n data_comparison_luminorm_2017_2018_highmass_nvertices -c "vertex_m>120"

python CompareData.py -x nvertices --logy --nbinsx 45 --xmin 0 --xmax 90 -n data_comparison_luminorm_2017_2018_zpeak_nvertices_bb -c "fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2 && vertex_m>60 && vertex_m<120"
python CompareData.py -x nvertices --logy --nbinsx 45 --xmin 0 --xmax 90 -n data_comparison_luminorm_2017_2018_highmass_nvertices_bb -c "fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2 && vertex_m>120"

python CompareData.py -x nvertices --logy --nbinsx 45 --xmin 0 --xmax 90 -n data_comparison_luminorm_2017_2018_zpeak_nvertices_beee -c "(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2) && vertex_m>60 && vertex_m<120"
python CompareData.py -x nvertices --logy --nbinsx 45 --xmin 0 --xmax 90 -n data_comparison_luminorm_2017_2018_highmass_nvertices_beee -c "(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2) && vertex_m>120"
