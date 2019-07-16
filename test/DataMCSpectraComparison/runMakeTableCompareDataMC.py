import os
import argparse 
parser = argparse.ArgumentParser()
parser.add_argument('-w','--where',default='test',help='Where to save')
args = parser.parse_args()

where = args.where

os.system('cp ~/public/index.php '+where+'/')

bins = [ [60,120], [120,400],[400,600],[600,900],[900,1300],[1300,1800],[1800,4000] ]
#bins = [ [60,120] ]
years = ['run2','2018','2017','2016']
cats = ['all','bb','beee']

#cmd_tmp = 'python CompareDataMC.py -d our -x vertex_m -s "vertex_m>60" -c {cat} --do-smear --nnpdf30 --order nnlo --do-fake-rate -ly --do-stack --do-paper --nbinsx {nbinsx} --xmin {xlow} --xmax {xhigh} -w {where} {overflow} -y {year} -n mass_{year}_{cat}_nnpdf30_nnlo_{xlow}_{xhigh} --do-uncert'
cmd_tmp = 'python CompareDataMC.py -d {tdir} -x vertex_m -s "vertex_m>50" -c {cat} --nnpdf30 --order nnlo {dojets} -ly --do-stack --do-paper --nbinsx {nbinsx} --xmin {xlow} --xmax {xhigh} -w {where} {overflow} -y {year} -n mass_{year}_{cat}_nnpdf30_nnlo_{xlow}_{xhigh} --do-uncert {scaleZ0} {prescale}'

for year in years:
    for cat in cats:
        for xlow,xhigh in bins:
            overflow = '--overflow' if xlow==1800 else ''
            dojets = '--do-fake-rate' if xlow>60 else ''
            scaleZ0 = '--scaleZ0' if xlow>60 else ''
            prescale = '--prescale-weight mc' if xlow<120 else ''
            tdir = 'our' if xlow>60 else 'ourcommonpre'
            nbinsx = xhigh-xlow
            print year,cat,xlow,xhigh
            cmd = cmd_tmp.format(**locals())
            print cmd
            os.system(cmd)

