import sys
from ROOT import *
import numpy as np

"""
Get filenames from arguments
sys.argv gives this: calcEfficiencies.py outputFilename inputFilename0 inputFilename1 ...
"""

if len(sys.argv)<3:
    print("[ERROR] Call calcEfficiencies.py like this: python calcEfficiencies.py outputFile inputFilename0 inputFilename1 ...")
    sys.exit()

outputFilename = sys.argv[1]
inputFilenames = sys.argv[2:]

print "[INFO] Output file:", outputFilename
print "[INFO] Input file (stat. error):", inputFilenames[0]
print "[INFO] Input files (sys. error):", inputFilenames[1:]

"""
Get TGraphAsymmErrors from input files
"""

canvasDir = "tpTree/MuonEfficiency/fit_eff_plots"

inputGraphs = []
for filename in inputFilenames:
    # Open file
    f = TFile(filename)
    # Find directory with canvas of efficiency plot
    d = f.GetDirectory(canvasDir)
    # Take first canvas and extract the TGraphAsymmError
    name = d.GetListOfKeys()[0].GetName()
    print "[INFO] Load graph from canvas:", filename, name
    inputGraphs.append(d.Get(name).GetPrimitive("hxy_fit_eff"))

"""
Put the first graph in the output file, this graph is the reference regarding
the statistical errors
"""

outputFile = TFile(outputFilename, "recreate")
gStat = inputGraphs[0]
gStat.SetName("stat_err")
gStat.Write()

"""
Calculate the mean squared differences to the reference graph (the first one)
per bin and put the best-fit values of the first graph with these systematical
errors as a new graph in the output file.
"""

numPoints = gStat.GetN()
numGraphs = len(inputGraphs)
gSys = TGraphAsymmErrors(numPoints)

for i in range(numPoints):
    vStatY = Double(0) # that is the reference
    vStatX = Double(0)
    gStat.GetPoint(i, vStatX, vStatY)
    gSys.SetPoint(i, vStatX, vStatY) # copy point from reference graph

    vDiffSysY = Double(0)
    for graph in inputGraphs[1:]: # get here the values from the other graphs
        vSysX = Double(0)
        vSysY = Double(0)
        graph.GetPoint(i, vSysX, vSysY)
        vDiffSysY += (vStatY - vSysY)**2 # squared difference as measure
    # FIXME: do i have to use the unbiased version here?
    vDiffSysY = np.sqrt(vDiffSysY/(numGraphs-1)) # take sqrt and mean
    vStatErrXlow = gStat.GetErrorXlow(i) # X error from reference graph is copied
    vStatErrXhigh = gStat.GetErrorXhigh(i)
    # FIXME: set the y errors correctly! Only half ov vDiffSysY?
    gSys.SetPointError(i, vStatErrXlow, vStatErrXhigh, vDiffSysY, vDiffSysY) # set Y error as RMS value of points from different graphs

# Copy style of graph and write it to file
gSys.SetTitle(gStat.GetTitle());
gSys.SetLineStyle(gStat.GetLineStyle());
gSys.SetLineWidth(gStat.GetLineWidth());
gSys.SetMarkerStyle(gStat.GetMarkerStyle());
gSys.SetMarkerSize(gStat.GetMarkerSize());
gSys.GetXaxis().SetTitle(gStat.GetXaxis().GetTitle());
gSys.GetXaxis().SetTitleFont(gStat.GetXaxis().GetTitleFont());
gSys.GetXaxis().SetTitleSize(gStat.GetXaxis().GetTitleSize());
gSys.GetXaxis().SetLabelFont(gStat.GetXaxis().GetLabelFont());
gSys.GetXaxis().SetLabelSize(gStat.GetXaxis().GetLabelSize());
gSys.GetYaxis().SetTitle(gStat.GetYaxis().GetTitle());
gSys.GetYaxis().SetTitleFont(gStat.GetYaxis().GetTitleFont());
gSys.GetYaxis().SetTitleSize(gStat.GetYaxis().GetTitleSize());
gSys.GetYaxis().SetLabelFont(gStat.GetYaxis().GetLabelFont());
gSys.GetYaxis().SetLabelSize(gStat.GetYaxis().GetLabelSize());
gSys.SetName("sys_err")
gSys.Write()

"""
Generate a control plot by putting all graphs together in one plot and
store it to the output file
"""

gControl = TMultiGraph()
for graph in inputGraphs:
    gControl.Add(graph)
gControl.SetTitle(gStat.GetTitle());
gControl.SetName("control_plot_graphs")
gControl.Write()

outputFile.Close()
