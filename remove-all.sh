#!/usr/bin/env bash
set -x

orchestrate env activate synthmed
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Remove all agents
for agent in ${SCRIPT_DIR}/agents/*.yaml; do
  if [ -f "$agent" ]; then
    filename=${agent##*/}
    agentname=${filename%.*}
    echo "Removing agent: $agentname"
    orchestrate agents remove --name $agentname --kind native
  fi
done

# Remove all knowledge bases
for kb in ${SCRIPT_DIR}/knowledge_bases/*.yaml; do
  if [ -f "$kb" ]; then
    filename=${kb##*/}
    kbname=${filename%.*}
    echo "Removing knowledge base: $kbname"
    orchestrate knowledge-bases remove --name $kbname
  fi
done
