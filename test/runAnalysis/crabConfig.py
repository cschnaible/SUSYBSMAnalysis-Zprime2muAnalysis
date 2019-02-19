
from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'dileptonAna_muons_2016_CITo2Mu_Lam16TeVDesLL_M300'
config.General.workArea = 'crab2'
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'cmssw_cfg.py'   
config.Data.inputDataset =  '/CITo2Mu_M300_CUETP8M1_Lam16TeVDesLL_13TeV_Pythia8_Corrected-v4/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.publication = False
config.Data.outputDatasetTag = 'dileptonAna_muons_2016_CITo2Mu_Lam16TeVDesLL_M300'
config.Data.outLFNDirBase = '/store/user/jschulte'
#config.Data.ignoreLocality = True
#config.General.instance = 'preprod' 
#config.Site.whitelist = ["T2_IT_Bari"]
config.Site.storageSite = 'T2_US_Purdue'
config.JobType.maxMemoryMB  = 8000

config.Data.splitting = 'EventAwareLumiBased'
config.Data.totalUnits = -1
config.Data.unitsPerJob  = 500000
