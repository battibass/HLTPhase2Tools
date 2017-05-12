import FWCore.ParameterSet.Config as cms

def getMuonValidationSequence(process):

    process.load("Validation.RecoMuon.muonValidationHLT_cff")
    process.load("DQMOffline.Trigger.MuonOffline_Trigger_cff")

    # Tracker muons iteration seeds (pixel tracks)
    process.tpToPTkMuMuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToPTkMuMuonAssociation.tracksTag = cms.InputTag("hltIter0HighPtTkMuPixelTracks")

    process.PTkMuMuonMuTrackV = process.l3TkMuonMuTrackV.clone()
    process.PTkMuMuonMuTrackV.associatormap = 'tpToPTkMuMuonAssociation'
    process.PTkMuMuonMuTrackV.label = cms.VInputTag("hltIter0HighPtTkMuPixelTracks")

    # Tracker muons iteration 0
    process.tpToTkMuIter0MuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToTkMuIter0MuonAssociation.tracksTag = cms.InputTag("hltIter0HighPtTkMuTrackSelectionHighPurity")

    process.TkMuIter0MuonMuTrackV = process.l3TkMuonMuTrackV.clone()
    process.TkMuIter0MuonMuTrackV.associatormap = 'tpToTkMuIter0MuonAssociation'
    process.TkMuIter0MuonMuTrackV.label = cms.VInputTag("hltIter0HighPtTkMuTrackSelectionHighPurity")

    # Tracker muons iteration 2
    process.tpToTkMuIter2MuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToTkMuIter2MuonAssociation.tracksTag = cms.InputTag("hltIter2HighPtTkMuTrackSelectionHighPurity")

    process.TkMuIter2MuonMuTrackV = process.l3TkMuonMuTrackV.clone()
    process.TkMuIter2MuonMuTrackV.associatormap = 'tpToTkMuIter2MuonAssociation'
    process.TkMuIter2MuonMuTrackV.label = cms.VInputTag("hltIter2HighPtTkMuTrackSelectionHighPurity")

    # Tracker muons final merging
    process.tpToTkMuMuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToTkMuMuonAssociation.tracksTag = cms.InputTag("hltIter2HighPtTkMuMerged")

    process.TkMuMuonMuTrackV = process.l3TkMuonMuTrackV.clone()
    process.TkMuMuonMuTrackV.associatormap = 'tpToTkMuMuonAssociation'
    process.TkMuMuonMuTrackV.label = cms.VInputTag("hltIter2HighPtTkMuMerged")

    # L3 muons OI from L2
    process.tpToL3MuonTracksOIMuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToL3MuonTracksOIMuonAssociation.tracksTag = cms.InputTag("hltIterL3OIMuCtfWithMaterialTracks")

    process.l3MuonTracksOIMuonV = process.l3TkMuonMuTrackV.clone()
    process.l3MuonTracksOIMuonV.associatormap = 'tpToL3MuonTracksOIMuonAssociation'
    process.l3MuonTracksOIMuonV.label = cms.VInputTag("hltIterL3OIMuCtfWithMaterialTracks")

    # L3 muons final merging
    process.tpToL3MuonTracksMergedMuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToL3MuonTracksMergedMuonAssociation.tracksTag = cms.InputTag("hltIterL3MuonMerged")

    process.l3MuonTracksMergedMuonV = process.l3TkMuonMuTrackV.clone()
    process.l3MuonTracksMergedMuonV.associatormap = 'tpToL3MuonTracksMergedMuonAssociation'
    process.l3MuonTracksMergedMuonV.label = cms.VInputTag("hltIterL3MuonMerged")

    

    process.hltMu50l3Filter = cms.EDProducer("HLTFilterToTrackProducer", 
                                             filterTag = cms.InputTag("hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q"),
                                             trigEvTag = cms.InputTag("hltTriggerSummaryAOD")
                                            )

    # L3 muons final merging
    process.tpToL3Mu50FilterMuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToL3Mu50FilterMuonAssociation.tracksTag = cms.InputTag("hltMu50l3Filter")

    process.l3Mu50FilterMuonV = process.l3TkMuonMuTrackV.clone()
    process.l3Mu50FilterMuonV.associatormap = 'tpToL3Mu50FilterMuonAssociation'
    process.l3Mu50FilterMuonV.label = cms.VInputTag("hltMu50l3Filter")

    
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
                                                + process.tpToL3MuonTracksOIMuonAssociation
                                                + process.l3MuonTracksOIMuonV
                                                + process.tpToL3MuonTracksMergedMuonAssociation
                                                + process.l3MuonTracksMergedMuonV                                               
                                                + process.hltMu50l3Filter
                                                + process.tpToL3Mu50FilterMuonAssociation
                                                + process.l3Mu50FilterMuonV                                               
                                                # + process.hltMuonValidator
                                                # + process.muonFullOfflineDQM
                                               
                                                #+tpToL3MuonAssociation + l3MuonMuTrackV
                                                )

    return muonValidationHLTPhase2_seq


