import FWCore.ParameterSet.Config as cms
import HLTrigger.Phase2.customiseTrackingForPhase2 as tracking

def customiseMuons(process):

    # process = customiseL1Unpacking(process)
    # process = customiseL1Seeds(process)
    process = addGemsToL2(process)
    process = tracking.customiseTracking(process)
    process = removeHLTIsoMu24Steps(process)
    process = removeHLTIsoTkMu24Steps(process)
    process = addTrigReport(process)

    return process


def customiseL1Unpacking(process):

    if hasattr(process,"rawDataCollector") :
        print "[customiseUnpacking] add stage2 L1 collections to rawDataCollector"

        process.rawDataCollector.RawCollectionList.append(cms.InputTag('caloStage2Raw'))
        process.rawDataCollector.RawCollectionList.append(cms.InputTag('gmtStage2Raw'))
        process.rawDataCollector.RawCollectionList.append(cms.InputTag('gtStage2Raw'))

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


def addGemsToL2(process):
   
    if hasattr(process,"muonDetIdAssociator") :
            print "[addGemsToL2] Enable GEM and ME0 in muonDetIdAssociator"

            process.muonDetIdAssociator.includeGEM = True
            process.muonDetIdAssociator.includeME0 = True

    if hasattr(process,"HLTMuonLocalRecoSequence") :
        print "[addGemsToL2] Add GEM and ME0 local reco to HLTMuonLocalRecoSequence"

        process.load("HLTrigger.Phase2.hlt_gem_local_reco_cff")

        process.HLTMuonLocalRecoSequence.replace(process.hltRpcRecHits, process.hltRpcRecHits + process.HLTMuonGemLocalRecoSequence)

    if hasattr(process,"hltL2Muons") :
            print "[addGemsToL2] Enable GEM and ME0 in hltL2Muons"

            process.hltL2Muons.L2TrajBuilderParameters.FilterParameters.EnableGEMMeasurement = cms.bool(True) 
            process.hltL2Muons.L2TrajBuilderParameters.FilterParameters.EnableME0Measurement = cms.bool(True)
            process.hltL2Muons.L2TrajBuilderParameters.FilterParameters.GEMRecSegmentLabel = cms.InputTag("hltGemRecHits")
            process.hltL2Muons.L2TrajBuilderParameters.FilterParameters.ME0RecSegmentLabel = cms.InputTag("hltMe0Segments")

            process.hltL2Muons.L2TrajBuilderParameters.BWFilterParameters.EnableGEMMeasurement = cms.bool(True) 
            process.hltL2Muons.L2TrajBuilderParameters.BWFilterParameters.EnableME0Measurement = cms.bool(True)
            process.hltL2Muons.L2TrajBuilderParameters.BWFilterParameters.GEMRecSegmentLabel = cms.InputTag("hltGemRecHits")
            process.hltL2Muons.L2TrajBuilderParameters.BWFilterParameters.ME0RecSegmentLabel = cms.InputTag("hltMe0Segments")

    return process


def removeHLTIsoMu24Steps(process):

    if hasattr(process,"HLT_IsoMu24_v4") :
        print "[removeHLTIsoMu24Steps] Removing steps not yet migrated to Phase2"
    
        process.HLT_IsoMu24_v4.replace(process.HLTL2muonrecoSequence, process.HLTL2muonrecoSequence \
                                                                      + process.HLTDoLocalPixelSequence \
                                                                      + process.HLTDoLocalStripSequence)
        process.HLT_IsoMu24_v4.remove(process.HLTL3muonrecoSequence)
        process.HLT_IsoMu24_v4.remove(process.hltL3fL1sMu22L1f0L2f10QL3Filtered24Q)
        process.HLT_IsoMu24_v4.remove(process.HLTMu24IsolationSequence)
        process.HLT_IsoMu24_v4.remove(process.hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09) 

    return process

def removeHLTIsoTkMu24Steps(process):

    if hasattr(process,"HLT_IsoTkMu24_v4") :
        print "[removeHLTIsoTkMu24Steps] Removing steps not yet migrated to Phase2"
    
