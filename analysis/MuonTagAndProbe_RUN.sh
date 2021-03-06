#!/bin/bash

# Setup

filename_DATA="../../data/TnPTree_80X_Run2016C_v2_GoldenJSON_Run276098to276384.root ../../data/TnPTree_80X_Run2016D_v2_GoldenJSON_Run276098to276384.root ../../data/TnPTree_80X_Run2016D_v2_GoldenJSON_Run276385to276811.root"
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

if [ -f highResEta/START ];
then
    echo "[INFO] Skip highResEta because START file already exists"
else
    echo "[INFO] Start highResEta ..."
    cd highResEta/
    touch START
    cmsRun MuonTagAndProbe_DATA.py ../$filename_SUBTREE
    cd ..
fi

# Make eta forward/backward plots

if [ -f eta_1p2_1p7/START ];
then
    echo "[INFO] Skip eta_1p2_1p7 because START file already exists"
else
    echo "[INFO] Start eta_1p2_1p7 ..."
    cd eta_1p2_1p7/
    touch START
    cmsRun MuonTagAndProbe_DATA_forward.py ../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_backward.py ../$filename_SUBTREE
    cd ..
    echo "[INFO] Collect plots from eta_1p2_1p7 ..."
    root -l -b -q 'collectPlots.C("eta_1p2_1p7/","eta_1p2_1p7/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from eta_1p2_1p7 ..."
    root -l -b -q 'comparePlots.C("eta_1p2_1p7/collectPlots.root","eta_1p2_1p7/comparePlots.root")'
fi


# Make L1 cut plots with different parameters

if [ -f l1/l1q/START ];
then
    echo "[INFO] Skip l1/l1q because START file already exists"
else
    echo "[INFO] Start l1/l1q ..."
    cd l1/l1q/
    touch START
    cmsRun MuonTagAndProbe_DATA_l1q_4.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_l1q_8.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_l1q_12.py ../../$filename_SUBTREE
    cd ../..
    echo "[INFO] Collect plots from l1/l1q ..."
    root -l -b -q 'collectPlots.C("l1/l1q/","l1/l1q/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from l1/l1q ..."
    root -l -b -q 'comparePlots.C("l1/l1q/collectPlots.root","l1/l1q/comparePlots.root")'
fi

if [ -f l1/l1pt/START ];
then
    echo "[INFO] Skip l1/l1pt because START file already exists"
else
    echo "[INFO] Start l1/l1pt ..."
    cd l1/l1pt/
    touch START
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

# Analysis of abseta in high resolution and pt plots for every bin

# Efficiency vs abseta and l1 with q12
if [ -f highResAbsEta/abseta_l1q12/START ];
then
    echo "[INFO] Skip highResAbsEta/abseta_l1q12 because START file already exists"
else
    echo "[INFO] Start highResAbsEta/abseta_l1q12 ..."
    cd highResAbsEta/abseta_l1q12/
    touch START
    cmsRun MuonTagAndProbe_DATA_delEta0p1.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_delEta0p05.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_delEta0p025.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_delEta0p01.py ../../$filename_SUBTREE
    cd ../..
    echo "[INFO] Collect plots from highResAbsEta/abseta_l1q12 ..."
    root -l -b -q 'collectPlots.C("highResAbsEta/abseta_l1q12/","highResAbsEta/abseta_l1q12/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from highResAbsEta/abseta_l1q12 ..."
    root -l -b -q 'comparePlots.C("highResAbsEta/abseta_l1q12/collectPlots.root","highResAbsEta/abseta_l1q12/comparePlots.root")'
fi

# Efficiency vs abseta and l1 with q4
if [ -f highResAbsEta/abseta_l1q4/START ];
then
    echo "[INFO] Skip highResAbsEta/abseta_l1q4 because START file already exists"
