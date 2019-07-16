#!/bin/bash

python acc_eff_parametrization.py -y 2018 -s ourZ
python acc_eff_parametrization.py -y 2018 --binning fixed -s ourZ
python acc_eff_parametrization.py -y 2018 --binning big -s ourZ

python acc_eff_parametrization.py -y 2017 -s ourZ
python acc_eff_parametrization.py -y 2017 --binning fixed -s ourZ
python acc_eff_parametrization.py -y 2017 --binning big -s ourZ

python acc_eff_parametrization.py -y 2016 -s ourZ
python acc_eff_parametrization.py -y 2016 --binning fixed -s ourZ
python acc_eff_parametrization.py -y 2016 --binning big -s ourZ
