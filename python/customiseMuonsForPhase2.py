import FWCore.ParameterSet.Config as cms

def addGemsToL2(process):
   
    objects = [ "muonDetIdAssociator", \
                "hcalDetIdAssociator", \
                "caloDetIdAssociator", \
                "ecalDetIdAssociator", \
                "preshowerDetIdAssociator", \
                "hoDetIdAssociator" ]
 
    for obj in objects : 
        if hasattr(process,obj) :
            print "[addGemsToL2] Enable GEM and ME0 in", obj

            getattr(process,obj).includeGEM = True
            getattr(process,obj).includeME0 = True

    if hasattr(process,"HLTMuonLocalRecoSequence") :
        print "[addGemsToL2] Add GEM and ME0 local reco to HLTMuonLocalRecoSequence"

        process.load("HLTrigger.Phase2.hlt_gem_local_reco_cff")

        process.HLTMuonLocalRecoSequence.replace(process.hltRpcRecHits, \
                                                 process.hltRpcRecHits + process.HLTMuonGemLocalRecoSequence)

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

def useRpcSimDigis(process):
   
    if hasattr(process,"hltRpcRecHits") :
            print "[useRpcSimDigis] Switch to use RPC sim digis (no packing/unpacking performed)"

            process.hltRpcRecHits.rpcDigiLabel = "simMuonRPCDigis"

    return process




# Keeping them here if debugging is needed
# not really used now

def removeHLTIsoMu24Steps(process):

    if hasattr(process,"HLT_IsoMu24_v4") :
        print "[removeHLTIsoMu24Steps] Removing steps not yet migrated to Phase2"
    
        #process.HLT_IsoMu24_v4.remove(process.HLTL3muonrecoSequence)
        #process.HLT_IsoMu24_v4.remove(process.hltL3fL1sMu22L1f0L2f10QL3Filtered24Q)
        #process.HLT_IsoMu24_v4.remove(process.HLTMu24IsolationSequence)
        #process.HLT_IsoMu24_v4.remove(process.hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09) 

    return process

def removeHLTMu50Steps(process):

    if hasattr(process,"HLT_Mu50_v5") :
        print "[removeHLTMu50Steps] Removing steps not yet migrated to Phase2"
    
        #process.HLT_Mu50_v5.remove(process.HLTL3muonrecoSequence)
        #process.HLT_Mu50_v5.remove(process.hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q)

    return process

def removeHLTIsoTkMu24Steps(process):

    if hasattr(process,"HLT_IsoTkMu24_v4") :
        print "[removeHLTIsoTkMu24Steps] Removing steps not yet migrated to Phase2"
    
        #process.HLT_IsoTkMu24_v4.remove(process.HLTTkMu24IsolationSequence)
        #process.HLT_IsoTkMu24_v4.remove(process.hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09) 

    return process