else
    echo "[INFO] Start highResAbsEta/abseta_l1q4 ..."
    cd highResAbsEta/abseta_l1q4/
    touch START
    cmsRun MuonTagAndProbe_DATA_delEta0p1.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_delEta0p05.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_delEta0p025.py ../../$filename_SUBTREE
    cmsRun MuonTagAndProbe_DATA_delEta0p01.py ../../$filename_SUBTREE
    cd ../..
    echo "[INFO] Collect plots from highResAbsEta/abseta_l1q4 ..."
    root -l -b -q 'collectPlots.C("highResAbsEta/abseta_l1q4/","highResAbsEta/abseta_l1q4/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from highResAbsEta/abseta_l1q4 ..."
    root -l -b -q 'comparePlots.C("highResAbsEta/abseta_l1q4/collectPlots.root","highResAbsEta/abseta_l1q4/comparePlots.root")'
fi

# Efficiency vs abseta and IsoMu22 AND/OR IsoTkMu22
if [ -f highResAbsEta/abseta_IsoMu22/START ];
then
    echo "[INFO] Skip highResAbsEta/abseta_IsoMu22 because START file already exists"
else
    echo "[INFO] Start highResAbsEta/abseta_IsoMu22 ..."
    cd highResAbsEta/abseta_IsoMu22/
    touch START
    cmsRun MuonTagAndProbe_DATA_delEta0p025.py ../../$filename_SUBTREE
    cd ../..
fi
if [ -f highResAbsEta/abseta_IsoTkMu22/START ];
then
    echo "[INFO] Skip highResAbsEta/abseta_IsoTkMu22 because START file already exists"
else
    echo "[INFO] Start highResAbsEta/abseta_IsoTkMu22 ..."
    cd highResAbsEta/abseta_IsoTkMu22/
    touch START
    cmsRun MuonTagAndProbe_DATA_delEta0p025.py ../../$filename_SUBTREE
    cd ../..
fi
if [ -f highResAbsEta/abseta_IsoMu22_OR_IsoTkMu22/START ];
then
    echo "[INFO] Skip highResAbsEta/abseta_IsoMu22_OR_IsoTkMu22 because START file already exists"
else
    echo "[INFO] Start highResAbsEta/abseta_IsoMu22_OR_IsoTkMu22 ..."
    cd highResAbsEta/abseta_IsoMu22_OR_IsoTkMu22/
    touch START
    cmsRun MuonTagAndProbe_DATA_delEta0p025.py ../../$filename_SUBTREE
    cd ../..
fi

# Efficiency vs pt in small abseta bins with l1 and q12
if [ -f highResAbsEta/pt_l1q12/START ];
then
    echo "[INFO] Skip highResAbsEta/pt_l1q12 because START file already exists"
