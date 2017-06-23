import FWCore.ParameterSet.Config as cms

def customiseTracking(process):

    process = customisePixelLocalReco(process)
    process = customiseStripLocalReco(process)
    process = customiseTrackClusterRemoval(process)
    process = customiseTrackerEventProducer(process)
    process = customiseTkESProducers(process)
    process = customiseL3MuReco(process)

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
               "hltIter2HighPtTkMuClustersRefRemoval",    \
               "hltIter2HighPtTkMuIsoClustersRefRemoval", \
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


def customiseTkESProducers(process):

    for obj in ["ClusterShapeHitFilterESProducer", \
                "hltESPMixedStepClusterShapeHitFilter", \
                "hltESPPixelLessStepClusterShapeHitFilter", \
                "hltESPTobTecStepClusterShapeHitFilter", \
                ] :
        if hasattr(process,obj) :
            print "[customiseTkESProducers] customise PxelShape file for", obj

            getattr(process,obj).PixelShapeFile = cms.string('RecoPixelVertexing/PixelLowPtUtilities/data/pixelShape_Phase2Tk.par')

    for obj in ["hltESPTTRHBWithTrackAngle", \
                "hltESPTTRHBuilderAngleAndTemplate"] :

        if hasattr(process,obj) :
            print "[customiseTkESProducers] customise to Phase2 CPE", obj

            getattr(process,obj).Phase2StripCPE = cms.string('Phase2StripCPE')

    return process


def customiseL3MuReco(process):

    for obj in ["hltIterL3OIMuonTrackCutClassifier"] :

        if hasattr(process,obj) :
            print "[customiseL3MuReco] customise", obj

            getattr(process,obj).ignoreVertices = cms.bool(True)

    return process

#****************************************
# Going beyond "technical" migration
# coping some adjustments from offline 
# (not really used for now)
#****************************************

def customiseLayerLists(process):

    import RecoPixelVertexing.PixelTriplets.quadrupletseedmerging_cff

    for obj in ["hltIter1PixelLayerQuadruplets", \
                "hltPixelLayerQuadruplets", \
                "hltIter1L3MuonPixelLayerQuadruplets", \
                "hltIterL3MuonPixelLayerQuadruplets"
                ] :
        if hasattr(process,obj) :
            print "[customiseLayerLists] customise layerList for high / low pT quadruplets", obj

            getattr(process,obj).layerList = \
                    RecoPixelVertexing.PixelTriplets.quadrupletseedmerging_cff.PixelSeedMergerQuadruplets.layerList.value()
 
    for obj in ["hltIter2L3MuonPixelLayerTriplets", \
                "hltIter2HighPtTkMuPixelLayerTriplets", \
                "hltIter2IterL3MuonPixelLayerTriplets", \
                "hltIter2PixelLayerTriplets"] :

        if hasattr(process,obj) :
            print "[customiseLayerLists] customise layerList for high pT triplets", obj

            getattr(process,obj).layerList = [ 'BPix1+BPix2+BPix3', 'BPix2+BPix3+BPix4',
                                               'BPix1+BPix3+BPix4', 'BPix1+BPix2+BPix4',
                                               'BPix2+BPix3+FPix1_pos', 'BPix2+BPix3+FPix1_neg',
                                               'BPix1+BPix2+FPix1_pos', 'BPix1+BPix2+FPix1_neg',
                                               'BPix2+FPix1_pos+FPix2_pos', 'BPix2+FPix1_neg+FPix2_neg',
                                               'BPix1+FPix1_pos+FPix2_pos', 'BPix1+FPix1_neg+FPix2_neg',
                                               # 'BPix1+BPix2+FPix2_pos', 'BPix1+BPix2+FPix2_neg',
                                               'FPix1_pos+FPix2_pos+FPix3_pos', 'FPix1_neg+FPix2_neg+FPix3_neg',
                                               'BPix1+FPix2_pos+FPix3_pos', 'BPix1+FPix2_neg+FPix3_neg',
                                               # 'BPix1+FPix1_pos+FPix3_pos', 'BPix1+FPix1_neg+FPix3_neg',
                                               'FPix2_pos+FPix3_pos+FPix4_pos', 'FPix2_neg+FPix3_neg+FPix4_neg',
                                               'FPix3_pos+FPix4_pos+FPix5_pos', 'FPix3_neg+FPix4_neg+FPix5_neg',
                                               'FPix4_pos+FPix5_pos+FPix6_pos', 'FPix4_neg+FPix5_neg+FPix6_neg',
                                               'FPix5_pos+FPix6_pos+FPix7_pos', 'FPix5_neg+FPix6_neg+FPix7_neg',
                                               # removed as redunant and covering effectively only eta>4
                                               # (here for documentation, to be optimized after TDR)
                                               # 'FPix6_pos+FPix7_pos+FPix8_pos', 'FPix6_neg+FPix7_neg+FPix8_neg',
                                               # 'FPix6_pos+FPix7_pos+FPix9_pos', 'FPix6_neg+FPix7_neg+FPix9_neg']
                                             ]
    return process

def customiseTrackingRegions(process):
    # Put here as it appears offline, regions are not defined the same way in HLT though ...

    for obj in [""] :

        if hasattr(process,obj) :
            print "[customiseTrackingRegions] customise region (high pT quadruplets)", obj

            getattr(process,obj).RegionPSet.ptMin = cms.double(0.8)

    for obj in [""] :

        if hasattr(process,obj) :
            print "[customiseTrackingRegions] customise region (high pT triplets)", obj

            getattr(process,obj).ptMin = cms.double(0.9)
            getattr(process,obj).originRadius = cms.double(0.9)


    for obj in [""] :

        if hasattr(process,obj) :
            print "[customiseTrackingRegions] customise region (low pT quadruplets)", obj

            getattr(process,obj).RegionPSet.ptMin = cms.double(0.35)

    return process



    
