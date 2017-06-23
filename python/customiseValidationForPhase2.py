import FWCore.ParameterSet.Config as cms

def getFilterValidationSequence(process, name, filterName, minPt, associator, validator):

    filterToTrack = cms.EDProducer("HLTFilterToTrackProducer", 
                                       filterTag = cms.InputTag(filterName),
                                       trigEvTag = cms.InputTag("hltTriggerSummaryAOD")
                                  )

    setattr(process, name, filterToTrack)

    filterMuonAssociation = associator.clone()
    filterMuonAssociation.tracksTag = cms.InputTag(name)

    setattr(process, name + "MuonAssociation", filterMuonAssociation)

    filterMuonV = validator.clone()
    filterMuonV.associatormap = name + "MuonAssociation"
    filterMuonV.label = cms.VInputTag(name)
    filterMuonV.ptMinTP = cms.double(minPt)

    setattr(process, name + "FilterMuonV", filterMuonV)

    muonValidationFilter_seq = cms.Sequence( getattr(process, name)
                                             + getattr(process, name + "MuonAssociation") 
                                             + getattr(process, name + "FilterMuonV") 
                                           )

    return muonValidationFilter_seq 


def getMuonValidationSequence(process, debug = True):

    process.load("Validation.RecoMuon.muonValidationHLT_cff")
    process.load("DQMOffline.Trigger.MuonOffline_Trigger_cff")

    # Tracker muons final merging
    process.tpToTkMuMuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToTkMuMuonAssociation.tracksTag = cms.InputTag("hltIter2HighPtTkMuMerged")

    process.TkMuMuonMuTrackV = process.l3TkMuonMuTrackV.clone()
    process.TkMuMuonMuTrackV.associatormap = 'tpToTkMuMuonAssociation'
    process.TkMuMuonMuTrackV.label = cms.VInputTag("hltIter2HighPtTkMuMerged")

    if debug :
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

    # L3 muons final merging
    process.tpToL3MuonTracksMergedMuonAssociation = process.tpToL3TkMuonAssociation.clone()
    process.tpToL3MuonTracksMergedMuonAssociation.tracksTag = cms.InputTag("hltIterL3MuonMerged")

    process.l3MuonTracksMergedMuonV = process.l3TkMuonMuTrackV.clone()
    process.l3MuonTracksMergedMuonV.associatormap = 'tpToL3MuonTracksMergedMuonAssociation'
    process.l3MuonTracksMergedMuonV.label = cms.VInputTag("hltIterL3MuonMerged")

    if debug :
        # L3 muons OI from L2
        process.tpToL3MuonTracksOIMuonAssociation = process.tpToL3TkMuonAssociation.clone()
        process.tpToL3MuonTracksOIMuonAssociation.tracksTag = cms.InputTag("hltIterL3OIMuCtfWithMaterialTracks")

        process.l3MuonTracksOIMuonV = process.l3TkMuonMuTrackV.clone()
        process.l3MuonTracksOIMuonV.associatormap = 'tpToL3MuonTracksOIMuonAssociation'
        process.l3MuonTracksOIMuonV.label = cms.VInputTag("hltIterL3OIMuCtfWithMaterialTracks")

        process.tpToL3MuonTracksOIMuonAssociationHP = process.tpToL3TkMuonAssociation.clone()
        process.tpToL3MuonTracksOIMuonAssociationHP.tracksTag = cms.InputTag("hltIterL3OIMuonTrackSelectionHighPurity")

        process.l3MuonTracksOIMuonVHP = process.l3TkMuonMuTrackV.clone()
        process.l3MuonTracksOIMuonVHP.associatormap = 'tpToL3MuonTracksOIMuonAssociationHP'
        process.l3MuonTracksOIMuonVHP.label = cms.VInputTag("hltIterL3OIMuonTrackSelectionHighPurity")


    process.hltMu50L2Filter_seq = getFilterValidationSequence(process, \
                                                              "hltMu50l2Filter", \
                                                              "hltL2fL1sMu22Or25L1f0L2Filtered10Q", \
                                                              55. ,\
                                                              process.tpToL2MuonAssociation, \
                                                              process.l2MuonMuTrackV)

    process.hltMu50L3Filter_seq = getFilterValidationSequence(process, \
                                                              "hltMu50l3Filter", \
                                                              "hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q", \
                                                              55. ,\
                                                              process.tpToL3MuonAssociation, \
                                                              process.l3MuonMuTrackV)

    process.hltTkMu50TkMuFilter_seq = getFilterValidationSequence(process, \
                                                                  "hltTkMu50TkMuFilter", \
                                                                  "hltL3fL1sMu25f0TkFiltered50Q", \
                                                                  55. ,\
                                                                  process.tpToL3MuonAssociation, \
                                                                  process.l3MuonMuTrackV)


    process.hltIsoMu27L2Filter_seq = getFilterValidationSequence(process, \
                                                                 "hltIsoMu27l2Filter", \
                                                                 "hltL2fL1sMu22Or25L1f0L2Filtered10Q", \
                                                                 30. ,\
                                                                 process.tpToL2MuonAssociation, \
                                                                 process.l2MuonMuTrackV)

    process.hltIsoMu27L3Filter_seq = getFilterValidationSequence(process, \
                                                                 "hltIsoMu27l3Filter", \
                                                                 "hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q", \
                                                                 30. ,\
                                                                 process.tpToL3MuonAssociation, \
                                                                 process.l3MuonMuTrackV)

    process.hltIsoMu27IsoFilter_seq = getFilterValidationSequence(process, \
                                                                  "hltIsoMu27IsoFilter", \
                                                                  "hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p09", \
                                                                  30. ,\
                                                                  process.tpToL3MuonAssociation, \
                                                                  process.l3MuonMuTrackV)

    process.hltIsoMu27TrkIsoFilter_seq = getFilterValidationSequence(process, \
                                                                     "hltTrkIsoMu27IsoFilter", \
                                                                     "hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoOnlyFiltered0p09", 
                                                                      30. ,\
                                                                      process.tpToL3MuonAssociation, \
                                                                      process.l3MuonMuTrackV)
    
    muonValidationHLTPhase2_seq = cms.Sequence( process.tpToL2MuonAssociation 
                                                + process.l2MuonMuTrackV
                                                + process.tpToL2UpdMuonAssociation 
                                                + process.l2UpdMuonMuTrackV

                                                + process.tpToTkMuMuonAssociation 
                                                + process.TkMuMuonMuTrackV
                                                
                                                + process.tpToL3MuonTracksMergedMuonAssociation
                                                + process.l3MuonTracksMergedMuonV

                                                + process.hltMu50L2Filter_seq
                                                + process.hltMu50L3Filter_seq
                                                + process.hltTkMu50TkMuFilter_seq

                                                + process.hltIsoMu27L2Filter_seq
                                                + process.hltIsoMu27L3Filter_seq
                                                + process.hltIsoMu27IsoFilter_seq
                                                + process.hltIsoMu27TrkIsoFilter_seq


                                                # + process.hltMuonValidator
                                                # + process.muonFullOfflineDQM
                                                )
    
        
    if debug:
        muonValidationHLTPhase2_seq.replace(process.l3MuonTracksMergedMuonV,
                                            process.l3MuonTracksMergedMuonV

                                            #+ process.tpToPTkMuMuonAssociation 
                                            #+ process.PTkMuMuonMuTrackV
                                            + process.tpToTkMuIter0MuonAssociation 
                                            + process.TkMuIter0MuonMuTrackV
                                            + process.tpToTkMuIter2MuonAssociation 
                                            + process.TkMuIter2MuonMuTrackV

                                            + process.tpToL3MuonTracksOIMuonAssociation
                                            + process.l3MuonTracksOIMuonV

                                            + process.tpToL3MuonTracksOIMuonAssociationHP
                                            + process.l3MuonTracksOIMuonVHP                                            
                                            )


    return muonValidationHLTPhase2_seq