else
    echo "[INFO] Start highResAbsEta/pt_l1q12 ..."
    cd highResAbsEta/pt_l1q12/
    touch START
    sed -e 's/@abseta_min@/1.0/' -e 's/@abseta_max@/1.1/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.0_1.1.py
    cmsRun MuonTagAndProbe_DATA_pt_1.0_1.1.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.1/' -e 's/@abseta_max@/1.2/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.1_1.2.py
    cmsRun MuonTagAndProbe_DATA_pt_1.1_1.2.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.2/' -e 's/@abseta_max@/1.3/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.2_1.3.py
    cmsRun MuonTagAndProbe_DATA_pt_1.2_1.3.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.3/' -e 's/@abseta_max@/1.4/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.3_1.4.py
    cmsRun MuonTagAndProbe_DATA_pt_1.3_1.4.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.4/' -e 's/@abseta_max@/1.5/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.4_1.5.py
    cmsRun MuonTagAndProbe_DATA_pt_1.4_1.5.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.5/' -e 's/@abseta_max@/1.6/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.5_1.6.py
    cmsRun MuonTagAndProbe_DATA_pt_1.5_1.6.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.6/' -e 's/@abseta_max@/1.7/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.6_1.7.py
    cmsRun MuonTagAndProbe_DATA_pt_1.6_1.7.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.7/' -e 's/@abseta_max@/1.8/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.7_1.8.py
    cmsRun MuonTagAndProbe_DATA_pt_1.7_1.8.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.8/' -e 's/@abseta_max@/1.9/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.8_1.9.py
    cmsRun MuonTagAndProbe_DATA_pt_1.8_1.9.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.9/' -e 's/@abseta_max@/2.0/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.9_2.0.py
    cmsRun MuonTagAndProbe_DATA_pt_1.9_2.0.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/2.0/' -e 's/@abseta_max@/2.1/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_2.0_2.1.py
    cmsRun MuonTagAndProbe_DATA_pt_2.0_2.1.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/2.1/' -e 's/@abseta_max@/2.2/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_2.1_2.2.py
    cmsRun MuonTagAndProbe_DATA_pt_2.1_2.2.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/2.2/' -e 's/@abseta_max@/2.3/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_2.2_2.3.py
    cmsRun MuonTagAndProbe_DATA_pt_2.2_2.3.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/2.3/' -e 's/@abseta_max@/2.4/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_2.3_2.4.py
    cmsRun MuonTagAndProbe_DATA_pt_2.3_2.4.py ../../$filename_SUBTREE
    cd ../..
    echo "[INFO] Collect plots from highResAbsEta/pt_l1q12 ..."
    root -l -b -q 'collectPlots.C("highResAbsEta/pt_l1q12/","highResAbsEta/pt_l1q12/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from highResAbsEta/pt_l1q12 ..."
    root -l -b -q 'comparePlots.C("highResAbsEta/pt_l1q12/collectPlots.root","highResAbsEta/pt_l1q12/comparePlots.root")'
fi

# Efficiency vs pt in small abseta bins with l1 and q4
if [ -f highResAbsEta/pt_l1q4/START ];
then
    echo "[INFO] Skip highResAbsEta/pt_l1q4 because START file already exists"
else
    echo "[INFO] Start highResAbsEta/pt_l1q4 ..."
    cd highResAbsEta/pt_l1q4/
    touch START
    sed -e 's/@abseta_min@/1.0/' -e 's/@abseta_max@/1.1/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.0_1.1.py
    cmsRun MuonTagAndProbe_DATA_pt_1.0_1.1.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.1/' -e 's/@abseta_max@/1.2/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.1_1.2.py
    cmsRun MuonTagAndProbe_DATA_pt_1.1_1.2.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.2/' -e 's/@abseta_max@/1.3/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.2_1.3.py
    cmsRun MuonTagAndProbe_DATA_pt_1.2_1.3.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.3/' -e 's/@abseta_max@/1.4/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.3_1.4.py
    cmsRun MuonTagAndProbe_DATA_pt_1.3_1.4.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.4/' -e 's/@abseta_max@/1.5/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.4_1.5.py
    cmsRun MuonTagAndProbe_DATA_pt_1.4_1.5.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.5/' -e 's/@abseta_max@/1.6/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.5_1.6.py
    cmsRun MuonTagAndProbe_DATA_pt_1.5_1.6.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.6/' -e 's/@abseta_max@/1.7/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.6_1.7.py
    cmsRun MuonTagAndProbe_DATA_pt_1.6_1.7.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.7/' -e 's/@abseta_max@/1.8/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.7_1.8.py
    cmsRun MuonTagAndProbe_DATA_pt_1.7_1.8.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.8/' -e 's/@abseta_max@/1.9/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.8_1.9.py
    cmsRun MuonTagAndProbe_DATA_pt_1.8_1.9.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.9/' -e 's/@abseta_max@/2.0/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.9_2.0.py
    cmsRun MuonTagAndProbe_DATA_pt_1.9_2.0.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/2.0/' -e 's/@abseta_max@/2.1/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_2.0_2.1.py
    cmsRun MuonTagAndProbe_DATA_pt_2.0_2.1.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/2.1/' -e 's/@abseta_max@/2.2/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_2.1_2.2.py
    cmsRun MuonTagAndProbe_DATA_pt_2.1_2.2.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/2.2/' -e 's/@abseta_max@/2.3/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_2.2_2.3.py
    cmsRun MuonTagAndProbe_DATA_pt_2.2_2.3.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/2.3/' -e 's/@abseta_max@/2.4/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_2.3_2.4.py
    cmsRun MuonTagAndProbe_DATA_pt_2.3_2.4.py ../../$filename_SUBTREE
    cd ../..
    echo "[INFO] Collect plots from highResAbsEta/pt_l1q4 ..."
    root -l -b -q 'collectPlots.C("highResAbsEta/pt_l1q4/","highResAbsEta/pt_l1q4/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from highResAbsEta/pt_l1q4 ..."
    root -l -b -q 'comparePlots.C("highResAbsEta/pt_l1q4/collectPlots.root","highResAbsEta/pt_l1q4/comparePlots.root")'
