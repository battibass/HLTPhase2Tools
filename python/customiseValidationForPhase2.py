import FWCore.ParameterSet.Config as cms

def getMuonValidationSequence(process):

    process.load("Validation.RecoMuon.muonValidationHLT_cff")
    process.load("DQMOffline.Trigger.MuonOffline_Trigger_cff")
    
    process.tpToPTkMuMuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToPTkMuMuonAssociation.tracksTag = cms.InputTag("hltIter0HighPtTkMuPixelTracks")

    process.PTkMuMuonMuTrackV = process.l3TkMuonMuTrackV.clone()
    process.PTkMuMuonMuTrackV.associatormap = 'tpToPTkMuMuonAssociation'
    process.PTkMuMuonMuTrackV.label = cms.VInputTag("hltIter0HighPtTkMuPixelTracks")

    process.tpToTkMuMuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToTkMuMuonAssociation.tracksTag = cms.InputTag("hltIter2HighPtTkMuMerged")

    process.TkMuMuonMuTrackV = process.l3TkMuonMuTrackV.clone()
    process.TkMuMuonMuTrackV.associatormap = 'tpToTkMuMuonAssociation'
    process.TkMuMuonMuTrackV.label = cms.VInputTag("hltIter2HighPtTkMuMerged")

    process.tpToTkMuIter0MuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToTkMuIter0MuonAssociation.tracksTag = cms.InputTag("hltIter0HighPtTkMuTrackSelectionHighPurity")

    process.TkMuIter0MuonMuTrackV = process.l3TkMuonMuTrackV.clone()
    process.TkMuIter0MuonMuTrackV.associatormap = 'tpToTkMuIter0MuonAssociation'
    process.TkMuIter0MuonMuTrackV.label = cms.VInputTag("hltIter0HighPtTkMuTrackSelectionHighPurity")

    process.tpToTkMuIter2MuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToTkMuIter2MuonAssociation.tracksTag = cms.InputTag("hltIter2HighPtTkMuTrackSelectionHighPurity")

    process.TkMuIter2MuonMuTrackV = process.l3TkMuonMuTrackV.clone()
    process.TkMuIter2MuonMuTrackV.associatormap = 'tpToTkMuIter2MuonAssociation'
    process.TkMuIter2MuonMuTrackV.label = cms.VInputTag("hltIter2HighPtTkMuTrackSelectionHighPurity")


    muonValidationHLTPhase2_seq = cms.Sequence( process.tpToL2MuonAssociation 
                                                + process.l2MuonMuTrackV
                                                + process.tpToL2UpdMuonAssociation 
                                                + process.l2UpdMuonMuTrackV
                                                + process.tpToTkMuMuonAssociation 
                                                + process.TkMuMuonMuTrackV
                                                + process.tpToPTkMuMuonAssociation 
                                                + process.PTkMuMuonMuTrackV
                                                + process.tpToTkMuIter0MuonAssociation 
                                                + process.TkMuIter0MuonMuTrackV
                                                + process.tpToTkMuIter2MuonAssociation 
                                                + process.TkMuIter2MuonMuTrackV
                                                + process.hltMuonValidator
                                                + process.muonFullOfflineDQM
                                                #+tpToL3MuonAssociation + l3MuonMuTrackV
                                                )

    return muonValidationHLTPhase2_seq


def getMuonValidationHarvestingSequence(process):

    process.load("Validation.RecoMuon.PostProcessorHLT_cff")
    process.load("DQMOffline.Trigger.MuonPostProcessor_cff")

    muonRecoHltPostProcessors_seq = cms.Sequence( process.postProcessorRecoMuon_Sta
                                                  + process.recoMuonPostProcessorsHLT
                                                  + process.hltMuonPostProcessors
                                                  + process.hltMuonPostVal 
                                                  )
    return muonRecoHltPostProcessors_seq



