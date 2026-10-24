
---
name: paper_analyst
description: Read scientific papers and produce standardized, evidence-backed Markdown summaries. Use when analyzing a PDF, DOI, arXiv paper, or item in the literature reading queue.
---

# Scientific Paper Analyst

## Purpose

Produce accurate, critical, standardized
summaries of scientific publications.

Each paper receives one Markdown document
under literature/papers/.

## Inputs

- Paper PDF, DOI, arXiv ID, or verified URL
- PROJECT.md for project-specific relevance
- assets/PAPER_SUMMARY_TEMPLATE.md
- Existing paper summary, if present

## Workflow

### 1. Retrieve and verify source

1. Verify paper title, authors, and publication.
2. Retrieve the full text when possible.
3. Prefer the publisher version when available.
4. Identify the version being analyzed.
5. Mark abstract-only analyses explicitly.

Do not claim to have read a complete paper
when only the abstract is available.

### 2. Understand the paper

Identify:
- Main research problem
- Authors' motivation
- Core methodology
- Important assumptions
- Formal definitions or algorithms
- Claimed contributions
- Experimental evaluation
- Reported limitations

Prioritize methodological substance over
generic summaries.

### 3. Critically evaluate

Consider:
- Are the assumptions justified?
- Does the evaluation support the conclusions?
- Are baselines appropriate?
- Is generalization sufficiently investigated?
- Which results are actually demonstrated?
- What remains unresolved?

Clearly distinguish:
A. Claims made by the authors
B. Evidence presented in the paper
C. Independent critical analysis

### 4. Relate to research project

Read PROJECT.md.

Identify:
- Research questions addressed or influenced
- Methodological similarities
- Significant differences
- How the paper is helpful for our project
- Potential threats to claimed novelty
- Ideas that could improve experiments
- Opportunities for further research

Do not force relevance where none exists.

### 5. Generate standardized summary

Use assets/PAPER_SUMMARY_TEMPLATE.md.

Save as:
literature/papers/<paper-id>.md

Include:
- Verified bibliographic metadata
- Executive summary
- Research problem
- Methodology
- Contributions
- Experimental evaluation
- Limitations
- Relevance to project
- Research opportunities
- Evidence references

For substantive technical claims, cite
specific pages, sections, equations, or tables
when available.

Explicitly flag claims that could not be
verified from the available source.

### 6. Propose literature index updates

Do not edit literature/INDEX.json directly. Return a task-local index proposal
using the contract in ../research-workflow/references/task_contracts.md.
Include analysis status, summary path, and analysis date. Record full_text,
abstract_only, or unavailable in summary source_access metadata and the task
result. The main Codex agent validates and merges proposals sequentially.

## Output

- Standardized paper summary
- Main contributions
- Critical limitations
- Project-specific implications
- Unresolved questions

## Restrictions

- Do not modify PROJECT.md.
- Do not invent mathematical formulations,
  experimental details, or quantitative results.
- Do not equate authors' claims with
  independently established facts.
- Do not overwrite an existing paper analysis
  without incorporating its useful content.
