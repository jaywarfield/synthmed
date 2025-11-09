#!/usr/bin/env bash
set -x

orchestrate env activate synthmed
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Import all tools
for tool in ${SCRIPT_DIR}/tools/*.py; do
  if [ -f "$tool" ]; then
    echo "Importing tool: $tool"
    orchestrate tools import -k python -r ${SCRIPT_DIR}/tools/requirements.txt -f "$tool"
  fi
done

# Import all knowledge bases
for kb in ${SCRIPT_DIR}/knowledge_bases/*.yaml; do
  if [ -f "$kb" ]; then
    echo "Importing knowledge base: $kb"
    orchestrate knowledge-bases import -f "$kb"
  fi
done

# Import all agents
for agent in ${SCRIPT_DIR}/agents/*.yaml; do
  if [ -f "$agent" ]; then
    if [ "$agent" = ${SCRIPT_DIR}/agents/synthmed_agent.yaml ]; then
      echo "Deferring agent: $agent"
    else
      echo "Importing agent: $agent"
      orchestrate agents import -f "$agent"
    fi
  fi
done
# Import main agent last since main agent refers to subagents.
echo "Importing agent: ${SCRIPT_DIR}/agents/synthmed_agent.yaml"
orchestrate agents import -f ${SCRIPT_DIR}/agents/synthmed_agent.yaml