#        process.HLT_IsoTkMu24_v4.replace(process.HLTHighPt24TrackerMuonSequence, process.HLTDoLocalPixelSequence \
#                                                                                 + process.HLTDoLocalStripSequence \
#                                                                                 + process.hltL1MuonsPt15 \
#                                                                                 + process.hltPixelLayerTriplets \
#                                                                                 + process.hltIter0HighPtTkMuPixelTracksFilter \
#                                                                                 + process.hltIter0HighPtTkMuPixelTracksFitter \
#                                                                                 + process.hltIter0HighPtTkMuPixelTracksTrackingRegions \
#                                                                                 + process.hltIter0HighPtTkMuPixelTracksHitDoublets \
#                                                                                 + process.hltIter0HighPtTkMuPixelTracksHitTriplets \
#
#                                                                                 + process.hltIter0HighPtTkMuPixelTracks \
#                                                                                 + process.hltIter0HighPtTkMuPixelSeedsFromPixelTracks \
#                                                                                 + process.hltIter0HighPtTkMuCkfTrackCandidates \
#                                                                                 + process.hltIter0HighPtTkMuCtfWithMaterialTracks \
#                                                                                 #+ process.hltIter0HighPtTkMuTrackSelectionHighPurity \
#                                                                                 # process.HLTIterativeTrackingHighPtTkMuIteration0
#                                                                                 )
#        process.HLT_IsoTkMu24_v4.remove(process.hltL3fL1sMu22f0TkFiltered24Q)
        process.HLT_IsoTkMu24_v4.remove(process.HLTTkMu24IsolationSequence)
        process.HLT_IsoTkMu24_v4.remove(process.hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09) 

    return process


def addTrigReport(process):
    # enable TrigReport, TimeReport and MultiThreading

    print "[addTrigReport] Adding report printout"

    process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool( True ),
        numberOfThreads = cms.untracked.uint32( 1 ),
        numberOfStreams = cms.untracked.uint32( 0 ),
        sizeOfStackForThreadsInKB = cms.untracked.uint32( 10*1024 )
        )

    print "[addTrigReport] Customise event content to keep hlt* "

    return process
        
def customiseMuonValidation(process):

    if hasattr(process,"globalPrevalidationMuons") :
        print "[customiseMuonValidation] Add HLT validation modules to offline muon validation"
    
        process.load("Validation.RecoMuon.muonValidationHLT_cff")
        process.load("DQMOffline.Trigger.MuonOffline_Trigger_cff")

        process.tpToL3TkMuonAssociation.tracksTag = cms.InputTag("hltIter2HighPtTkMuMerged")
        process.l3TkMuonMuTrackV.label = cms.VInputTag("hltIter2HighPtTkMuMerged")

        process.muonValidationHLTPhase2_seq = cms.Sequence( process.tpToL2MuonAssociation 
                                                            + process.l2MuonMuTrackV
                                                            + process.tpToL2UpdMuonAssociation 
                                                            + process.l2UpdMuonMuTrackV
                                                            + process.tpToL3TkMuonAssociation 
                                                            + process.l3TkMuonMuTrackV
                                                            + process.muonFullOfflineDQM
                                                            #+tpToL3MuonAssociation + l3MuonMuTrackV
                                                           )

        process.globalPrevalidationMuons.replace(process.glbMuonTrackVMuonAssoc, 
                                                 process.glbMuonTrackVMuonAssoc + process.muonValidationHLTPhase2_seq)
  
        #process.globalValidation.remove(process.hcaldigisValidationSequence)
        

    if hasattr(process,"postValidation") and \
       hasattr(process,"recoMuonPostProcessors") :

        process.load("Validation.RecoMuon.PostProcessorHLT_cff")
        process.load("DQMOffline.Trigger.MuonPostProcessor_cff")

        if hasattr(process,"postValidation") :
            print "[customiseMuonValidation] Add HLT validation modules to offline muon validation harvesting"

            process.muonRecoHltPostProcessors_seq = cms.Sequence( process.postProcessorRecoMuon_Sta
                                                                  + process.recoMuonPostProcessorsHLT
                                                                  + process.hltMuonPostVal 
                                                                )

            process.postValidation_muons.replace( process.postProcessorRecoMuon_Sta,
                                                  process.muonRecoHltPostProcessors_seq )

    return process


