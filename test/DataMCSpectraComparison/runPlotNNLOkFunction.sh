#!/bin/bash

#python PlotNNLOkFunction.py -c all -s high -n kFunc_high_all_logx --logx --fmin 120 --fmax 6000
#python PlotNNLOkFunction.py -c bb -s high -n kFunc_high_bb_logx --logx --fmin 120 --fmax 6000
#python PlotNNLOkFunction.py -c beee -s high -n kFunc_high_beee_logx --logx --fmin 120 --fmax 6000

#python PlotNNLOkFunction.py -c all -s low -n kFunc_low_all_logx --logx --fmin 60 --fmax 6000
#python PlotNNLOkFunction.py -c bb -s low -n kFunc_low_bb_logx --logx --fmin 60 --fmax 170
#python PlotNNLOkFunction.py -c beee -s low -n kFunc_low_beee_logx --logx --fmin 60 --fmax 170

#python PlotNNLOkFunction.py -c all -s low -n kFunc_low_all_logx --logx --fmin 60 --fmax 6000
python PlotNNLOkFunction.py -c bb -s low -n kFunc_low_bb --fmin 60 --fmax 170
python PlotNNLOkFunction.py -c beee -s low -n kFunc_low_beee --fmin 60 --fmax 170
