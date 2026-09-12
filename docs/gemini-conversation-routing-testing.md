# Gemini conversation-routing regression

> Historical pre-UX evidence. These runs exercised the earlier output and unconditional model-ask hold; they do not validate the action-first UX update. See [UX validation](ux-validation.md).

The user reported a routing note containing both AI settings and a deferred model-switch
decision, but no conversation recommendation or window-switch answer. The installed startup
payload already contained the conversation rules. A fresh baseline installed-extension run
did show the missing block, so this does not establish a deterministic installation failure.

The correction makes the conversation result part of the main rendering sequence and combines
the separate examples into one complete note. The example is explicitly conditional on both
routers being enabled. Context-off removes the conversation block and its suitability claim;
deferring a model change does not remove an enabled conversation result.

## Reproduction

After building and installing the Gemini package, use an authenticated CLI with a compatible
Node runtime on `PATH`:

```sh
.venv/bin/python scripts/smoke_gemini_routing.py \
  --output build/gemini-context-regression/results.json
```

This opt-in command makes three live model requests and may consume account usage. It uses
Gemini CLI's configured model, the installed `adaptive-task-routing` extension, disposable
fixtures and plan approval mode. There is no workspace `GEMINI.md`, explicit Skill request,
or requested routing-output template. JSON is only the CLI transport format.

The cases cover an implicit audit, a proposed document/test-review phase, and an explicit
context-off request. Output checks cover the conversation/window answer before both model
settings, its omission when disabled, the model-switch assessment, consistent retention,
and unchanged fixtures. Read the responses as well as the automated checks.

## Scope and limitations

The test targets conversation-block completeness and independent mode behavior. It does not
prove that every long-running conversation or model will obey the instructions. No actual
context transfer or model change is performed. The next-phase responses also broadened the
proposed review into test rewriting; visibility checks are not a pass for that separate
plan-fidelity concern. They did not execute those proposals or modify the fixtures.

An initial strengthened-template revision passed the two enabled-context cases but failed
context-off by still displaying a suitability recommendation. The final revision therefore
states the mode-dependent block omissions before the complete example. The evidence preserves
that failed iteration rather than treating all live runs as passes.

See [sanitized execution evidence](evidence/gemini-conversation-routing.json) for the baseline,
first revision and final installed-extension responses, observed model names and checks.

## Final results — 2026-09-12

Gemini CLI 0.59.0 passed all three conversation-visibility cases with the final installed
payload: audit (13.96 s), next phase (11.54 s), and context-off (110.20 s). Both enabled
cases explained why the current conversation was useful; the off case omitted that
assessment. CLI statistics recorded `gemini-3.1-pro-preview-customtools` and
`gemini-3-flash-preview` during the runs, without an explicit test model override.

All 61 unit tests and release/source/archive checksum validation passed. The installed
Gemini startup, Skill and shared payloads matched the final build byte for byte.
The context-off run reported saving a native Gemini plan outside the task fixture;
the fixture checks do not claim that the host writes no session or plan files.
