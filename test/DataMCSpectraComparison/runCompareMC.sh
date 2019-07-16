#!/bin/bash

where=www_compare_mc

# Normal analysis comparison
python CompareMC.py -d our -x vertex_m --logx --nbinsx 30 --xmin 60 --xmax 3500 -bw --logy -n vertex_m_compare_mc_full_all -w ${where} | tee ${where}/vertex_m_compare_mc_full_all.log
python CompareMC.py -d our -x vertex_m --logx --nbinsx 30 --xmin 60 --xmax 3500 -bw --logy -c "(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)" -n vertex_m_compare_mc_full_bb -w ${where} | tee ${where}/vertex_m_compare_mc_full_bb.log
python CompareMC.py -d our -x vertex_m --logx --nbinsx 30 --xmin 60 --xmax 3500 -bw --logy -c "(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -n vertex_m_compare_mc_full_beee -w ${where} | tee ${where}/vertex_m_compare_mc_full_beee.log

python CompareMC.py -d our -x vertex_m --logx --nbinsx 30 --xmin 120 --xmax 3500 -bw --logy -n vertex_m_compare_mc_120m_all -w ${where} | tee ${where}/vertex_m_compare_mc_120m_all.log
python CompareMC.py -d our -x vertex_m --logx --nbinsx 30 --xmin 120 --xmax 3500 -bw --logy -c "(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)" -n vertex_m_compare_mc_120m_bb -w ${where} | tee ${where}/vertex_m_compare_mc_120m_bb.log
python CompareMC.py -d our -x vertex_m --logx --nbinsx 30 --xmin 120 --xmax 3500 -bw --logy -c "(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -n vertex_m_compare_mc_120m_beee -w ${where} | tee ${where}/vertex_m_compare_mc_120m_beee.log

python CompareMC.py -d our -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -n vertex_m_compare_mc_60m120_all -w ${where} | tee ${where}/vertex_m_compare_mc_60m120_all.log
python CompareMC.py -d our -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -c "(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)" -n vertex_m_compare_mc_60m120_bb -w ${where} | tee ${where}/vertex_m_compare_mc_60m120_bb.log
python CompareMC.py -d our -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -c "(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -n vertex_m_compare_mc_60m120_beee -w ${where} | tee ${where}/vertex_m_compare_mc_60m120_beee.log

# Z-peak comparison

python CompareMC.py -d ourpre -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -n vertex_m_compare_mc_mu27_pre_60m120_all -w ${where} | tee ${where}/vertex_m_compare_mc_mu27_pre_60m120_all.log
python CompareMC.py -d ourpre -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -c "(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)" -n vertex_m_compare_mc_mu27_pre_60m120_bb -w ${where} | tee ${where}/vertex_m_compare_mc_mu27_pre_60m120_bb.log
python CompareMC.py -d ourpre -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -c "(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -n vertex_m_compare_mc_mu27_pre_60m120_beee -w ${where} | tee ${where}/vertex_m_compare_mc_mu27_pre_60m120_beee.log