def customiseMuonRelVal(process):

    if hasattr(process,"globalPrevalidationMuons") :
        print "[customiseMuonValidation] Add HLT validation modules to offline muon validation"
    
        process.muonValidationHLTPhase2_seq = getMuonValidationSequence(process)

        process.globalPrevalidationMuons.replace(process.glbMuonTrackVMuonAssoc, 
                                                 process.glbMuonTrackVMuonAssoc 
                                                 + process.muonValidationHLTPhase2_seq)
  

        #process.globalValidation.remove(process.hcaldigisValidationSequence)
        

    if hasattr(process,"postValidation") and \
       hasattr(process,"recoMuonPostProcessors") :

        if hasattr(process,"postValidation") :
            print "[customiseMuonValidation] Add HLT validation modules to offline muon validation harvesting"

            process.muonRecoHltPostProcessors_seq = getMuonValidationHarvestingSequence(process)

            process.postValidation_muons.replace( process.postProcessorRecoMuon_Sta,
                                                  process.muonRecoHltPostProcessors_seq )

    return process


def getMuonValidationSequenceLight(process):

    process.tpToPTkMuMuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToPTkMuMuonAssociation.tracksTag = cms.InputTag("hltIter0HighPtTkMuPixelTracks")

    process.PTkMuMuonMuTrackV = process.l3TkMuonMuTrackV.clone()
    process.PTkMuMuonMuTrackV.associatormap = 'tpToPTkMuMuonAssociation'
    process.PTkMuMuonMuTrackV.label = cms.VInputTag("hltIter0HighPtTkMuPixelTracks")

    process.tpToTkMuMuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToTkMuMuonAssociation.tracksTag = cms.InputTag("hltIter2HighPtTkMuMerged")

    process.TkMuMuonMuTrackV = process.l3TkMuonMuTrackV.clone()
    process.TkMuMuonMuTrackV.associatormap = 'tpToTkMuMuonAssociation'
    process.TkMuMuonMuTrackV.label = cms.VInputTag("hltIter2HighPtTkMuMerged")

    process.tpToTkMuIter0MuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToTkMuIter0MuonAssociation.tracksTag = cms.InputTag("hltIter0HighPtTkMuTrackSelectionHighPurity")

    process.TkMuIter0MuonMuTrackV = process.l3TkMuonMuTrackV.clone()
    process.TkMuIter0MuonMuTrackV.associatormap = 'tpToTkMuIter0MuonAssociation'
    process.TkMuIter0MuonMuTrackV.label = cms.VInputTag("hltIter0HighPtTkMuTrackSelectionHighPurity")

    process.tpToTkMuIter2MuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToTkMuIter2MuonAssociation.tracksTag = cms.InputTag("hltIter2HighPtTkMuTrackSelectionHighPurity")

    process.TkMuIter2MuonMuTrackV = process.l3TkMuonMuTrackV.clone()
    process.TkMuIter2MuonMuTrackV.associatormap = 'tpToTkMuIter2MuonAssociation'
    process.TkMuIter2MuonMuTrackV.label = cms.VInputTag("hltIter2HighPtTkMuTrackSelectionHighPurity")


    muonValidationHLTPhase2_seq = cms.Sequence( process.tpToTkMuMuonAssociation 
                                                + process.TkMuMuonMuTrackV
                                                + process.tpToPTkMuMuonAssociation 
                                                + process.PTkMuMuonMuTrackV
                                                + process.tpToTkMuIter0MuonAssociation 
                                                + process.TkMuIter0MuonMuTrackV
                                                + process.tpToTkMuIter2MuonAssociation 
                                                + process.TkMuIter2MuonMuTrackV
                                                + process.hltMuonValidator
                                                + process.muonFullOfflineDQM
                                                #+tpToL3MuonAssociation + l3MuonMuTrackV
                                                )

    return muonValidationHLTPhase2_seq

def customiseMuonRelValLight(process):

    if hasattr(process,"validation") :
        print "[customiseMuonValidationLight] Add HLT TkMu validation ... JUST A TEST!"
    
        process.muonValidationHLTPhase2_seq = getMuonValidationSequenceLight(process)

        process.validation.replace(process.glbMuonTrackVMuonAssoc, 
                                   process.glbMuonTrackVMuonAssoc 
                                   + process.muonValidationHLTPhase2_seq)
  
    return process

