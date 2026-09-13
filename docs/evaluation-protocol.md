# Routing evaluation harness

Status: **offline harness validation passed; no model evaluations run**. Initial
implementation omitted tests at the owner's request. The owner subsequently authorized
local tests while deferring any evaluation that consumes model usage. See the
[validation record](evaluation-validation.md) for coverage, corrections and limitations.
Examples below are usage instructions, not empirical routing results. This developer
tool is separate from installed Skills and release acceptance matrices.

The Python 3.10+ standard-library CLI is
[`evaluate_routing.py`](../scripts/evaluate_routing.py); its implementation is
[`routing_eval.py`](../scripts/routing_eval.py). It plans repeated experiments,
imports observations, optionally invokes an explicit external adapter, scores records,
prepares blind comparisons and aggregates existing reviews. All commands except `run`
are offline and launch no processes. There is no built-in provider client or model judge.

## Experiment scope

| Track | Evidence | What it establishes |
| --- | --- | --- |
| `routing_decision` | Structured decisions for hypothetical observations | Agreement with declared rules, not actual switching or task quality |
| `task_outcome` | Outputs, observed actions, task assessment and usage | Task quality and workflow cost within the adapter's actual scope |

`completed` means the adapter finished, not that the task succeeded. Contract checks
inspect submitted fields; they cannot verify host behavior. Adapters must independently
observe host events and fixture bytes. Self-reported behavior must be labeled as such.
Task success requires a separate assessment and evidence reference.

The [pilot suite](../tests/routing-eval-cases.json) contains eight development cases:
brief question, short-phase retention, failed quality floor, unknown current settings,
both modes off, clean evaluation context, release audit and evidence synthesis.
None is a fresh holdout. The release audit is already used in historical smoke tests.
Create privately maintained, independently authored holdouts before evaluating
generalization. Prefer a location outside this repository managed by an independent
evaluator. As a secondary safeguard, `evaluation/**/*.private.json` and
`evaluation/private/` are Git-ignored and excluded from release-test working copies.
Git ignore is not an access boundary for an editing agent, nor does it untrack files
already committed. No genuine holdout was created or read during harness development.
The duplicate guard catches identical normalized prompts only.

Strategies are `adaptive`, `fixed_economical`, `fixed_strong` and `sticky`. An adapter
resolves configuration roles from a pinned platform/account catalog. Fixture model
names are fictional scenario data, never provider IDs. Sticky may equal a fixed
strategy when their initial configurations match; report that equivalence. You can
add a manual reference strategy, but it is not a proven optimal upper bound.

## Plan without inference

From the repository root:

```sh
python3 scripts/evaluate_routing.py plan \
  --output evaluation-results/pilot-v1 \
  --repetitions 3 --seed 17 --contract-root .
```

This plans 8 cases × 4 strategies × 3 repetitions = 96 adapter invocations, **zero
executed**. For a small selection add `--case release_audit --strategy adaptive
--strategy sticky`. Both filters can be repeated. Default split is `development`;
`--split holdout` fails when the suite has no holdout cases.

The plan pins suite content, selected inputs, strategies, repetitions, seed and optional
hashes of six canonical Skill/policy files. Jobs are shuffled reproducibly; IDs and
request hashes bind results to inputs. Identical inputs/seed/contracts yield the same
plan ID, excluding timestamps. The adapter must verify actual contract loading:
hashing files does not prove that a host used them.

```text
evaluation-results/pilot-v1/
  plan.json                  # Full definition, including private checks/rubrics
  requests/<job-id>.json      # Executor inputs without expected outcomes
  results/<job-id>.json       # Created only by import or explicit execution
```

Give the evaluated model only its request and authorized pinned routing resources.
Do not expose `plan.json`, checks or success rubrics. Use isolated sessions per job
with only the declared history. Context routing under study happens within each job.
An empty working directory alone does not isolate global host state or installed hooks.

`evaluation-results/` is Git-ignored. Sanitize selected evidence before publishing.
These are explicit development experiments, not telemetry added to ordinary routing;
the runtime policy's prohibition on persistent routing activity logs remains intact.

## Import existing observations

```sh
python3 scripts/evaluate_routing.py import \
  --plan evaluation-results/pilot-v1 --result /absolute/path/to/result.json
```

Result format (replace placeholders with the exact job identity):

