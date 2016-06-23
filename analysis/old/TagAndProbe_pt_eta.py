"""
Basic Setup
"""

import FWCore.ParameterSet.Config as cms
import numpy as np

process = cms.Process("TagProbe")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

"""
TnP Configuration
"""

process.TnP_Muon_Z_DATA = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    InputFileNames = cms.vstring("file://../data/TnPTree_80X_Run2016B_v2_DCSOnly_RunList.root"),
    #InputFileNames = cms.vstring("file://../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run273731_to_274240_IncludingMissingLumi_Completed.root"),
    OutputFileName = cms.string("TagAndProbe.root"),
    InputTreeName = cms.string("fitter_tree"),
    InputDirectoryName = cms.string("tpTree"),

    # Variables for binning
    Variables = cms.PSet(
        dzPV = cms.vstring('dzPV', '-10.0', '10.0', ''),
        dB = cms.vstring('dB', '0.0', '1.5', ''),
        pair_probeMultiplicity = cms.vstring('pair_probeMultiplicity', '0.20', '30.0', ''),
        mass = cms.vstring('Tag-muon Mass', '70', '110', 'GeV/c^{2}'),
        pt = cms.vstring('muon p_{T}', '0', '1000', 'GeV/c'),
        l1pt = cms.vstring('L1 muon p_{T}', '0', '999', 'GeV/c'),
        l1dr = cms.vstring('L1 Delta r', '0', '999', '-'),
        l1q = cms.vstring('L1 quality', '0', '999', '-'),
        abseta = cms.vstring('muon |#eta|', '0', '20', '-'),
        eta = cms.vstring('muon #eta', '-2.4', '2.4', '-'),
        ),

    # Flags you want to use to define numerator and possibly denominator
    Categories = cms.PSet(
        NewHighPtID = cms.vstring('NewHighPtID', 'dummy[pass=1,fail=0]'),
        tag_IsoMu20 = cms.vstring('Tag matched to IsoMu20', 'dummy[pass=1,fail=0]'),
        Mu50 = cms.vstring('Mu50', 'dummy[pass=1,fail=0]'),
        ),

    # What to fit
    Efficiencies = cms.PSet(
        MuEff_pt = cms.PSet(
            UnbinnedVariables = cms.vstring("mass"),
            EfficiencyCategoryAndState = cms.vstring("Mu50", "pass"),
            BinnedVariables = cms.PSet(
                pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
                dzPV = cms.vdouble(-10.0, 10.0),
                dB = cms.vdouble(0.0, 1.5),
                eta = cms.vdouble(-2.4, 2.4),
                pt = cms.vdouble(np.linspace(40, 120, 20)),
                NewHighPtID = cms.vstring('pass'),
                tag_IsoMu20 = cms.vstring('pass')
                ),
            BinToPDFmap = cms.vstring("voigtPlusExpo"),
            ),
        MuEff_eta = cms.PSet(
            UnbinnedVariables = cms.vstring("mass"),
            EfficiencyCategoryAndState = cms.vstring("Mu50", "pass"),
            BinnedVariables = cms.PSet(
                pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
                dzPV = cms.vdouble(-10.0, 10.0),
                dB = cms.vdouble(0.0, 1.5),
                eta = cms.vdouble(np.linspace(-2.4, 2.4, 10)),
                pt = cms.vdouble(50,2000),
                NewHighPtID = cms.vstring('pass'),
                tag_IsoMu20 = cms.vstring('pass')
                ),
            BinToPDFmap = cms.vstring("voigtPlusExpo"),
            ),
        ),

    # PDF for signal and background (double voigtian + exponential background)
    PDFs = cms.PSet(
        voigtPlusExpo = cms.vstring(
            "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
            ),
        ),

    # How to do the fit
    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(40),
    saveDistributionsPlot = cms.bool(True),
    NumCPU = cms.uint32(1), # leave to 1 for now, RooFit gives funny results otherwise
    SaveWorkspace = cms.bool(False),
)

"""
Process Path
"""

process.p1 = cms.Path(process.TnP_Muon_Z_DATA)
