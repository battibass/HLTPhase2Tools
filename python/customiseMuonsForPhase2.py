import FWCore.ParameterSet.Config as cms

def customiseMuons(process):

    process = customiseL1Unoacking(process)
    process = customiseL1Seeds(process)
    process = removeHLTIsoMu24Steps(process)
    process = addTrigReport(process)

    return process


def customiseL1Unpacking(process):

    if hasattr(process,"rawDataCollector") :
        print "[customiseUnpacking] add stage2 L1 collections to rawDataCollector"

        process.rawDataCollector.RawCollectionList.append(cms.InputTag('caloStage2Raw'))
        process.rawDataCollector.RawCollectionList.append(cms.InputTag('gmtStage2Raw'))
        process.rawDataCollector.RawCollectionList.append(cms.InputTag('gtStage2Raw'))

    return process

     
def customiseL1Seeds(process):
   
    if hasattr(process,"HLT_IsoMu24_v4") :
        print "[customiseL1Seeds] Add cms.Ignore() to IsoMu24 l1 related filters"

        process.HLT_IsoMu24_v4.replace(process.hltL1sSingleMu22,cms.ignore(process.hltL1sSingleMu22))
        process.HLT_IsoMu24_v4.replace(process.hltL1fL1sMu22L1Filtered0,cms.ignore(process.hltL1fL1sMu22L1Filtered0))

    return process

def removeHLTIsoMu24Steps(process):

    if hasattr(process,"HLT_IsoMu24_v4") :
        print "[removeHLTIsoMu24Steps] Removing steps not yet migrated to Phase2"
    
        process.HLT_IsoMu24_v4.remove(process.HLTL3muonrecoSequence)
        process.HLT_IsoMu24_v4.remove(process.hltL3fL1sMu22L1f0L2f10QL3Filtered24Q)
        process.HLT_IsoMu24_v4.remove(process.HLTMu24IsolationSequence)
        process.HLT_IsoMu24_v4.remove(process.hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09) 

    return process


def addTrigReport(process):
    # enable TrigReport, TimeReport and MultiThreading

    print "[addTrigReport] Adding report printout"

    process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool( True ),
        numberOfThreads = cms.untracked.uint32( 4 ),
        numberOfStreams = cms.untracked.uint32( 0 ),
        sizeOfStackForThreadsInKB = cms.untracked.uint32( 10*1024 )
        )

    return process
        
        
