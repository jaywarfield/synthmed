from ibmdiagrams.ibmcloud.diagram import *
from ibmdiagrams.ibmcloud.ai import *
from ibmdiagrams.ibmcloud.actors import *
from ibmdiagrams.ibmcloud.connectors import *
from ibmdiagrams.ibmcloud.data import *
from ibmdiagrams.ibmcloud.devops import *
from ibmdiagrams.ibmcloud.observability import *
from ibmdiagrams.ibmcloud.security import *
from ibmdiagrams.ibmcloud.groups import *

with Diagram("synthmed_midpoint"):
  with PublicNetwork("Public Network", direction="TB"):
    researcher = User("Researcher")
  with IBMCloud("IBM Cloud", direction="TB"):
    with Region("Toronto", direction="TB"):
      with watsonx("watsonx", direction="TB"):
        with watsonxOrchestrate("watsonx Orch", "Manage Agents") as orchestrate:
          mainagentquery = CloudLogs("Input")
          mainagent = WatsonStudio("Agent", "Main")
          mainagentreply = CloudLogs("Output")
          mainagentquery >> mainagent
          mainagent >> mainagentreply
          researcher >> SolidEdge("Query") >> mainagentquery
          with ExpandedApplication("Disease Agents", direction="TB") as diseaseagents:
            with ExpandedApplication("Agent"):
              autismagent = WatsonStudio("Agent", "Autism")
              autismkb = Database("Vector DB", "Autism")
              autismagent >> autismkb
            with ExpandedApplication("Agent"):
              canceragent = WatsonStudio("Agent", "Cancer")
              cancerkb = Database("Vector DB", "Cancer")
              canceragent >> cancerkb
            with ExpandedApplication("Agent"):
              dimentiaagent = WatsonStudio("Agent", "Dimentia")
              dimentiakb = Database("Vector DB", "Dimentia")
              dimentiaagent >> dimentiakb
            with ExpandedApplication("Agent"):
              epilepsyagent = WatsonStudio("Agent", "Epilepsy")
              epilepsykb = Database("Vector DB", "Epilepsy")
              epilepsyagent >> epilepsykb
            with ExpandedApplication("Agent"):
              rareagent = WatsonStudio("Agent", "Rare")
              rarekb = Database("Vector DB", "Rare")
              rareagent >> rarekb
          mainagent >> diseaseagents
          with ExpandedApplication("RAG") as rag:
            vdb = Database("Vector DBs")
            llm = Database("Granite LLM")
            vdb >> llm
          diseaseagents >> rag
          #rag >> SolidEdge("Reply") >> researcher
          mainagentreply >> SolidEdge("Reply") >> researcher