def getMuonValidationHarvestingSequence(process):

    process.load("Validation.RecoMuon.PostProcessorHLT_cff")
    process.load("DQMOffline.Trigger.MuonPostProcessor_cff")

    muonHltPostProcessors_seq = cms.Sequence( process.postProcessorRecoMuon_Sta
                                                      + process.recoMuonPostProcessorsHLT
                                                      #+ process.hltMuonPostProcessors
                                                      #+ process.hltMuonPostVal 
                                                      )
    return muonHltPostProcessors_seq

def getJetMETValidationSequence(process):
    
    process.singleJetMetPaths = cms.EDAnalyzer("HLTJetMETValidation",
                triggerEventObject    = cms.untracked.InputTag("hltTriggerSummaryRAW"),
                DQMFolder             = cms.untracked.string("HLT/HLTJETMET/"),
                PatternJetTrg         = cms.untracked.string("HLT_PF(NoPU)?Jet([0-9])+(_v[0-9]+)?$"),                                   
                PatternMetTrg         = cms.untracked.string("HLT_PF(ch)?MET([0-9])+(_HBHECleaned+)+(_v[0-9]+)?$"),
                triggerProcessName    = cms.untracked.string("HLT"), 
                PatternMuTrg          = cms.untracked.string("HLT_Mu([0-9])+(_v[0-9]+)?$"),
                LogFileName           = cms.untracked.string('JetMETSingleJetValidation.log'),
                PFJetAlgorithm        = cms.untracked.InputTag("hltAK4PFJets"),
                GenJetAlgorithm       = cms.untracked.InputTag("ak4GenJets"),
                CaloMETCollection     = cms.untracked.InputTag("hltMet"),
                GenMETCollection      = cms.untracked.InputTag("genMetCalo"),
                HLTriggerResults      = cms.InputTag("TriggerResults"),
            )

    jetMETValidationHLTPhase2_seq = cms.Sequence(process.singleJetMetPaths)
    
    return  jetMETValidationHLTPhase2_seq
   

