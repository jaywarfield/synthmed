# **SynthMed Agent - IBM AI Lab Challenge: AI Medical Research Synthesis Agent**

## Setup

### Obtain API Key
1. Go to cloud.ibm.com
2. At top go to Manage -> Access (IAM)
3. On left go to API keys
4. Select Create
5. Enter key name and description
6. Options can be left as is or change if desired
7. Select Create
8. Select Copy or Download - important to save a copy of the key value 

### View orchestrate help:
- orchestrate –help
- orchestrate env --help
- orchestrate agents –help
- orchestrate agents remove --help
- etc

### Setup orchestrate instance:
- orchestrate env add -n synthmed -u https://api.ca-tor.watson-orchestrate.cloud.ibm.com/instances/d5d11d07-ece4-4eb3-aaf8-6f91dc58181f --type ibm_iam --activate

### Activate orchestrate instance:
- orchestrate env activate synthmed
- Please enter WXO API key:  (cut-and-paste your API Key here) 

### Remove agent:
 orchestrate agents remove --name my-agent --kind native

### List agents:
- orchestrate agents list -v

Note: Follow imports are done by import-all.sh

### Import tools:
- orchestrate tools import -f my-file.py -k python

### Import knowledge bases:
- orchestrate knowledge-bases import -f my-kb.yaml

### Import agents:
- orchestrate agents import -f my-agent.yaml

---

# License

This application is licensed under the Apache License, Version 2.  Separate third-party code objects invoked by this application are licensed by their respective providers pursuant to their own separate licenses.  Contributions are subject to the [Developer Certificate of Origin, Version 1.1](https://developercertificate.org/) and the [Apache License, Version 2](https://www.apache.org/licenses/LICENSE-2.0.txt).

