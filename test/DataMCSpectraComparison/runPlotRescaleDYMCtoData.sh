#!/bin/bash

#python PlotRescaleDYMCtoData.py -d ourcommonpre --do-stack --rescale-hists ourcommonpre --rescale-by gen_dil_rap --rescale-to 80X -ly -y 2017 -n ourcommonpre --overflow &
#python PlotRescaleDYMCtoData.py -d ourcommonpre --do-stack --rescale-hists ourcommonpre --rescale-by gen_dil_pt --rescale-to 80X -ly -y 2017 -n ourcommonpre --overflow &
#python PlotRescaleDYMCtoData.py -d ourcommonpre --do-stack --rescale-hists ourcommonpre --rescale-by gen_lead_pt --rescale-to 80X -ly -y 2017 -n ourcommonpre  --overflow

python PlotRescaleDYMCtoData.py -d ourcommonpre --do-stack --rescale-hists ourcommonpre --rescale-by gen_dil_rap --rescale-to 80X -ly -y 2018 -n ourcommonpre  --overflow &
#python PlotRescaleDYMCtoData.py -d ourcommonpre --do-stack --rescale-hists ourcommonpre --rescale-by gen_dil_pt --rescale-to 80X -ly -y 2018 -n ourcommonpre --overflow &
#python PlotRescaleDYMCtoData.py -d ourcommonpre --do-stack --rescale-hists ourcommonpre --rescale-by gen_lead_pt --rescale-to 80X -ly -y 2018 -n ourcommonpre  --overflow &

