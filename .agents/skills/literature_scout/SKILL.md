
---
name: literature_scout
description: Discover, verify, deduplicate, and rank scientific papers relevant to a research project. Use when searching related work, identifying competing methods, exploring research gaps, or expanding the literature reading queue.
---

# Literature Scout

## Purpose

Discover academically relevant literature and
maintain a reproducible literature search record.

## Inputs

Always read:
- PROJECT.md
- literature/INDEX.json (if present)

Inspect:
- The literature/searches directory, listing your past searches. 

Extract:
- Research questions
- Methodology and technical concepts
- Claimed contributions
- Existing related work
- Relevant application domains

## Workflow

### 1. Define search strategy

Translate the research scope into search queries.

Search across:
- Direct terminology from the project
- Synonyms and alternative terminology
- Closely related methodological families
- Competing approaches
- Foundational work
- Recent developments

Avoid relying on a single terminology.

### 2. Search scientific sources

Prefer:
- Semantic Scholar
- OpenAlex
- arXiv
- Crossref
- Publisher or institutional repositories

Use available scholarly APIs, MCP integrations,
or web search tools.

Never invent paper metadata, identifiers, or URLs.

Record which search sources were accessible.

### 3. Screen and deduplicate

For each candidate:
1. Verify title and authors.
2. Record DOI or arXiv ID when available.
3. Check whether it is already indexed.
4. Evaluate relevance against the RQs.
5. Identify methodological overlap.
6. Decide whether detailed analysis is warranted.

Do not assume a title match alone proves that
two records are identical.

### 4. Rank candidates

Assign relevance:
- High: directly competing or closely related
  method, problem, or contribution.
- Medium: relevant technical foundation,
  evaluation methodology, or application.
- Low: useful background or peripheral topic.

Explain each relevance assessment briefly.

### 5. Persist findings and propose index updates

Do not edit literature/INDEX.json directly. Save a task-local index proposal
using ../research-workflow/references/task_contracts.md. The main Codex agent
validates and merges it. Use only assigned paper IDs when working in parallel.
The format can be found in templates/INDEX_template.json
For each entry, only fill fields which are completable by your summaries knowledge. Beware that some fields will be completed by the paper_analyst agent.


For each search session, create:
literature/searches/YYYY-MM-DD-topic.md

### 6. Prepare handoff

Identify the papers most deserving full analysis.

Do not create full paper summaries.
Pass selected identifiers and verified links
to the paper_analyst workflow.

## Output

Report:
- Number of candidates screened
- Number of new relevant papers
- Highest-priority papers
- Potentially competing approaches
- Recommended papers for analysis
- Search limitations

## Restrictions

- Do not modify PROJECT.md.
- Do not write detailed paper summaries.
- Do not claim an exhaustive literature search
  unless coverage is genuinely established.
- Do not treat unverified search snippets as
  reliable evidence of a paper's results.
