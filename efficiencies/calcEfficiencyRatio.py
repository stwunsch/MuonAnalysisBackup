import sys
from ROOT import *
import numpy as np

"""
Get filenames from arguments
sys.argv gives this: calcEfficiencyRatio.py outputFilename inputFilenameDATA0
inputFilenameDATA1 ... inputFilenameMC0 inputFilenameMC1 ...
"""

if len(sys.argv)<3:
    print("[ERROR] Call calcEfficiencyRatio.py like this: python calcEfficiencyRatio.py outputFilename inputFilenameDATA0 inputFilenameDATA1 ... inputFilenameMC0 inputFilenameMC1 ...")
    sys.exit()

outputFilename = sys.argv[1]
numRootFiles = len(sys.argv[2:])
inputFilenamesDATA = sys.argv[2:2+numRootFiles/2]
inputFilenamesMC = sys.argv[2+numRootFiles/2:]

print "[INFO] Output file:", outputFilename
print "[INFO] Input files (DATA):", inputFilenamesDATA
print "[INFO] Input files (MC):", inputFilenamesMC

"""
Get TGraphAsymmErrors from input files
"""

canvasDir = "tpTree/MuonEfficiency/fit_eff_plots"

inputGraphsDATA = []
for filename in inputFilenamesDATA:
    # Open file
    f = TFile(filename)
    # Find directory with canvas of efficiency plot
    d = f.GetDirectory(canvasDir)
    # Take first canvas and extract the TGraphAsymmError
    name = d.GetListOfKeys()[0].GetName()
    print "[INFO] Load graph from canvas:", filename, name
    inputGraphsDATA.append(d.Get(name).GetPrimitive("hxy_fit_eff"))

inputGraphsMC = []
for filename in inputFilenamesMC:
    # Open file
    f = TFile(filename)
    # Find directory with canvas of efficiency plot
    d = f.GetDirectory(canvasDir)
    # Take first canvas and extract the TGraphAsymmError
    name = d.GetListOfKeys()[0].GetName()
    print "[INFO] Load graph from canvas:", filename, name
    inputGraphsMC.append(d.Get(name).GetPrimitive("hxy_fit_eff"))

"""
Get the ratios of all input graphs. The ratios are calculated like this:
inputGraphDATA0/inputGraphMC0 inputGraphDATA1/inputGraphMC1 ...
"""

numPoints = inputGraphsDATA[0].GetN()
numGraphs = len(inputGraphsDATA)
valuesXDATA = np.zeros(numPoints)
valuesYDATA = np.zeros((numGraphs, numPoints), dtype=np.double)
valuesXMC = np.zeros(numPoints)
valuesYMC = np.zeros((numGraphs, numPoints), dtype=np.double)
ratios = np.zeros((numGraphs, numPoints), dtype=np.double)

for iGraph in range(numGraphs):
    for iPoint in range(numPoints):
        # DATA
        vYDATA = Double(0)
        vXDATA = Double(0)
        inputGraphsDATA[iGraph].GetPoint(iPoint, vXDATA, vYDATA)
        if iGraph==0:
            valuesXDATA[iPoint] = vXDATA
        valuesYDATA[iGraph, iPoint] = vYDATA
        # MC
        vYMC = Double(0)
        vXMC = Double(0)
        inputGraphsMC[iGraph].GetPoint(iPoint, vXMC, vYMC)
        if iGraph==0:
            valuesXMC[iPoint] = vXMC
        valuesYMC[iGraph, iPoint] = vYMC
        # Ratio
        # NOTE: Set ratio to zero, if MC efficiency (denominator) is zero
        if vYMC != 0:
            ratios[iGraph, iPoint] = vYDATA/vYMC
        else:
            ratios[iGraph, iPoint] = 0

"""
Take the first graphs from DATA and MC filelists and use them to calculate the
statistical uncertainty. From the asymmetric uncertainty in the tag and probe efficiency
plots, we take the largest uncertainty (upper or lower) and make this one symmetrical
around the ratio of the best-fit values.
"""

gStat = TGraphAsymmErrors(numPoints)

for iPoint in range(numPoints):
    # Set ratio
    gStat.SetPoint(iPoint, valuesXDATA[iPoint], ratios[0, iPoint])
    # Get/set errors
    vStatErrXlowDATA = inputGraphsDATA[0].GetErrorXlow(iPoint)
    vStatErrXhighDATA = inputGraphsDATA[0].GetErrorXhigh(iPoint)
    vStatErrYlowDATA = inputGraphsDATA[0].GetErrorYlow(iPoint)
    vStatErrYhighDATA = inputGraphsDATA[0].GetErrorYhigh(iPoint)
    vStatErrYlowMC = inputGraphsMC[0].GetErrorYlow(iPoint)
    vStatErrYhighMC = inputGraphsMC[0].GetErrorYhigh(iPoint)
    gStat.SetPointError(iPoint, vStatErrXlowDATA, vStatErrXhighDATA, max(vStatErrYlowDATA, vStatErrYlowMC), max(vStatErrYhighDATA, vStatErrYhighMC))

