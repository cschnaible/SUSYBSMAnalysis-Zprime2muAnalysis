import copy
from FWCore.PythonUtilities.LumiList import LumiList

def for_cmssw(ll):
    return ll.getCMSSWString().split(',')

# These run numbers guide the combination of the prompt and DCS-only
# JSONs.
first_run = 314472 #first DCS run or first analyzed run
last_rereco_run = 325175
last_prompt_run = 325175
last_run = 325175 #last DCS run or last analyzed run

# Sometimes the same run-range json gets made in other versions.
prompt_version = ''

# Lumis to manually throw out.
to_remove = {}
to_remove = LumiList(compactList=to_remove)

# These runs are <= last_prompt_run, but they were not actually
# considered in the certification for the latest prompt JSON. So,
# don't drop them from the DCS-only list when combining later.
holes = []

# Order of priorities: rereco, then prompt reco, and then DCS.
runs_to_remove_from_prompt  = range(first_run, last_rereco_run+1)
runs_to_remove_from_dcsonly = range(first_run, last_prompt_run+1)
for hole in holes:
    print 'goodlumis warning: re-adding "hole" run %i from DCS-only list' % hole
    runs_to_remove_from_dcsonly.remove(hole)

# 2016
ReRecoMuonsOnly16_ll = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON_MuonPhys.txt')

# 2017
ReRecoMuonsOnly17_ll = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_MuonPhys.txt')

# 2018
ReRecoMuonsOnly18_ll = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON_MuonPhys.txt')


def combine(prompt_ll, rereco1_ll, rereco2_ll, rereco3_ll, dcsonly_ll=None):
    prompt_ll = copy.deepcopy(prompt_ll)
    prompt_ll.removeRuns(runs_to_remove_from_prompt)
    ll = prompt_ll | rereco1_ll | rereco2_ll | rereco3_ll
    if dcsonly_ll is not None:
        dcsonly_ll = copy.deepcopy(dcsonly_ll)
        dcsonly_ll.removeRuns(runs_to_remove_from_dcsonly)
        ll = ll | dcsonly_ll
    return ll

# Combine all lists
Run2018MuonsOnly_ll = ReRecoMuonsOnly18_ll
Run2017MuonsOnly_ll = ReRecoMuonsOnly17_ll
Run2016MuonsOnly_ll = ReRecoMuonsOnly16_ll
all_ll_names = ['Run2018MuonsOnly','Run2017MuonsOnly','Run2016MuonsOnly']

def all_lls():
    return [(x, eval(x + '_ll')) for x in all_ll_names]

for base_name, ll in all_lls():
    exec '%s_ll = ll - to_remove' % base_name
    exec '%s = for_cmssw(%s_ll)' % (base_name, base_name)

if __name__ == '__main__':
    import sys
    if 'write' in sys.argv:
        Run2018MuonsOnly_ll.writeJSON('Run2018MuonsOnly.json')
        #Run2018_ll.writeJSON('Run2018.json')
    elif 'write_all' in sys.argv:
        for base_name, ll in all_lls():
            ll.writeJSON('zp2mu_goodlumis_%s.json' % base_name)
