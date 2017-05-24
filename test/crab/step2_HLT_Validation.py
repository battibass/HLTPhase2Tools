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
    fileNames = cms.untracked.vstring('file:step2.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2_crab nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition
#
#process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
#    dataset = cms.untracked.PSet(
#        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW'),
#        filterName = cms.untracked.string('')
#    ),
#    eventAutoFlushCompressedSize = cms.untracked.int32(10485760),
#    fileName = cms.untracked.string('file:test.root'),
#    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
#    splitLevel = cms.untracked.int32(0)
#)

# Additional output definition

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '90X_upgrade2023_realistic_v9', '')

from HLTrigger.Phase2.customiseForPhase2 import customiseTrigger,customiseRelValStep2 

process = customiseTrigger(process)
process = customiseRelValStep2(process)

# Schedule definition
process.schedule = process.HLTSchedule
process.schedule.extend([process.hltValidationPhase2, process.DQMoutput])

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
