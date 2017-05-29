# Run HLT (+ Validation) jobs and Harvesting

## Standard HLT + Validation workflow (locally) :
```bash
voms-proxy-init --voms cms --valid 168:00 # step2_HLT_Validation.py uses TTbar samples "from the grid"
cmsRun step2_HLT_Validation.py
cmsRun step3_HARVESTING.py  dqmSaverWorkflow=/TTbar-pilot/CMSSW_9_0_0-NoPU/DQM
```

## Standard HLT + Validation workflow (on the grid) :
```bash
source /cvmfs/cms.cern.ch/crab3/crab.sh
# adjust crab cfg
crab submit -c my_crab_cfg.py # there are few examples in the directory
# usual crab jobs baby-sitting
crab getoutput -d my_crab_job_dir/results/ # there are few examples in the directory
cmsRun step3_HARVESTING.py inputFolder=crab_SingleMu_Pt-8to100_NoPU_Phase2_HLT_Validation_v3/results/ dqmSaverWorkflow=/MY/WORKFLOW/DQM 
```

## Run only HLT workflow :
Edit `step2_HLT_Validation.py` :
```python
...
from HLTrigger.Phase2.customiseForPhase2 import customiseTrigger,customiseRelValStep2

process = customiseTrigger(process)
process = customiseRelValStep2(process)

# Schedule definition                                                                                                                                                                                       
process.schedule = process.HLTSchedule
process.schedule.extend([process.hltValidationPhase2, process.DQMoutput])
#process.schedule.extend([process.EDMoutput])
...
```

should become :

```python
...
from HLTrigger.Phase2.customiseForPhase2 import customiseTrigger, addEdmOutput,

process = customiseTrigger(process)
process = addEdmOutput(process,process.FEVTDEBUGHLTEventContent.outputCommands,"HLT.root")

# Schedule definition                                                                                                                                                                                       
process.schedule = process.HLTSchedule
#process.schedule.extend([process.hltValidationPhase2, process.DQMoutput])
process.schedule.extend([process.EDMoutput])
...
```

