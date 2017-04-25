import FWCore.ParameterSet.Config as cms

import HLTrigger.Phase2.customiseMuonsForPhase2      as muons
import HLTrigger.Phase2.customiseTrackingForPhase2   as tracking
import HLTrigger.Phase2.customiseValidationForPhase2 as val

def customiseMuons(process):

    # process = customiseL1Unpacking(process)
    # process = customiseL1Seeds(process)
    process = muons.useRpcSimDigis(process)
    process = muons.addGemsToL2(process)
    process = tracking.customiseTracking(process)
    process = muons.removeHLTIsoMu24Steps(process)
    process = muons.removeHLTIsoTkMu24Steps(process)
    process = addTrigReport(process)

    return process

def customiseRelVal(process):

    process = val.customiseMuonRelVal(process)

    return process

def customiseRelValLight(process):

    process = addTrigReport(process)
    process = val.customiseMuonRelValLight(process)

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

    if hasattr(process,"FEVTDEBUGHLToutput") :
        print "[addTrigReport] Customise event content to keep hltIter* "
        process.FEVTDEBUGHLToutput.outputCommands.append('keep *_hltIter*_*_HLT')

    return process


def customiseL1Seeds( process):
   
    if hasattr(process,"HLT_IsoMu24_v4") :
        print "[customiseL1Seeds] Add cms.Ignore() to IsoMu24 L1 related filters"

        process.HLT_IsoMu24_v4.replace(process.hltL1sSingleMu22,cms.ignore(process.hltL1sSingleMu22))
        process.HLT_IsoMu24_v4.replace(process.hltL1fL1sMu22L1Filtered0,cms.ignore(process.hltL1fL1sMu22L1Filtered0))

    if hasattr(process,"HLT_IsoTkMu24_v4") :
        print "[customiseL1Seeds] Add cms.Ignore() to IsoTkMu24 L1 related filters"

        process.HLT_IsoTkMu24_v4.replace(process.hltL1sSingleMu22,cms.ignore(process.hltL1sSingleMu22))
        process.HLT_IsoTkMu24_v4.replace(process.hltL1fL1sMu22L1Filtered0,cms.ignore(process.hltL1fL1sMu22L1Filtered0))

    return process


        
