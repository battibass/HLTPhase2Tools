import FWCore.ParameterSet.Config as cms

import HLTrigger.Phase2.customiseMuonsForPhase2      as muons
import HLTrigger.Phase2.customiseTrackingForPhase2   as tracking
import HLTrigger.Phase2.customiseValidationForPhase2 as val

def customiseTrigger(process):

    process = muons.useRpcSimDigis(process)
    process = muons.addGemsToL2(process)
    process = tracking.customiseTracking(process)

    process = customiseEventContent(process)
    process = addTrigReport(process)
    #process.Tracer = cms.Service("Tracer")

    return process

def customiseRelVal(process):

    process = val.customiseMuonRelVal(process)
    process = val.customiseJetMETRelVal(process)

    return process

def customiseRelValStep2(process):

    process = val.customiseRelValStep2(process)
    process = addFastTimerService(process)

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

def addFastTimerService(process):

    print "[addMemoryCheck] Adding FastTimer service"

    # remove any instance of the FastTimerService
    if 'FastTimerService' in process.__dict__:
        del process.FastTimerService

    # instrument the menu with the FastTimerService
    process.load( "HLTrigger.Timer.FastTimerService_cfi" )

    # print a text summary at the end of the job
    process.FastTimerService.printEventSummary        = False
    process.FastTimerService.printRunSummary          = False
    process.FastTimerService.printJobSummary          = True

    # enable DQM plots
    process.FastTimerService.enableDQM                = True

    # enable per-module DQM plots
    process.FastTimerService.enableDQMbyModule        = True

    # enable DQM plots vs lumisection
    process.FastTimerService.enableDQMbyLumiSection   = False
    process.FastTimerService.dqmLumiSectionsRange     = 2500    # lumisections (23.31 s)

    # set the time resolution of the DQM plots
    process.FastTimerService.dqmTimeRange             = 1000.   # ms
    process.FastTimerService.dqmTimeResolution        =    5.   # ms
    process.FastTimerService.dqmPathTimeRange         =  100.   # ms
    process.FastTimerService.dqmPathTimeResolution    =    0.5  # ms
    process.FastTimerService.dqmModuleTimeRange       =   40.   # ms
    process.FastTimerService.dqmModuleTimeResolution  =    0.2  # ms

    # set the base DQM folder for the plots
    process.FastTimerService.dqmPath                  = "HLT/TimerService"
    process.FastTimerService.enableDQMbyProcesses     = False

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



        
