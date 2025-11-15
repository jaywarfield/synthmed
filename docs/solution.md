# **SynthMed Agent - IBM AI Lab Challenge: AI Medical Research Synthesis Agent**

## Solution

Description

watsonx enables a powerful Agentic AI medical research assistant by utilizing a pipeline that ingests, analyzes, and synthesizes insights from medical papers.  

The solution uses watsonx Orchestrate and Retrieval-Augmented Generation (RAG) to enable role-based multi-agent collaboration with queries to the main agent which invokes the appropriate subagent, and a response is returned back to the researcher showing where the response was obtained from.

RAG retrieves relevant chunks as the context for foundation models (LLMs) to generate narrative synthesis to ensure that outputs are grounded in source text and also shows which retrieved chunks support the output.

Researchers interact with the watsonx Orchestrate UI to submit complex queries, inspect retrieved passages, and see the agent’s results and use Prompt Lab to design prompts comparing output across Granite models to determine the appropriate model.

The architecture includes a main agent and multiple subagents organized by disease types that include autism, cancer, dementia, epilepsy, and rare diseases:

SynthMed Agent (main agent)
SynthMed Autism Agent
SynthMed Cancer Agent
SynthMed Dementia Agent
SynthMed Epilepsy Agent
SynthMed Rare Agent

Medical papers are uploaded into the vector DB (knowledge bases) of each subagent for use in answering questions related to a particular disease.

Additional work and testing was done on the descriptions and instructions of the main agent and each sub-agent to ensure repeatable and well-organized output.

Ambiguous instructions can lead to varying  layouts for the output, for example, 
Extra questions – Additional questions as needed to help clarify a query.  
Section headers – Section headers sometimes added but not consistently.
References – References combined together in a single paragraph making it difficult to find where the number of the reference is located.

Now we have stream-lined the descriptions and instructions of the main agent to help ensure repeatable and well-organized output.

For example:

SynthMed Main Agent:

description:  You are the central orchestrator agent of the SynthMed research ecosystem that coordinates disease sub-agents including Autism, Cancer, Dementia, Epilepsy, and Rare Diseases.

instructions: You interpret user query, identify relevant sub-agents,
route tasks accordingly, and compile a unified response across all relevant sub-agents that satisifies the user query in the following format:

1. Section named Executive Summary with brief executive summary of 2 to 4 sentences.
2. Section named Synthesis combining sub-agent responses logically.
3. Section named Disease Domain containing a domain table with following column headings:
 | Disease Domain | Key Findings | References | Level of Evidence |
 |------------------------|-------------------|-----------------|-------------------------|
4. Section named References with each reference starting on a separate line.
5. Section named Note with "This summary is for research synthesis purposes only, not for clinical decision-making."

SynthMed Cancer Agent:

description: You are the disease sub-agent for cancer-related topics including metastasis, molecular mechanisms, biomarkers, treatments, and clinical trials.

instructions: You are the disease sub-agent for cancer-related topics.  You interpret the user query in terms of cancer-related topics and produce accurate, cohesive, and well-structured summaries, and return a response.

IBM watsonx Orchestrate makes it easy to embed intelligent agents directly into your web applications by using the embedded chat feature. It enables interactive, contextual conversations while maintaining enterprise-grade security and flexibility.
Intelligent agents are embedded directly into a web application using the embedded chat features to create rich, interactive experiences..  Agents connect with users through channels to entry points like websites, Slack workspaces, or other message platforms.   With the web chat channel, the agent is embedded directly into a web page, enabling dynamic, interactive conversations that boost engagement and productivity.  You can customize the UI and behavior to match your brand and user needs, handle advanced events securely, and work with both draft and live agents for testing and production.

Example agent workflow (from question to answer)
1. Researcher: “What are the emerging biomarkers for pancreatic cancer prognosis?”
2. Main agent parses the request and determines which subagent can handle the request.  
3. Synthesis omposes a structured summary that includes a link to the source of the answer. 
4, Researcher reviews the answer and source used to validate the answer.

---

# License

This application is licensed under the Apache License, Version 2.  Separate third-party code objects invoked by this application are licensed by their respective providers pursuant to their own separate licenses.  Contributions are subject to the [Developer Certificate of Origin, Version 1.1](https://developercertificate.org/) and the [Apache License, Version 2](https://www.apache.org/licenses/LICENSE-2.0.txt).

