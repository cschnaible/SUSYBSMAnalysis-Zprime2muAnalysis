
dy_nnpdf_func = '(({a}) + ({b})*pow(gen_dil_mass,1) + ({c})*pow(gen_dil_mass,2) + ({d})*pow(gen_dil_mass,3) + ({e})*pow(gen_dil_mass,4) + ({f})*pow(gen_dil_mass,5))'
WW_nnpdf_func = '(({a}) + ({b})*pow(gen_dil_mass,1) + ({c})*pow(gen_dil_mass,2) + ({d})*pow(gen_dil_mass,3) + ({e})*pow(gen_dil_mass,4))'
ttbar_nnpdf_func = '((gen_dil_mass<120)*1. + (gen_dil_mass>120 && gen_dil_mass<3000)*(({a}) + ({b})*pow(gen_dil_mass,1) + ({c})*pow(gen_dil_mass,2) + ({d})*pow(gen_dil_mass,3)) + (gen_dil_mass>3000)*(0.436005))'
zpeak_nnpdf_func = '((gen_lead_pt<30)*0.9 + (gen_lead_pt>30 && gen_lead_pt<100)*(({a}) + ({b})*pow(gen_lead_pt,1) + ({c})*pow(gen_lead_pt,2) + ({d})*pow(gen_lead_pt,3) + ({e})*pow(gen_lead_pt,4) + ({f})*pow(gen_lead_pt,5)) + (gen_lead_pt>100)*({g}))'
toNNPDF30 = {
        2017:{
            'our':{
                'powheg':{
                    #'all':dy_nnpdf_func.format(a='0.9292',b='+ 5.486E-5',c='+ 6.572E-9',d='- 1.142E-11',e='+ 4.876E-15',f='- 4.117E-19'),
                    'all': dy_nnpdf_func.format(a='0.918129',b='6.92702e-05',c='1.62175e-08',d='-2.47833e-11',e='8.75707e-15',f='-7.53019e-19'),
                    'bb':  dy_nnpdf_func.format(a='0.914053',b='7.91618e-05',c='2.19722e-08',d='-3.49212e-11',e='1.22504e-14',f='-1.07347e-18'),
                    'beee':dy_nnpdf_func.format(a='0.933214',b='3.76813e-05',c='1.95612e-08',d='-1.2688e-11', e='3.69867e-15',f='-2.62212e-19'),
                    'ee':  dy_nnpdf_func.format(a='0.952255',b='-7.67452e-05',c='1.69935e-07',d='-9.44719e-11',e='2.28419e-14',f='-1.72926e-18'),
                    },
                'ttbar':{ # same for both 2017 and 2018
                    #'all':  ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                    #'bb':   ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                    #'beee': ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                    #'all':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                    #'bb':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                    #'beee':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                    'all': ttbar_nnpdf_func.format(a='0.994078695151',b='2.64819793287e-05',c='-3.73996461024e-08',d='-1.11452866827e-11'),
                    'bb': ttbar_nnpdf_func.format(a='0.994078695151',b='2.64819793287e-05',c='-3.73996461024e-08',d='-1.11452866827e-11'),
                    'beee': ttbar_nnpdf_func.format(a='0.994078695151',b='2.64819793287e-05',c='-3.73996461024e-08',d='-1.11452866827e-11'),
                    },
                #'diboson':{
                #    'all':'(1.)',
                #    'bb':'(1.)',
                #    'beee':WW_nnpdf_func.format(a='1.0031',b='-6.30717e-05',c='-3.14538e-08',d='2.68999e-11',e='-5.66054e-15'),
                #    },
                },
            'ourcommonpre':{
                'powheg':{
                    'all':zpeak_nnpdf_func.format(a='1.8245728118',b='-0.0537728412909',c='0.000731365981935',d='7.16669312495e-06',e='-1.99723894101e-07',f='1.0112316789e-09',g='1.01849023288'),
                    'bb': zpeak_nnpdf_func.format(a='1.91383074609',b='-0.0596201865777',c='0.000811074027001',d='7.90677720686e-06',e='-2.21489848717e-07',f='1.12700571973e-09',g='1.00484010198'),
                    'beee':zpeak_nnpdf_func.format(a='1.71913319508',b='-0.0481243962238',c='0.000666286154366',d='6.45776405133e-06',e='-1.82202504311e-07',f='9.24567381899e-10',g='1.02790393101'),
                    },
                },
            },
        2018:{
            'our':{
                'powheg':{
                    'all': dy_nnpdf_func.format(a='0.919027',b='5.98337e-05', c='2.56077e-08', d='-2.82876e-11',e='9.2782e-15', f='-7.77529e-19'),
                    'bb':  dy_nnpdf_func.format(a='0.911563',b='0.000113313', c='-2.35833e-08',d='-1.44584e-11',e='8.41748e-15',f='-8.16574e-19'),
                    'beee':dy_nnpdf_func.format(a='0.934502',b='2.21259e-05', c='4.14656e-08', d='-2.26011e-11',e='5.58804e-15',f='-3.92687e-19'),
                    'ee':  dy_nnpdf_func.format(a='0.954175',b='-9.68066e-05',c='2.09278e-07', d='-1.15712e-10',e='2.77047e-14',f='-2.11731e-18'),
                    },
                'ttbar':{ # same for both 2017 and 2018
                    #'all':  ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                    #'bb':   ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                    #'beee': ttbar_nnpdf_func.format(a='0.991403',b='3.05593e-05',c='-2.21967e-07',d='6.63658e-11'),
                    #'all':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                    #'bb':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                    #'beee':  ttbar_nnpdf_func.format(a='0.990845504142',b='2.20626340524e-05',c='-2.28996426677e-07',d='5.41247595873e-11'),
                    'all': ttbar_nnpdf_func.format(a='0.994078695151',b='2.64819793287e-05',c='-3.73996461024e-08',d='-1.11452866827e-11'),
                    'bb': ttbar_nnpdf_func.format(a='0.994078695151',b='2.64819793287e-05',c='-3.73996461024e-08',d='-1.11452866827e-11'),
                    'beee': ttbar_nnpdf_func.format(a='0.994078695151',b='2.64819793287e-05',c='-3.73996461024e-08',d='-1.11452866827e-11'),
                    },
                },
            'ourcommonpre':{
                'powheg':{
                    'all':zpeak_nnpdf_func.format(a='1.69147781688',b='-0.0473286496053',c='0.000661599919558',d='6.33324308996e-06',e='-1.80459280586e-07',f='9.19632449685e-10',g='1.02344217328'),
                    'bb': zpeak_nnpdf_func.format(a='1.65477513925',b='-0.0472097707001',c='0.000681831627146',d='6.15645344304e-06',e='-1.82810037593e-07',f='9.43667804224e-10',g='1.01489199674'),
                    'beee':zpeak_nnpdf_func.format(a='1.60977951604',b='-0.0426122819079',c='0.000599273084801',d='5.88395881526e-06',e='-1.66414436738e-07',f='8.4690800397e-10',g='1.02846360871'),
                    },
                },
            },
        }

