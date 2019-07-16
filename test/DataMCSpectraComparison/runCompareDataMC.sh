#!/bin/bash

#where=www_compare_datamc
#where=www_preapp_edit
#where=www_datamc_forSam
#where=www_datamc_20190701
#where=test
#where=www_forPAS_20190620
#where=www_datamc_20190702_forApproval
#where=www_datamc_20190704_mu27_test
#where=www_datamc_20190708_mu27

#where=www_datamc_20190709
#where=www_datamc_20190710_style2
#where=www_datamc_20190710_style3
#where=www_datamc_20190710_style4

#where=www_datamc_20190713_style1
where=www_datamc_20190716
#where=www_datamc_20190713_new_jets
name=20190715

#order=nnlo
cp ~/public/index.php ${where}

#for year in {2017,2018}
#do
#    python CompareDataMC.py -d our -x vertex_m -c all -s "(vertex_m>60 && ((fabs(lep_eta[0])<1.4442 || fabs(lep_eta[1])<1.4442) && (fabs(lep_eta[0])>1.566 || fabs(lep_eta[1])>1.566)))" --nbinsx 40 --xmin 120 --xmax 3700 --nnpdf30 --order nnlo -ly -lx --do-stack -y ${year} -n mass_${year}_be_nnpdf30_nnlo_bw -w ${where} --bin-width --overflow --scaleZ0 --do-smear --do-fake-rate --do-paper --do-uncert
#    python CompareDataMC.py -d our -x vertex_m -c all -s "(vertex_m>60 && ((fabs(lep_eta[0])<1.4442 || fabs(lep_eta[1])<1.4442) && (fabs(lep_eta[0])>1.566 || fabs(lep_eta[1])>1.566)))" --nbinsx 40 --xmin 120 --xmax 3700 --nnpdf30 --order nnlo -ly -lx --do-stack -y ${year} -n mass_${year}_be_nnpdf30_nnlo_cum -w ${where} --overflow --scaleZ0 --do-smear --do-fake-rate --do-paper --cumulative --do-uncert
#done

#for year in {2017,2018}
#do
#    for cat in {all,bb,beee}
#    do
#        python CompareDataMC.py -d ourcommonpre -c ${cat} -x vertex_m  -s "vertex_m>60 && vertex_m<120" -n mass_${year}_${cat}_zpeak  --nbinsx 30 --xmin 60 --xmax 120 --logy --do-stack -y ${year} -w ${where}
#        python CompareDataMC.py -d ourcommonpre -c ${cat} -x dil_pt  -s "vertex_m>60 && vertex_m<120" -n dil_pt_${year}_${cat}_zpeak  --nbinsx 30 --xmin 0 --xmax 300 --logy --do-stack -y ${year} -w ${where} --overflow 
#        python CompareDataMC.py -d ourcommonpre -c ${cat} -x dil_rap  -s "vertex_m>60 && vertex_m<120" -n dil_rap_${year}_${cat}_zpeak  --nbinsx 15 --xmin -3 --xmax 3 --logy --do-stack -y ${year} -w ${where}
#    done
#done
#for year in {2017,2018}
#do
#    python CompareDataMC.py -d ourcommonpre -c all -x lead_pt  -s "vertex_m>60 && vertex_m<120" -n lead_pt_${year}_all_zpeak  --nbinsx 24 --xmin 30 --xmax 150 --logy --do-stack -y ${year} -w ${where} --overflow
#    python CompareDataMC.py -d ourcommonpre -c all -x lead_pt_b  -s "vertex_m>60 && vertex_m<120" -n lead_pt_${year}_b_zpeak  --nbinsx 24 --xmin 30 --xmax 150 --logy --do-stack -y ${year} -w ${where} --overflow
#    python CompareDataMC.py -d ourcommonpre -c all -x lead_pt_e  -s "vertex_m>60 && vertex_m<120" -n lead_pt_${year}_e_zpeak  --nbinsx 24 --xmin 30 --xmax 150 --logy --do-stack -y ${year} -w ${where} --overflow
#    python CompareDataMC.py -d ourcommonpre -c all -x sub_pt  -s "vertex_m>60 && vertex_m<120" -n sub_pt_${year}_all_zpeak  --nbinsx 24 --xmin 30 --xmax 150 --logy --do-stack -y ${year} -w ${where} --overflow
#    python CompareDataMC.py -d ourcommonpre -c all -x sub_pt_b  -s "vertex_m>60 && vertex_m<120" -n sub_pt_${year}_b_zpeak  --nbinsx 24 --xmin 30 --xmax 150 --logy --do-stack -y ${year} -w ${where} --overflow
#    python CompareDataMC.py -d ourcommonpre -c all -x sub_pt_e  -s "vertex_m>60 && vertex_m<120" -n sub_pt_${year}_e_zpeak  --nbinsx 24 --xmin 30 --xmax 150 --logy --do-stack -y ${year} -w ${where} --overflow
#done

