f2016 = open('lists/data_Run2016_All_07Aug2017_list.txt')
f2017 = open('lists/data_Run2017_All_17Nov2017_list.txt')
f2018 = open('lists/data_Run2018_All_PromptReco_list.txt')

n2016 = 0.
for line in f2016:
    cols = line.strip('\n').split()
    mass = float(cols[0])
    if mass >= 60. and mass <= 120:
        n2016 += 1

n2017 = 0.
for line in f2017:
    cols = line.strip('\n').split()
    mass = float(cols[0])
    if mass >= 60. and mass <= 120:
        n2017 += 1

n2018 = 0.
for line in f2018:
    cols = line.strip('\n').split()
    mass = float(cols[0])
    if mass >= 60. and mass <= 120:
        n2018 += 1


print n2016,n2018/n2016
print n2017,n2018/n2017