fi

# Efficiency vs pt in small abseta bins with IsoMu22 AND/OR IsoTkMu22
if [ -f highResAbsEta/pt_IsoMu22/START ];
then
    echo "[INFO] Skip highResAbsEta/pt_IsoMu22 because START file already exists"
else
    echo "[INFO] Start highResAbsEta/pt_IsoMu22 ..."
    cd highResAbsEta/pt_IsoMu22/
    touch START
    sed -e 's/@abseta_min@/1.4/' -e 's/@abseta_max@/1.5/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.4_1.5.py
    cmsRun MuonTagAndProbe_DATA_pt_1.4_1.5.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.5/' -e 's/@abseta_max@/1.6/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.5_1.6.py
    cmsRun MuonTagAndProbe_DATA_pt_1.5_1.6.py ../../$filename_SUBTREE
    cd ../..
    echo "[INFO] Collect plots from highResAbsEta/pt_IsoMu22 ..."
    root -l -b -q 'collectPlots.C("highResAbsEta/pt_IsoMu22/","highResAbsEta/pt_IsoMu22/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from highResAbsEta/pt_IsoMu22 ..."
    root -l -b -q 'comparePlots.C("highResAbsEta/pt_IsoMu22/collectPlots.root","highResAbsEta/pt_IsoMu22/comparePlots.root")'
fi

if [ -f highResAbsEta/pt_IsoTkMu22/START ];
then
    echo "[INFO] Skip highResAbsEta/pt_IsoTkMu22 because START file already exists"
else
    echo "[INFO] Start highResAbsEta/pt_IsoTkMu22 ..."
    cd highResAbsEta/pt_IsoTkMu22/
    touch START
    sed -e 's/@abseta_min@/1.4/' -e 's/@abseta_max@/1.5/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.4_1.5.py
    cmsRun MuonTagAndProbe_DATA_pt_1.4_1.5.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.5/' -e 's/@abseta_max@/1.6/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.5_1.6.py
    cmsRun MuonTagAndProbe_DATA_pt_1.5_1.6.py ../../$filename_SUBTREE
    cd ../..
    echo "[INFO] Collect plots from highResAbsEta/pt_IsoTkMu22 ..."
    root -l -b -q 'collectPlots.C("highResAbsEta/pt_IsoTkMu22/","highResAbsEta/pt_IsoTkMu22/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from highResAbsEta/pt_IsoTkMu22 ..."
    root -l -b -q 'comparePlots.C("highResAbsEta/pt_IsoTkMu22/collectPlots.root","highResAbsEta/pt_IsoTkMu22/comparePlots.root")'
fi

if [ -f highResAbsEta/pt_IsoMu22_OR_IsoTkMu22/START ];
then
    echo "[INFO] Skip highResAbsEta/pt_IsoMu22_OR_IsoTkMu22 because START file already exists"
