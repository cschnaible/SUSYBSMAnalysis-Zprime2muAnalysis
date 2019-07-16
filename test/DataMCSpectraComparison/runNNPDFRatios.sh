#!/bin/bash

flow=0
fhigh=6500
hlow=0
hhigh=8000
nbinsx=40

#python NNPDFRatios.py -x res_mass --nbinsx ${nbinsx} --xmin ${hlow} --xmax ${hhigh} -c all --fmin ${flow} --fmax ${fhigh}
#python NNPDFRatios.py -x res_mass --nbinsx ${nbinsx} --xmin ${hlow} --xmax ${hhigh} -c acc --fmin ${flow} --fmax ${fhigh} --fit-func pol5 -n 20190704
#python NNPDFRatios.py -x res_mass --nbinsx ${nbinsx} --xmin ${hlow} --xmax ${hhigh} -c bb --fmin ${flow} --fmax ${fhigh} --fit-func pol5 -n 20190704
#python NNPDFRatios.py -x res_mass --nbinsx ${nbinsx} --xmin ${hlow} --xmax ${hhigh} -c beee --fmin ${flow} --fmax ${fhigh} --fit-func pol5 -n 20190704

#python NNPDFRatios.py -x res_mass --nbinsx ${nbinsx} --xmin ${hlow} --xmax ${hhigh} -c all --no-fit
#python NNPDFRatios.py -x res_mass --nbinsx ${nbinsx} --xmin ${hlow} --xmax ${hhigh} -c acc --no-fit
#python NNPDFRatios.py -x res_mass --nbinsx ${nbinsx} --xmin ${hlow} --xmax ${hhigh} -c bb --no-fit
#python NNPDFRatios.py -x res_mass --nbinsx ${nbinsx} --xmin ${hlow} --xmax ${hhigh} -c beee --no-fit
#python NNPDFRatios.py -x res_mass --nbinsx ${nbinsx} --xmin ${hlow} --xmax ${hhigh} -c ee --no-fit

#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c all --no-fit -mc WW --name WW
#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c acc --no-fit -mc WW --name WW
#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c bb --no-fit -mc WW --name WW
#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c beee --no-fit -mc WW --name WW

#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c all -mc WW --name WW
#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c acc -mc WW --name WW
#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c bb -mc WW --name WW
#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c beee -mc WW --name WW

#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c all --no-fit -mc ttbar_lep --name ttbar_lep
#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c acc --no-fit -mc ttbar_lep --name ttbar_lep
#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c bb --no-fit -mc ttbar_lep --name ttbar_lep
#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c beee --no-fit -mc ttbar_lep --name ttbar_lep
#
#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c all -mc ttbar_lep --name ttbar_lep --fmax 3000
#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c acc -mc ttbar_lep --name ttbar_lep --fmax 3000
#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c bb -mc ttbar_lep --name ttbar_lep --fmax 3000
#python NNPDFRatios.py -x res_mass --nbinsx 15 --xmin 0 --xmax 3000 -c beee -mc ttbar_lep --name ttbar_lep --fmax 3000

#python NNPDFRatios.py -x res_mass -var --bin-width -c all --no-fit -mc WW --name WW
#python NNPDFRatios.py -x res_mass -var --bin-width -c acc --no-fit -mc WW --name WW
#python NNPDFRatios.py -x res_mass -var --bin-width -c bb --no-fit -mc WW --name WW
#python NNPDFRatios.py -x res_mass -var --bin-width -c beee --no-fit -mc WW --name WW

#python NNPDFRatios.py -x res_mass -var --bin-width -c all  -mc WW --fmax 3000 --fit-func pol4 -n WW_20190704
#python NNPDFRatios.py -x res_mass -var --bin-width -c acc  -mc WW --fmax 3000 --fit-func pol4 -n WW_20190704
#python NNPDFRatios.py -x res_mass -var --bin-width -c bb   -mc WW --fmax 3000 --fit-func pol4 -n WW_20190704
#python NNPDFRatios.py -x res_mass -var --bin-width -c beee -mc WW --fmax 3000 --fit-func pol4 -n WW_20190704

#python NNPDFRatios.py -x res_mass -var --bin-width -c all --no-fit -mc ttbar_lep --name ttbar_lep
#python NNPDFRatios.py -x res_mass -var --bin-width -c acc --no-fit -mc ttbar_lep --name ttbar_lep
#python NNPDFRatios.py -x res_mass -var --bin-width -c bb --no-fit -mc ttbar_lep --name ttbar_lep
#python NNPDFRatios.py -x res_mass -var --bin-width -c beee --no-fit -mc ttbar_lep --name ttbar_lep

python NNPDFRatios.py -x res_mass -var --bin-width -c all  -mc ttbar_lep --fmax 4250 --fit-func pol3 -n ttbar_lep_20190707
python NNPDFRatios.py -x res_mass -var --bin-width -c acc  -mc ttbar_lep --fmax 4250 --fit-func pol3 -n ttbar_lep_20190707
python NNPDFRatios.py -x res_mass -var --bin-width -c bb   -mc ttbar_lep --fmax 4250 --fit-func pol3 -n ttbar_lep_20190707
python NNPDFRatios.py -x res_mass -var --bin-width -c beee -mc ttbar_lep --fmax 4250 --fit-func pol3 -n ttbar_lep_20190707

#python NNPDFRatios.py -x lead_pt --nbinsx 24 --xmin 30 --xmax 150 --fmin 30 --fmax 150 -c all  -s "res_mass>60 && res_mass<120" --fit-func pol6 -n zpeak_20190704
#python NNPDFRatios.py -x lead_pt --nbinsx 24 --xmin 30 --xmax 150 --fmin 30 --fmax 150 -c acc  -s "res_mass>60 && res_mass<120" --fit-func pol6 -n zpeak_20190704
#python NNPDFRatios.py -x lead_pt --nbinsx 24 --xmin 30 --xmax 150 --fmin 30 --fmax 150 -c bb   -s "res_mass>60 && res_mass<120" --fit-func pol6 -n zpeak_20190704
#python NNPDFRatios.py -x lead_pt --nbinsx 24 --xmin 30 --xmax 150 --fmin 30 --fmax 150 -c beee -s "res_mass>60 && res_mass<120" --fit-func pol6 -n zpeak_20190704
#python NNPDFRatios.py -x lead_pt -var --bin-width --fmin 30 --fmax 200 -c all  -s "res_mass>60 && res_mass<200" --fit-func pol6 -n 60m200_20190704
#python NNPDFRatios.py -x lead_pt -var --bin-width --fmin 30 --fmax 600 -c acc  -s "res_mass>60 && res_mass<200" --fit-func pol4 -n 60m200_20190704
#python NNPDFRatios.py -x lead_pt -var --bin-width --fmin 30 --fmax 600 -c bb   -s "res_mass>60 && res_mass<200" --fit-func pol4 -n 60m200_20190704
#python NNPDFRatios.py -x lead_pt -var --bin-width --fmin 30 --fmax 600 -c beee -s "res_mass>60 && res_mass<200" --fit-func pol4 -n 60m200_20190704
