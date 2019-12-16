#!/bin/bash

OUTDIR='www_datamc_atZ'

#Total 42036.9393414
#    59 86.8712438022
#    70 275.190535276
#    74 163.661209166
#    117 46.2436284491
#    120 4123.72145243
#    140 2413.39785073
#    148 541.983190576
#    176 860.668911332
#    210 5560.95773849
#    222 951.36024321
#    234 2050.1262438
#    280 6535.92676296
#    281 1111.61316576
#    296 1188.58563938
#    315 770.139832091
#    328 1921.36662493
#    336 1626.58354641
#    341 525.035573921
#    356 463.119019459
#    375 119.156046088
#    385 483.395320788
#    392 911.390557063
#    415 621.24955696
#    422 141.494069456
#    445 2846.99397805
#    449 752.926446731
#    458 26.4998925556
#    480 14.0916112563
#    505 2198.24925031
#    561 2704.94019996
#Mu27
#Total 178.058438126
#    59 1.47239396275
#    70 3.93129336107
#    74 2.21163796169
#    117 0.395244687597
#    120 34.364345437
#    140 17.2385560766
#    148 3.66204858499
#    176 4.89016426893
#    210 26.4807511356
#    222 4.28540650095
#    234 8.76122326406
#    280 23.3425955821
#    281 3.95591873938
#    296 4.01549202491
#    315 2.44488835583
#    328 5.85782507604
#    336 4.84102245952
#    341 1.53969376516
#    356 1.30089612208
#    375 0.317749456237
#    385 1.25557226181
#    392 2.32497591087
#    415 1.49698688423
#    422 0.335294003445
#    445 6.39773927651
#    449 1.67689631787
#    458 0.057860027413
#    480 0.029357523443
#    505 4.3529688125
#    561 4.82164028514

commonPreLumi=178.019823704 # excludes 9.2 pb-1 of prescale=1 data
commonLumi=41992.3386644 # excludes 9.2 pb-1 of prescale=1 data

Lumi59=1.47239396275
Lumi70=3.93129336107
Lumi74=2.21163796169
Lumi117=0.395244687597
Lumi120=34.364345437
Lumi140=17.2385560766
Lumi148=3.66204858499
Lumi176=4.89016426893
Lumi210=26.4807511356
Lumi222=4.28540650095
Lumi234=8.76122326406
Lumi280=23.3425955821
Lumi281=3.95591873938
Lumi296=4.01549202491
Lumi315=2.44488835583
Lumi328=5.85782507604
Lumi336=4.84102245952
Lumi341=1.53969376516
Lumi356=1.30089612208
Lumi375=0.317749456237
Lumi385=1.25557226181
Lumi392=2.32497591087
Lumi415=1.49698688423
Lumi422=0.335294003445
Lumi445=6.39773927651
Lumi449=1.67689631787
Lumi458=0.057860027413
Lumi480=0.029357523443
Lumi505=4.3529688125
Lumi561=4.82164028514

python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_20190416.root -d Our2017MuPrescaledMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${commonLumi} -p 561 -n vertex_m_mu27_common_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_common_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_20190416.root -d Our2017MuPrescaledMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${commonLumi} -p 561 -n vertex_m_mu27_common_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_common_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_20190416.root -d Our2017MuPrescaledMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${commonLumi} -p 561 -n vertex_m_mu27_common_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_common_beee.log

