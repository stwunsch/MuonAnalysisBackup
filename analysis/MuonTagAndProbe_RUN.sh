#!/bin/bash

# Setup

filename_DATA="../../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run273731_to_274240_IncludingMissingLumi_Completed.root ../../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run274241to274421.root ../../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run274422to274443.root ../../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run274444to275125.root"
echo "[INFO] Input files:" $filename_DATA

filename_SUBTREE="subTree_IsoMu20.root"

# Creating subtree if the file doesn't exist, otherwise skip producing subtree

if [ -f $filename_SUBTREE ];
then
    echo "[INFO] File" $filename_SUBTREE "already exists, skip creating subtree."
else
    echo "[INFO] Creating subtree from input files."
    root -l -b -q $filename_DATA subTree.C
fi

# Make high resolution eta plot

if [ -f highResEta/MuonTagAndProbe_DATA.root ];
then
    echo "[INFO] Skip highResEta because ROOT file already exists"
else
    echo "[INFO] Start highResEta ..."
    cd highResEta/
    cmsRun MuonTagAndProbe_DATA.py ../$filename_SUBTREE
    cd ..
fi

# Make eta forward/backward plots

if [ -f eta_1p2_1p7/MuonTagAndProbe_DATA_forward.root ];
then
    echo "[INFO] Skip eta_1p2_1p7 because ROOT file already exists"
else
    echo "[INFO] Start eta_1p2_1p7 ..."
    cd eta_1p2_1p7/
    cmsRun MuonTagAndProbe_DATA_forward.py ../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_backward.py ../$filename_SUBTREE
    cd ..
    echo "[INFO] Collect plots from eta_1p2_1p7..."
    root -l -b -q 'collectPlots.C("eta_1p2_1p7/","eta_1p2_1p7/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from eta_1p2_1p7..."
    root -l -b -q 'comparePlots.C("eta_1p2_1p7/collectPlots.root","eta_1p2_1p7/comparePlots.root")'
fi

