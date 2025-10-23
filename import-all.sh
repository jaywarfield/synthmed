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

for kb in synthmed_kb.yaml; do
  orchestrate knowledge-bases import -f ${SCRIPT_DIR}/knowledge_bases/${kb}
done

for agent in synthmed_agent.yaml; do
  orchestrate agents import -f ${SCRIPT_DIR}/agents/${agent}
done