python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi59} -dc "Mu27_prescale==59" -n vertex_m_mu27_pre59_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre59_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi70} -dc "Mu27_prescale==70" -n vertex_m_mu27_pre70_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre70_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi74} -dc "Mu27_prescale==74" -n vertex_m_mu27_pre74_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre74_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi117} -dc "Mu27_prescale==117" -n vertex_m_mu27_pre117_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre117_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi120} -dc "Mu27_prescale==120" -n vertex_m_mu27_pre120_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre120_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi140} -dc "Mu27_prescale==140" -n vertex_m_mu27_pre140_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre140_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi148} -dc "Mu27_prescale==148" -n vertex_m_mu27_pre148_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre148_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi176} -dc "Mu27_prescale==176" -n vertex_m_mu27_pre176_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre176_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi210} -dc "Mu27_prescale==210" -n vertex_m_mu27_pre210_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre210_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi222} -dc "Mu27_prescale==222" -n vertex_m_mu27_pre222_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre222_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi234} -dc "Mu27_prescale==234" -n vertex_m_mu27_pre234_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre234_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi280} -dc "Mu27_prescale==280" -n vertex_m_mu27_pre280_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre280_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi281} -dc "Mu27_prescale==281" -n vertex_m_mu27_pre281_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre281_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi296} -dc "Mu27_prescale==296" -n vertex_m_mu27_pre296_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre296_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi315} -dc "Mu27_prescale==315" -n vertex_m_mu27_pre315_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre315_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi328} -dc "Mu27_prescale==328" -n vertex_m_mu27_pre328_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre328_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi336} -dc "Mu27_prescale==336" -n vertex_m_mu27_pre336_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre336_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi341} -dc "Mu27_prescale==341" -n vertex_m_mu27_pre341_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre341_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi356} -dc "Mu27_prescale==356" -n vertex_m_mu27_pre356_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre356_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi375} -dc "Mu27_prescale==375" -n vertex_m_mu27_pre375_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre375_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi385} -dc "Mu27_prescale==385" -n vertex_m_mu27_pre385_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre385_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi392} -dc "Mu27_prescale==392" -n vertex_m_mu27_pre392_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre392_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi415} -dc "Mu27_prescale==415" -n vertex_m_mu27_pre415_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre415_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi422} -dc "Mu27_prescale==422" -n vertex_m_mu27_pre422_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre422_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi445} -dc "Mu27_prescale==445" -n vertex_m_mu27_pre445_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre445_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi449} -dc "Mu27_prescale==449" -n vertex_m_mu27_pre449_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre449_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi458} -dc "Mu27_prescale==458" -n vertex_m_mu27_pre458_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre458_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi480} -dc "Mu27_prescale==480" -n vertex_m_mu27_pre480_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre480_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi505} -dc "Mu27_prescale==505" -n vertex_m_mu27_pre505_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre505_all.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi561} -dc "Mu27_prescale==561" -n vertex_m_mu27_pre561_all -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre561_all.log

python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi59} -dc "Mu27_prescale==59" -n vertex_m_mu27_pre59_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre59_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi70} -dc "Mu27_prescale==70" -n vertex_m_mu27_pre70_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre70_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi74} -dc "Mu27_prescale==74" -n vertex_m_mu27_pre74_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre74_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi117} -dc "Mu27_prescale==117" -n vertex_m_mu27_pre117_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre117_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi120} -dc "Mu27_prescale==120" -n vertex_m_mu27_pre120_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre120_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi140} -dc "Mu27_prescale==140" -n vertex_m_mu27_pre140_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre140_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi148} -dc "Mu27_prescale==148" -n vertex_m_mu27_pre148_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre148_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi176} -dc "Mu27_prescale==176" -n vertex_m_mu27_pre176_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre176_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi210} -dc "Mu27_prescale==210" -n vertex_m_mu27_pre210_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre210_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi222} -dc "Mu27_prescale==222" -n vertex_m_mu27_pre222_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre222_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi234} -dc "Mu27_prescale==234" -n vertex_m_mu27_pre234_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre234_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi280} -dc "Mu27_prescale==280" -n vertex_m_mu27_pre280_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre280_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi281} -dc "Mu27_prescale==281" -n vertex_m_mu27_pre281_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre281_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi296} -dc "Mu27_prescale==296" -n vertex_m_mu27_pre296_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre296_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi315} -dc "Mu27_prescale==315" -n vertex_m_mu27_pre315_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre315_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi328} -dc "Mu27_prescale==328" -n vertex_m_mu27_pre328_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre328_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi336} -dc "Mu27_prescale==336" -n vertex_m_mu27_pre336_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre336_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi341} -dc "Mu27_prescale==341" -n vertex_m_mu27_pre341_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre341_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi356} -dc "Mu27_prescale==356" -n vertex_m_mu27_pre356_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre356_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi375} -dc "Mu27_prescale==375" -n vertex_m_mu27_pre375_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre375_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi385} -dc "Mu27_prescale==385" -n vertex_m_mu27_pre385_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre385_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi392} -dc "Mu27_prescale==392" -n vertex_m_mu27_pre392_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre392_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi415} -dc "Mu27_prescale==415" -n vertex_m_mu27_pre415_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre415_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi422} -dc "Mu27_prescale==422" -n vertex_m_mu27_pre422_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre422_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi445} -dc "Mu27_prescale==445" -n vertex_m_mu27_pre445_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre445_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi449} -dc "Mu27_prescale==449" -n vertex_m_mu27_pre449_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre449_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi458} -dc "Mu27_prescale==458" -n vertex_m_mu27_pre458_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre458_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi480} -dc "Mu27_prescale==480" -n vertex_m_mu27_pre480_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre480_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi505} -dc "Mu27_prescale==505" -n vertex_m_mu27_pre505_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre505_bb.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && fabs(lep_eta[0])<1.2 && fabs(lep_eta[1])<1.2" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi561} -dc "Mu27_prescale==561" -n vertex_m_mu27_pre561_bb -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre561_bb.log

