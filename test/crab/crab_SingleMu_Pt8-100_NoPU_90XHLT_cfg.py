from WMCore.Configuration import Configuration
config = Configuration()

sample  = "SingleMu_Pt-8to100_NoPU"
version = "v1"

config.section_('General')
config.General.transferLogs = True
config.General.transferOutputs = True
config.General.requestName = sample + '_Phase2_HLT_Validation_' + version

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName    = 'step2_crab_HLT_Validation.py'
config.JobType.outputFiles = ['step2_inDQM.root']

#config.JobType.allowUndistributedCMSSW = True  # To fix cmssw releases

config.section_('Data')

config.Data.inputDataset = '/SingleMu_FlatPt-8to100/PhaseIISpring17D-NoPU_90X_upgrade2023_realistic_v9-v1/GEN-SIM-DIGI-RAW'

config.Data.splitting      = 'FileBased'
config.Data.unitsPerJob    = 1  # Since files based, 10 files per job
config.Data.totalUnits     = 100000
config.Data.inputDBS       = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader/'
config.Data.outLFNDirBase  = '/store/user/battilan/HLTPhase2/prova/'

config.Data.publication = False

config.section_('Site')
config.Site.storageSite = 'T3_IT_Bologna'
#config.Site.whitelist = ["T3_IT_Bologna"]
