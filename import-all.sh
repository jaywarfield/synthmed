#!/usr/bin/env bash
set -x

orchestrate env activate synthmed
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

#for openapi_tool in get-healthcare-providers.yml; do
#  orchestrate tools import -k openapi -f ${SCRIPT_DIR}/tools/${openapi_tool} -r ${SCRIPT_DIR}/tools/requirements.txt;
#done

# Import all Python tools
for tool in ${SCRIPT_DIR}/tools/*; do
  if [ -f "$tool" ]; then
    echo "Importing python tool: $tool"
    orchestrate tools import -f "$tool" -k python
  fi
done

# Import all knowledge bases
#for kb in ${SCRIPT_DIR}/knowledge_bases/*.yaml; do
#  if [ -f "$kb" ]; then
#    echo "Importing knowledge base: $kb"
#    orchestrate knowledge-bases import -f "$kb"
#  fi
#done

# Import all agents
#for agent in ${SCRIPT_DIR}/agents/*.yaml; do
#  if [ -f "$agent" ]; then
#    echo "Importing agent: $agent"
#    orchestrate agents import -f "$agent"
#  fi
#done

for kb in synthmed_autism_kb.yaml; do
  orchestrate knowledge-bases import -f ${SCRIPT_DIR}/knowledge_bases/${kb}
done

for kb in synthmed_cancer_kb.yaml; do
  orchestrate knowledge-bases import -f ${SCRIPT_DIR}/knowledge_bases/${kb}
done

for kb in synthmed_dementia_kb.yaml; do
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

for agent in synthmed_dementia_agent.yaml; do
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
