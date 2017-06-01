import FWCore.ParameterSet.Config as cms

import HLTrigger.Phase2.customiseMuonsForPhase2      as muons
import HLTrigger.Phase2.customiseTrackingForPhase2   as tracking
import HLTrigger.Phase2.customiseValidationForPhase2 as val

def customiseTrigger(process):

    # process = customiseL1Seeds(process)
    process = muons.useRpcSimDigis(process)
    process = muons.addGemsToL2(process)
    process = tracking.customiseTracking(process)
    # process = muons.removeHLTIsoMu24Steps(process)
    # process = muons.removeHLTIsoTkMu24Steps(process)
    # process = muons.removeHLTMu50Steps(process)
    process = customiseEventContent(process)
    process = addTrigReport(process)

    return process

def customiseRelVal(process):

    process = val.customiseMuonRelVal(process)
    process = val.customiseJetMETRelVal(process)

    return process

def customiseRelValStep2(process):

    process = val.customiseRelValStep2(process)

    return process

def customiseRelValStep2Harvesting(process):

    process = val.customiseRelValStep2Harvesting(process)

    return process


def addTrigReport(process):
    # enable TrigReport, TimeReport and MultiThreading

    print "[addTrigReport] Adding report printout and set # threads to 1"

    process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool( True ),
        numberOfThreads = cms.untracked.uint32( 1 ),
        numberOfStreams = cms.untracked.uint32( 0 ),
        sizeOfStackForThreadsInKB = cms.untracked.uint32( 10*1024 )
        )

    return process

def addEdmOutput(process,outputCommands,fileName):

    print "[addEdmReport] Adding EDM output module with given outputCommands definition"

    process.EDMoutput = cms.OutputModule("PoolOutputModule",
                                         dataset = cms.untracked.PSet( dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW'),
                                                                       filterName = cms.untracked.string('')
                                                                       ),
                                         eventAutoFlushCompressedSize = cms.untracked.int32(10485760),
                                         fileName = cms.untracked.string('file:'+fileName),
                                         outputCommands = outputCommands,
                                         splitLevel = cms.untracked.int32(0)
                                         )
    return process

def addMemoryCheck(process):

    print "[addMemoryCheck] Adding SimpleMemoryCheck service"

    process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",
                                            ignoreTotal = cms.untracked.int32(-1)
                                            )

    return process

def customiseEventContent(process):

    if hasattr(process,"FEVTDEBUGHLToutput") :
        print "[customiseEventContent] Customise event content to keep hltIter* "
        process.FEVTDEBUGHLToutput.outputCommands.append('keep *_hltIter*_*_HLT')
        process.FEVTDEBUGHLToutput.outputCommands.append('keep *_MuonsIter*_*_HLT')
        process.FEVTDEBUGHLToutput.outputCommands.append('keep Phase2TrackerCluster1D*_*_*_HLT')
        
    return process


# Keeping this for debugging 
def customiseL1Seeds( process):
   
    if hasattr(process,"HLT_IsoMu24_v4") :
        print "[customiseL1Seeds] Add cms.Ignore() to IsoMu24 L1 related filters"

        process.HLT_IsoMu24_v4.replace(process.hltL1sSingleMu22, \
                                       cms.ignore(process.hltL1sSingleMu22))
        process.HLT_IsoMu24_v4.replace(process.hltL1fL1sMu22L1Filtered0, \
                                       cms.ignore(process.hltL1fL1sMu22L1Filtered0))

    if hasattr(process,"HLT_IsoTkMu24_v4") :
        print "[customiseL1Seeds] Add cms.Ignore() to IsoTkMu24 L1 related filters"

        process.HLT_IsoTkMu24_v4.replace(process.hltL1sSingleMu22, \
                                         cms.ignore(process.hltL1sSingleMu22))
        process.HLT_IsoTkMu24_v4.replace(process.hltL1fL1sMu22L1Filtered0, \
                                         cms.ignore(process.hltL1fL1sMu22L1Filtered0))
        
    if hasattr(process,"HLT_IsoMu50_v5") :
        print "[customiseL1Seeds] Add cms.Ignore() to Mu50 L1 related filters"
        process.HLT_IsoTkMu50_v5.replace(process.hltL1sV0SingleMu22IorSingleMu25, \
                                         cms.ignore(process.hltL1sV0SingleMu22IorSingleMu25))
        process.HLT_IsoTkMu50_v5.replace(process.hltL1fL1sMu22Or25L1Filtered0, \
                                         cms.ignore(process.hltL1fL1sMu22Or25L1Filtered0))

    return process


        
