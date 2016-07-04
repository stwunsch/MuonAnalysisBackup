import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring(),
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1))

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.Reconstruction_cff")

import os
if "CMSSW_8_0_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('80X_mcRun2_asymptotic_v4')
    process.source.fileNames = [
        '/store/relval/CMSSW_8_0_0/RelValZMM_13/GEN-SIM-RECO/PU25ns_80X_mcRun2_asymptotic_v4-v1/10000/382BADA2-A3DA-E511-9E07-0CC47A4D769E.root',
        '/store/relval/CMSSW_8_0_0/RelValZMM_13/GEN-SIM-RECO/PU25ns_80X_mcRun2_asymptotic_v4-v1/10000/6200B483-9EDA-E511-A354-0CC47A4D7636.root',
        '/store/relval/CMSSW_8_0_0/RelValZMM_13/GEN-SIM-RECO/PU25ns_80X_mcRun2_asymptotic_v4-v1/10000/70B70BFF-32DB-E511-A4C6-0CC47A4C8E1C.root',
        '/store/relval/CMSSW_8_0_0/RelValZMM_13/GEN-SIM-RECO/PU25ns_80X_mcRun2_asymptotic_v4-v1/10000/80CC4165-9FDA-E511-815B-0CC47A78A4A0.root',
        '/store/relval/CMSSW_8_0_0/RelValZMM_13/GEN-SIM-RECO/PU25ns_80X_mcRun2_asymptotic_v4-v1/10000/80F7131A-33DB-E511-A2B5-0CC47A4D75F6.root',
        '/store/relval/CMSSW_8_0_0/RelValZMM_13/GEN-SIM-RECO/PU25ns_80X_mcRun2_asymptotic_v4-v1/10000/8AC339C5-A0DA-E511-9B02-0CC47A4C8E96.root',
        '/store/relval/CMSSW_8_0_0/RelValZMM_13/GEN-SIM-RECO/PU25ns_80X_mcRun2_asymptotic_v4-v1/10000/D279741B-9EDA-E511-A88D-0025905A6110.root',
    ]
else: raise RuntimeError, "Unknown CMSSW version %s" % os.environ['CMSSW_VERSION']

## SELECT WHAT DATASET YOU'RE RUNNING ON
TRIGGER="SingleMu"
#TRIGGER="Any"

## ==== Fast Filters ====
process.goodVertexFilter = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && ndof > 4 && abs(z) <= 25 && position.Rho <= 2"),
    filter = cms.bool(True),
)
process.noScraping = cms.EDFilter("FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
    debugOn = cms.untracked.bool(False), ## Or 'True' to get some per-event info
    numtrack = cms.untracked.uint32(10),
    thresh = cms.untracked.double(0.25)
)
process.fastFilter = cms.Sequence(process.goodVertexFilter + process.noScraping)

##    __  __                       
##   |  \/  |_   _  ___  _ __  ___ 
##   | |\/| | | | |/ _ \| '_ \/ __|
##   | |  | | |_| | (_) | | | \__ \
##   |_|  |_|\__,_|\___/|_| |_|___/
##                                 
## ==== Merge CaloMuons and Tracks into the collection of reco::Muons  ====
from RecoMuon.MuonIdentification.calomuons_cfi import calomuons;
process.mergedMuons = cms.EDProducer("CaloMuonMerger",
    mergeTracks = cms.bool(True),
    mergeCaloMuons = cms.bool(False), # AOD
    muons     = cms.InputTag("muons"), 
    caloMuons = cms.InputTag("calomuons"),
    tracks    = cms.InputTag("generalTracks"),
    minCaloCompatibility = calomuons.minCaloCompatibility,
    ## Apply some minimal pt cut
    muonsCut     = cms.string("pt > 3 && track.isNonnull"),
    caloMuonsCut = cms.string("pt > 3"),
    tracksCut    = cms.string("pt > 3"),
)

## ==== Trigger matching
process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")
## with some customization
process.muonMatchHLTL2.maxDeltaR = 0.3 # Zoltan tuning - it was 0.5
process.muonMatchHLTL3.maxDeltaR = 0.1
from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import *
changeRecoMuonInput(process, "mergedMuons")
#useExtendedL1Match(process) #MM no idea what the sequence did, not available since git migration
#addHLTL1Passthrough(process)
#changeTriggerProcessName(process, "*") # auto-guess

from MuonAnalysis.TagAndProbe.common_variables_cff import *
process.load("MuonAnalysis.TagAndProbe.common_modules_cff")

