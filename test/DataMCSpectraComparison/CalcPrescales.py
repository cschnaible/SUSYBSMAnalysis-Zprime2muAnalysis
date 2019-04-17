import os
import Cert_314472_325175_13TeV_PromptReco_Collisions18_JSON_MuonPhys as json

for r,run in enumerate(json.jsonDICT):
    os.system('brilcalc trg --prescale --hltpath HLT_Mu27_v* -r '+run)
    lumis = str(json.jsonDICT[run])
    open('tmp.json','wt').write('{\"'+run+'\":'+lumis+'}')
    os.system('brilcalc lumi --hltpath HLT_Mu27_v* -r '+run+' -i tmp.json -u /nb')
    os.system('brilcalc lumi --hltpath HLT_Mu50_v* -r '+run+' -i tmp.json -u /nb')
    print '*'*30
