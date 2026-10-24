# Research Workspace Instructions

## Source of Truth
- PROJECT.md contains the accepted research scope.
- Paper notes contain source-specific evidence.
- ideas/BACKLOG.md contains unapproved proposals.
- Always read PROJECT.md before project-specific work.

## Roles
- project_manager: synthesizes findings and maintains
  the project definition.
- literature_scout: discovers and ranks relevant work.
- paper_analyst: generates standardized paper analyses.

## Workflow
- Delegate independent literature work when available.
- Scout updates only literature discovery records.
- Analyst updates only individual paper summaries.
- Project manager proposes important scope changes
  and applies them after user approval.

## Scientific Integrity
- Never invent citations, results, or paper details.
- Prefer primary sources and full-text evidence.
- Distinguish authors' claims from agent analysis.
- Cite sections/pages for substantive paper claims.
- Mark unavailable information explicitly.
- Do not claim research novelty solely because
  a search found no competing paper.

## Persistence
- Save research findings in repository files.
- Do not rely on conversation history as the
  authoritative project record.
- Preserve existing accepted research decisions.

## Obsidian Integration

Use the `obsidian_sync` skill for:
- Creating or locating project folders in Obsidian
- Synchronizing PROJECT.md and paper summaries
- Maintaining internal links
- Identifying meaningful relationships
- Updating the research knowledge graph

The local repository is the source of truth.

Obsidian synchronization must not silently
change scientific content or accepted project
decisions.

When syncing, preserve user-authored notes
and identify conflicts before overwriting.

Use stable paper IDs from literature/INDEX.json
as Obsidian note filenames.

## Codex Workflow Orchestration

For end-to-end research cycles, use `.agents/skills/research-workflow/SKILL.md`.
The main Codex agent maintains `workflow/STATE.json` and is the sole writer of
`literature/INDEX.json`. Scouts and analysts save task-local index proposals;
the main agent validates and merges them sequentially with the repository helper.
This refines the role boundaries above: analysts own assigned paper summaries,
scouts own discovery records, and neither writes the shared index directly.
Delegate independent research work with explicit task IDs and output paths.
Run `python3 scripts/validate_workspace.py` before resuming and after a cycle.
Operational checkpoints never constitute approval of scientific scope changes.
