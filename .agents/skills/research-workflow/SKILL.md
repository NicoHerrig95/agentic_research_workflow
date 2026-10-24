---
name: research-workflow
description: Run or resume a bounded research cycle in this Codex repository, coordinating literature discovery, parallel paper analysis, synthesis, and review with persisted progress. Use for end-to-end research work rather than a standalone paper summary or repository inspection.
---

# Codex Research Workflow

The main Codex agent owns orchestration. Use existing specialist skills for
scientific reasoning and repository scripts for mechanical validation. This
skill does not launch an external agent runtime.

## Start or resume

1. Read AGENTS.md, PROJECT.md, workflow/STATE.json, and RESEARCH_PROPOSAL.md
   when present. Run `python3 scripts/validate_workspace.py`.
2. Run `python3 scripts/workflow_config.py` to resolve `.env` settings. Never
   source `.env` as shell code or print unrelated settings. Treat
   MAX_PARALLEL_PAPERS as a ceiling, even if a saved run requests more. Only
   change the configured ceiling when the user requests a configuration change.
   If the proposal is absent, report the missing intake input; do not invent a
   topic. Inspection and workflow maintenance do not require a proposal.
3. Read [task contracts](references/task_contracts.md) before delegating or
   recording tasks. Check existing outputs before retrying interrupted tasks.
   A task marked running from a previous chat is not proof an agent is active.
4. Compare PROJECT.md against the saved hash. If changed, reassess pending tasks
   and mark affected completed tasks for review in unresolved_issues. Never
   silently discard summaries or accepted decisions.
5. Establish a bounded cycle using user limits or STATE.json defaults. Limits
   are maximums, not targets. Save changes and checkpoint before delegation.

## Research cycle

- **Intake:** Use research_coordinator to draft a project definition from the
  proposal. Save material changes under workflow/proposals/ with rationale,
  evidence, and current/proposed text. Obtain user approval before applying
  accepted research scope changes. Record the actual decision reference.
- **Discovery:** Delegate independent search strands to literature_scout when
  useful. Assign nonoverlapping task IDs, search filenames, and paper ID ranges.
  Scouts save search records and index proposals, never the shared index.
- **Analysis:** Select papers within the cycle limit. Delegate one paper per
  analyst task. Before every dispatch batch, reload configuration and run
  `python3 scripts/workflow_config.py --check-capacity`. Use at most the returned
  available_slots and actual host capacity. Save each task as running before
  launching; on launch failure record failure and release its slot. Wait for
  completion and update task state before filling freed slots. Never exceed
  min(MAX_PARALLEL_PAPERS, max_parallel_analysts). If existing running tasks
  exceed a lowered cap, reconcile them and wait before further dispatch. Each reads
  paper_analyst and writes only its assigned summary and task-local proposal.
- **Collection:** Inspect results and source access. Validate summaries and
  index proposals. Only the main agent runs index merges, sequentially. Rebase
  stale proposals by inspecting the current index and reconciling conflicts;
  never merely replace the hash. Count inaccessible papers as attempted tasks,
  record the limitation, and do not label them analyzed without evidence.
- **Synthesis:** Use research_coordinator to save a dated synthesis under
  ideas/ and unapproved directions in ideas/BACKLOG.md. Propose rather than
  silently apply material PROJECT.md changes.
- **Review:** Delegate a separate reviewer using research_reviewer. Request a
  saved review explicitly, scoped to existing evidence. Do not request venue
  recommendations unless the user requested them. Save concerns and next steps.
- **Finish:** Validate the workspace, save unresolved issues and checkpoint.
  Stop after one cycle by default; reviewer concerns do not authorize unlimited
  searches. Report outputs, limitations, and any pending decision.

If subagents are unavailable, perform specialist stages sequentially and state
that the review was not independent. Avoid nested delegation. A failed task
gets at most max_task_attempts attempts; then record failure and continue useful
independent work. Pause only dependent work at approval or missing-input points.

Obsidian sync is optional and requires the user's requested target/scope. Use
obsidian_sync, use the configured OBSIDIAN_VAULT unless the user explicitly
selects another target, verify the vault, and report conflicts before overwriting. A
local research run does not itself authorize remote synchronization.

## Helpers

Run from the repository root with Python 3.10+; no third-party dependencies:

```sh
python3 scripts/workflow_state.py status
python3 scripts/workflow_state.py checkpoint --stage analysis
python3 scripts/validate_paper_summary.py literature/papers/P001.md
python3 scripts/merge_index_updates.py workflow/tasks/analysis-P001/index-update.json
python3 scripts/merge_index_updates.py workflow/tasks/analysis-P001/index-update.json --apply
python3 scripts/validate_workspace.py
```

Scripts validate structure and references, not the truth of scientific claims.
File ownership is an instruction convention, not an OS sandbox. Do not run two
orchestrators against the same repository concurrently.