#pi_func =  '({a} {b}*pow(gen_dil_mass,1) {c}*pow(gen_dil_mass,2) {d}*pow(gen_dil_mass,3))'.format(a='1.067',b='- 0.000112',c='+ 3.176e-8',d='- 4.068e-12')
#k_func_high = '({a} {b}*pow(gen_dil_mass-400.0,1) {c}*pow(gen_dil_mass-400.0,2) {d}*pow(gen_dil_mass-400.0,3))'
#k_func_low  = '({a} {b}*pow(gen_dil_mass-130.0,1) {c}*pow(gen_dil_mass-130.0,2) {d}*pow(gen_dil_mass-130.0,3))'
kfunc = '(({a}) + ({b})*pow(gen_res_mass,1) + ({c})*pow(gen_res_mass,2) + ({d})*pow(gen_res_mass,3))'
kFunction = {
        'our':{ # m > 150 GeV
            'all' :kfunc.format(a='1.053',b='-0.0001552',c='5.661e-08',d='-8.382e-12'),
            'bb'  :kfunc.format(a='1.032',b='-0.000138', c='4.827e-08',d='-7.321e-12'),
            'beee':kfunc.format(a='1.064',b='-0.0001674',c='6.599e-08',d='-9.657e-12'),
            },
        #'our':{ # pt > 53 GeV and m > 120
        #    #'all': k_func_high.format(a='1.067',b='- 0.000112',c='+ 3.176e-8',d='- 4.068e-12'),
        #    'all': k_func_high.format(a='1.047',b='- 0.000143', c='+ 5.167e-8',d='- 7.84e-12'),
        #    'bb' : k_func_high.format(a='1.036',b='- 0.0001441',c='+ 5.068e-8',d='- 7.581e-12'),
        #    'beee':k_func_high.format(a='1.052',b='- 0.0001471',c='+ 5.903e-8',d='- 9.037e-12'),
        #    },
        #'ourpre':{ # pt > 30 and m < 170
        #    'all': k_func_low.format(a='1.067',b='- 0.000112',c='+ 3.176e-8',d='- 4.068e-12'),
        #    'bb' : k_func_low.format(a='1.036',b='- 0.0001441',c='+ 5.058e-8',d='- 7.581e-12'),
        #    'beee':k_func_low.format(a='1.052',b='- 0.0001471',c='+ 5.903e-8',d='- 9.037e-12'),
        #    },
        #'ourcommonpre':{
        #    'all': k_func_high.format(a='1.067',b='- 0.000112',c='+ 3.176e-8',d='- 4.068e-12'),
        #    'bb' : k_func_high.format(a='1.036',b='- 0.0001441',c='+ 5.058e-8',d='- 7.581e-12'),
        #    'beee':k_func_high.format(a='1.052',b='- 0.0001471',c='+ 5.903e-8',d='- 9.037e-12'),
        #    },
        }
