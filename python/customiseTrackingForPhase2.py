import FWCore.ParameterSet.Config as cms

def customiseTracking(process):

    process = customisePixelLocalReco(process)
    process = customiseStripLocalReco(process)
    process = customiseTrackClusterRemoval(process)
    process = customiseTrackerEventProducer(process)
    process = customiseTkMuTrackerReco(process)
    process = customisePFMerging(process)

    return process


def customisePixelLocalReco(process):

    if hasattr(process,"hltSiPixelClusters") :
        print "[customisePixelLocalReco] switch to simSiPixelDigis as source"

        process.hltSiPixelClusters.src = cms.InputTag( "simSiPixelDigis","Pixel" )
        process.hltSiPixelClusters.payloadType = cms.string('Offline') # CB to be checked
        process.hltSiPixelClusters.MissCalibrate = cms.untracked.bool(False)
        process.hltSiPixelClusters.ElectronPerADCGain = cms.double(600.0) #CB to be checked as well, was not in HLT
        process.hltSiPixelClusters.maxNumberOfClusters = cms.int32(-1)

    process.load("CondTools.SiPixel.SiPixelGainCalibrationService_cfi")
    
    if hasattr(process,"hltESPPixelCPEGeneric") :
        print "[customisePixelLocalReco] customise hltESPPixelCPEGeneric"

        process.hltESPPixelCPEGeneric.useLAWidthFromDB = False
        process.hltESPPixelCPEGeneric.UseErrorsFromTemplates = False
        process.hltESPPixelCPEGeneric.LoadTemplatesFromDB = False
        process.hltESPPixelCPEGeneric.TruncatePixelCharge = False
        process.hltESPPixelCPEGeneric.IrradiationBiasCorrection = False
        process.hltESPPixelCPEGeneric.DoCosmics = False
        process.hltESPPixelCPEGeneric.Upgrade = cms.bool(True)

    if hasattr(process,"HLTDoLocalPixelSequence") :
        print "[customisePixelLocalReco] customise HLTDoLocalPixelSequence"

        process.HLTDoLocalPixelSequence.remove(process.hltSiPixelDigis)

        #process.HLTDoLocalPixelSequence.replace(process.hltSiPixelClusters , \
        #                                        process.hltSiPhase2Clusters 
        #                                        + process.hltSiPixelClusters)
        #phase2_tracker.toModify(clusterSummaryProducer,
        #  doStrips = False,
        #  stripClusters = ''
        #)

    return process

def customiseStripLocalReco(process):

    process.hltSiPhase2Clusters = cms.EDProducer("Phase2TrackerClusterizer",
                                                 maxClusterSize = cms.uint32(0),
                                                 maxNumberClusters = cms.uint32(0),
                                                 src = cms.InputTag("mix","Tracker")
                                                 )

    if hasattr(process,"hltSiStripClusters") :
        print "[customiseStripLocalReco] customise hltSiStripClusters"

        process.hltSiStripClusters.Phase2TrackerCluster1DProducer = cms.string('hltSiPhase2Clusters')
        process.hltSiStripClusters.inactivePixelDetectorLabels = []
        process.hltSiStripClusters.inactiveStripDetectorLabels = [cms.InputTag("siStripDigis")]
        process.hltSiStripClusters.stripClusterProducer = ''
        #process.hltSiStripClusters.measurementTracker = ''


    process.load("RecoLocalTracker.Phase2TrackerRecHits.Phase2StripCPEGeometricESProducer_cfi")

    if hasattr(process,"hltESPMeasurementTracker") :
        print "[customiseStripLocalReco] customise hltESPMeasurementTracker"

        process.hltESPMeasurementTracker.Phase2StripCPE = cms.string('Phase2StripCPE')

    if hasattr(process,"HLTDoLocalStripSequence") :
        print "[customiseStripLocalReco] customise HLTDoLocalStripSequence"

        process.HLTDoLocalStripSequence.remove(process.hltSiStripExcludedFEDListProducer)

        process.HLTDoLocalStripSequence.replace(process.hltSiStripRawToClustersFacility, \
                                                process.hltSiPhase2Clusters)
 
    return process


