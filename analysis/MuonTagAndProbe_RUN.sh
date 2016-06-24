#!/bin/bash

# Set filepath for MC and DATA files here
filename_MC="../../treeGeneration/tnpZ_MC.root"
filename_DATA="../../../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run273731_to_274240_IncludingMissingLumi_Completed.root"

# Perform pile-up reweighting according to number of primary vertices
root -b -l -q $filename_MC $filename_DATA addNVtxWeight.cxx

# Run efficiency measurement using tag and probe for MC and DATA
cmsRun MuonTagAndProbe_DATA.py $filename_DATA
cmsRun MuonTagAndProbe_MC.py tnpZ_withNVtxWeights.root