process.tagMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("pt > 15 && "+MuonIDFlags.Tight2012.value()+
                     " && pfIsolationR04().sumChargedHadronPt/pt < 0.2"),
)
if TRIGGER != "SingleMu":
    process.tagMuons.cut = ("pt > 6 && (isGlobalMuon || isTrackerMuon) && isPFMuon "+
                            " && pfIsolationR04().sumChargedHadronPt/pt < 0.2")

process.oneTag  = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tagMuons"), minNumber = cms.uint32(1))

process.probeMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("track.isNonnull"),  # no real cut now
)

process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    #cut = cms.string('60 < mass < 140 && abs(daughter(0).vz - daughter(1).vz) < 4'),
    cut = cms.string('60 < mass && abs(daughter(0).vz - daughter(1).vz) < 4'),
    decay = cms.string('tagMuons@+ probeMuons@-')
)
process.onePair = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tpPairs"), minNumber = cms.uint32(1))

process.tagMuonsMCMatch = cms.EDProducer("MCMatcher", # cut on deltaR, deltaPt/Pt; pick best by deltaR
    src     = cms.InputTag("tagMuons"), # RECO objects to match
    matched = cms.InputTag("goodGenMuons"),   # mc-truth particle collection
    mcPdgId     = cms.vint32(13),  # one or more PDG ID (13 = muon); absolute values (see below)
    checkCharge = cms.bool(False), # True = require RECO and MC objects to have the same charge
    mcStatus = cms.vint32(1),      # PYTHIA status code (1 = stable, 2 = shower, 3 = hard scattering)
    maxDeltaR = cms.double(0.3),   # Minimum deltaR for the match
    maxDPtRel = cms.double(0.5),   # Minimum deltaPt/Pt for the match
    resolveAmbiguities = cms.bool(True),    # Forbid two RECO objects to match to the same GEN object
    resolveByMatchQuality = cms.bool(True), # False = just match input in order; True = pick lowest deltaR pair first
)
process.probeMuonsMCMatch = process.tagMuonsMCMatch.clone(src = "probeMuons", maxDeltaR = 0.3, maxDPtRel = 1.0, resolveAmbiguities = False,  resolveByMatchQuality = False)

from MuonAnalysis.TagAndProbe.muon.tag_probe_muon_extraIso_cff import ExtraIsolationVariables

process.load("MuonAnalysis.TagAndProbe.mvaIsoVariables_cff")
from MuonAnalysis.TagAndProbe.mvaIsoVariables_cff import MVAIsoVariablesPlain, MVAIsoVariablesPlainTag
process.load("MuonAnalysis.TagAndProbe.radialIso_cfi")


from MuonAnalysis.TagAndProbe.puppiIso_cfi import load_fullPFpuppiIsolation
process.fullPuppIsolationSequence = load_fullPFpuppiIsolation(process)
from MuonAnalysis.TagAndProbe.puppiIso_cff import PuppiIsolationVariables

