"""
Workflow Description
"""

# TODO

"""
Imports
"""

import numpy as np
import FWCore.ParameterSet.Config as cms

"""
TnP Configuration: General
"""

# Set the appropriate tree and folder of the input file and define the output file
InputDirectoryName = cms.string("tpTree")
InputTreeName = cms.string("fitter_tree")

# Defines all the real variables which are intended for use in the efficiencies
Variables = cms.PSet(
    dzPV = cms.vstring('dzPV', '-10.0', '10.0', ''),
    dB = cms.vstring('dB', '0.0', '1.5', ''),
    pair_probeMultiplicity = cms.vstring('pair_probeMultiplicity', '0.20', '30.0', ''),
    mass = cms.vstring('Tag-muon Mass', '80', '100', 'GeV/c^{2}'),
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

# Selecte the parameter whose efficiency is measured
Efficiency = cms.PSet(
    UnbinnedVariables = cms.vstring("mass"),
    EfficiencyCategoryAndState = cms.vstring("Mu50", "pass"),
    BinnedVariables = cms.PSet(
        pair_probeMultiplicity = cms.vdouble(0.5, 1.5),
        dzPV = cms.vdouble(-10.0, 10.0),
        dB = cms.vdouble(0.0, 1.5),
        eta = cms.vdouble(-2.4, 2.4),
        pt = cms.vdouble(np.linspace(30, 70, 10)),
        NewHighPtID = cms.vstring('pass'),
        tag_IsoMu20 = cms.vstring('pass')
        ),
    BinToPDFmap = cms.vstring("voigtPlusExpo"),
)

# Define which PDFs for signal and background are fitted to the data
PDFs = cms.PSet(
    voigtPlusExpo = cms.vstring(
        "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])",
        "Exponential::backgroundPass(mass, lp[0,-5,5])",
        "Exponential::backgroundFail(mass, lf[0,-5,5])",
        "efficiency[0.9,0,1]",
        "signalFractionInPassing[0.9]"
    ),
)

# Configure the fitting
binnedFit = cms.bool(True)
binsForFit = cms.uint32(10) # Select the number of bins which are fitted in the invariant mass histo
saveDistributionsPlot = cms.bool(True)
NumCPU = cms.uint32(1) # Leave to 1 for now, RooFit gives funny results otherwise
SaveWorkspace = cms.bool(False)

"""
TnP Configuration: DATA Specific Parameters
"""

# Set DATA input and output files
DATA_InputFileNames = cms.vstring("file://../data/TnPTree_80X_Run2016B_v2_DCSOnly_RunList.root")
DATA_OutputFileName = cms.string("DATA_TagAndProbe.root")

"""
TnP Configuration: MC Specific Parameters
"""

# Set MC input and output files
MC_InputFileNames = cms.vstring("file://../data/TnPTree_80X_DYLL_M50_MadGraphMLM_part1.root")
MC_OutputFileName = cms.string("MC_TagAndProbe.root")

# Define the weight variable and add it the the global variable set
WeightVariable = cms.string("weight")
MC_Variables = Variables

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

process.TnP_DATA = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    # Select files, trees and folders
    InputFileNames = DATA_InputFileNames,
    InputDirectoryName = InputDirectoryName,
    InputTreeName = InputTreeName,
    OutputFileName = DATA_OutputFileName,

    # Variables for binning
    Variables = Variables,

    # Flags you want to use to define numerator and possibly denominator
    Categories = Categories,

    # Define custom categories out of expressions
    Expressions = Expressions,

    # Select the parameter whose efficiency is measured
    Efficiencies = cms.PSet(
        DATA_Efficiency = Efficiency,
     ),

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
Define MC TnP Process
"""

process.TnP_MC = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    # Select files, trees and folders
    InputFileNames = MC_InputFileNames,
    InputDirectoryName = InputDirectoryName,
    InputTreeName = InputTreeName,
    OutputFileName = MC_OutputFileName,

    # Set the weight variable
    WeightVariable = WeightVariable,

    # Variables for binning
    Variables = MC_Variables,

    # Flags you want to use to define numerator and possibly denominator
    Categories = Categories,

    # Define custom categories out of expressions
    Expressions = Expressions,

    # Select the parameter whose efficiency is measured
    Efficiencies = cms.PSet(
        MC_Efficiency = Efficiency,
     ),

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
Process Paths
"""

process.p1 = cms.Path(process.TnP_DATA)
process.p2 = cms.Path(process.TnP_MC)
