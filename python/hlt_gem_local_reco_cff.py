import FWCore.ParameterSet.Config as cms

hltGemRecHits = cms.EDProducer("GEMRecHitProducer",
    recAlgoConfig = cms.PSet(

    ),
    recAlgo = cms.string('GEMRecHitStandardAlgo'),
    gemDigiLabel = cms.InputTag("simMuonGEMDigis")
)

hltGemSegments = cms.EDProducer("GEMSegmentProducer",
    gemRecHitLabel = cms.InputTag("hltGemRecHits"),
    algo_name = cms.string("GEMSegmentAlgorithm"),
    algo_pset = cms.PSet(
        GEMDebug = cms.untracked.bool(True),
        minHitsPerSegment = cms.uint32(2),
        preClustering = cms.bool(True),            # False => all hits in chamber are given to the fitter 
        dXclusBoxMax = cms.double(1.),             # Clstr Hit dPhi
        dYclusBoxMax = cms.double(5.),             # Clstr Hit dEta
        preClusteringUseChaining = cms.bool(True), # True ==> use Chaining() , False ==> use Clustering() Fnct
        dPhiChainBoxMax = cms.double(.02),         # Chain Hit dPhi
        dEtaChainBoxMax = cms.double(.05),         # Chain Hit dEta
        maxRecHitsInCluster = cms.int32(4),        # Does 4 make sense here?
        clusterOnlySameBXRecHits = cms.bool(True), # only working for (preClustering && preClusteringUseChaining)
    ),
)

hltMe0RecHits = cms.EDProducer("ME0RecHitProducer",
    recAlgoConfig = cms.PSet(),
    recAlgo = cms.string('ME0RecHitStandardAlgo'),
    me0DigiLabel = cms.InputTag("simMuonME0ReDigis"),
)

hltMe0Segments = cms.EDProducer("ME0SegmentProducer",
    me0RecHitLabel = cms.InputTag("hltMe0RecHits"),
    algo_name = cms.string("ME0SegmentAlgorithm"),                             
    algo_pset = cms.PSet(
        ME0Debug = cms.untracked.bool(True),
        minHitsPerSegment = cms.uint32(3),
        preClustering = cms.bool(True),
        dXclusBoxMax = cms.double(1.),
        dYclusBoxMax = cms.double(5.),
        preClusteringUseChaining = cms.bool(True),
        dPhiChainBoxMax = cms.double(.02),
        dEtaChainBoxMax = cms.double(.15),
        dTimeChainBoxMax = cms.double(15.0), # 1ns, +/- time to fly through 30cm thick ME0
        maxRecHitsInCluster = cms.int32(6)
    )
)

HLTMuonGemLocalRecoSequence = cms.Sequence( cms.ignore(hltGemRecHits) 
                                            + cms.ignore(hltGemSegments) 
                                            + cms.ignore(hltMe0RecHits)
                                            + cms.ignore(hltMe0Segments))