process.tpTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
    # choice of tag and probe pairs, and arbitration
    tagProbePairs = cms.InputTag("tpPairs"),
    arbitration   = cms.string("None"),
    # probe variables: all useful ones
    variables = cms.PSet(
        AllVariables,
        ExtraIsolationVariables,
        PuppiIsolationVariables,
        MVAIsoVariablesPlain, 
        isoTrk03Abs = cms.InputTag("probeMuonsIsoValueMaps","probeMuonsIsoFromDepsTk"),
        isoTrk03Rel = cms.InputTag("probeMuonsIsoValueMaps","probeMuonsRelIsoFromDepsTk"),
        dxyBS = cms.InputTag("muonDxyPVdzmin","dxyBS"),
        dxyPVdzmin = cms.InputTag("muonDxyPVdzmin","dxyPVdzmin"),
        dzPV = cms.InputTag("muonDxyPVdzmin","dzPV"),
        PtRatio= cms.InputTag("AddPtRatioPtRel","PtRatio"),
        PtRel= cms.InputTag("AddPtRatioPtRel","PtRel"),
        radialIso = cms.InputTag("radialIso"), 
        miniIsoCharged = cms.InputTag("muonMiniIsoCharged","miniIso"), 
        activity_miniIsoCharged = cms.InputTag("muonMiniIsoCharged","activity"), 
        miniIsoPUCharged = cms.InputTag("muonMiniIsoPUCharged","miniIso"), 
        activity_miniIsoPUCharged = cms.InputTag("muonMiniIsoPUCharged","activity"), 
        miniIsoNeutrals = cms.InputTag("muonMiniIsoNeutrals","miniIso"), 
        activity_miniIsoNeutrals = cms.InputTag("muonMiniIsoNeutrals","activity"), 
        miniIsoPhotons = cms.InputTag("muonMiniIsoPhotons","miniIso"), 
        activity_miniIsoPhotons = cms.InputTag("muonMiniIsoPhotons","activity"), 
        nSplitTk  = cms.InputTag("splitTrackTagger"),
        mt  = cms.InputTag("probeMetMt","mt"),
    ),
    flags = cms.PSet(
       TrackQualityFlags,
       MuonIDFlags,
       HighPtTriggerFlags,
       HighPtTriggerFlagsDebug,
    ),
    tagVariables = cms.PSet(
     #   TriggerVariables, 
     #   MVAIsoVariablesPlainTag, 
     #   pt = cms.string("pt"),
     #   eta = cms.string("eta"),
     #   phi = cms.string("phi"),
     #   combRelIso = cms.string("(isolationR03.emEt + isolationR03.hadEt + isolationR03.sumPt)/pt"),
     #   chargedHadIso04 = cms.string("pfIsolationR04().sumChargedHadronPt"),
     #   neutralHadIso04 = cms.string("pfIsolationR04().sumNeutralHadronEt"),
     #   photonIso04 = cms.string("pfIsolationR04().sumPhotonEt"),
     #   combRelIsoPF04dBeta = IsolationVariables.combRelIsoPF04dBeta,
     #   combRelIsoPF03dBeta = IsolationVariables.combRelIsoPF03dBeta,
     #   dzPV = cms.InputTag("muonDxyPVdzminTags","dzPV"),
        AllVariables,
        ExtraIsolationVariables,
        MVAIsoVariablesPlain, 
        nVertices   = cms.InputTag("nverticesModule"),
        isoTrk03Abs = cms.InputTag("probeMuonsIsoValueMaps","probeMuonsIsoFromDepsTk"),
        isoTrk03Rel = cms.InputTag("probeMuonsIsoValueMaps","probeMuonsRelIsoFromDepsTk"),
        dxyBS = cms.InputTag("muonDxyPVdzminTags","dxyBS"),
        dxyPVdzmin = cms.InputTag("muonDxyPVdzminTags","dxyPVdzmin"),
        dzPV = cms.InputTag("muonDxyPVdzminTags","dzPV"),
        radialIso = cms.InputTag("radialIso"), 
        nSplitTk  = cms.InputTag("splitTrackTagger"),
        met = cms.InputTag("tagMetMt","met"),
        mt  = cms.InputTag("tagMetMt","mt"),
    ),
    tagFlags = cms.PSet(HighPtTriggerFlags,HighPtTriggerFlagsDebug),
    pairVariables = cms.PSet(
        nJets30 = cms.InputTag("njets30Module"),
        dz      = cms.string("daughter(0).vz - daughter(1).vz"),
        pt      = cms.string("pt"), 
        rapidity = cms.string("rapidity"),
        deltaR   = cms.string("deltaR(daughter(0).eta, daughter(0).phi, daughter(1).eta, daughter(1).phi)"), 
        probeMultiplicity = cms.InputTag("probeMultiplicity"),
        probeMultiplicity_TMGM = cms.InputTag("probeMultiplicityTMGM"),
        probeMultiplicity_Pt10_M60140 = cms.InputTag("probeMultiplicityPt10M60140"),
        ## Gen Weight variable
        genWeight = cms.InputTag("genWeightInfo", "genWeight"),
        ## New TuneP variables
        newTuneP_probe_pt            = cms.InputTag("newTunePVals", "pt"),
        newTuneP_probe_sigmaPtOverPt = cms.InputTag("newTunePVals", "ptRelError"),
        newTuneP_probe_trackType     = cms.InputTag("newTunePVals", "trackType"),
        newTuneP_mass                = cms.InputTag("newTunePVals", "mass"),
    ),
    pairFlags = cms.PSet(
        BestZ = cms.InputTag("bestPairByZMass"),
    ),
    isMC           = cms.bool(True),
    addRunLumiInfo = cms.bool(True),
    tagMatches       = cms.InputTag("tagMuonsMCMatch"),
    probeMatches     = cms.InputTag("probeMuonsMCMatch"),
    motherPdgId      = cms.vint32(22, 23),
    makeMCUnbiasTree       = cms.bool(False), 
    checkMotherInUnbiasEff = cms.bool(True),
    allProbes              = cms.InputTag("probeMuons"),
)
if TRIGGER != "SingleMu":
    for K,F in MuonIDFlags.parameters_().iteritems():
        setattr(process.tpTree.tagFlags, K, F)


