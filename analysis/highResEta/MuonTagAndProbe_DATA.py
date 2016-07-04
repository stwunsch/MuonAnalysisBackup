"""
Imports
"""

import numpy as np
import sys
import FWCore.ParameterSet.Config as cms

# Get command line arguments (the filename)
if len(sys.argv)<3:
    print "[ERROR] Call the script this way: cmsRun <this script> <paths to root files>"
else:
    filename = sys.argv[2:]

"""
TnP Configuration
"""

# Set the appropriate tree and folder of the input file and define the output file
InputFileNames = cms.vstring(filename)
InputDirectoryName = cms.string("tpTree")
InputTreeName = cms.string("fitter_tree")
OutputFileName = cms.string("MuonTagAndProbe_DATA.root")

# Defines all the real variables which are intended for use in the efficiencies
Variables = cms.PSet(
    dzPV = cms.vstring('dzPV', '-10.0', '10.0', ''),
    dB = cms.vstring('dB', '0.0', '1.5', ''),
    pair_probeMultiplicity = cms.vstring('pair_probeMultiplicity', '0.20', '30.0', ''),
    mass = cms.vstring('Tag-muon Mass', '76', '125', 'GeV/c^{2}'),
    pt = cms.vstring('muon p_{T}', '0', '1000', 'GeV/c'),
    eta = cms.vstring('muon #eta', '-2.4', '2.4', '-'),
)

# Defines all the discrete variables which are intended for use in the efficiencies
Categories = cms.PSet(
    NewHighPtID = cms.vstring('NewHighPtID', 'dummy[pass=1,fail=0]'),
    tag_IsoMu20 = cms.vstring('Tag matched to IsoMu20', 'dummy[pass=1,fail=0]'),
    Mu50 = cms.vstring('Mu50', 'dummy[pass=1,fail=0]'),
)

# Define expressions to implement custom categories
# Leave it empty if you don't need this feature.
Expressions = cms.PSet(
)

# Define cuts on variables
# Leave it empty if you don't need this feature.
Cuts = cms.PSet(
)

# Select the parameter whose efficiency is measured
Efficiencies = cms.PSet(
    MuonEfficiency = cms.PSet(
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring("Mu50", "pass"),
        BinnedVariables = cms.PSet(
            pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
            dzPV = cms.vdouble(-10.0, 10.0),
            dB = cms.vdouble(0.0, 1.5),
            eta = cms.vdouble(np.linspace(-2.4,2.4,30)),
            pt = cms.vdouble(52, 1000),
            NewHighPtID = cms.vstring('pass'),
            tag_IsoMu20 = cms.vstring('pass')
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"),
    )
)

# Define which PDFs for signal and background are fitted to the data
PDFs = cms.PSet(
    vpvPlusExpo = cms.vstring(
        "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
        "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,2,10])",
        "SUM::signal(vFrac[0.8,0,1]*signal1, signal2)",
        "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
        "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])",
        "efficiency[0.9,0,1]",
        "signalFractionInPassing[0.9]"
        ),
)

# Configure the fitting
binnedFit = cms.bool(True)
binsForFit = cms.uint32(40) # Select the number of bins which are fitted in the invariant mass histo
saveDistributionsPlot = cms.bool(True)
NumCPU = cms.uint32(1) # Leave to 1 for now, RooFit gives funny results otherwise
SaveWorkspace = cms.bool(False)

"""
Basic Process Setup
"""

import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

"""
Define DATA TnP Process
"""

process.TnP = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    # Select files, trees and folders
    InputFileNames = InputFileNames,
    InputDirectoryName = InputDirectoryName,
    InputTreeName = InputTreeName,
    OutputFileName = OutputFileName,

    # Variables for binning
    Variables = Variables,

    # Flags you want to use to define numerator and possibly denominator
    Categories = Categories,

    # Define custom categories out of expressions
    Expressions = Expressions,

    # Define cuts on variables
    Cuts = Cuts,

    # Select the parameter whose efficiency is measured
    Efficiencies = Efficiencies,

    # PDF for signal and background (double voigtian + exponential background)
    PDFs = PDFs,

    # How to do the fit
    binnedFit = binnedFit,
    binsForFit = binsForFit,
    saveDistributionsPlot = saveDistributionsPlot,
    NumCPU = NumCPU,
    SaveWorkspace = SaveWorkspace,
)

"""
Process Path
"""

process.p1 = cms.Path(process.TnP)
