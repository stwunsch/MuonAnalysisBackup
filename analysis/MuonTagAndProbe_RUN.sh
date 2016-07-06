#!/bin/bash

# Setup

filename_DATA="../../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run273731_to_274240_IncludingMissingLumi_Completed.root ../../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run274241to274421.root ../../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run274422to274443.root ../../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run274444to275125.root"
echo "[INFO] Input files:" $filename_DATA

filename_SUBTREE="subTree_IsoMu20.root"

# Check whether CMSSW is setup

if [ -z $CMSSW_BASE ];
then
    echo "[ERROR] Please setup CMSSW"
    exit 1
fi

# Creating subtree if the file doesn't exist, otherwise skip producing subtree

if [ -f $filename_SUBTREE ];
then
    echo "[INFO] Skip creating subtree because file" $filename_SUBTREE "already exists."
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
    echo "[INFO] Collect plots from eta_1p2_1p7 ..."
    root -l -b -q 'collectPlots.C("eta_1p2_1p7/","eta_1p2_1p7/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from eta_1p2_1p7 ..."
    root -l -b -q 'comparePlots.C("eta_1p2_1p7/collectPlots.root","eta_1p2_1p7/comparePlots.root")'
fi


# Make L1 cut plots with different parameters

if [ -f l1/l1q/MuonTagAndProbe_DATA_l1q_4.root ];
then
    echo "[INFO] Skip l1/l1q because ROOT file already exists"
else
    echo "[INFO] Start l1/l1q ..."
    cd l1/l1q/
    cmsRun MuonTagAndProbe_DATA_l1q_4.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_l1q_8.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_l1q_12.py ../../$filename_SUBTREE
    cd ../..
    echo "[INFO] Collect plots from l1/l1q ..."
    root -l -b -q 'collectPlots.C("l1/l1q/","l1/l1q/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from l1/l1q ..."
    root -l -b -q 'comparePlots.C("l1/l1q/collectPlots.root","l1/l1q/comparePlots.root")'
fi

if [ -f l1/l1pt/MuonTagAndProbe_DATA_l1pt_16.root ];
then
    echo "[INFO] Skip l1/l1pt because ROOT file already exists"
else
    echo "[INFO] Start l1/l1pt ..."
    cd l1/l1pt/
    cmsRun MuonTagAndProbe_DATA_l1pt_16.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_l1pt_20.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_l1pt_22.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_l1pt_26.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_l1pt_30.py ../../$filename_SUBTREE
    cd ../..
    echo "[INFO] Collect plots from l1/l1pt ..."
    root -l -b -q 'collectPlots.C("l1/l1pt/","l1/l1pt/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from l1/l1pt ..."
    root -l -b -q 'comparePlots.C("l1/l1pt/collectPlots.root","l1/l1pt/comparePlots.root")'
fi
