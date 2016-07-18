#!/bin/bash

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

# Go through files in directory $processes_dir and execute the python configuration files with csmRun

processes_dir="processes/"

if [ -f $processes_dir/SKIP ];
then
    echo "[INFO] Skip executing python configuration files in " $processes_dir "because SKIP file exists."
else
    echo "[INFO] Execute all python files in directory:" $processes_dir
    touch $processes_dir/SKIP
    find $(pwd)/$processes_dir -name *.py -exec echo Executing: cmsRun {} \; -exec csmRun {} \;
fi
