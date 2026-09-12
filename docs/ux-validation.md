# Action-first UX validation

This update changes presentation and the meaning of `ask`. It does not change model capability
ranking, create a runtime routing service, or add a fourth control mode. The canonical interaction
and output rules are in [routing-ux.md](../shared/routing-ux.md).

## Offline coverage

- Defaults require compact presentation, visible advice when context routing is enabled, no retention confirmation,
  a material-blocker check for defer, and separate task authorization before continuation.
- Mutation tests reject an authorization bypass, unconditional retention confirmation, hidden
  conversation advice, stale hold instructions, missing Skill consumers and a missing Gemini UX appendix.
- Packaging tests verify that all platforms carry the same UX contract and both Gemini entrypoints
  embed it. Native metadata smoke checks load the packages without inference or persistent install.
- U01–U14 in [the surface matrix](../tests/surface-matrix.json) specify behavioral acceptance for
  keep/defer/change, authorization, mixed modes, handoff/clean, explicit targets and detail requests.
  They remain `not_run`. Earlier results were reset for the updated expectations; original live
  responses remain in the historical evidence files.

```sh
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/build_release.py
.venv/bin/python scripts/validate_release.py --require-archives
.venv/bin/python scripts/smoke_local.py --platform all
```

## Human review

Read the examples in [English](full-example.md) or [Traditional Chinese](full-example.zh-TW.md).
For each, check that a reader can identify the action, whether any operation is needed, whether
work is already authorized, and why a task-fit setting need not be applied immediately.
Verify that provisional retention does not certify suitability, that enabled conversation advice
remains visible, and that a retained model does not erase a pending context change.

## Limits

This iteration uses no live inference, cross-platform A/B tests, large task evaluations or cost
benchmarks. Static checks protect the delivered instructions and examples; they cannot prove that
models will obey them. The updated optional `smoke_gemini_routing.py` targets compact output but
was not run against a model for this update. Long-session adherence, actual model/context switches
and measurable cost/quality improvements remain unverified.

The numeric package version is still 0.4.2 with an Unreleased changelog. Published v0.4.2 packages
and existing installations do not acquire these changes until rebuilt and installed or released.

## Local result — 2026-09-13

All 68 Python tests passed. All three Skills passed frontmatter/structure validation.
The three platform staging trees, archive contents and SHA-256 checks passed. Native metadata
loading passed for Codex, Claude Code and Gemini CLI without inference or persistent installation.
These results validate packaging and instruction invariants, not model adherence.

## Final polish result — 2026-09-13

All 76 Python tests passed, including offline fixtures for the optional Gemini output checker.
The fixtures cover the plain heading, merged conversation sentence, verified keep without a
task-fit alternative, provisional keep with uncertain switching costs, unknown values in prose,
and context-off omission. Mutation checks protect current-only keep and target-only questions.
All three Skills passed structure validation. Rebuilt archives and SHA-256 checks passed; native
metadata loading passed for Codex, Claude Code and Gemini CLI without inference or persistent
installation. U01–U14 remain acceptance specifications, not live model results.
