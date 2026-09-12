# Release verification — 0.4.1

Audit date: 2026-09-12 (Asia/Taipei). This release updates discovery, recommendation,
direct-selection dispatch, plan-first routing and the `ask` hold while preserving the three Skill names. Local automated checks passed;
public submission and conversational acceptance remain outstanding.

## Automated results

| Check | Result | Scope |
|---|---|---|
| Python unit/integration tests | PASS, 54 tests | 39 release tests plus 15 metadata-helper tests |
| Source validation | PASS | Three checked frontmatters/trigger contracts, links/anchors, defaults, required host guides, manifests/version |
| Release validation | PASS | Three staging trees, exact ZIP members/bytes, shared files, manifest isolation, SHA-256 |
| Reproducibility | PASS | Build-twice integration compares ZIP bytes and preserves old output |
| Claude Code 2.1.269 | PASS | claude plugin validate dist/claude/adaptive-task-routing --strict |
| Gemini CLI 0.59.0 | PASS | gemini extensions validate dist/gemini/adaptive-task-routing |
| Codex runtime install | PASS | Installed and enabled `0.4.1+codex.20260912071849` from the personal marketplace |
| Bundled Codex compatibility validator | KNOWN LIMITATION | Its older schema rejects the runtime-supported manifest `hooks` field |
| Three Skill validators | PASS | Bundled skill-creator quick_validate.py |

The helper tests cover catalog pagination/cycles, hidden models, malformed/duplicate
catalogs, partial failure, exact thread matching, scope labeling, filtered output,
unknown current values, write/history rejection, bounded timeouts, malformed/oversized
protocol output and redacted project-sandbox startup classification. Release tests additionally enforce the bundled registry's complete model count, runtime and official descriptions, task-selection guidance, reasoning metadata, scope, structure and seven-day expiry, seven surfaces, complete case sets,
evidence for executed results, required guides, automatic activation payloads, the compact
Gemini coordinator projection and the one allowed helper source.

## Native local discovery and probe

- Codex CLI 0.154.0: plugin/read in a disposable marketplace found all three namespaced
  Skills and localVersion 0.4.0. It did not install or enable that temporary plugin.
- Claude Code 2.1.269: strict validation accepted the plugin manifest and packaged
  `UserPromptSubmit` hook. A live inference run was blocked because this local CLI is no
  longer authenticated; this is not counted as a behavioral pass.
- Gemini CLI 0.59.0: temporary GEMINI_CLI_HOME, link with scoped consent, extensions
  list and skills list discovered all three Skills. Temporary registry/trust changes
  were removed with the test workspace.
- The helper from the generated OpenAI package completed model/list, config/read and
  thread/read in an explicitly identified CLI environment. Six visible models were
  returned and the catalog was marked applicable to that CLI. Disk and saved thread
  settings were gpt-5.6-sol / high; the thread was notLoaded. Output correctly retained
  unknown current values. No inference, thread-start/resume or config-write RPC was called.
- Earlier installed-host Codex runs established automatic activation and the former
  rough-plan-first/non-blocking behavior. Those observations are retained as historical evidence
  and are superseded by the plan-first `ask` contract below.
- A fresh installed-host Codex CLI 0.154.0 session loaded final development build
  `0.4.1+codex.20260912071849` without naming the Skill. It completed and presented the requested
  three-point documentation improvement plan before the localized conversation and two AI-setting
  blocks. Default `ask` then ended the turn without downstream execution or a required confirmation
  word. A preceding Gemini release-flow audit on build `0.4.1+codex.20260912071227` showed the same
  ordering with a full release assessment before routing advice.
- Two fresh installed-host dispatch runs used the updated Skill descriptions. An
  ordinary release-audit prompt selected `adaptive-task-routing` without naming a
  Skill and showed conversation plus Model routing. A second run explicitly started from
  `research-model-router` while requesting the full routing scope; it dispatched to
  the coordinator and produced the same three-block result without recursion.
- A later fresh Traditional Chinese CLI run verified localized presentation. It showed
  `【對話設定】`, `建議：留在目前對話`, and `是否切換視窗：否`; the compact output
  contained none of the three raw context enum tokens or the English Context label.
- Manual model-setting guidance now follows the surface: ChatGPT App and web name only
  their visible model/reasoning selector, while an identified Codex CLI names `/model`.
- When OpenAI App runtime metadata is inaccessible, the bundled registry's dated official
  cross-surface capability reference now produces both concrete recommendations without
  asking the user to copy the selector. Account availability remains internal and unverified.
- A fresh installed-host challenge fixture questioned a fallback recommendation while the
  only possible read belonged to a separate CLI process. The response disclosed the actual
  source, observation and expiry dates, account-availability limit and task mapping. It did
  not start the probe or request permission that could not reach the same App/session.
