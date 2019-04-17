mu50 = open('duplicate_prescales_byls_mu50.lumi')
mu27 = open('duplicate_prescales_byls_mu27.lumi')

mu50lines = mu50.read().split('\n')
mu27lines = mu27.read().split('\n')
if len(mu50lines)!=len(mu27lines): exit()

totals = {
        222:0.,
        296:0.,
        385:0.,
        }

for i in range(0,len(mu50lines)-1):
    if mu50lines[i][0]=='#': continue
    if mu50lines[i][0]=='+': continue
    mu50data = mu50lines[i].replace(' ','').split('|')
    mu27data = mu27lines[i].replace(' ','').split('|')
    if mu50data[1]=='run:fill': continue
    if mu50data[1][0]=='H': continue
    if mu50data[1]!=mu27data[1]: 
        print 'error 1'
        exit()
    if mu50data[2]!=mu27data[2]:
        print 'error 2'
        exit()
    if mu27data[6][0]=='t':continue
    if float(mu27data[6])==0.0: 
        continue
        #print 'bad',mu50data[1],mu50data[2],mu50data[6],mu27data[6]
    else: 
        print mu50data[1],mu50data[2],mu50data[6], mu27data[6], float(mu50data[6])/float(mu27data[6]), int(round(float(mu50data[6])/float(mu27data[6])))
        prescale = int(round(float(mu50data[6])/float(mu27data[6])))
        if prescale in [222,296,385]:
            totals[prescale] += float(mu50data[6])/1000. # convert to pb-1
        else:
            found = False
            for realprescale in [222,296,385]:
                if abs(prescale-realprescale)<5:
                    totals[realprescale] += float(mu50data[6])/1000.
                    found = True
            if not found:
                print mu50data[1],mu50data[2],mu50data[6], mu27data[6], float(mu50data[6])/float(mu27data[6]), int(round(float(mu50data[6])/float(mu27data[6])))

print totals