else
    echo "[INFO] Start highResAbsEta/pt_IsoMu22_OR_IsoTkMu22 ..."
    cd highResAbsEta/pt_IsoMu22_OR_IsoTkMu22/
    touch START
    sed -e 's/@abseta_min@/1.4/' -e 's/@abseta_max@/1.5/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.4_1.5.py
    cmsRun MuonTagAndProbe_DATA_pt_1.4_1.5.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.5/' -e 's/@abseta_max@/1.6/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.5_1.6.py
    cmsRun MuonTagAndProbe_DATA_pt_1.5_1.6.py ../../$filename_SUBTREE
    cd ../..
    echo "[INFO] Collect plots from highResAbsEta/pt_IsoMu22_OR_IsoTkMu22 ..."
    root -l -b -q 'collectPlots.C("highResAbsEta/pt_IsoMu22_OR_IsoTkMu22/","highResAbsEta/pt_IsoMu22_OR_IsoTkMu22/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from highResAbsEta/pt_IsoMu22_OR_IsoTkMu22 ..."
    root -l -b -q 'comparePlots.C("highResAbsEta/pt_IsoMu22_OR_IsoTkMu22/collectPlots.root","highResAbsEta/pt_IsoMu22_OR_IsoTkMu22/comparePlots.root")'
fi

if [ -f highResAbsEta/pt_IsoMu20/START ];
then
    echo "[INFO] Skip highResAbsEta/pt_IsoMu20 because START file already exists"
else
    echo "[INFO] Start highResAbsEta/pt_IsoMu20 ..."
    cd highResAbsEta/pt_IsoMu20/
    touch START
    sed -e 's/@abseta_min@/1.4/' -e 's/@abseta_max@/1.5/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.4_1.5.py
    cmsRun MuonTagAndProbe_DATA_pt_1.4_1.5.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.5/' -e 's/@abseta_max@/1.6/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.5_1.6.py
    cmsRun MuonTagAndProbe_DATA_pt_1.5_1.6.py ../../$filename_SUBTREE
    cd ../..
    echo "[INFO] Collect plots from highResAbsEta/pt_IsoMu20 ..."
    root -l -b -q 'collectPlots.C("highResAbsEta/pt_IsoMu20/","highResAbsEta/pt_IsoMu20/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from highResAbsEta/pt_IsoMu20 ..."
    root -l -b -q 'comparePlots.C("highResAbsEta/pt_IsoMu20/collectPlots.root","highResAbsEta/pt_IsoMu20/comparePlots.root")'
fi

if [ -f highResAbsEta/pt_IsoTkMu20/START ];
then
    echo "[INFO] Skip highResAbsEta/pt_IsoTkMu20 because START file already exists"
else
    echo "[INFO] Start highResAbsEta/pt_IsoTkMu20 ..."
    cd highResAbsEta/pt_IsoTkMu20/
    touch START
    sed -e 's/@abseta_min@/1.4/' -e 's/@abseta_max@/1.5/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.4_1.5.py
    cmsRun MuonTagAndProbe_DATA_pt_1.4_1.5.py ../../$filename_SUBTREE
    sed -e 's/@abseta_min@/1.5/' -e 's/@abseta_max@/1.6/' MuonTagAndProbe_DATA_pt.template > MuonTagAndProbe_DATA_pt_1.5_1.6.py
    cmsRun MuonTagAndProbe_DATA_pt_1.5_1.6.py ../../$filename_SUBTREE
    cd ../..
    echo "[INFO] Collect plots from highResAbsEta/pt_IsoTkMu20 ..."
    root -l -b -q 'collectPlots.C("highResAbsEta/pt_IsoTkMu20/","highResAbsEta/pt_IsoTkMu20/collectPlots.root","MuonTagAndProbe")'
    echo "[INFO] Compare plots from highResAbsEta/pt_IsoTkMu20 ..."
    root -l -b -q 'comparePlots.C("highResAbsEta/pt_IsoTkMu20/collectPlots.root","highResAbsEta/pt_IsoTkMu20/comparePlots.root")'
fi