process.load("MuonAnalysis.TagAndProbe.muon.tag_probe_muon_extraIso_cfi")
process.load("PhysicsTools.PatAlgos.recoLayer0.pfParticleSelectionForIso_cff")

process.miniIsoSeq = cms.Sequence(
    process.pfParticleSelectionForIsoSequence +
    process.muonMiniIsoCharged + 
    process.muonMiniIsoPUCharged + 
    process.muonMiniIsoNeutrals + 
    process.muonMiniIsoPhotons 
)

# process.load("JetMETCorrections.Configuration.JetCorrectionProducersAllAlgos_cff")
# process.ak4PFCHSJetsL1L2L3 = process.ak4PFCHSJetsL1.clone( correctors = ['ak4PFCHSL1FastL2L3'] )

process.extraProbeVariablesSeq = cms.Sequence(
    process.probeMuonsIsoSequence +
    process.computeCorrectedIso + 
    process.mvaIsoVariablesSeq * process.mvaIsoVariablesTag * process.radialIso +
    process.splitTrackTagger +
    process.muonDxyPVdzmin + 
    process.probeMetMt + process.tagMetMt +
    process.miniIsoSeq +
    # process.ak4PFCHSJetsL1L2L3 +
    process.ak4PFCHSL1FastL2L3CorrectorChain * process.jetAwareCleaner +
    process.AddPtRatioPtRel +
    process.fullPuppIsolationSequence
)

process.tnpSimpleSequence = cms.Sequence(
    process.goodGenMuons +
    process.tagMuons   * process.tagMuonsMCMatch   +
    process.oneTag     +
    process.probeMuons * process.probeMuonsMCMatch +
    process.tpPairs    +
    process.onePair    +
    process.nverticesModule +
    process.njets30Module +
    process.extraProbeVariablesSeq +
    process.probeMultiplicities + 
    process.bestPairByZMass + 
    process.newTunePVals +
    process.genWeightInfo +
    process.muonDxyPVdzminTags +
    process.tpTree
)

process.tagAndProbe = cms.Path( 
    process.fastFilter +
    process.mergedMuons                 *
    process.patMuonsWithTriggerSequence +
    process.tnpSimpleSequence
)

##    _____               _    _             
##   |_   _| __ __ _  ___| | _(_)_ __   __ _ 
##     | || '__/ _` |/ __| |/ / | '_ \ / _` |
##     | || | | (_| | (__|   <| | | | | (_| |
##     |_||_|  \__,_|\___|_|\_\_|_| |_|\__, |
##                                     |___/ 

## Then make another collection for standalone muons, using standalone track to define the 4-momentum
process.muonsSta = cms.EDProducer("RedefineMuonP4FromTrack",
    src   = cms.InputTag("muons"),
    track = cms.string("outer"),
)
## Match to trigger, to measure the efficiency of HLT tracking
from PhysicsTools.PatAlgos.tools.helpers import *
process.patMuonsWithTriggerSequenceSta = cloneProcessingSnippet(process, process.patMuonsWithTriggerSequence, "Sta")
process.muonMatchHLTL2Sta.maxDeltaR = 0.5
process.muonMatchHLTL3Sta.maxDeltaR = 0.5
massSearchReplaceAnyInputTag(process.patMuonsWithTriggerSequenceSta, "mergedMuons", "muonsSta")

## Define probes and T&P pairs
process.probeMuonsSta = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTriggerSta"),
    cut = cms.string("outerTrack.isNonnull"), # no real cut now
)
process.probeMuonsMCMatchSta = process.tagMuonsMCMatch.clone(src = "probeMuonsSta")

process.tpPairsSta = process.tpPairs.clone(decay = "tagMuons@+ probeMuonsSta@-", cut = '40 < mass < 150')

process.onePairSta = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tpPairsSta"), minNumber = cms.uint32(1))

process.staToTkMatch.maxDeltaR     = 0.3
process.staToTkMatch.maxDeltaPtRel = 2.
process.staToTkMatchNoZ.maxDeltaR     = 0.3
process.staToTkMatchNoZ.maxDeltaPtRel = 2.

process.load("MuonAnalysis.TagAndProbe.tracking_reco_info_cff")


