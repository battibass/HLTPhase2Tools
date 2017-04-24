# HLTPhase2Tools

## Installation :
Environment setup :
```bash
cmsrel CMSSW_9_0_0
cd CMSSW_9_0_0/src
cmsenv
```

Get HLT_Iso(Tk)Mu24, prepare and run customized sequences :

```bash
git cms-addpkg HLTrigger/Configuration
git cms-merge-topic battibass:myTrackingFix

git clone https://github.com/battibass/HLTPhase2Tools/ HLTrigger/Phase2

scramv1 b -j 5

hltGetConfiguration --cff --offline /dev/CMSSW_9_0_0/GRun --paths HLTriggerFirstPath,HLT_IsoTkMu24_v4,HLTriggerFinalPath --unprescale --l1=L1Menu_Collisions2016_v9_m2_xml > HLTrigger/Configuration/python/HLT_UserIsoTkMu24_cff.py

# Or IsoMu24: hltGetConfiguration --cff --offline /dev/CMSSW_9_0_0/GRun --paths HLTriggerFirstPath,HLT_IsoMu24_v4,HLTriggerFinalPath --unprescale --l1=L1Menu_Collisions2016_v9_m2_xml > HLTrigger/Configuration/python/HLT_UserIsoMu24_cff.py

mkdir HLTrigger/Phase2/test
cd HLTrigger/Phase2/test



# From runTheMatrix.py  -ne -w upgrade -l 21208.0 (SingleMuPt100 no PU)
cmsDriver.py SingleMuPt100_pythia8_cfi  --conditions auto:phase2_realistic -n 10 --era Phase2C2 --eventcontent FEVTDEBUG --relval 9000,100 -s GEN,SIM --datatier GEN-SIM --beamspot HLLHC --geometry Extended2023D4

cmsDriver.py step2 --conditions auto:phase2_realistic -s DIGI:pdigi_valid,L1,L1TrackTrigger,DIGI2RAW,HLT:UserIsoTkMu24 --datatier GEN-SIM-DIGI-RAW -n -1 --geometry Extended2023D4 --era Phase2C2 --eventcontent FEVTDEBUGHLT --filein=file:SingleMuPt100_pythia8_cfi_GEN_SIM.root --fileout=file:step2.root --customise HLTrigger/Phase2/customiseMuonsForPhase2.customiseMuons

cmsDriver.py step3  --conditions auto:phase2_realistic -n -1 --era Phase2C2 --eventcontent FEVTDEBUGHLT,MINIAODSIM,DQM --runUnscheduled  -s RAW2DIGI,L1Reco,RECO,PAT,VALIDATION:@phase2Validation+@miniAODValidation,DQM:@phase2+@miniAODDQM --datatier GEN-SIM-RECO,MINIAODSIM,DQMIO --geometry Extended2023D4 --filein=file:step2.root --fileout=file:step3.root --customise HLTrigger/Phase2/customiseMuonsForPhase2.customiseMuonValidation

cmsDriver.py step4 --conditions auto:phase2_realistic -s HARVESTING:@phase2Validation+@phase2+@miniAODValidation+@miniAODDQM --era Phase2C2 --filein file:step3_inDQM.root --scenario pp --filetype DQM --geometry Extended2023D4 --mc -n 500 --customise HLTrigger/Phase2/customiseMuonsForPhase2.customiseMuonValidation
```