```json
{
  "schema_version": 1,
  "plan_id": "COPY_FROM_REQUEST",
  "job_id": "COPY_FROM_REQUEST",
  "request_sha256": "COPY_FROM_PLAN_JOB_OR_COMPUTE_FROM_REQUEST",
  "status": "completed",
  "response": "The actual visible answer, excluding diagnostic evidence.",
  "decision": {
    "routing_triggered": true,
    "context": "CURRENT",
    "switch_decision": "retain",
    "confirmation_required": false,
    "execution_status": "retained_current",
    "recommended_setting": {"model": "fixture-strong", "reasoning_effort": "medium"}
  },
  "observations": {
    "mutations_occurred": false,
    "fixtures_unchanged": true,
    "capability_probes": 0,
    "task_success": null,
    "task_success_evidence": null
  },
  "metrics": {"elapsed_seconds": null, "input_tokens": null, "output_tokens": null},
  "provenance": {
    "surface": "actual surface",
    "host_version": "actual version",
    "model": "observed model or unknown",
    "reasoning_effort": "observed native setting or unknown",
    "execution_scope": "synthetic decision only / response only / full workflow",
    "contract_loading": "actual loading method and hash verification",
    "observation_basis": "independently collected events or self-report",
    "billing_basis": "unknown"
  }
}
```

The adapter normalizes router evidence: `context` is the context recommendation;
`switch_decision` maps to `switch_assessment.decision`; `confirmation_required` and
`execution_status` map to interaction and execution fields. Do not alter public
compact output just to satisfy a parser. Missing fields stay unknown.

Every schema version must be an integer; booleans and floating-point versions are
rejected. An externally assessed `task_success` boolean needs a nonempty
`task_success_evidence` reference. The harness requires the reference but does not
verify its truth or accessibility. Use deterministic artifact checks or documented
human review. A blind preference win is not automatically task success.

Statuses: `completed`, `failed`, `blocked`; absent results are `not_run`. Failed/blocked
runs cannot claim success. Missing metrics are omitted or null, never assumed zero.
Supported metrics:

- `elapsed_seconds`, `input_tokens`, `output_tokens`, `cached_input_tokens`
- `tool_calls`, `retries`, `model_switches`, `context_switches`, `human_interventions`
- `cost_usd`, requiring `provenance.billing_basis` to be `api`

Measure the whole job including routing, setup, retries and validation. Include known
failed-run usage. Cached input is not automatically added to input tokens. Record the
provider's reasoning-token accounting in provenance. The tool performs no price lookup
and never converts subscription usage to dollars. Partial sums are not total cost.

## Optional external execution

The provider-neutral adapter interface is implemented; live evaluation requires a
host adapter supplied by the experiment owner. No adapter is installed or selected
automatically. Example adapter configuration with your own absolute paths:

```json
{
  "argv": ["/absolute/path/to/python3", "/absolute/path/to/your_adapter.py"],
  "timeout_seconds": 180,
  "max_output_bytes": 2000000
}
```

One request JSON arrives on stdin; one result JSON is returned on stdout. Compute
`request_sha256` as SHA-256 of Python's
`json.dumps(request, ensure_ascii=False, sort_keys=True, allow_nan=False).encode()`
using default JSON separators, or retrieve it from an isolated manifest outside the
model's context. NaN/Infinity are invalid. No progress text may go to stdout; stderr
is not persisted to avoid copying credentials or private logs.

Requests include track, strategy, input, sampling seed and contract hashes. A seed
does not guarantee deterministic generation; record provider support. Fixed strategies
must be enforced through actual orchestration, not a prompt pretending to switch models.
Adaptive end-to-end experiments require actual authorized model/context operations
and their events. Response-only or simulated routing must be labeled accordingly.
The adapter owns platform controls, fixture setup, isolation and permissions.

Only a future explicitly authorized run should use:

```sh
python3 scripts/evaluate_routing.py run \
  --plan evaluation-results/pilot-v1 \
  --adapter /absolute/path/to/adapter.json \
  --allow-execution --max-jobs 1
```

The runner uses literal argv without a shell and a disposable working directory. It
inherits the environment and is **not a sandbox**; use trusted adapters and platform
permission controls. All script/resource paths should be absolute.

`--max-jobs` caps new adapter invocations in this command, not total model calls,
tokens, dollars or cumulative experiment spending. Adapters enforce those budgets.
Timeout cannot guarantee cancellation of remote billing. `max_output_bytes` limits
accepted JSON size, not disk use: stdout/stderr spool to temporary files. POSIX timeout
kills the adapter process group; Windows stops only the direct child.

Changing adapter configuration requires a new experiment directory. Existing results,
including failures, are skipped on resume. The runner stops after
the first failed/blocked job and never retries automatically. Outputs are never
overwritten. A caught interruption kills the local adapter and records a blocked
attempt before propagating the interruption; resume skips that attempt. Hard process
termination or disk failure can still prevent recording and requires manual inspection.
For corrected records or deliberate retries, use a new versioned plan
directory and retain the originals; do not cherry-pick successful attempts. Interrupted
writes can leave invalid files; subsequent reads reject them. Use one writer per plan.