process.tpTreeSta = process.tpTree.clone(
    tagProbePairs = "tpPairsSta",
    arbitration   = "OneProbe",
    variables = cms.PSet(
        KinematicVariables, 
        StaOnlyVariables,
        ## track matching variables
        tk_deltaR     = cms.InputTag("staToTkMatch","deltaR"),
        tk_deltaEta   = cms.InputTag("staToTkMatch","deltaEta"),
        tk_deltaR_NoZ   = cms.InputTag("staToTkMatchNoZ","deltaR"),
        tk_deltaEta_NoZ = cms.InputTag("staToTkMatchNoZ","deltaEta"),
    ),
    flags = cms.PSet(
        outerValidHits = cms.string("outerTrack.numberOfValidHits > 0"),
        TM  = cms.string("isTrackerMuon"),
        Glb = cms.string("isGlobalMuon"),
        Tk  = cms.string("track.isNonnull"),
        StaTkSameCharge = cms.string("outerTrack.isNonnull && innerTrack.isNonnull && (outerTrack.charge == innerTrack.charge)"),
    ),
    tagVariables = cms.PSet(
        pt = cms.string("pt"),
        eta = cms.string("eta"),
        phi = cms.string("phi"),
        vz = cms.string("vz"), #Z point of closest approach of the track to the beam line 
        nVertices = cms.InputTag("nverticesModule"),
        combRelIso = cms.string("(isolationR03.emEt + isolationR03.hadEt + isolationR03.sumPt)/pt"),
        chargedHadIso04 = cms.string("pfIsolationR04().sumChargedHadronPt"),
        neutralHadIso04 = cms.string("pfIsolationR04().sumNeutralHadronEt"),
        photonIso04 = cms.string("pfIsolationR04().sumPhotonEt"),
        combRelIsoPF04dBeta = IsolationVariables.combRelIsoPF04dBeta,
    ),
    pairVariables = cms.PSet(
        nJets30 = cms.InputTag("njets30ModuleSta"),
        dz      = cms.string("daughter(0).vz - daughter(1).vz"),
        pt      = cms.string("pt"), 
        rapidity = cms.string("rapidity"),
        deltaR   = cms.string("deltaR(daughter(0).eta, daughter(0).phi, daughter(1).eta, daughter(1).phi)"), 
    ),
    pairFlags = cms.PSet(),
    allProbes     = "probeMuonsSta",
    probeMatches  = "probeMuonsMCMatchSta",
)
process.njets30ModuleSta = process.njets30Module.clone(pairs = "tpPairsSta")

process.tnpSimpleSequenceSta = cms.Sequence(
    process.tagMuons   * process.tagMuonsMCMatch   +
    process.oneTag     +
    process.probeMuonsSta * process.probeMuonsMCMatchSta +
    process.tpPairsSta      +
    process.onePairSta      +
    process.nverticesModule +
    process.staToTkMatchSequenceZ +
    process.njets30ModuleSta +
    process.tpTreeSta
)

## Add extra RECO-level info
if False:
    process.tnpSimpleSequenceSta.replace(process.tpTreeSta, process.tkClusterInfo+process.tpTreeSta)
    process.tpTreeSta.tagVariables.nClustersStrip = cms.InputTag("tkClusterInfo","siStripClusterCount")
    process.tpTreeSta.tagVariables.nClustersPixel = cms.InputTag("tkClusterInfo","siPixelClusterCount")
    process.tnpSimpleSequenceSta.replace(process.tpTreeSta, process.tkLogErrors+process.tpTreeSta)
    process.tpTreeSta.tagVariables.nLogErrFirst = cms.InputTag("tkLogErrors","firstStep")
    process.tpTreeSta.tagVariables.nLogErrPix   = cms.InputTag("tkLogErrors","pixelSteps")
    process.tpTreeSta.tagVariables.nLogErrAny   = cms.InputTag("tkLogErrors","anyStep")

