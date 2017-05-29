import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('HLTPhase2Upgrade',eras.Phase2C2)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometryExtended2023D4Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('HLTrigger.Configuration.HLT_phaseIIbasic_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    fileNames = cms.untracked.vstring(
        '/store/mc/PhaseIISpring17D/TT_TuneCUETP8M1_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/NoPU_pilot_90X_upgrade2023_realistic_v9-v1/50000/1E42323E-4024-E711-B4A6-0025905B859E.root',
        '/store/mc/PhaseIISpring17D/TT_TuneCUETP8M1_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/NoPU_pilot_90X_upgrade2023_realistic_v9-v1/50000/1EF8E786-4024-E711-B8A3-0025904C7F5E.root',
        '/store/mc/PhaseIISpring17D/TT_TuneCUETP8M1_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/NoPU_pilot_90X_upgrade2023_realistic_v9-v1/50000/422F46CA-D523-E711-BE82-A0000420FE80.root',
        '/store/mc/PhaseIISpring17D/TT_TuneCUETP8M1_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/NoPU_pilot_90X_upgrade2023_realistic_v9-v1/50000/8C786BBA-4024-E711-8562-549F3525CD78.root',
        '/store/mc/PhaseIISpring17D/TT_TuneCUETP8M1_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/NoPU_pilot_90X_upgrade2023_realistic_v9-v1/50000/96D498CD-E023-E711-B301-0CC47A7E6A2C.root',
        '/store/mc/PhaseIISpring17D/TT_TuneCUETP8M1_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/NoPU_pilot_90X_upgrade2023_realistic_v9-v1/50000/A2F37ACE-DC23-E711-9927-0242AC130004.root',
        '/store/mc/PhaseIISpring17D/TT_TuneCUETP8M1_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/NoPU_pilot_90X_upgrade2023_realistic_v9-v1/50000/B4B4B551-DD23-E711-A566-00259029E87C.root',
        '/store/mc/PhaseIISpring17D/TT_TuneCUETP8M1_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/NoPU_pilot_90X_upgrade2023_realistic_v9-v1/50000/CE984B0B-EA23-E711-BFB8-24BE05C60802.root',
        '/store/mc/PhaseIISpring17D/TT_TuneCUETP8M1_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/NoPU_pilot_90X_upgrade2023_realistic_v9-v1/50000/E02EA977-4024-E711-AB5E-F02FA768CFD2.root',
        '/store/mc/PhaseIISpring17D/TT_TuneCUETP8M1_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/NoPU_pilot_90X_upgrade2023_realistic_v9-v1/50000/E2F16F19-4024-E711-887D-008CFAF2224C.root'
        ),
    #fileNames = cms.untracked.vstring('file:step2.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Additional definitions

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '90X_upgrade2023_realistic_v9', '')

from HLTrigger.Phase2.customiseForPhase2 import customiseTrigger,customiseRelValStep2 

process = customiseTrigger(process)
process = customiseRelValStep2(process)

# Schedule definition
process.schedule = process.HLTSchedule
process.schedule.extend([process.hltValidationPhase2, process.DQMoutput])
#process.schedule.extend([process.EDMoutput])

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
