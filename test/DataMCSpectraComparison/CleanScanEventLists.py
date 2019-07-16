import os
#edir = 'www_preapp_lists/'
edir = 'for_jan/'
#years = ['2018','2017']
years = ['2016']#,'2017']
cats = ['all']#,'bb','beee']
for year in years:
    for cat in cats:
        with open(edir+'event_list_'+year+'_'+cat+'_scan.txt') as scanFile:
            lines = scanFile.read().splitlines()
        print len(lines)
        print lines[0]
        print lines[-1]
        #print lines[5].split()[3]
        #cleanLines = [l.split()[3] for l in lines[3:-1] if '***' not in l or 'Row' not in l]
        #print lines[0]
        cleanLines = ['\t'.join([x for x in l.split()[2:] if x!='*']) for l in lines if '***' not in l or 'Row' not in l]
        #print cleanLines[0]
        print len(cleanLines)
        print cleanLines[0]
        print cleanLines[-1]
        name = edir+'event_list_'+year+'_'+cat
        open(name+'_clean.txt','wt').write('\n'.join(cleanLines))
        os.system('sort -n -r -k 4 '+name+'_clean.txt > '+name+'_clean_sort.txt')