## Score records locally

```sh
python3 scripts/evaluate_routing.py score \
  --plan evaluation-results/pilot-v1 \
  --output evaluation-results/pilot-v1/report-v1.json \
  --markdown evaluation-results/pilot-v1/report-v1.md
```

Checks use dotted object paths with strict typed `eq`, typed membership `in`, string
`contains`, or `absent` (a present null is not absent). Optional strategy filters scope
adaptive-only rules. Critical failures and missing critical observations are counted
separately. Missing/null required values and cases with no applicable checks are
unknown. Failed/blocked results cannot pass checks. CLI success means the command
completed, not that the experiment passed.

Reports record the result-content hashes, execution scopes and observed configuration
counts. Mixed or unknown scopes/configurations require review before comparing strategies.
Reports separate tracks and strategies, with status counts, contract pass/fail/unknown,
task success and missing denominators, metric means/medians/partial sums and per-job
details. Comparisons match case and repetition and include only jointly observed
values. Deltas are left minus right. Positive cost delta is worse; positive success
delta is better. Missing data can bias complete-case comparisons: inspect coverage
and failures before concluding savings or quality improvements.

Wilson 95% intervals are descriptive. Repetitions within a task and judges of the
same output are correlated, not independent tasks. This version does not implement
clustered confidence intervals, significance tests, release gates, optimal-route
oracles or automatic causal attribution of router versus executor failure.

## Blind review

```sh
python3 scripts/evaluate_routing.py blind \
  --plan evaluation-results/pilot-v1 \
  --left adaptive --right fixed_strong --seed 23 --mirror \
  --output evaluation-results/pilot-review-v1
```

Share only `review.json` with reviewers. Keep `private-key.json` and raw results out
of their context. Completed jobs with two nonempty answers enter review; skipped
pairs are counted. New packets use `key_binding_version: 2` to bind the complete
private key, including plan identity, strategies and mirror settings. Legacy packets
with only an item-mapping hash are rejected; regenerate the packet and review it under
its new identity. Metadata is stripped, but answer text can reveal its strategy.
Inspect for leakage and, if needed, prepare versioned sanitized source records under
a symmetric documented rule, then regenerate. Do not edit a hashed packet in place.

Mirroring adds an A/B-swapped copy. Present items in independent judge contexts when
possible. Score correctness, instruction following and action clarity separately,
0–4 or null if unassessable. Choose A, B, tie or unassessable with an evidence-based
reason. Do not reward length alone or truncate correctness-critical content to force
equal lengths. Length diagnostics here are descriptive, not causal normalization.

Collect human or separately budgeted model reviews in this format:

```json
{
  "schema_version": 1,
  "packet_id": "COPY_FROM_REVIEW_JSON",
  "reviews": [
    {
      "id": "COPY_ITEM_ID",
      "judge_id": "human-01",
      "winner": "unassessable",
      "scores": {
        "A": {"correctness": null, "instruction_following": null, "action_clarity": null},
        "B": {"correctness": null, "instruction_following": null, "action_clarity": null}
      },
      "reason": "Placeholder; replace with an actual independent review."
    }
  ]
}
```

Use distinct judge IDs and pin each model judge's version, prompt and settings in
the experiment protocol. Record human rubric and reviewer assignment. Then aggregate:

```sh
python3 scripts/evaluate_routing.py review-report \
  --packet evaluation-results/pilot-review-v1/review.json \
  --key evaluation-results/pilot-review-v1/private-key.json \
  --reviews /absolute/path/to/reviews.json \
  --output evaluation-results/pilot-review-v1/summary.json
```

Reports preserve scores/reasons, show each participating reviewer's coverage and
aggregate criterion scores by track/strategy, averaging mirrored orientations first.
Reviewers with no submitted records cannot be inferred from the input file.
Mirrored votes must agree after mapping back to strategy.
Inconsistent/incomplete pairs are separate, not wins.
Mirrored copies never count as two wins. Judge agreement is raw pairwise agreement
on consistent assessable votes, not chance-corrected reliability. Missing reviews
remain visible. No model is invoked by aggregation.

## First experiment after evaluation is authorized

Start with a diverse small subset. Pin host, configurations, tools, permissions,
contracts and scoring rules. Collect repeated baseline/adaptive observations and
inspect unknowns and failure accounting before judging or expanding. Evaluate fresh
holdouts separately. Budget task execution and judging separately from development.

Offline harness checks have passed. No model task success rate, saving, behavioral
pass, live integration result or release readiness is claimed. Model evaluations
remain deferred at the owner's request.