if True: 
    process.tracksNoMuonSeeded = cms.EDFilter("TrackSelector",
      src = cms.InputTag("generalTracks"),
      cut = cms.string(" || ".join("isAlgoInMask('%s')" % a for a in [
                    'initialStep', 'lowPtTripletStep', 'pixelPairStep', 'detachedTripletStep',
                    'mixedTripletStep', 'pixelLessStep', 'tobTecStep', 'jetCoreRegionalStep'] ) )
    )
    process.pCutTracks0 = process.pCutTracks.clone(src = 'tracksNoMuonSeeded')
    #process.pCutTracks0 = process.pCutTracks.clone(src = 'earlyGeneralTracks')
    process.tkTracks0 = process.tkTracks.clone(src = 'pCutTracks0')
    process.tkTracksNoZ0 = process.tkTracksNoZ.clone(src = 'tkTracks0')
    process.preTkMatchSequenceZ.replace(
            process.tkTracksNoZ, process.tkTracksNoZ +
            process.tracksNoMuonSeeded + process.pCutTracks0 + process.tkTracks0 + process.tkTracksNoZ0)
    #        process.pCutTracks0 + process.tkTracks0 + process.tkTracksNoZ0)
    process.staToTkMatch0 = process.staToTkMatch.clone(matched = 'tkTracks0')
    process.staToTkMatchNoZ0 = process.staToTkMatchNoZ.clone(matched = 'tkTracksNoZ0')
    process.staToTkMatchSequenceZ.replace( process.staToTkMatch, process.staToTkMatch + process.staToTkMatch0 )
    process.staToTkMatchSequenceZ.replace( process.staToTkMatchNoZ, process.staToTkMatchNoZ + process.staToTkMatchNoZ0 )
    process.tpTreeSta.variables.tk0_deltaR     = cms.InputTag("staToTkMatch0","deltaR")
    process.tpTreeSta.variables.tk0_deltaEta   = cms.InputTag("staToTkMatch0","deltaEta")
    process.tpTreeSta.variables.tk0_deltaR_NoZ   = cms.InputTag("staToTkMatchNoZ0","deltaR")
    process.tpTreeSta.variables.tk0_deltaEta_NoZ = cms.InputTag("staToTkMatchNoZ0","deltaEta")

process.tagAndProbeSta = cms.Path( 
    process.fastFilter +
    process.muonsSta                       +
    process.patMuonsWithTriggerSequenceSta +
    process.tnpSimpleSequenceSta
)


if True: # turn on for tracking efficiency using gen particles as probe
    process.probeGen = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("genParticles"),
        cut = cms.string("abs(pdgId) == 13 && pt > 3 && abs(eta) < 2.4 && isPromptFinalState"),
    )
    process.tpPairsTkGen = process.tpPairs.clone(decay = "tagMuons@+ probeGen@-", cut = '40 < mass < 150')
    process.genToTkMatch    = process.staToTkMatch.clone(src = "probeGen", srcTrack="none")
    process.genToTkMatchNoZ = process.staToTkMatchNoZ.clone(src = "probeGen", srcTrack="none")
    process.genToTkMatch0    = process.staToTkMatch0.clone(src = "probeGen", srcTrack="none")
    process.genToTkMatchNoZ0 = process.staToTkMatchNoZ0.clone(src = "probeGen", srcTrack="none")
    process.probeMuonsMCMatchGen = process.tagMuonsMCMatch.clone(src = "probeGen")
    process.tpTreeGen = process.tpTreeSta.clone(
        tagProbePairs = "tpPairsTkGen",
        arbitration   = "OneProbe",
        variables = cms.PSet(
            KinematicVariables, 
            ## track matching variables
            tk_deltaR     = cms.InputTag("genToTkMatch","deltaR"),
            tk_deltaEta   = cms.InputTag("genToTkMatch","deltaEta"),
            tk_deltaR_NoZ   = cms.InputTag("genToTkMatchNoZ","deltaR"),
            tk_deltaEta_NoZ = cms.InputTag("genToTkMatchNoZ","deltaEta"),
            ## track matching variables (early general tracks)
            tk0_deltaR     = cms.InputTag("genToTkMatch0","deltaR"),
            tk0_deltaEta   = cms.InputTag("genToTkMatch0","deltaEta"),
            tk0_deltaR_NoZ   = cms.InputTag("genToTkMatchNoZ0","deltaR"),
            tk0_deltaEta_NoZ = cms.InputTag("genToTkMatchNoZ0","deltaEta"),
        ),
        flags = cms.PSet(
        ),
        tagVariables = cms.PSet(
            pt = cms.string("pt"),
            eta = cms.string("eta"),
            phi = cms.string("phi"),
            nVertices   = cms.InputTag("nverticesModule"),
            combRelIso = cms.string("(isolationR03.emEt + isolationR03.hadEt + isolationR03.sumPt)/pt"),
            chargedHadIso04 = cms.string("pfIsolationR04().sumChargedHadronPt"),
            neutralHadIso04 = cms.string("pfIsolationR04().sumNeutralHadronEt"),
            photonIso04 = cms.string("pfIsolationR04().sumPhotonEt"),
            combRelIsoPF04dBeta = IsolationVariables.combRelIsoPF04dBeta,
        ),
        pairVariables = cms.PSet(
            #nJets30 = cms.InputTag("njets30ModuleSta"),
            dz      = cms.string("daughter(0).vz - daughter(1).vz"),
            pt      = cms.string("pt"), 
            rapidity = cms.string("rapidity"),
            deltaR   = cms.string("deltaR(daughter(0).eta, daughter(0).phi, daughter(1).eta, daughter(1).phi)"), 
        ),
        pairFlags = cms.PSet(),
        allProbes     = cms.InputTag("probeGen"),
        probeMatches  = cms.InputTag("probeMuonsMCMatchGen"),
    )
    process.tagAndProbeTkGen = cms.Path( 
        process.fastFilter +
        process.probeGen +
        process.tpPairsTkGen + 
        process.preTkMatchSequenceZ + 
        process.genToTkMatch + process.genToTkMatchNoZ +
        process.genToTkMatch0 + process.genToTkMatchNoZ0 +
        process.probeMuonsMCMatchGen +
        process.nverticesModule +
        process.tpTreeGen
    )

