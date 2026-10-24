---
name: obsidian-sync
description: Synchronize a research project's Markdown knowledge base with an Obsidian vault through MCP. Use when creating a research project folder in Obsidian, syncing PROJECT.md and literature summaries, discovering relationships between publications, building an Obsidian knowledge graph, or maintaining existing research notes.
---

# Obsidian Research Knowledge Manager

## Purpose

Maintain an organized, interconnected research
knowledge base in an Obsidian vault.

Use the configured Obsidian MCP server for all
remote vault operations.

The local research repository is the authoritative
source for scientific document content.

Obsidian provides a synchronized knowledge layer
with navigable links between research artifacts.

## Inputs

Read the following local files when available:

- PROJECT.md
- literature/INDEX.json
- literature/papers/*.md
- ideas/BACKLOG.md

Optional inputs:
- Target Obsidian vault
- Destination folder
- Research project name
- Specific files to synchronize
- Graph generation scope

## Workflow

### 1. Discover MCP Capabilities

Before performing remote operations:

1. Identify the configured Obsidian MCP server.
2. Inspect its available tools.
3. Determine whether it supports:
   - Listing vaults
   - Listing files and folders
   - Creating folders
   - Reading notes
   - Creating notes
   - Updating notes
   - Deleting or moving files

Use only capabilities actually exposed by the
connected MCP server.

Never invent MCP tool names or capabilities.

If required capabilities are unavailable,
report the limitation.

### 2. Resolve Target Vault

Determine the requested target vault. In this repository, run
`python3 scripts/workflow_config.py` and use obsidian_vault from `.env` when
no explicit target was requested. An explicit user target takes precedence.
A null value means unconfigured; never use the placeholder `your_vault`.
Verify that the configured vault is accessible through MCP before writing.
Configuration alone does not authorize a synchronization operation.

If no vault is specified:
- Use a previously established project-vault
  mapping when available.
- Otherwise identify available vaults.
- Request a vault selection if necessary.

Never silently select an unrelated vault.

Do not create a new vault unless explicitly
requested and supported by MCP.

### 3. Create Research Project Folder

When requested, create:

<project-folder>/

Recommended structure:

<project-folder>/
├── PROJECT.md
├── INDEX.json
├── Papers/
├── Concepts/
└── Graph/

Before creation:
1. Check whether the target folder exists.
2. Avoid creating duplicate project folders.
3. Reuse the existing folder if appropriate.
4. Preserve unrelated existing content.

Folder creation is optional.

If a folder already exists, perform synchronization
within the existing location.

### 4. Synchronize Research Documents

Synchronize the following:

Required:
- PROJECT.md
- literature/papers/*.md

Optional:
- literature/INDEX.json
- experiments/EXPERIMENTS.md
- ideas/BACKLOG.md

Maintain stable destination paths.

Example mappings:

Local:
PROJECT.md

Obsidian:
<project-folder>/PROJECT.md

Local:
literature/papers/P001.md

Obsidian:
<project-folder>/Papers/P001.md

### 5. Incremental Synchronization

For each source document:

1. Verify that the local source exists.
2. Resolve the mapped Obsidian destination.
3. Check whether the destination exists.
4. Compare local and remote content.
5. Create missing notes.
6. Update changed notes.
7. Skip unchanged notes.

Never overwrite unrelated vault files.

Treat source documents as authoritative, but
preserve Obsidian-only user annotations.

If a remotely modified document conflicts
with the local source, report the conflict
and obtain a resolution before overwriting.

Do not perform destructive synchronization
or automatically delete remote notes.

### 6. Identify Knowledge Relationships

Analyze the synchronized research documents.

Identify relationships at three levels:

A. Project-to-Paper
- Paper supports a project claim
- Paper challenges a project claim
- Paper motivates the research problem
- Paper provides a methodological foundation
- Paper provides an experimental baseline

B. Paper-to-Paper
- Similar methodology
- Shared problem formulation
- Direct methodological extension
- Competing approaches
- Explicitly discussed prior work

C. Concept-Level
- Shared theoretical concepts
- Algorithms and mathematical methods
- Evaluation metrics
- Datasets and benchmarks
- Research domains

Use explicit citations, verified methodological
similarities, and existing paper summaries.

Do not create relationships solely because
papers share generic keywords.

Distinguish:
- Verified relationships
- Reasonably inferred relationships
- Hypothetical relationships requiring review

### 7. Create Obsidian Links

Use Obsidian-compatible internal links.

Examples:

[[PROJECT]]

[[Papers/P001|Paper Title]]

[[Concepts/JSD Alignment]]

Prefer vault-relative paths when note names
could otherwise be ambiguous.

Do not add links to nonexistent notes unless
creating the target note is part of the workflow.

Preserve existing links and manually authored
content.

Prefer updating a dedicated managed section
rather than rewriting an entire note.

### 8. Create Concept Notes

When recurring scientific concepts are found,
create concept notes under:

<project-folder>/Concepts/

Each note should include:

- Concept name
- Concise scientific definition
- Relevance to the research project
- Related papers
- Related project contributions
- Relationships to other concepts
- Source references

Reuse existing concept notes whenever possible.

Do not create separate notes for trivial
keywords or incidental terminology.

### 9. Build Knowledge Graph

Use Obsidian's native graph functionality
through Markdown internal links.

Ensure that:

1. PROJECT.md links to relevant paper notes.
2. Paper notes link to relevant concepts.
3. Related paper notes link to one another
   when a meaningful relationship exists.
4. Concept notes link to relevant project
   sections and publications.
5. All generated links resolve correctly.

Create:

<project-folder>/Graph/RELATIONSHIPS.md

Document important relationships in a
human-readable table containing:

- Source note
- Target note
- Relationship type
- Evidence
- Confidence

Do not assume the MCP server supports
direct manipulation of Obsidian's graph UI.

### 10. Validate Synchronization

After synchronization:

1. Verify required destination files exist.
2. Verify their content was written correctly.
3. Check generated internal links.
4. Check for duplicate paper notes.
5. Check for broken references.
6. Identify unresolved synchronization conflicts.
7. Report any unsupported MCP operations.

## Output

Provide a synchronization report containing:

- Target vault
- Target project folder
- Files created
- Files updated
- Files unchanged
- Conflicts detected
- New concept notes
- New knowledge relationships
- Broken or unresolved links
- Any synchronization limitations

## Restrictions

- Never modify the local research scope
  based solely on Obsidian content.
- Never silently overwrite user annotations.
- Never delete remote notes without approval.
- Never invent paper relationships or citations.
- Never create duplicate paper notes.
- Never use an unverified target vault.
- Do not modify the substance of PROJECT.md.
- Do not present inferred links as proven facts.
- Do not claim synchronization succeeded
  without confirming the remote write.