def customiseTrackClusterRemoval(process):

    objects = ["hltIter2IterL3MuonClustersRefRemoval",    \
               "hltIter2HighPtTkMuIsoClustersRefRemoval", \
               "hltIter2HighPtTkMuClustersRefRemoval",    \
               "hltIter1HighPtTkMuIsoClustersRefRemoval", \
               "hltIter1L3MuonClustersRefRemoval", \
               "hltIter2L3MuonClustersRefRemoval", \
               "hltIter1ClustersRefRemoval", \
               "hltIter2ClustersRefRemoval" ] 

    for obj in objects : 
        if hasattr(process,obj) :
            print "[customiseTrackClusterRemoval] customise ", obj

            removalPhase2 = cms.EDProducer("TrackClusterRemoverPhase2")
            removalPhase2.phase2OTClusters = cms.InputTag("hltSiPhase2Clusters")
            removalPhase2.phase2pixelClusters = cms.InputTag("hltSiPixelClusters")
 
            for paramName, param in getattr(process,obj).parameters_().iteritems() :

                if not paramName.find("Clusters") >=0 :
                    setattr(removalPhase2,paramName,param)
                    
            setattr(process,obj,removalPhase2) 

    return process

def customiseTrackerEventProducer(process):

    objects = [ "hltIter2IterL3MuonMaskedMeasurementTrackerEvent",    \
                "hltIter2HighPtTkMuMaskedMeasurementTrackerEvent",    \
                "hltIter1HighPtTkMuIsoMaskedMeasurementTrackerEvent", \
                "hltIter2HighPtTkMuIsoMaskedMeasurementTrackerEvent", \
                "hltIter1L3MuonMaskedMeasurementTrackerEvent", \
                "hltIter2L3MuonMaskedMeasurementTrackerEvent", \
                "hltIter1MaskedMeasurementTrackerEvent", \
                "hltIter2MaskedMeasurementTrackerEvent", ]
 
    for obj in objects : 
        if hasattr(process,obj) :
            print "[customiseTrackerEventProducer] customise ", obj

            producerPhase2 = cms.EDProducer("MaskedMeasurementTrackerEventProducer")
            producerPhase2.phase2clustersToSkip = cms.InputTag("hltSiStripClusters")

            for paramName, param in getattr(process,obj).parameters_().iteritems() :

                if not paramName.find("ToSkip") >= 0 :
                    setattr(producerPhase2,paramName,param)
                else :
                    setattr(producerPhase2,"phase2clustersToSkip",param)

            setattr(process,obj,producerPhase2)

    return process


def customiseTkMuTrackerReco(process):

    for obj in ["ClusterShapeHitFilterESProducer", \
                "hltESPMixedStepClusterShapeHitFilter", \
                "hltESPPixelLessStepClusterShapeHitFilter", \
                "hltESPTobTecStepClusterShapeHitFilter", \
                ] :
        if hasattr(process,obj) :
            print "[customiseTkMuTrackerReco] customise", obj

            getattr(process,obj).PixelShapeFile = cms.string('RecoPixelVertexing/PixelLowPtUtilities/data/pixelShape_Phase2Tk.par')

    for obj in ["hltESPTTRHBWithTrackAngle", \
                "hltESPTTRHBuilderAngleAndTemplate"] :

        if hasattr(process,obj) :
            print "[customiseTkMuTrackerReco] customise", obj

            # process.hltESPTTRHBWithTrackAngle.StripCPE = ""
            getattr(process,obj).Phase2StripCPE = cms.string('Phase2StripCPE')

    # for obj in ["hltESPTTRHBuilderPixelOnly"] :
   
    #     if hasattr(process,obj) :
    #         print "[customiseTkMuTrackerReco] customise", obj

    #         # process.hltESPTTRHBWithTrackAngle.StripCPE = ""
    #         getattr(process,obj).Phase2StripCPE = cms.string('Fake')

    return process

def customisePFMerging(process):

    for obj in ["hltPFMuonMerging"] :
        if hasattr(process,obj) :
            print "[customisePFMerging] customise", obj

            inputTags = cms.VInputTag("hltIterL3MuonMerged", "hltIter2Merged")

            getattr(process,obj).TrackProducers = inputTags
            getattr(process,obj).selectedTrackQuals = inputTags

    return process

