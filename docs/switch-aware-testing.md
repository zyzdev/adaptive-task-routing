# Switch-aware routing behavioral tests

Date: 2026-09-12 (UTC). Baseline: `8478e7c`. The evidence records hashes of the
final contract files so the unreleased candidate is distinguishable from the published
0.4.2 package. These runs use actual model inference; they complement the static tests.

## Results and scope

| Check | Result | What was exercised |
| --- | --- | --- |
| Decision fixtures | 17/17 passed | Fresh Codex CLI runs using GPT-5.6 Sol / high and synthetic host observations |
| Codex CLI 0.154.0 | Passed after fix | Explicit local `.agents` Skill loading, static three-file audit, plan before routing, retention action |
| Claude Code 2.1.269 | Passed after stream review | Session-only candidate plugin and read-only tools; assistant text captured in stream order |
| Gemini CLI 0.59.0 | Passed after fix | Workspace `GEMINI.md` containing the exact generated startup contract; installed extensions disabled |
| Python regression suite | 61/61 passed | Includes guards against conflicting manual-switch templates |

The decision fixtures cover short-phase retention, an already matching pair, failed
quality validation, unknown settings/cost, new or declined handoffs, context-off,
model-only, model-off, both-off, reasoning-only changes, return to a reusable cache,
remaining-phase amortization, explicit user targets and unchanged/end-of-phase behavior.
The evaluator received scenario observations and the contract, not the expected answer.
Each scenario was sampled once; this is not a statistical reliability estimate.

## Defect found and corrected

Both Gemini and Codex initially said that switching benefit was unestablished and then
appended the old invitation to use a model selector. Checking only the presence of a
switch-assessment line incorrectly appeared to pass. Manual review caught the conflict.

The corrected contract selects the action paragraph from the switch decision first:
retention or deferral ends with a retention/hold statement, while a justified change or
an explicit user target may show model controls. Unknown current settings alone no longer
trigger manual-switch advice. The model Skill, Traditional Chinese guidance, shared
policy, OpenAI guide and Gemini projection now agree. Regression tests reject removal
of the selection rule and restoration of Gemini's old unconditional control instruction.

The successful native retention ending is:

> 目前保留設定；我先停在這裡，等你決定是否沿用目前設定開始下一階段。

One Codex retry timed out after 180 seconds. It was recorded as blocked, not passed.
A subsequent retry limited the audit to static reading and completed in about 103 seconds.
An initial Claude launch used an invalid empty MCP configuration and was corrected to
`{"mcpServers": {}}` before inference. An overly strict fixture assertion also rejected
`context_off` followed by an explanation; semantic review corrected the assertion.

## Reproduction method

Decision scenarios and observed responses are in the [sanitized evidence](evidence/switch-aware-behavior.json).
For each scenario, start a fresh `codex exec` with `--ignore-user-config`,
`--ignore-rules`, `--ephemeral`, `--sandbox read-only`, a disposable working directory,
model `gpt-5.6-sol`, and `model_reasoning_effort="high"`. Supply the candidate shared
policy, defaults, context/model Skills and evidence schema as diagnostic test instructions.
Use the fictional catalog and scenario observations recorded in the evidence; do not
execute the hypothetical setting operations or provide expected outcomes to the model.
Compare structured decisions and review the visible response separately.

The native audit uses these three files:

- `manifest.json`: version `1.2.0`.
- `release.py`: a `release()` function writing hardcoded version `1.1.0` to `artifact.txt`.
- `test_release.py`: a test containing only `assert True`.

Ask for findings and three concrete improvements in Traditional Chinese without editing
files. Codex explicitly reads a temporary `.agents/skills` copy with matching shared
references. Claude uses `--plugin-dir`, `--setting-sources ""`,
`--no-session-persistence`, `--permission-mode dontAsk`, only `Read,Glob,Grep,Skill`
tools, and an empty explicit MCP configuration. Use `--verbose --output-format stream-json`
to inspect all visible assistant text, since the final-only JSON result can omit findings
emitted before the last routing message. Gemini uses `--extensions none`,
`--approval-mode plan`, and `--model gemini-3.1-flash-lite`, with the generated startup
contract copied to the temporary workspace's `GEMINI.md`.

Check findings before the resource note, localized context/model blocks, consistency
between the switch assessment and action, the ask hold, unchanged fixture bytes and
absence of a generated artifact. Native loading methods are deliberately recorded
separately; a workspace Skill/context test is not an installed-plugin hook test.

## Limits

No real model/effort change or context transfer was executed. No cache savings,
workflow-cost reduction, or application-quality improvement was established. Claude
serving-model metadata is recorded separately from unverified selector/effort controls.
ChatGPT web/desktop/mobile and Codex App were not exercised. Synthetic decision tests do
not establish all variants of the seven-surface acceptance matrix, so those cells are
not promoted to passes. Installed-hook and full native switching tests remain separate.
