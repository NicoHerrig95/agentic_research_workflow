# Agentic research workflow for Codex

A repository-based research workspace: Codex coordinates literature discovery,
paper analysis, research synthesis, and critical review through specialist skills.
The repository is the source of truth; Obsidian synchronization is optional.

## Start in Codex

1. Add your research proposal as `RESEARCH_PROPOSAL.md`.
2. Open this repository in Codex and ask:

   > Use $research-workflow to start a research cycle from my proposal. Analyze
   > up to five papers and delegate independent paper analyses to subagents.

3. Review proposed initial scope or material changes before they are applied.

To resume in a fresh chat:

> Use $research-workflow to resume from workflow/STATE.json. Check existing
> artifacts and pending decisions before repeating work.

The skill contains orchestration instructions, not a background service. Codex
runs the stages during the active task. Python helpers do not launch agents,
call model APIs, approve research changes, or synchronize Obsidian.

## Repository records

- `PROJECT.md`: accepted scope, research questions, methodology, experiments.
- `literature/INDEX.json`: paper registry; schema in `templates/INDEX_template.json`.
- `literature/searches/`: reproducible discovery records.
- `literature/papers/<paper-id>.md`: evidence-backed paper analyses.
- `ideas/BACKLOG.md`: unapproved research proposals.
- `reviews/`: saved critical assessments.
- `workflow/STATE.json`: stage, limits, task results, and pending approvals.
- `workflow/tasks/`: task-local index proposals; `workflow/proposals/`: scope changes.

## Local helpers

Python 3.10+ is required; no additional packages are needed.

```sh
python3 scripts/validate_workspace.py
python3 scripts/workflow_state.py status
python3 scripts/workflow_state.py checkpoint --stage analysis
python3 scripts/validate_paper_summary.py literature/papers/P001.md
python3 scripts/merge_index_updates.py workflow/tasks/analysis-P001/index-update.json
# Only the coordinating Codex agent applies proposals, one at a time:
python3 scripts/merge_index_updates.py workflow/tasks/analysis-P001/index-update.json --apply
python3 -m unittest discover -s tests -v
```

Index proposals are dry-run by default and must reference the SHA-256 of the
current index. Stale proposals require reconciliation against the current
contents. Writes use atomic replacement. Run only one coordinating chat per
checkout; the scripts do not provide cross-process locking or enforce agent
file permissions. The small schema validator supports the index schema's
current keyword subset and rejects unsupported validation keywords.

Validation checks structure, paths, and references. It does not verify citations,
scientific conclusions, actual human approval, or publication readiness.
Missing intake documents and an unfilled project template produce warnings.
The initial workspace intentionally contains no invented research topic.

## Local configuration

Edit `.env` (ignored by Git); `example.env` documents the supported settings:

```dotenv
OBSIDIAN_VAULT="your_vault"
MAX_PARALLEL_PAPERS=3
```

Replace `your_vault` with the exact vault name. This config selects a destination;
it does not authorize synchronization or configure the MCP connection.

`MAX_PARALLEL_PAPERS` is a positive integer ceiling for simultaneous paper
analyst tasks. Set it to `1` for sequential reading. The effective limit is the
smaller of this ceiling and `workflow/STATE.json`'s `max_parallel_analysts`;
Codex host capacity can reduce it further. `max_papers` still limits the total
papers in a cycle. Invalid values fail validation. Missing settings default to
three concurrent papers and an unconfigured vault. The file is parsed as literal
KEY=value data, never sourced as shell code; environment variables do not override it.

```sh
python3 scripts/workflow_config.py
python3 scripts/workflow_config.py --check-capacity
```

Codex checks capacity before dispatch and records running tasks before launching
them. Workspace validation rejects recorded concurrency above the cap. This is
an orchestration guardrail, not an operating-system limit: it relies on accurate
state and a single coordinating chat. Lowering the cap does not terminate existing
agents; reconcile them before starting additional work.