cats = {
        'all':'(1.)',
        'bb':'(fabs(lep_eta[0])<=1.2 && fabs(lep_eta[1])<=1.2)',
        'beee':'(fabs(lep_eta[0])>1.2 || fabs(lep_eta[1])>1.2)',
        'ee':'(fabs(lep_eta[0])>1.2 && fabs(lep_eta[1])>1.2)',
        'b':'(fabs(lep_eta)<1.2)',
        'e':'(fabs(lep_eta)>1.2 && fabs(lep_eta)<2.4)',
        }

gRand = 'sin(2.0*pi*rndm)*sqrt(-2.0*log(rndm))'
smear = {
        # 10% for bb 20% for beee
        2016:{'bb':'sqrt(pow(1.10,2)-1)','beee':'sqrt(pow(1.20,2)-1)'},
        # no smearing for bb 15% for beee
        2017:{'bb':'sqrt(pow(1.0,2)-1)','beee':'sqrt(pow(1.15,2)-1)'},
        2018:{'bb':'sqrt(pow(1.0,2)-1)','beee':'sqrt(pow(1.15,2)-1)'},
        }
# Smear mass = reco mass + reco mass * rand->gaus(0,res(gen mass)*extraSmear)
resFunc = '({a} + ({b})*pow(gen_res_mass,1) + ({c})*pow(gen_res_mass,2) + ({d})*pow(gen_res_mass,3) + ({e})*pow(gen_res_mass,4))'
resMass = {
        2018:{
            'bb':resFunc.format(a='0.00608',b='3.42e-05',c='-1.34e-08',d='2.4e-12',e='-1.5e-16'),
            'beee':resFunc.format(a='0.0135',b='2.83e-05',c='-9.71e-09',d='1.71e-12',e='-1.09e-16'),
            },
        2017:{
            'bb':resFunc.format(a='0.00606',b='3.41e-05',c='-1.33e-08',d='2.39e-12',e='-1.5e-16'),
            'beee':resFunc.format(a='0.0108',b='3.25e-05',c='-1.18e-08',d='2.11e-12',e='-1.35e-16'),
            },
        2016:{
            'bb':resFunc.format(a='0.00701',b='3.32e-05',c='-1.29e-08',d='2.73e-12',e='-2.05e-16'),
            'beee':resFunc.format(a='0.0124',b='3.75e-05',c='-1.52e-08',d='3.44e-12',e='-2.85e-16'),
            },
        }


print '*'*15
print '\n','TTree Alias'
print 'gen_lead_pt','(gen_lep_pt[0]*(gen_lep_pt[0]>gen_lep_pt[1]) + gen_lep_pt[1]*(gen_lep_pt[1]>gen_lep_pt[0]))'
print '\n','*'*15,'\n'
for year in [2017,2018]:
    for cat in ['all','bb','beee']:
        print year,cat
        print 
        print
        print 'NNLO k-function'
        print kFunction['our'][cat]
        print
        print 'm > 120 DY NNPDF3.0 Scaling'
        print toNNPDF30[year]['our']['powheg'][cat]
        print
        print '60 < m < 120 DY NNPDF3.0 Scaling'
        print toNNPDF30[year]['ourcommonpre']['powheg'][cat]
        print
        print 'm > 120 ttbar'
        print toNNPDF30[year]['our']['ttbar'][cat]
        print
        print 'Mass Smearing'
        print 
        if cat=='all':
            drawThis = 'vertex_m + vertex_m*'+gRand+'*('+\
                    cats['bb']  +'*'+smear[year]['bb']  +'*'+resMass[year]['bb']+' + '+\
                    cats['beee']+'*'+smear[year]['beee']+'*'+resMass[year]['beee']+')'
        elif cat=='bb':
            drawThis = 'vertex_m + vertex_m*'+gRand+'*'+smear[year]['bb']+'*'+resMass[year]['bb']
        elif cat=='beee':
            drawThis = 'vertex_m + vertex_m*'+gRand+'*'+smear[year]['beee']+'*'+resMass[year]['beee']
        print drawThis
        print
        print '*'*15

