#!/bin/bash
python trigeffvmass_chris.py -d www_eff --individual-plots --individual-effs | tee www_eff/effs.txt
python trigeffvmass_chris.py -d www_effZ -w Our2018AtZOppSignEfficiency --individual-plots --individual-effs | tee www_effZ/effs.txt

cp ~/public/index.php www_eff/
cp trigeffvmass_chris.py www_eff/
cp run_trigeffvmass_chris.sh www_eff/
cp ~/public/index.php www_effZ/
cp trigeffvmass_chris.py www_effZ/
cp run_trigeffvmass_chris.sh www_effZ/