# Copy style of graph and write it to file
gRef = inputGraphsDATA[0]
gStat.SetTitle("Ratio: "+gRef.GetTitle());
gStat.SetLineStyle(gRef.GetLineStyle());
gStat.SetLineWidth(gRef.GetLineWidth());
gStat.SetMarkerStyle(gRef.GetMarkerStyle());
gStat.SetMarkerSize(gRef.GetMarkerSize());
gStat.GetXaxis().SetTitle(gRef.GetXaxis().GetTitle());
gStat.GetXaxis().SetTitleFont(gRef.GetXaxis().GetTitleFont());
gStat.GetXaxis().SetTitleSize(gRef.GetXaxis().GetTitleSize());
gStat.GetXaxis().SetLabelFont(gRef.GetXaxis().GetLabelFont());
gStat.GetXaxis().SetLabelSize(gRef.GetXaxis().GetLabelSize());
gStat.GetYaxis().SetTitle("Ratio: "+gRef.GetYaxis().GetTitle());
gStat.GetYaxis().SetTitleFont(gRef.GetYaxis().GetTitleFont());
gStat.GetYaxis().SetTitleSize(gRef.GetYaxis().GetTitleSize());
gStat.GetYaxis().SetLabelFont(gRef.GetYaxis().GetLabelFont());
gStat.GetYaxis().SetLabelSize(gRef.GetYaxis().GetLabelSize());
gStat.SetName("stat_err")

"""
Use the ratio of the first graphs from DATA and MC filelists as reference and all
other graphs are taken into account for the systematical uncertainty measurement. We
calculate the RMS value to the reference ratio and put it symmetrical around
the ratio of the best-fit values.
"""

gSys = TGraphAsymmErrors(numPoints)

for iPoint in range(numPoints):
    # Set ratio
    gSys.SetPoint(iPoint, valuesXDATA[iPoint], ratios[0, iPoint])
    # Get/set errors
    vStatErrXlowDATA = inputGraphsDATA[0].GetErrorXlow(iPoint)
    vStatErrXhighDATA = inputGraphsDATA[0].GetErrorXhigh(iPoint)
    vDiffSysY = 0
    for iGraph in range(1,numGraphs):
        vDiffSysY += (ratios[0, iPoint] - ratios[iGraph, iPoint])**2 # squared difference as measure
    # NOTE: We sum the errors in quadrature as a conservative measurement. You
    # have to ensure that the tested configurations are sensible!
    vDiffSysY = np.sqrt(vDiffSysY) # take sqrt
    gSys.SetPointError(iPoint, vStatErrXlowDATA, vStatErrXhighDATA, vDiffSysY, vDiffSysY) # set Y error

# Copy style of graph and write it to file
gRef = inputGraphsDATA[0]
gSys.SetTitle("Ratio: "+gRef.GetTitle());
gSys.SetLineStyle(gRef.GetLineStyle());
gSys.SetLineWidth(gRef.GetLineWidth());
gSys.SetMarkerStyle(gRef.GetMarkerStyle());
gSys.SetMarkerSize(gRef.GetMarkerSize());
gSys.GetXaxis().SetTitle(gRef.GetXaxis().GetTitle());
gSys.GetXaxis().SetTitleFont(gRef.GetXaxis().GetTitleFont());
gSys.GetXaxis().SetTitleSize(gRef.GetXaxis().GetTitleSize());
gSys.GetXaxis().SetLabelFont(gRef.GetXaxis().GetLabelFont());
gSys.GetXaxis().SetLabelSize(gRef.GetXaxis().GetLabelSize());
gSys.GetYaxis().SetTitle("Ratio: "+gRef.GetYaxis().GetTitle());
gSys.GetYaxis().SetTitleFont(gRef.GetYaxis().GetTitleFont());
gSys.GetYaxis().SetTitleSize(gRef.GetYaxis().GetTitleSize());
gSys.GetYaxis().SetLabelFont(gRef.GetYaxis().GetLabelFont());
gSys.GetYaxis().SetLabelSize(gRef.GetYaxis().GetLabelSize());
gSys.SetName("sys_err")

"""
Put graphs used for uncertainty/error calculations in a control plot
"""

gControlGraphsDATA = TMultiGraph()
for graph in inputGraphsDATA:
    gControlGraphsDATA.Add(graph)
gControlGraphsDATA.SetTitle(gRef.GetTitle());
gControlGraphsDATA.SetName("control_plot_graphs_DATA")

gControlGraphsMC = TMultiGraph()
for graph in inputGraphsMC:
    gControlGraphsMC.Add(graph)
gControlGraphsMC.SetTitle(gRef.GetTitle());
gControlGraphsMC.SetName("control_plot_graphs_MC")

"""
Plot all ratios (without uncertainties/errors) in a control plot.
"""

gControlRatios = TMultiGraph()
for iGraph in range(numGraphs):
    graph = TGraph(numPoints)
    for iPoint in range(numPoints):
        graph.SetPoint(iPoint, valuesXDATA[iPoint], ratios[iGraph, iPoint])
    graph.SetLineStyle(gRef.GetLineStyle());
    graph.SetLineWidth(gRef.GetLineWidth());
    graph.SetMarkerStyle(gRef.GetMarkerStyle());
    graph.SetMarkerSize(gRef.GetMarkerSize());
    gControlRatios.Add(graph)
gControlRatios.SetTitle("Ratio: "+gRef.GetTitle())

gControlRatios.SetName("control_plot_ratios")

"""
Write plots to file
"""

outputFile = TFile(outputFilename, "recreate")
gStat.Write()
gSys.Write()
gControlGraphsDATA.Write()
gControlGraphsMC.Write()
gControlRatios.Write()
outputFile.Close()
