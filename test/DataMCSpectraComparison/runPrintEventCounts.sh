#!/bin/bash

python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120" -p 148 | tee www_ratios/z_peak_ratio_all_148.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120" -p 222 | tee www_ratios/z_peak_ratio_all_222.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120" -p 296 | tee www_ratios/z_peak_ratio_all_296.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120" -p 385 | tee www_ratios/z_peak_ratio_all_385.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120" -p 445 | tee www_ratios/z_peak_ratio_all_445.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120" -p 500 | tee www_ratios/z_peak_ratio_all_500.txt

python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -p 148 | tee www_ratios/z_peak_ratio_bb_148.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -p 222 | tee www_ratios/z_peak_ratio_bb_222.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -p 296 | tee www_ratios/z_peak_ratio_bb_296.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -p 385 | tee www_ratios/z_peak_ratio_bb_385.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -p 445 | tee www_ratios/z_peak_ratio_bb_445.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -p 500 | tee www_ratios/z_peak_ratio_bb_500.txt

python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -p 148 | tee www_ratios/z_peak_ratio_beee_148.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -p 222 | tee www_ratios/z_peak_ratio_beee_222.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -p 296 | tee www_ratios/z_peak_ratio_beee_296.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -p 385 | tee www_ratios/z_peak_ratio_beee_385.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -p 445 | tee www_ratios/z_peak_ratio_beee_445.txt
python PrintEventCounts.py -s ourpre -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -p 500 | tee www_ratios/z_peak_ratio_beee_500.txt
