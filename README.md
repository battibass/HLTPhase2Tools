# HLTPhase2Tools

## Installation :
Environment setup :
```bash
cmsrel CMSSW_9_0_0_pre2
cd CMSSW_9_0_0_pre2/src
cmsenv
```

Get PRs enabling stage-2 L1 in Phase2 eras :

```bash
git cms-merge-topic 17248
git cms-merge-topic 17309
```

Get HLT_IsoMu24, prepare and run customized sequences :

```bash
git cms-addpkg HLTrigger/Configuration 
hltGetConfiguration --cff --offline /dev/CMSSW_9_0_0/GRun --paths HLTriggerFirstPath,HLT_IsoMu24_v4,HLTriggerFinalPath --unprescale > Configuration/python/HLT_User_cff.py

scramv1 b -j 5

git clone https://github.com/battibass/HLTPhase2Tools/ HLTrigger/Phase2
cd HLTrigger/Phase2/

# From runTheMatrix.py  -ne -w upgrade -l 21208.0 (SingleMuPt100 no PU)

cmsDriver.py SingleMuPt100_pythia8_cfi  --conditions auto:phase2_realistic -n 10 --era Phase2C2 --eventcontent FEVTDEBUG --relval 9000,100 -s GEN,SIM --datatier GEN-SIM --beamspot HLLHC --geometry Extended2023D4

cmsDriver.py step2 --conditions auto:phase2_realistic -s DIGI:pdigi_valid,L1,DIGI2RAW,HLT:User --datatier GEN-SIM-DIGI-RAW -n 10 --geometry Extended2023D4 --era Phase2C2 --eventcontent FEVTDEBUGHLT --filein=file:step1.root --customise HLTrigger/Phase2/customiseMuonsForPhase2.customiseMuons
```

