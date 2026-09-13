# Routing harness offline validation

Date: 2026-09-14 (Asia/Taipei). Branch: `feat/routing-evaluation-harness`.
Baseline implementation: `bd20b4d`. Scope: local harness correctness, synthetic
records and fake subprocess adapter. No provider CLI, API, model judge or live
model/context switch was invoked. These results do not establish routing efficacy.

## Executed checks

| Check | Result | Scope |
| --- | --- | --- |
| Dedicated harness suite | 22 tests passed | Planning, input binding, validation, scoring, blind review, CLI and fake adapter |
| Full repository suite | 106 tests passed | 22 new harness tests plus 84 existing offline tests |

Commands from the repository root:

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_routing_eval.py' -v
.venv/bin/python -m unittest discover -s tests -v
```

The focused suite completes in about 3 seconds on the development machine; the
first full run completed in about 7.4 seconds. Timings include deliberate fake
adapter timeouts and are not model-latency measurements. Repository release tests
build disposable copies under temporary directories, without publishing or installing.

## Coverage

- Repeatable plans and schedule order, contract hashes, selection and duplicate guards.
- Executor requests exclude checks and gold success rubrics.
- Wrong plan/job/request hash rejected; existing results never overwritten.
- Missing metrics remain unknown; failed-run cost retained; paired comparisons use
  the same case/repetition; tracks remain separate; completion is not task success.
- Strict check types, result success evidence, API cost provenance and malformed JSON.
- Execution opt-in and invocation cap, fake process isolation, resume, changed adapter
  rejection, invalid output, wrong hash, nonzero exit, output size and timeout.
- Interrupted attempts retained rather than silently retried.
- A/B packet creation, mirrored votes counted once, order inconsistency, missing
  reviews, criterion scores, judge agreement and complete private-key binding.
- Offline CLI plan → import → score → blind → review-report; separate real CLI
  subprocess → fake adapter integration. No actual model responses are used.

Tests are in [`test_routing_eval.py`](../tests/test_routing_eval.py). The only
subprocess adapter used is the readable local
[`routing_eval_fake_adapter.py`](../tests/fixtures/routing_eval_fake_adapter.py).
It fabricates transport observations without reading expected decisions and labels
its execution scope `synthetic_harness_fixture`. Token usage stays unknown.
The fake adapter's audit hook rejects networking and child processes. Library tests
also deny socket creation; offline CLI paths are checked with process creation forbidden.

## Defects reproduced and corrected

The first focused run had six failing assertions across three defect categories;
all passed after the corresponding fixes:

1. Interrupting an adapter left no result. The runner now stores a blocked attempt
   before propagating a caught interruption, so resume does not resubmit it silently.
2. The blind packet hashed item mappings but not private-key metadata. The commitment
   now includes plan identity, selected strategies, mirroring and skipped-pair count.
   New packets identify binding version 2; old packets must be regenerated.
3. Python equality allowed boolean/float schema versions to compare equal to integer 1.
   Schema validation now requires an actual integer. Schedule comparison also uses
   canonical JSON hashing to distinguish boolean and numeric values.

## Limits and next work

Unit tests calibrate the harness on specified examples; they are not a formal proof.
Private holdouts, multistage task execution, real platform adapters, actual model
switches, empirical strategy comparisons and independent human/model judging remain
separate work. No holdout was manufactured from these already-seen examples.
Caught interrupts are covered; forced termination and disk failure can still prevent
recording. Do not infer zero remote cost from a missing or interrupted result.

The next live pilot remains optional and deferred: two tasks × Adaptive/Sticky ×
one repetition. It needs a real adapter and separate authorization for model usage.