if True: # turn on for tracking efficiency using L1 seeds
    process.probeL1 = cms.EDFilter("CandViewSelector",
        src = cms.InputTag("l1extraParticles"),
        cut = cms.string("pt >= 5 && abs(eta) < 2.4"),
    )
    process.tpPairsTkL1 = process.tpPairs.clone(decay = "tagMuons@+ probeL1@-", cut = 'mass > 30')
    process.l1ToTkMatch    = process.staToTkMatch.clone(src = "probeL1", srcTrack="none")
    process.l1ToTkMatchNoZ = process.staToTkMatchNoZ.clone(src = "probeL1", srcTrack="none")
    process.l1ToTkMatch0    = process.staToTkMatch0.clone(src = "probeL1", srcTrack="none")
    process.l1ToTkMatchNoZ0 = process.staToTkMatchNoZ0.clone(src = "probeL1", srcTrack="none")
    process.probeMuonsMCMatchL1 = process.tagMuonsMCMatch.clone(src = "probeL1")
    process.tpTreeL1 = process.tpTreeSta.clone(
        tagProbePairs = "tpPairsTkL1",
        arbitration   = "OneProbe",
        variables = cms.PSet(
            KinematicVariables, 
            bx = cms.string("bx"),
            quality = cms.string("gmtMuonCand.quality"),
            ## track matching variables
            tk_deltaR     = cms.InputTag("l1ToTkMatch","deltaR"),
            tk_deltaEta   = cms.InputTag("l1ToTkMatch","deltaEta"),
            tk_deltaR_NoZ   = cms.InputTag("l1ToTkMatchNoZ","deltaR"),
            tk_deltaEta_NoZ = cms.InputTag("l1ToTkMatchNoZ","deltaEta"),
            ## track matching variables (early general tracks)
            tk0_deltaR     = cms.InputTag("l1ToTkMatch0","deltaR"),
            tk0_deltaEta   = cms.InputTag("l1ToTkMatch0","deltaEta"),
            tk0_deltaR_NoZ   = cms.InputTag("l1ToTkMatchNoZ0","deltaR"),
            tk0_deltaEta_NoZ = cms.InputTag("l1ToTkMatchNoZ0","deltaEta"),
        ),
        flags = cms.PSet(
        ),
        tagVariables = cms.PSet(
            pt = cms.string("pt"),
            eta = cms.string("eta"),
            phi = cms.string("phi"),
            nVertices   = cms.InputTag("nverticesModule"),
            combRelIso = cms.string("(isolationR03.emEt + isolationR03.hadEt + isolationR03.sumPt)/pt"),
            chargedHadIso04 = cms.string("pfIsolationR04().sumChargedHadronPt"),
            neutralHadIso04 = cms.string("pfIsolationR04().sumNeutralHadronEt"),
            photonIso04 = cms.string("pfIsolationR04().sumPhotonEt"),
            combRelIsoPF04dBeta = IsolationVariables.combRelIsoPF04dBeta,
        ),
        pairVariables = cms.PSet(
            #nJets30 = cms.InputTag("njets30ModuleSta"),
            pt      = cms.string("pt"),
            rapidity = cms.string("rapidity"),
            deltaR   = cms.string("deltaR(daughter(0).eta, daughter(0).phi, daughter(1).eta, daughter(1).phi)"), 
        ),
        pairFlags = cms.PSet(),
        allProbes     = cms.InputTag("probeL1"),
        probeMatches  = cms.InputTag("probeMuonsMCMatchL1"),
    )
    process.tagAndProbeTkL1 = cms.Path(
        process.fastFilter +
        process.probeL1 +
        process.tpPairsTkL1 +
        process.preTkMatchSequenceZ +
        process.l1ToTkMatch + process.l1ToTkMatchNoZ +
        process.l1ToTkMatch0 + process.l1ToTkMatchNoZ0 +
        process.probeMuonsMCMatchL1 +
        process.nverticesModule +
        process.tpTreeL1
    )