- Earlier Gemini CLI 0.59.0 runs established automatic `activate_skill` behavior, localized
  blocks and a negative control for `1 + 1`. Their final action predates the current order and
  mode boundary. The generated Gemini runtime now requires plan-first output, an `ask` hold and
  continuation only in `auto`; package validation passed. Fresh installed-host Gemini acceptance
  for this exact change remains pending.
- The fresh Codex CLI run used hook trust bypass only for the reviewed local test invocation.
  Normal interactive use still presents one-time hook review.

Evidence: [sanitized native inventory](evidence/native-smoke.json) and
[metadata-probe summary](evidence/routing-probe.json), plus the
[Codex CLI R05 behavioral result](evidence/codex-cli-r05.json) and
[direct-selection result](evidence/codex-cli-direct-selection.json), plus the
[localized conversation-output result](evidence/codex-cli-localized-context.json) and
[App fallback-reference fixture](evidence/codex-app-fallback-reference.json), plus the
[deferred-permission challenge fixture](evidence/codex-app-permission-challenge.json) and
[Gemini CLI model-routing result](evidence/gemini-cli-model-routing.json), plus
[Gemini automatic activation](evidence/gemini-cli-auto-activation.json) and
[Codex CLI automatic activation](evidence/codex-cli-auto-activation.json), plus the
[historical Codex CLI routing-order result](evidence/codex-cli-routing-order.json), and the
[current plan-first ask-hold result](evidence/codex-cli-plan-first-ask-hold.json).
Raw inventory is regenerated locally at build/native-smoke.json.
Host startup may update its own logs/caches or contact its provider.

The persistent personal plugin was updated and enabled as development build
`0.4.1+codex.20260912071849`. A new conversation is still required to load it. No user
model/effort setting was changed.
Native discovery is not behavioral execution, and no live App control socket was tested.

## Archive inventory and SHA-256

| Archive | Bytes |
|---|---:|
| adaptive-task-routing-openai-0.4.1.zip | 105038 |
| adaptive-task-routing-claude-0.4.1.zip | 103728 |
| adaptive-task-routing-gemini-0.4.1.zip | 105337 |

```text
4b8de163f6c524fe2d1e3984eea594f1bcd36be5709e6887aa1f3cca62e65a52  adaptive-task-routing-openai-0.4.1.zip
6540314ac792787c45aed8152b0f036b907cc1ebb03bf6fa6499f5df40b4fe32  adaptive-task-routing-claude-0.4.1.zip
2074ab752ddecaa40202e4a63286614fed434d1930c75abf70f550ea8fcbc6f2  adaptive-task-routing-gemini-0.4.1.zip
```

Each ZIP has manifests at its root without a wrapper. All three Skills, shared guides
and the single optional Codex helper are generated from canonical sources. The helper
does not run on installation, Skill loading, or prompt-hook execution. Codex and Claude
hooks print a fixed reminder; Gemini loads a fixed context reminder. No daemon is introduced.
Finder metadata, Python caches, old dist content, foreign manifests and build/test
executables are excluded.

## Manual acceptance still required

1. Run the remaining cases in [the seven-surface matrix](../tests/surface-matrix.json).
   Codex CLI R05 passed; 237 of 238 cells remain not_run. The original 24 fixtures and five-positive/three-negative
   OpenAI submission set are retained in [behavioral cases](../tests/behavioral-cases.md).
2. Test explicit and implicit activation independently in new installed-host sessions;
   record exact Skill paths, model/effort evidence, control mode, output and disposition.
3. In Codex App, manually change model/power, then ensure the next gate detects the
   change or explicitly reports that only persisted settings are readable. Check
   that a different CLI account/provider/catalog cannot leak into App recommendations.
4. On ChatGPT web/desktop/mobile, verify available host resources and correct fallback
   without assuming a local CLI. Do not treat a sandbox shell as the user's computer.
5. On Claude Code, check live metadata/selector behavior and existing status-line
   payload scope; do not install instrumentation to make the test pass. On Gemini,
   test Auto, actual thinking controls and the self-contained single-activation coordinator.
6. Exercise ask/decline/auto/manual actions only with actual authorization and tools.
   Verify independent context-only/model-only/off behavior and no false applied claims.
7. Complete publisher identity/assets/URLs, portal import, upload resource access and
   eventual real repository/tag installation before public release.

## Difference review and recovery

Git began with all project files untracked and no tracked diff baseline. Work was
reviewed with no-index differences against /tmp/atr-routing-before.KR0ufx.
That snapshot preserves source/documents before 0.4.0. Skill names remain stable;
frontmatter descriptions, their checked trigger contract, and relevant behavioral
expectations now cover direct child selection. Unrelated existing content is retained.

The final build moved the previous dist to
.release-backups/dist-8qaeh3yp/dist. It is recoverable and was not used as input.
No Git index/history/remotes, remote repository, push, release or submission was changed.
See [release and owner submission steps](release.md).