for order in nnlo
do
    #for cat in all
    for cat in {all,bb,beee}
    do
        #for year in {run2,2018,2017}
        #for year in {2018,2017}
        for year in {run2,2018,2017,2016}
        #for year in 2018 
        do

            # Combined low- and high-mass, logarithmic mass axis
            python CompareDataMC_stitch.py -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 52 --xmin 60 --xmax 4000 --logy --do-stack -y ${year} -n mass_${year}_${cat}_nnpdf30_log_bw_prescaleMC_${name} -w ${where} --do-paper --do-uncert --nnpdf30 --logx --order ${order} --do-fake-rate --bin-width --overflow --scaleZ0 --prescale-weight mc
            python CompareDataMC_stitch.py -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 52 --xmin 60 --xmax 4000 --logy --do-stack -y ${year} -n mass_${year}_${cat}_nnpdf30_log_cum_prescaleMC_${name} -w ${where} --do-paper --do-uncert --nnpdf30 --logx --order ${order} --do-fake-rate --overflow --scaleZ0 --prescale-weight mc --cumulative --do-separate
            python CompareDataMC_stitch.py -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 52 --xmin 60 --xmax 4000 --logy --do-stack -y ${year} -n mass_${year}_${cat}_nnpdf30_log_bw_prescaleData_${name} -w ${where} --do-paper --do-uncert --nnpdf30 --logx --order ${order} --do-fake-rate --bin-width --overflow --scaleZ0 --prescale-weight data 
            python CompareDataMC_stitch.py -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 52 --xmin 60 --xmax 4000 --logy --do-stack -y ${year} -n mass_${year}_${cat}_nnpdf30_log_cum_prescaleData_${name} -w ${where} --do-paper --do-uncert --nnpdf30 --logx --order ${order} --do-fake-rate --overflow --scaleZ0 --prescale-weight data --cumulative --do-separate

            # High-mass, logarithmic mass axis
            #python CompareDataMC.py -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 44 --xmin 120 --xmax 4000 --logy --do-stack -y ${year} -n mass_120m_${year}_${cat}_nnpdf30_log_bw_${name} -w ${where} --do-paper --do-uncert --nnpdf30 --logx --order ${order} --do-fake-rate --bin-width --overflow --scaleZ0 
            #python CompareDataMC.py -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 44 --xmin 120 --xmax 4000 --logy --do-stack -y ${year} -n mass_120m_${year}_${cat}_nnpdf30_log_cum_${name} -w ${where} --do-paper --do-uncert --nnpdf30 --logx --order ${order} --do-fake-rate --overflow --scaleZ0 --cumulative
            #python CompareDataMC.py -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 38 --xmin 150 --xmax 4000 --logy --do-stack -y ${year} -n mass_150m_${year}_${cat}_nnpdf30_log_bw_${name} -w ${where} --do-paper --do-uncert --nnpdf30 --logx --order ${order} --do-fake-rate --bin-width --overflow --scaleZ0 
            #python CompareDataMC.py -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 38 --xmin 150 --xmax 4000 --logy --do-stack -y ${year} -n mass_150m_${year}_${cat}_nnpdf30_log_cum_${name} -w ${where} --do-paper --do-uncert --nnpdf30 --logx --order ${order} --do-fake-rate --overflow --scaleZ0 --cumulative

            # High-mass, linear mass axis
            #python CompareDataMC.py -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 194 --xmin 120 --xmax 4000 --logy --do-stack -y ${year} -n mass_120m_${year}_${cat}_nnpdf30_lin_${name} -w ${where} --do-paper --do-uncert --nnpdf30 --order ${order} --do-fake-rate --overflow --scaleZ0
            #python CompareDataMC.py -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 194 --xmin 120 --xmax 4000 --logy --do-stack -y ${year} -n mass_120m_${year}_${cat}_nnpdf30_lin_cum_${name} -w ${where} --do-paper --do-uncert --nnpdf30 --order ${order} --do-fake-rate --overflow --scaleZ0 --cumulative

            # Low-mass, linear mass axis
            #python CompareDataMC.py -d ourcommonpre -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 30 --xmin 60 --xmax 120 --logy --do-stack -y ${year} -n mass_zpeak_${year}_${cat}_nnpdf30_lin_${name} -w ${where} --do-paper --do-uncert --nnpdf30 --order ${order}  --prescale-weight mc
            #python CompareDataMC.py -d ourcommonpre -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 30 --xmin 60 --xmax 120 --logy --do-stack -y ${year} -n mass_zpeak_${year}_${cat}_nnpdf30_lin_cum_${name} -w ${where} --do-paper --do-uncert --nnpdf30 --order ${order}  --prescale-weight mc --cumulative

            #python CompareDataMC_stitch.py -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 50 --xmin 60 --xmax 4000 --logy --do-stack -y ${year} -n mass_stitch_${year}_${cat}_nnpdf30_cum_20190707_preWeight -w ${where} --do-paper --do-uncert --nnpdf30 --logx --order ${order} --do-fake-rate --cumulative --overflow --scaleZ0
            #python CompareDataMC_stitch.py -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 197 --xmin 60 --xmax 4000 --logy --do-stack -y ${year} -n mass_stitch_${year}_${cat}_nnpdf30_lin_20190707 -w ${where} --do-paper --do-uncert --nnpdf30 --order ${order} --do-fake-rate --overflow --scaleZ0
            #python CompareDataMC_stitch.py -x vertex_m -c ${cat} -s "vertex_m>50" --nbinsx 197 --xmin 60 --xmax 4000 --logy --do-stack -y ${year} -n mass_stitch_${year}_${cat}_nnpdf30_lin_cum_20190707 -w ${where} --do-paper --do-uncert --nnpdf30 --order ${order} --do-fake-rate --cumulative --overflow --scaleZ0

            # log paper --do-uncert
            #python CompareDataMC.py -d our -x vertex_m -c ${cat} -s "vertex_m>60" --nbinsx 51 --xmin 70 --xmax 4000 --nnpdf30 --order ${order} -ly -lx --do-stack -y ${year} -n mass_${year}_${cat}_nnpdf30_${order}_bw_20190702 -w ${where} --bin-width --overflow --scaleZ0 --do-smear --do-fake-rate --do-paper --do-uncert
            #python CompareDataMC.py -d our -x vertex_m -c ${cat} -s "vertex_m>60" --nbinsx 120 --xmin 70 --xmax 4000 --nnpdf30 --order ${order} -ly -lx --do-stack -y ${year} -n mass_${year}_${cat}_nnpdf30_${order}_cum_log -w ${where} --overflow --scaleZ0 --do-smear --do-fake-rate --do-paper --cumulative --do-uncert
            # linear paper --do-uncert
            #python CompareDataMC.py -d our -x vertex_m -c ${cat} -s "vertex_m>60" --nbinsx 157 --xmin 75 --xmax 4000 --nnpdf30 --order ${order} -ly --do-stack -y ${year} -n mass_${year}_${cat}_nnpdf30_${order}_lin -w ${where} --bin-width --overflow --scaleZ0 --do-smear --do-fake-rate --do-paper --do-uncert
            #python CompareDataMC.py -d our -x vertex_m -c ${cat} -s "vertex_m>60" --nbinsx 157 --xmin 75 --xmax 4000 --nnpdf30 --order ${order} -ly --do-stack -y ${year} -n mass_${year}_${cat}_nnpdf30_${order}_cum_lin -w ${where} --overflow --scaleZ0 --do-smear --do-fake-rate --do-paper --cumulative --do-uncert

            # log
            #python CompareDataMC.py -d our -x vertex_m -c ${cat} -s "vertex_m>60" --nbinsx 40 --xmin 120 --xmax 3700 --nnpdf30 --order ${order} -ly -lx --do-stack -y ${year} -n mass_${year}_${cat}_nnpdf30_${order}_bw -w ${where} --bin-width --overflow --scaleZ0 --do-smear --do-fake-rate --do-paper
            #python CompareDataMC.py -d our -x vertex_m -c ${cat} -s "vertex_m>60" --nbinsx 40 --xmin 120 --xmax 3700 --nnpdf30 --order ${order} -ly -lx --do-stack -y ${year} -n mass_${year}_${cat}_nnpdf30_${order}_cum -w ${where} --overflow --do-smear --scaleZ0 --cumulative --do-fake-rate
            # linear bin width = 25 GeV
            #python CompareDataMC.py -d our -x vertex_m -c ${cat} -s "vertex_m>60" --nbinsx 144 --xmin 100 --xmax 3700 --nnpdf30 --order ${order} -ly --do-stack -y ${year} -n mass_${year}_${cat}_nnpdf30_${order}_lin -w ${where} --overflow --scaleZ0 --do-smear --do-fake-rate
            #python CompareDataMC.py -d our -x vertex_m -c ${cat} -s "vertex_m>60" --nbinsx 144 --xmin 100 --xmax 3700 --nnpdf30 --order ${order} -ly --do-stack -y ${year} -n mass_${year}_${cat}_nnpdf30_${order}_cum_lin -w ${where} --overflow --do-smear --scaleZ0 --cumulative --do-fake-rate

            # test
            #python CompareDataMC.py -d our -x vertex_m -c ${cat} -s "vertex_m>60" --nbinsx 51 --xmin 120 --xmax 400 --nnpdf30 --order ${order} -ly -lx --do-stack -y ${year} -n mass_${year}_${cat}_nnpdf30_${order}_bw_log_err_test -w ${where} --bin-width --overflow --scaleZ0 --do-smear --do-fake-rate --do-paper

            #python CompareDataMC.py -d ourcommonpre -x vertex_m -c ${cat} -s "vertex_m>60" --nbinsx 65 --xmin 70 --xmax 200 --logy --do-stack -y ${year} -n mass_70m200_${year}_${cat}_nnpdf30_20190704 -w ${where} --do-paper --do-uncert --nnpdf30
        done
    done
done