python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi59} -dc "Mu27_prescale==59" -n vertex_m_mu27_pre59_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre59_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi70} -dc "Mu27_prescale==70" -n vertex_m_mu27_pre70_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre70_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi74} -dc "Mu27_prescale==74" -n vertex_m_mu27_pre74_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre74_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi117} -dc "Mu27_prescale==117" -n vertex_m_mu27_pre117_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre117_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi120} -dc "Mu27_prescale==120" -n vertex_m_mu27_pre120_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre120_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi140} -dc "Mu27_prescale==140" -n vertex_m_mu27_pre140_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre140_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi148} -dc "Mu27_prescale==148" -n vertex_m_mu27_pre148_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre148_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi176} -dc "Mu27_prescale==176" -n vertex_m_mu27_pre176_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre176_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi210} -dc "Mu27_prescale==210" -n vertex_m_mu27_pre210_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre210_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi222} -dc "Mu27_prescale==222" -n vertex_m_mu27_pre222_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre222_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi234} -dc "Mu27_prescale==234" -n vertex_m_mu27_pre234_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre234_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi280} -dc "Mu27_prescale==280" -n vertex_m_mu27_pre280_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre280_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi281} -dc "Mu27_prescale==281" -n vertex_m_mu27_pre281_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre281_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi296} -dc "Mu27_prescale==296" -n vertex_m_mu27_pre296_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre296_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi315} -dc "Mu27_prescale==315" -n vertex_m_mu27_pre315_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre315_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi328} -dc "Mu27_prescale==328" -n vertex_m_mu27_pre328_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre328_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi336} -dc "Mu27_prescale==336" -n vertex_m_mu27_pre336_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre336_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi341} -dc "Mu27_prescale==341" -n vertex_m_mu27_pre341_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre341_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi356} -dc "Mu27_prescale==356" -n vertex_m_mu27_pre356_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre356_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi375} -dc "Mu27_prescale==375" -n vertex_m_mu27_pre375_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre375_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi385} -dc "Mu27_prescale==385" -n vertex_m_mu27_pre385_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre385_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi392} -dc "Mu27_prescale==392" -n vertex_m_mu27_pre392_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre392_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi415} -dc "Mu27_prescale==415" -n vertex_m_mu27_pre415_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre415_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi422} -dc "Mu27_prescale==422" -n vertex_m_mu27_pre422_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre422_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi445} -dc "Mu27_prescale==445" -n vertex_m_mu27_pre445_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre445_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi449} -dc "Mu27_prescale==449" -n vertex_m_mu27_pre449_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre449_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi458} -dc "Mu27_prescale==458" -n vertex_m_mu27_pre458_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre458_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi480} -dc "Mu27_prescale==480" -n vertex_m_mu27_pre480_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre480_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi505} -dc "Mu27_prescale==505" -n vertex_m_mu27_pre505_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre505_beee.log
python QuickDrawDataMC.py -f data/ana_datamc_Run2017BCDEF_nocommon_20190417.root -d Our2017MuPrescaledNoCommonMuonsPlusMuonsMinusNtuple -x vertex_m -c "vertex_m>60 && vertex_m<120 && (fabs(lep_eta[0])>=1.2 || fabs(lep_eta[1])>=1.2)" -ly --nbinsx 30 --xmin 60 --xmax 120 --do-stack --lumi ${Lumi561} -dc "Mu27_prescale==561" -n vertex_m_mu27_pre561_beee -w www_datamc_atZ | tee ${OUTDIR}/vertex_m_mu27_pre561_beee.log
