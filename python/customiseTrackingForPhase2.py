import FWCore.ParameterSet.Config as cms

def customiseTracking(process):

    process = customisePixelLocalReco(process)
    process = customiseStripLocalReco(process)
    process = customiseTrackClusterRemoval(process)
    process = customiseTrackerEventProducer(process)
    process = customiseTkMuTrackerReco(process)
    return process


def customisePixelLocalReco(process):

    if hasattr(process,"hltSiPixelClusters") :
        print "[customisePixelLocalReco] switch to simSiPixelDigis as source"

        process.hltSiPixelClusters.src = cms.InputTag( "simSiPixelDigis","Pixel" )
        process.hltSiPixelClusters.payloadType = cms.string('Offline') # CB to be checked
        process.hltSiPixelClusters.MissCalibrate = cms.untracked.bool(False)
        process.hltSiPixelClusters.ElectronPerADCGain = cms.double(600.0) #CB to be checked as well, was not in HLT

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
        
    if hasattr(process,"hltIter2HighPtTkMuIsoClustersRefRemoval") :
        print "[customiseTrackClusterRemoval] customise hltIter2HighPtTkMuIsoClustersRefRemoval"

        removalPhase2 = cms.EDProducer("TrackClusterRemoverPhase2")
        removalPhase2.phase2OTClusters = cms.InputTag("hltSiPhase2Clusters")
        removalPhase2.phase2pixelClusters = cms.InputTag("hltSiPixelClusters")

        for paramName, param in process.hltIter2HighPtTkMuIsoClustersRefRemoval.parameters_().iteritems() :

            if not paramName.find("Clusters") >=0 :
                setattr(removalPhase2,paramName,param)

        process.hltIter2HighPtTkMuIsoClustersRefRemoval = removalPhase2

    if hasattr(process,"hltIter2HighPtTkMuClustersRefRemoval") :
        print "[customiseTrackClusterRemoval] customise hltIter2HighPtTkMuClustersRefRemoval"

        removalPhase2 = cms.EDProducer("TrackClusterRemoverPhase2")
        removalPhase2.phase2OTClusters = cms.InputTag("hltSiPhase2Clusters")
        removalPhase2.phase2pixelClusters = cms.InputTag("hltSiPixelClusters")

        for paramName, param in process.hltIter2HighPtTkMuClustersRefRemoval.parameters_().iteritems() :

            if not paramName.find("Clusters") >= 0 :
                setattr(removalPhase2,paramName,param)

        process.hltIter2HighPtTkMuClustersRefRemoval = removalPhase2

    if hasattr(process,"hltIter1HighPtTkMuIsoClustersRefRemoval") :
        print "[customisTrackClusterRemoval] customise hltIter1HighPtTkMuIsoClustersRefRemoval"

        removalPhase2 = cms.EDProducer("TrackClusterRemoverPhase2")
        removalPhase2.phase2OTClusters = cms.InputTag("hltSiPhase2Clusters")
        removalPhase2.phase2pixelClusters = cms.InputTag("hltSiPixelClusters")

        for paramName, param in process.hltIter1HighPtTkMuIsoClustersRefRemoval.parameters_().iteritems() :

            if not paramName.find("Clusters") >= 0 :
                setattr(removalPhase2,paramName,param)

        process.hltIter1HighPtTkMuIsoClustersRefRemoval = removalPhase2

    return process

def customiseTrackerEventProducer(process):

    if hasattr(process,"hltIter2HighPtTkMuMaskedMeasurementTrackerEvent") :
        print "[customiseTrackerEventProducer] customise hltIter2HighPtTkMuMaskedMeasurementTrackerEvent"

        producerPhase2 = cms.EDProducer("MaskedMeasurementTrackerEventProducer")
        producerPhase2.phase2clustersToSkip = cms.InputTag("hltSiStripClusters")

        for paramName, param in process.hltIter2HighPtTkMuMaskedMeasurementTrackerEvent.parameters_().iteritems() :

            if not paramName.find("ToSkip") >= 0 :
                setattr(producerPhase2,paramName,param)
            else :
                setattr(producerPhase2,"phase2clustersToSkip",param)

        process.hltIter2HighPtTkMuMaskedMeasurementTrackerEvent = producerPhase2

    if hasattr(process,"hltIter2HighPtTkMuIsoMaskedMeasurementTrackerEvent") :
        print "[customiseTrackerEventProducer] customise hltIter2HighPtTkMuIsoMaskedMeasurementTrackerEvent"

        producerPhase2 = cms.EDProducer("MaskedMeasurementTrackerEventProducer")
        producerPhase2.phase2clustersToSkip = cms.InputTag("hltSiStripClusters")

        for paramName, param in process.hltIter2HighPtTkMuIsoMaskedMeasurementTrackerEvent.parameters_().iteritems() :

            if not paramName.find("ToSkip") >= 0 :
                setattr(producerPhase2,paramName,param)
            else :
                setattr(producerPhase2,"phase2clustersToSkip",param)
                

        process.hltIter2HighPtTkMuIsoMaskedMeasurementTrackerEvent = producerPhase2

    if hasattr(process,"hltIter1HighPtTkMuIsoMaskedMeasurementTrackerEvent") :
        print "[customiseTrackerEventProducer] customise hltIter1HighPtTkMuIsoMaskedMeasurementTrackerEvent"

        producerPhase2 = cms.EDProducer("MaskedMeasurementTrackerEventProducer")
        producerPhase2.phase2clustersToSkip = cms.InputTag("hltSiStripClusters")
       
        for paramName, param in process.hltIter1HighPtTkMuIsoMaskedMeasurementTrackerEvent.parameters_().iteritems() :

            if not paramName.find("ToSkip") >= 0 :
                setattr(producerPhase2,paramName,param)
            else :
                setattr(producerPhase2,"phase2clustersToSkip",param)

        process.hltIter1HighPtTkMuIsoMaskedMeasurementTrackerEvent = producerPhase2

    return process


def customiseTkMuTrackerReco(process):

    if hasattr(process,"hltESPTTRHBWithTrackAngle") :
        print "[customiseTkMuTrackerReco] customise customiseTkMuTrackerReco"

        # process.hltESPTTRHBWithTrackAngle.StripCPE = ""
        process.hltESPTTRHBWithTrackAngle.Phase2StripCPE = cms.string('Phase2StripCPE')

    return process

