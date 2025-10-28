# **SynthMed Agent - IBM AI Lab Challenge: AI Medical Research Synthesis Agent**

## Setup

### Setup Orchestrate and SynthMed:
1. Obtain API Key:
	- Go to cloud.ibm.com
	- Go to Manage -> Access (IAM) and select API keys on left.
	- Select Create and enter key name and description.
	- Select Create followed by Copy or Download - important to save key value. 
2. Setup virtual environment:
	- python3 -m venv venv
	- source venv/bin/activate
3. Setup orchestrate environment:
	- pip install ibm-watsonx-orchestrate
	- orchestrate env add -n synthmed -u https://api.ca-tor.watson-orchestrate.cloud.ibm.com/instances/d5d11d07-ece4-4eb3-aaf8-6f91dc58181f --type ibm_iam --activate
	- orchestrate env activate synthmed
	- Please enter WXO API key:  (cut-and-paste your API Key here) 
	- Note: Token will need to be reactivated when it expires.
4. Clone and run SynthMed project locally:
	- Browse to https://github.com/jaywarfield/synthmed
	- Select Code and Open with GitHub Desktop.
	- Execute locally: import-all.sh
	- Test in UI

Note: The following are additional orchestrate commands if needed.

### View orchestrate help:
- orchestrate –help
- orchestrate env --help
- orchestrate agents –help
- orchestrate agents remove --help
- etc

### Remove agent:
 orchestrate agents remove --name my-agent --kind native

### List agents:
- orchestrate agents list -v

### Import tools:
- orchestrate tools import -f my-file.py -k python

### Import knowledge bases:
- orchestrate knowledge-bases import -f my-kb.yaml

### Import agents:
- orchestrate agents import -f my-agent.yaml

---

# License

This application is licensed under the Apache License, Version 2.  Separate third-party code objects invoked by this application are licensed by their respective providers pursuant to their own separate licenses.  Contributions are subject to the [Developer Certificate of Origin, Version 1.1](https://developercertificate.org/) and the [Apache License, Version 2](https://www.apache.org/licenses/LICENSE-2.0.txt).

