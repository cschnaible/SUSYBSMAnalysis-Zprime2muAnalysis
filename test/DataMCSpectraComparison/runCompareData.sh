#!/bin/bash
where=www_compare_data

## Normal analysis comparison
#python CompareData.py -d our -x vertex_m --logx --nbinsx 30 --xmin 60 --xmax 3500 -bw --logy -n vertex_m_compare_data_full_all -w ${where} | tee ${where}/vertex_m_compare_data_full_all.log
#python CompareData.py -d our -x vertex_m --logx --nbinsx 30 --xmin 60 --xmax 3500 -bw --logy -c "(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)" -n vertex_m_compare_data_full_bb -w ${where} | tee ${where}/vertex_m_compare_data_full_bb.log
#python CompareData.py -d our -x vertex_m --logx --nbinsx 30 --xmin 60 --xmax 3500 -bw --logy -c "(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -n vertex_m_compare_data_full_beee -w ${where} | tee ${where}/vertex_m_compare_data_full_beee.log
#
#python CompareData.py -d our -x vertex_m --logx --nbinsx 30 --xmin 120 --xmax 3500 -bw --logy -n vertex_m_compare_data_120m_all -w ${where} | tee ${where}/vertex_m_compare_data_120m_all.log
#python CompareData.py -d our -x vertex_m --logx --nbinsx 30 --xmin 120 --xmax 3500 -bw --logy -c "(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)" -n vertex_m_compare_data_120m_bb -w ${where} | tee ${where}/vertex_m_compare_data_120m_bb.log
#python CompareData.py -d our -x vertex_m --logx --nbinsx 30 --xmin 120 --xmax 3500 -bw --logy -c "(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -n vertex_m_compare_data_120m_beee -w ${where} | tee ${where}/vertex_m_compare_data_120m_beee.log
#
#python CompareData.py -d our -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -n vertex_m_compare_data_60m120_all -w ${where} | tee ${where}/vertex_m_compare_data_60m120_all.log
#python CompareData.py -d our -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -c "(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)" -n vertex_m_compare_data_60m120_bb -w ${where} | tee ${where}/vertex_m_compare_data_60m120_bb.log
#python CompareData.py -d our -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -c "(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -n vertex_m_compare_data_60m120_beee -w ${where} | tee ${where}/vertex_m_compare_data_60m120_beee.log
#
## Z-peak common prescale comparison
#
#python CompareData.py -d ourcommonpre -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -n vertex_m_compare_data_mu27_common_pre_60m120_all -w ${where} | tee ${where}/vertex_m_compare_data_mu27_common_pre_60m120_all.log
#python CompareData.py -d ourcommonpre -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -c "(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)" -n vertex_m_compare_data_mu27_common_pre_60m120_bb -w ${where} | tee ${where}/vertex_m_compare_data_mu27_common_pre_60m120_bb.log
#python CompareData.py -d ourcommonpre -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -c "(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -n vertex_m_compare_data_mu27_common_pre_60m120_beee -w ${where} | tee ${where}/vertex_m_compare_data_mu27_common_pre_60m120_beee.log
#
## Z-peak no common prescale, scaled by lumi & average prescale
#
#python CompareData.py -d ourpre -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -n vertex_m_compare_data_mu27_avg_pre_60m120_all -w ${where} | tee ${where}/vertex_m_compare_data_mu27_avg_pre_60m120_all.log
#python CompareData.py -d ourpre -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -c "(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)" -n vertex_m_compare_data_mu27_avg_pre_60m120_bb -w ${where} | tee ${where}/vertex_m_compare_data_mu27_avg_pre_60m120_bb.log
#python CompareData.py -d ourpre -x vertex_m --nbinsx 30 --xmin 60 --xmax 120 --logy -c "(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -n vertex_m_compare_data_mu27_avg_pre_60m120_beee -w ${where} | tee ${where}/vertex_m_compare_data_mu27_avg_pre_60m120_beee.log

## Compare pT spectra in data
#python CompareData.py -d ourcommonpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_common_pre_60m120_all -w ${where} -c "vertex_m>60 && vertex_m<120" | tee ${where}/lep_pt_compare_data_mu27_common_pre_60m120_all.log
#python CompareData.py -d ourcommonpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_common_pre_60m120_b -w ${where} -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta)<=1.2" | tee ${where}/lep_pt_compare_data_mu27_common_pre_60m120_b.log
#python CompareData.py -d ourcommonpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_common_pre_60m120_e -w ${where} -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta)>1.2" | tee ${where}/lep_pt_compare_data_mu27_common_pre_60m120_e.log
#python CompareData.py -d ourcommonpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_common_pre_60m120_o -w ${where} -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta)>0.9 && fabs(lep_eta)<1.2" | tee ${where}/lep_pt_compare_data_mu27_common_pre_60m120_o.log
#python CompareData.py -d ourcommonpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_common_pre_60m120_fwd -w ${where} -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta)>2.1" | tee ${where}/lep_pt_compare_data_mu27_common_pre_60m120_fwd.log

python CompareData.py -d ourpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_pre_60m120_all -w ${where} -c "vertex_m>60 && vertex_m<120" | tee ${where}/lep_pt_compare_data_mu27_pre_60m120_all.log
python CompareData.py -d ourpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_pre_60m120_b -w ${where} -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta)<=1.2" | tee ${where}/lep_pt_compare_data_mu27_pre_60m120_b.log
python CompareData.py -d ourpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_pre_60m120_e -w ${where} -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta)>1.2" | tee ${where}/lep_pt_compare_data_mu27_pre_60m120_e.log
python CompareData.py -d ourpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_pre_60m120_o -w ${where} -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta)>0.9 && fabs(lep_eta)<1.2" | tee ${where}/lep_pt_compare_data_mu27_pre_60m120_o.log
python CompareData.py -d ourpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_pre_60m120_fwd -w ${where} -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta)>2.1" | tee ${where}/lep_pt_compare_data_mu27_pre_60m120_fwd.log

#python CompareData.py -d ourpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_zpeak_norm_pre_60m120_all -w ${where} -c "vertex_m>60 && vertex_m<120" | tee ${where}/lep_pt_compare_data_mu27_zpeak_norm_pre_60m120_all.log
#python CompareData.py -d ourpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_zpeak_norm_pre_60m120_b -w ${where} -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta)<=1.2" | tee ${where}/lep_pt_compare_data_mu27_zpeak_norm_pre_60m120_b.log
#python CompareData.py -d ourpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_zpeak_norm_pre_60m120_e -w ${where} -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta)>1.2" | tee ${where}/lep_pt_compare_data_mu27_zpeak_norm_pre_60m120_e.log
#python CompareData.py -d ourpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_zpeak_norm_pre_60m120_o -w ${where} -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta)>0.9 && fabs(lep_eta)<1.2" | tee ${where}/lep_pt_compare_data_mu27_zpeak_norm_pre_60m120_o.log
#python CompareData.py -d ourpre -x lep_pt --nbinsx 30 --logx --xmin 30 --xmax 550 --logy -n lep_pt_compare_data_mu27_zpeak_norm_pre_60m120_fwd -w ${where} -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta)>2.1" | tee ${where}/lep_pt_compare_data_mu27_zpeak_norm_pre_60m120_fwd.log
