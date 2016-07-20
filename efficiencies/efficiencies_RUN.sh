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
# FOR EFFICIENCY AND STATISTICAL ERROR
###############################################################################

configuration_dir=configurations/stat
pwd_dir=$(pwd)
mkdir -p $configuration_dir
sed -e 's/@identifier/DATA/' \
    -e 's/@massMin/"70"/' \
    -e 's/@massMax/"110"/' \
    -e 's/@binsForFit/40/' \
    -e 's/@defineVariableWeight//' \
    -e 's/@unbinnedVariableWeight//' \
    -e 's/@setProcessVariableWeight//' \
    MuonTagAndProbe.template.py > $configuration_dir/MuonTagAndProbe_DATA.py
sed -e 's/@identifier/MC/' \
    -e 's/@massMin/"70"/' \
    -e 's/@massMax/"110"/' \
    -e 's/@binsForFit/40/' \
    -e 's/@defineVariableWeight/weight = cms.vstring("weight", "-10", "10", ""),/' \
    -e 's/@unbinnedVariableWeight/"weight"/' \
    -e 's/@setProcessVariableWeight/WeightVariable = cms.string("weight"),/' \
    MuonTagAndProbe.template.py > $configuration_dir/MuonTagAndProbe_MC.py

if [ -f $configuration_dir/SKIP ];
then
    echo "[INFO] Skip executing files in" $configuration_dir
else
    echo "[INFO] Run files in " $configuration_dir
    cd $configuration_dir
    touch SKIP
    cmsRun MuonTagAndProbe_DATA.py $pwd_dir/subTree_DATA.root
    cmsRun MuonTagAndProbe_MC.py $pwd_dir/tnpZ_withNVtxWeights.root
    cd $pwd_dir
fi

###############################################################################
# GENERATE AND RUN CONFIGURATION FILES FROM TEMPLATE
# FOR SYSTEMATICAL ERROR
###############################################################################

# Make different configurations for systematical error measurement.
# Simply do a copy and paste from the configuration above and change the
# 'configuration_dir' variable.

configuration_dir=configurations/sys/1
pwd_dir=$(pwd)
mkdir -p $configuration_dir
sed -e 's/@identifier/DATA/' \
    -e 's/@massMin/"70"/' \
    -e 's/@massMax/"110"/' \
    -e 's/@binsForFit/30/' \
    -e 's/@defineVariableWeight//' \
    -e 's/@unbinnedVariableWeight//' \
    -e 's/@setProcessVariableWeight//' \
    MuonTagAndProbe.template.py > $configuration_dir/MuonTagAndProbe_DATA.py
sed -e 's/@identifier/MC/' \
    -e 's/@massMin/"70"/' \
    -e 's/@massMax/"110"/' \
    -e 's/@binsForFit/30/' \
    -e 's/@defineVariableWeight/weight = cms.vstring("weight", "-10", "10", ""),/' \
    -e 's/@unbinnedVariableWeight/"weight"/' \
    -e 's/@setProcessVariableWeight/WeightVariable = cms.string("weight"),/' \
    MuonTagAndProbe.template.py > $configuration_dir/MuonTagAndProbe_MC.py

if [ -f $configuration_dir/SKIP ];
then
    echo "[INFO] Skip executing files in" $configuration_dir
else
    echo "[INFO] Run files in " $configuration_dir
    cd $configuration_dir
    touch SKIP
    cmsRun MuonTagAndProbe_DATA.py $pwd_dir/subTree_DATA.root
    cmsRun MuonTagAndProbe_MC.py $pwd_dir/tnpZ_withNVtxWeights.root
    cd $pwd_dir
fi

configuration_dir=configurations/sys/2
pwd_dir=$(pwd)
mkdir -p $configuration_dir
sed -e 's/@identifier/DATA/' \
    -e 's/@massMin/"70"/' \
    -e 's/@massMax/"100"/' \
    -e 's/@binsForFit/40/' \
    -e 's/@defineVariableWeight//' \
    -e 's/@unbinnedVariableWeight//' \
    -e 's/@setProcessVariableWeight//' \
    MuonTagAndProbe.template.py > $configuration_dir/MuonTagAndProbe_DATA.py
sed -e 's/@identifier/MC/' \
    -e 's/@massMin/"80"/' \
    -e 's/@massMax/"110"/' \
    -e 's/@binsForFit/40/' \
    -e 's/@defineVariableWeight/weight = cms.vstring("weight", "-10", "10", ""),/' \
    -e 's/@unbinnedVariableWeight/"weight"/' \
    -e 's/@setProcessVariableWeight/WeightVariable = cms.string("weight"),/' \
    MuonTagAndProbe.template.py > $configuration_dir/MuonTagAndProbe_MC.py

if [ -f $configuration_dir/SKIP ];
then
    echo "[INFO] Skip executing files in" $configuration_dir
else
    echo "[INFO] Run files in " $configuration_dir
    cd $configuration_dir
    touch SKIP
    cmsRun MuonTagAndProbe_DATA.py $pwd_dir/subTree_DATA.root
    cmsRun MuonTagAndProbe_MC.py $pwd_dir/tnpZ_withNVtxWeights.root
    cd $pwd_dir
fi

###############################################################################
# CALCULATE EFFICIENCIES OF DATA AND MC SEPARATELY
# WITH STATISTICAL AND SYSTEMATICAL ERRORS
###############################################################################

# The first ROOT file is the 'main' configuration file output, which is used to
# calculate the statistical error and the efficiencies per bin. The other files
# are used to calculate the systematical error by calculating the RMS value with
# a fixed mean of the first 'main' ROOT file.

filelist_DATA="configurations/sys/MuonTagAndProbe_DATA.root configurations/stat/1/MuonTagAndProbe_DATA.root configurations/stat/2/MuonTagAndProbe_DATA.root"

root -l -b -q $filelist_DATA calcEfficiencies.C

###############################################################################
# CALCULATE EFFICIENCY RATIO OF DATA AND MC
# WITH STATISTICAL AND SYSTEMATICAL ERRORS
###############################################################################