##    _____     _          ____       _            
##   |  ___|_ _| | _____  |  _ \ __ _| |_ ___  ___ 
##   | |_ / _` | |/ / _ \ | |_) / _` | __/ _ \/ __|
##   |  _| (_| |   <  __/ |  _ < (_| | ||  __/\__ \
##   |_|  \__,_|_|\_\___| |_| \_\__,_|\__\___||___/
##                                                 
##   
process.load("MuonAnalysis.TagAndProbe.fakerate_all_cff")

process.fakeRateJetPlusProbeTree = process.tpTree.clone(
    tagProbePairs = 'jetPlusProbe',
    arbitration   = 'None', 
    tagVariables = process.JetPlusProbeTagVariables,
    tagFlags = cms.PSet(),
    pairVariables = cms.PSet(deltaPhi = cms.string("deltaPhi(daughter(0).phi, daughter(1).phi)")), 
    pairFlags     = cms.PSet(), 
    isMC = False, # MC matches not in place for FR yet
)
process.fakeRateWPlusProbeTree = process.tpTree.clone(
    tagProbePairs = 'wPlusProbe',
    arbitration   = 'None', 
    tagVariables = process.WPlusProbeTagVariables,
    tagFlags = cms.PSet(),
    pairVariables = cms.PSet(), 
    pairFlags     = cms.PSet(SameSign = cms.string('daughter(0).daughter(0).charge == daughter(1).charge')), 
    isMC = False, # MC matches not in place for FR yet
)
process.fakeRateZPlusProbeTree = process.tpTree.clone(
    tagProbePairs = 'zPlusProbe',
    arbitration   = 'None', 
    tagVariables  = process.ZPlusProbeTagVariables,
    tagFlags      = cms.PSet(),
    pairVariables = cms.PSet(), 
    pairFlags     = cms.PSet(), 
    isMC = False, # MC matches not in place for FR yet
)

process.fakeRateJetPlusProbe = cms.Path(
    process.fastFilter +
    process.mergedMuons * process.patMuonsWithTriggerSequence +
    process.tagMuons + process.probeMuons + process.extraProbeVariablesSeq + 
    process.jetPlusProbeSequence +
    process.fakeRateJetPlusProbeTree
)
process.fakeRateWPlusProbe = cms.Path(
    process.fastFilter +
    process.mergedMuons * process.patMuonsWithTriggerSequence +
    process.tagMuons + process.probeMuons + process.extraProbeVariablesSeq + 
    process.wPlusProbeSequence +
    process.fakeRateWPlusProbeTree
)
process.fakeRateZPlusProbe = cms.Path(
    process.fastFilter +
    process.mergedMuons * process.patMuonsWithTriggerSequence +
    process.tagMuons + process.probeMuons + process.extraProbeVariablesSeq + 
    process.zPlusProbeSequence +
    process.fakeRateZPlusProbeTree
)

process.schedule = cms.Schedule(
   process.tagAndProbe, 
   process.tagAndProbeSta, 
   process.tagAndProbeTkGen, 
   process.tagAndProbeTkL1, 
   process.fakeRateJetPlusProbe,
   process.fakeRateWPlusProbe,
   process.fakeRateZPlusProbe,
)

process.RandomNumberGeneratorService.tkTracksNoZ  = cms.PSet( initialSeed = cms.untracked.uint32(81) )
process.RandomNumberGeneratorService.tkTracksNoZ0 = cms.PSet( initialSeed = cms.untracked.uint32(81) )


process.TFileService = cms.Service("TFileService", fileName = cms.string("tnpZ_MC.root"))

if True: # enable and do cmsRun tp_from_aod_MC.py /eos/path/to/run/on [ extra_postfix ] to run on all files in that eos path 
    import sys
    args = sys.argv[1:]
    if (sys.argv[0] == "cmsRun"): args = sys.argv[2:]
    scenario = args[0] if len(args) > 0 else ""
    if scenario:
        if scenario.startswith("/"):
            import subprocess
            files = subprocess.check_output([ "/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select", "ls", scenario ])
            process.source.fileNames = [ scenario+"/"+f for f in files.split() ]
            import os.path
            process.TFileService.fileName = "tnpZ_MC_%s.root" % os.path.basename(scenario)
        else:
            process.TFileService.fileName = "tnpZ_MC_%s.root" % scenario
    if len(args) > 1:
        process.TFileService.fileName = process.TFileService.fileName.value().replace(".root", ".%s.root" % args[1])