def getMuonValidationHarvestingSequence(process):

    process.load("Validation.RecoMuon.PostProcessorHLT_cff")
    process.load("DQMOffline.Trigger.MuonPostProcessor_cff")

    muonRecoHltPostProcessors_seq = cms.Sequence( process.postProcessorRecoMuon_Sta
                                                  + process.recoMuonPostProcessorsHLT
                                                  #+ process.hltMuonPostProcessors
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
  

    if hasattr(process,"postValidation") and \
       hasattr(process,"recoMuonPostProcessors") :

        if hasattr(process,"postValidation") :
            print "[customiseMuonValidation] Add HLT validation modules to offline muon validation harvesting"

            process.muonRecoHltPostProcessors_seq = getMuonValidationHarvestingSequence(process)

            process.postValidation_muons.replace( process.postProcessorRecoMuon_Sta,
                                                  process.muonRecoHltPostProcessors_seq )

    return process


def customiseMuonRelValStep2(process):

    if hasattr(process,"schedule") :
        print "[customiseMuonValidationStep2] Add HLT muon validation to step2 ... JUST A TEST!"

        process.load("DQMServices.Components.MEtoEDMConverter_cfi")
        process.load("DQMServices.Components.DQMEnvironment_cfi")
        process.load("DQMServices.Core.DQM_cfg")

        process.dqmEnvHLT = process.dqmEnv.clone()
        process.dqmEnvHLT.subSystemFolder = 'HLT'

        process.load("SimTracker.TrackAssociation.LhcParametersDefinerForTP_cfi")
        
        process.LhcParametersDefinerForTP.beamSpot = "hltOnlineBeamSpot"
    
        process.muonHLTValidationPhase2_seq = getMuonValidationSequence(process)
        
        for obj in process.muonHLTValidationPhase2_seq.moduleNames() :
            
            if hasattr(process,obj) and hasattr(getattr(process,obj),'beamSpot') :
                print "[customiseMuonValidationStep2] use hlt beam spot for", obj
                                
                getattr(process,obj).beamSpot = 'hltOnlineBeamSpot'         

        process.muonHLTValidationPhase2 = cms.EndPath(process.dqmEnvHLT 
                                                      + process.muonHLTValidationPhase2_seq 
                                                      ) 
            
        process.DQMoutput_seq = cms.OutputModule("DQMRootOutputModule",
            dataset = cms.untracked.PSet(
                dataTier = cms.untracked.string('DQMIO'),
                filterName = cms.untracked.string('')
            ),
            fileName = cms.untracked.string('file:step2_inDQM.root'),
            outputCommands = process.DQMEventContent.outputCommands,
            splitLevel = cms.untracked.int32(0)
        )
        
        process.DQMoutput = cms.EndPath(process.DQMoutput_seq)
                
    return process

def customiseMuonRelValStep2Harvesting(process):

    if hasattr(process,"DQMSaver") :
        print "[customiseMuonRelValStep2Harvesting] Add HLT validation modules to offline muon validation harvesting"

        process.muonHLTPostProcessors_seq = getMuonValidationHarvestingSequence(process)

        process.load("Configuration.StandardSequences.EDMtoMEAtJobEnd_cff")

        process.muonHLTPostProcessors = cms.Path(process.EDMtoME
                                                 + process.muonHLTPostProcessors_seq)                     
        process.pDQMSaver = cms.Path(process.DQMSaver)                     
        process.schedule = cms.Schedule(process.muonHLTPostProcessors,process.pDQMSaver)

    return process
