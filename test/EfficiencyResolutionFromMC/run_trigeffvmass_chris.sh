#!/bin/bash
date=20190506

# 2018
#python trigeffvmass_chris.py -d www_eff  -o mc_2018_${date} -w Our2018OppSignEfficiency    --individual-plots --individual-effs | tee www_eff/effs_mc_2018_${date}.txt
python trigeffvmass_chris.py -d www_effZ -o mc_2018_${date} -w Our2018AtZOppSignEfficiency --individual-plots --individual-effs | tee www_effZ/effs_mc_2018_${date}.txt
cp ~/public/index.php www_eff/mc_2018_${date}

# 2017
#python trigeffvmass_chris.py -mc mc_2017 -d www_eff  -o mc_2017_${date} -w Our2018OppSignEfficiency    --individual-plots --individual-effs | tee www_eff/effs_mc_2017_${date}.txt
python trigeffvmass_chris.py -mc mc_2017 -d www_effZ -o mc_2017_${date} -w Our2018AtZOppSignEfficiency --individual-plots --individual-effs | tee www_effZ/effs_mc_2017_${date}.txt
cp ~/public/index.php www_eff/mc_2017_${date}

# 2016
#python trigeffvmass_chris.py -mc mc_2016 -d www_eff  -o mc_2016_${date} -w Our2016OppSignEfficiency --individual-plots --individual-effs | tee www_eff/effs_mc_2016_${date}.txt
#python trigeffvmass_chris.py -mc mc_2016 -d www_effZ -o mc_2016_${date} -w Our2016AtZOppSignEfficiency --individual-plots --individual-effs | tee www_effZ/effs_mc_2016_${date}.txt
cp ~/public/index.php www_eff/mc_2016_${date}
