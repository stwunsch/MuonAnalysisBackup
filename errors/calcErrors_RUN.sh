#!/bin/bash

###############################################################################
# ERROR HANDLING
###############################################################################

# Check whether CMSSW is setup

if [ -z $CMSSW_BASE ];
then
    echo "[ERROR] Please setup CMSSW."
    exit 1
fi

# Check whether the file is executed in the same directory where it is placed

if [ ! -f calcErrors_RUN.sh ];
then
    echo "[ERROR] Please execute the script in the same folder where it is placed."
    exit 1
fi

###############################################################################
# PREPROCESS INPUT FILES
###############################################################################

# Setup input files (DATA and MC)

filenames_DATA="../../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run271036to275125_incomplete.root ../../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run275126to275783.root ../../data/TnPTree_80X_Run2016C_v2_GoldenJSON_Run275126to275783.root ../../data/TnPTree_80X_Run2016C_v2_GoldenJSON_Run275784to276097.root"

filenames_MC="../../data/TnPTree_80X_DYLL_M50_MadGraphMLM_part1.root"

echo "[INFO] Input DATA files:" $filenames_DATA
echo "[INFO] Input MC files:" $filenames_MC

# Reducing DATA and MC files to subtrees to reduce processing later

if [ -f "subTree_DATA.root" ];
then
    echo "[INFO] Skip creating DATA subtree because file subTree_DATA.root already exists."
else
    echo "[INFO] Creating DATA subtree from input files."
    root -l -b -q $filenames_DATA 'subTree.C("tpTree", "tag_IsoMu20", "subTree_DATA.root")'
fi

if [ -f "subTree_MC.root" ];
then
    echo "[INFO] Skip creating MCsubtree because file subTree_MC.data already exists."
else
    echo "[INFO] Creating MC subtree from input files."
    root -l -b -q $filenames_MC 'subTree.C("tpTree", "tag_IsoMu20", "subTree_MC.root")'
fi

# Add weights to MC file calculated from DATA

if [ -f "tnpZ_withNVtxWeights.root" ];
then
    echo "[INFO] Skip adding weights to MC file because file tnpZ_withNVtxWeights.root already exists."
else
    echo "[INFO] Adding weights to MC file calculated from DATA."
    root -l -b -q subTree_MC.root subTree_DATA.root addNVtxWeight.cxx
fi

###############################################################################
# GENERATE AND RUN CONFIGURATION FILES FROM TEMPLATE
###############################################################################

# Make main configuration files for efficiency measurement and statistical error measurement

mkdir -p configurations/stat
# DATA process
sed -e 's/@type/DATA/' \
    -e 's/@massMin/"70"/' \
    -e 's/@massMax/"110"/' \
    -e 's/@binsForFit/40/' \
    -e 's/@defineVariableWeight//' \
    -e 's/@unbinnedVariableWeight//' \
    -e 's/@setProcessVariableWeight//' \
    MuonTagAndProbe.template.py > configurations/stat/MuonTagAndProbe_DATA.py
# MC process
sed -e 's/@type/MC/' \
    -e 's/@massMin/"70"/' \
    -e 's/@massMax/"110"/' \
    -e 's/@binsForFit/40/' \
    -e 's/@defineVariableWeight/weight = cms.vstring('weight', '-10', '10', ''),/' \
    -e 's/@unbinnedVariableWeight/"weight"/' \
    -e 's/@setProcessVariableWeight/WeightVariable = cms.string("weight"),/' \
    MuonTagAndProbe.template.py > configurations/stat/MuonTagAndProbe_MC.py

# Make different configurations for systematical error measurement

# Run all of the generated configuration files

if [ -f configurations/stat/SKIP ];
then
    echo "[INFO] Skip executing files in configurations/stat"
else
    echo "[INFO] Run files in configurations/stat"
    cd configurations/stat
    touch SKIP
    cmsRun MuonTagAndProbe_DATA.py ../../subTree_DATA.root
    cmsRun MuonTagAndProbe_MC.py ../../tnpZ_withNVtxWeights.root
    cd ../..
fi

###############################################################################
# CALCULATE EFFICIENCIES OF DATA AND MC SEPARATELY
###############################################################################


###############################################################################
# CALCULATE EFFICIENCY RATIO OF DATA AND MC
###############################################################################
