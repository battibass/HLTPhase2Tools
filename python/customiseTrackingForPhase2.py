import FWCore.ParameterSet.Config as cms

def customiseTracking(process):

    process = customisePixelLocalReco(process)
    process = customiseStripLocalReco(process)

    return process


def customisePixelLocalReco(process):

    if hasattr(process,"hltSiPixelClusters") :
        print "[customisePixelLocalReco] switch to simSiPixelDigis as source"

        process.hltSiPixelClusters.src = cms.InputTag( "simSiPixelDigis","Pixel" )
        process.hltSiPixelClusters.payloadType = cms.string('Offline') # CB to be checked
        process.hltSiPixelClusters.MissCalibrate = cms.untracked.bool(False) 

    #if hasattr(process,"hltSiPixelClustersCache") :
    #    print "[customisePixelLocalReco] switch to simSiPixelDigis as source"
    #    process.hltSiPixelClustersCache.src = cms.InputTag( "simSiPixelDigis","Pixel" )

    #process.siPixelFakeGainOfflineESSource = cms.ESSource("SiPixelFakeGainOfflineESSource",
    #                                                  file = cms.FileInPath('SLHCUpgradeSimulations/Geometry/data/PhaseII/Tilted/EmptyPixelSkimmedGeometry.txt')
    #                                                  )
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
        process.hltSiStripClusters.stripClusterProducer = ''

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
