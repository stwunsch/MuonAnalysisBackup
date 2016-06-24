#!/bin/bash

filename_DATA="../../../../../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run273731_to_274240_IncludingMissingLumi_Completed.root ../../../../../data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run271036to273730_NotCompleted.root"
echo "Input files:" $filename_DATA

cd 271036_273422/
cd pt/
cmsRun MuonTagAndProbe_DATA.py $filename_DATA
cd ../
cd eta/
cmsRun MuonTagAndProbe_DATA.py $filename_DATA
cd ../
cd ../

cd 273423_274093/
cd pt/
cmsRun MuonTagAndProbe_DATA.py $filename_DATA
cd ../
cd eta/
cmsRun MuonTagAndProbe_DATA.py $filename_DATA
cd ../
cd ../

cd 274094_274240/
cd pt/
cmsRun MuonTagAndProbe_DATA.py $filename_DATA
cd ../
cd eta/
cmsRun MuonTagAndProbe_DATA.py $filename_DATA
cd ../
cd ../
