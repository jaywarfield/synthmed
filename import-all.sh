#!/usr/bin/env bash
set -x

orchestrate env activate synthmed
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

#for openapi_tool in get-healthcare-providers.yml; do
#  orchestrate tools import -k openapi -f ${SCRIPT_DIR}/tools/${openapi_tool} -r ${SCRIPT_DIR}/tools/requirements.txt;
#done

for tool in ${SCRIPT_DIR}/tools/*; do
  if [ -f "tool" ]; then
    echo "Importing python tool: $file"
    #orchestrate tools import -f ${SCRIPT_DIR}/tools/example.py -k python
    orchestrate tools import -f $file -k python
  fi
done

for kb in synthmed_autism_kb.yaml; do
  orchestrate knowledge-bases import -f ${SCRIPT_DIR}/knowledge_bases/${kb}
done

for kb in synthmed_cancer_kb.yaml; do
  orchestrate knowledge-bases import -f ${SCRIPT_DIR}/knowledge_bases/${kb}
done

for kb in synthmed_dimentia_kb.yaml; do
  orchestrate knowledge-bases import -f ${SCRIPT_DIR}/knowledge_bases/${kb}
done

for kb in synthmed_epilepsy_kb.yaml; do
  orchestrate knowledge-bases import -f ${SCRIPT_DIR}/knowledge_bases/${kb}
done

for kb in synthmed_rare_kb.yaml; do
  orchestrate knowledge-bases import -f ${SCRIPT_DIR}/knowledge_bases/${kb}
done

for kb in synthmed_kb.yaml; do
  orchestrate knowledge-bases import -f ${SCRIPT_DIR}/knowledge_bases/${kb}
done

for agent in synthmed_autism_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done

for agent in synthmed_cancer_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done

for agent in synthmed_dimentia_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done

for agent in synthmed_epilepsy_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done

for agent in synthmed_rare_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done

for agent in synthmed_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done