def getJetMETValidationHarvestingSequence(process):

    process.load("HLTriggerOffline.JetMET.Validation.JetMETPostProcessor_cff")

    jetMETHltPostProcessors_seq = cms.Sequence(process.JetMETPostVal)

    return jetMETHltPostProcessors_seq


def customiseJetMETRelVal(process):

    if hasattr(process,"validationMiniAOD") :
        print "[customiseJetMETValidation] Add HLT validation modules to offline JetMET validation"

        process.HLTJetMETValSeq = getJetMETValidationSequence(process)
        process.validation_step6.replace(process.validationMiniAOD,process.validationMiniAOD+process.HLTJetMETValSeq)

    if hasattr(process,"DQMHarvestMiniAOD_step") :

        process.myJetValidation_seq = getJetMETValidationHarvestingSequence(process)
        process.DQMHarvestMiniAOD_step.replace(process.DQMHarvestMiniAOD,process.DQMHarvestMiniAOD+process.myJetValidation_seq)

    return process


def customiseMuonRelVal(process):

    if hasattr(process,"globalPrevalidationMuons") :
        print "[customiseMuonValidation] Add HLT validation modules to offline muon validation"
    
        process.muonValidationHLTPhase2_seq = getMuonValidationSequence(process,True)

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


def customiseRelValStep2(process):

    if hasattr(process,"schedule") :
        print "[customiseValidationStep2] Add DQM framework and HLT muon + PFJets validation to step2"

        process.load("DQMServices.Components.DQMEnvironment_cfi")

        process.dqmEnvHLT = process.dqmEnv.clone()
        process.dqmEnvHLT.subSystemFolder = 'HLT'

        process.load("SimTracker.TrackAssociation.LhcParametersDefinerForTP_cfi")        
        process.LhcParametersDefinerForTP.beamSpot = "hltOnlineBeamSpot"
    

        process.muonHLTValidationPhase2_seq   = getMuonValidationSequence(process,True)
        process.jetMETHLTValidationPhase2_seq = getJetMETValidationSequence(process)
        
        
        for obj in process.muonHLTValidationPhase2_seq.moduleNames() :
            
            if hasattr(process,obj) and hasattr(getattr(process,obj),'beamSpot') :
                print "[customiseValidationStep2] use hlt beam spot for", obj
                                
                getattr(process,obj).beamSpot = 'hltOnlineBeamSpot'         

        if hasattr(process,"singleJetMetPaths") :
            print "[customiseValidationStep2] singleJetMetPaths.triggerProcessName = HLTPhase2Upgrade"
            process.singleJetMetPaths.triggerProcessName = cms.untracked.string("HLTPhase2Upgrade")

                
        process.hltValidationPhase2 = cms.EndPath(process.dqmEnvHLT 
                                                  + process.muonHLTValidationPhase2_seq 
                                                  + process.jetMETHLTValidationPhase2_seq
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

def customiseRelValStep2Harvesting(process):

    if hasattr(process,"DQMSaver") :
        print "[customiseRelValStep2Harvesting] Add DQM framework and HLT muon + PFJets to harvesting"

        process.muonHLTPostProcessors_seq   = getMuonValidationHarvestingSequence(process)
        process.jetMETHLTPostProcessors_seq = getJetMETValidationHarvestingSequence(process)

        process.muonHLTPostProcessors = cms.Path(process.muonHLTPostProcessors_seq
                                                 + process.jetMETHLTPostProcessors_seq)  
        
        process.pDQMSaver = cms.Path(process.DQMSaver)                     
        process.schedule = cms.Schedule(process.muonHLTPostProcessors,process.pDQMSaver)

    return process
