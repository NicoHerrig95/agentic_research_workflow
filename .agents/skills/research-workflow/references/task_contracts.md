# Persisted task contracts

STATE.json is operational state; PROJECT.md and paper notes remain scientific
sources of truth. Only the main Codex agent edits state and the shared index.
Checkpoint after accepted scope edits and at stage boundaries, not before
checking whether a changed project invalidates previous task assumptions.

## Task record

Append objects to STATE.json.tasks with:

```json
{
  "id": "analysis-P001-cycle1",
  "role": "paper_analyst",
  "status": "pending",
  "attempts": 0,
  "project_sha256": "SHA256 of the project supplied to the task",
  "inputs": ["PROJECT.md", "literature/INDEX.json"],
  "allowed_outputs": ["literature/papers/P001.md", "workflow/tasks/analysis-P001-cycle1/index-update.json"],
  "outputs": [],
  "source_access": null,
  "error": null
}
```

Statuses: pending, running, completed, failed, blocked. Increment attempts before
execution. Mark completed only after inspecting outputs and running applicable
validators. Record partial outputs and errors on failures. Source access is
full_text, abstract_only, unavailable, or null when not applicable.

For each delegated task, supply its role skill path, precise research question
or paper identifier, verified source link if known, project hash, inputs,
allowed output paths, limits, and expected return (paths, findings, source
access, limitations). Tell subagents not to modify other tasks or shared state.
Assign paper IDs centrally before launching analysts; scouts use disjoint ID
ranges and the main agent reconciles duplicate papers before merging.

## Index proposal

Save as workflow/tasks/<task-id>/index-update.json:

```json
{
  "base_sha256": "SHA256 of the exact current literature/INDEX.json bytes",
  "updates": {
    "P001": {"status": "analyzed", "summary_path": "literature/papers/P001.md", "date_analyzed": "2026-10-24"}
  }
}
```

Calculate hashes using Python hashlib.sha256(path.read_bytes()).hexdigest().
Dates in examples are illustrative: use the actual work date.
New entries must supply all fields required by templates/INDEX_template.json.
Unknown nullable metadata uses null; use empty lists or explicitly marked
unavailable text where appropriate. Never invent data to satisfy a validator.
Patches merge at the paper's top level: replace nested relevance objects in
full. Deletion is unsupported. Existing unrelated entries are preserved.
The empty initial index is treated as {} without changing it during validation.

Analyst source_access goes in summary YAML and task state, since the existing
index schema does not contain that field. Abstract-only limitations must also
be clear in the summary body. Unavailable sources remain unresolved rather than
receiving a fabricated complete analysis.

## Approval requests

Save a Markdown proposal with the current statement, replacement, rationale,
evidence, and impact. Add to STATE.json.approval_requests:

```json
{
  "id": "scope-cycle1",
  "proposal_path": "workflow/proposals/scope-cycle1.md",
  "status": "pending",
  "user_decision_reference": null
}
```

Record approved/rejected only after an explicit human decision; reference the
actual user message or saved decision record. Scripts do not grant approval.
On approval, apply only the agreed changes and checkpoint. Resume unrelated
work while awaiting a decision when useful.
