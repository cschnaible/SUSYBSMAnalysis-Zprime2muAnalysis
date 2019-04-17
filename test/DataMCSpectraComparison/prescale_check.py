prescales = {
# prescale: [lumi,[ a ratio, err],[bb ratio, err],[be ratio, err]]
        14: [  11,[0.9573,0.0490],[0.9484,0.0755],[0.9637,0.0645]],
        35: [  59,[1.0383,0.0344],[0.9934,0.0521],[1.0708,0.0459]],
        40: [  48,[0.9500,0.0391],[0.9486,0.0604],[0.9511,0.0513]],
        70: [1455,[0.9738,0.0096],[0.9639,0.0147],[0.9812,0.0126]],
        100:[7065,[0.9809,0.0052],[0.9807,0.0080],[0.9815,0.0068]],
        120:[ 479,[0.9890,0.0220],[0.9995,0.0342],[0.9822,0.0288]],
        140:[4516,[0.9864,0.0077],[0.9850,0.0118],[0.9883,0.0101]],
        150:[4828,[0.9428,0.0075],[0.9370,0.0116],[0.9479,0.0099]],
        160:[2738,[0.9856,0.0105],[0.9931,0.0163],[0.9811,0.0138]],
        170:[3081,[0.9187,0.0099],[0.9471,0.0155],[0.8993,0.0128]],
        180:[ 518,[1.0002,0.0261],[1.0209,0.0407],[0.9865,0.0340]],
        200:[3719,[0.9327,0.0098],[0.9408,0.0152],[0.9280,0.0128]],
        230:[3299,[0.9479,0.0112],[0.9696,0.0176],[0.9337,0.0146]],
        250:[1010,[0.9510,0.0214],[0.9794,0.0335],[0.9321,0.0277]],
        260:[2345,[0.9447,0.0141],[0.9857,0.0223],[0.9168,0.0183]],
        290:[1828,[0.9481,0.0169],[0.9556,0.0263],[0.9446,0.0222]],
        320:[ 196,[0.9387,0.0540],[0.9145,0.0825],[0.9581,0.0716]],
}


cats = ['a','bb','be']
num = {c:0. for c in cats}
den = {c:0. for c in cats}
prenum = 0.
preden = 0.
lumitot = 0.
for prescale in prescales:
    for i,c in enumerate(cats):
        w = 1./pow(prescales[prescale][i+1][1],2)
        num[c] += prescales[prescale][i+1][0]*w
        den[c] += w
    prenum += prescale*prescales[prescale][0]
    preden += prescales[prescale][0]
    lumitot += prescales[prescale][0]

for c in ['a','bb','be']:
    print c,'avg',num[c]/den[c],'err',pow(den[c],-0.5)
print prenum/preden
print lumitot

#-36295 0.9638 0.002 0.9688 0.0042 0.9610 0.0035
