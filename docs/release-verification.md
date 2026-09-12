# Release verification — 0.4.0

Audit date: 2026-09-12 (Asia/Taipei). This release updates discovery, recommendation,
and direct-selection dispatch guidance while preserving the three Skill names. Local automated checks passed;
public submission and conversational acceptance remain outstanding.

## Automated results

| Check | Result | Scope |
|---|---|---|
| Python unit/integration tests | PASS, 50 tests | 35 release tests plus 15 metadata-helper tests |
| Source validation | PASS | Three checked frontmatters/trigger contracts, links/anchors, defaults, required host guides, manifests/version |
| Release validation | PASS | Three staging trees, exact ZIP members/bytes, shared files, manifest isolation, SHA-256 |
| Reproducibility | PASS | Build-twice integration compares ZIP bytes and preserves old output |
| Claude Code 2.1.152 | PASS | claude plugin validate dist/claude/adaptive-task-routing --strict |
| Gemini CLI 0.59.0 | PASS | gemini extensions validate dist/gemini/adaptive-task-routing |
| Codex compatibility validator | PASS | Bundled plugin-creator validate_plugin.py |
| Three Skill validators | PASS | Bundled skill-creator quick_validate.py |

The helper tests cover catalog pagination/cycles, hidden models, malformed/duplicate
catalogs, partial failure, exact thread matching, scope labeling, filtered output,
unknown current values, write/history rejection, bounded timeouts, malformed/oversized
protocol output and redacted project-sandbox startup classification. Release tests additionally enforce the bundled registry's complete model count, runtime and official descriptions, task-selection guidance, reasoning metadata, scope, structure and seven-day expiry, seven surfaces, complete case sets,
evidence for executed results, required guides and the one allowed helper source.

## Native local discovery and probe

- Codex CLI 0.154.0: plugin/read in a disposable marketplace found all three namespaced
  Skills and localVersion 0.4.0. It did not install or enable that temporary plugin.
- Claude Code 2.1.152: isolated session --plugin-dir discovered version 0.4.0 and three
  Skills; bare credential-free inventory found no hooks, agents or MCP servers.
- Gemini CLI 0.59.0: temporary GEMINI_CLI_HOME, link with scoped consent, extensions
  list and skills list discovered all three Skills. Temporary registry/trust changes
  were removed with the test workspace.
- The helper from the generated OpenAI package completed model/list, config/read and
  thread/read in an explicitly identified CLI environment. Six visible models were
  returned and the catalog was marked applicable to that CLI. Disk and saved thread
  settings were gpt-5.6-sol / high; the thread was notLoaded. Output correctly retained
  unknown current values. No inference, thread-start/resume or config-write RPC was called.
- A fresh installed-host Codex CLI session with `workspace-write` and `approval: never`
  reproduced `codex_state_unwritable`. It stopped after one attempt, requested no broader
  access, and used the unexpired bundled inventory internally. The compact result showed
  a plain-language conversation recommendation, no window switch, minimum GPT-5.6 Terra / high,
  recommended GPT-5.6 Sol / high, and medium upgrade value. It omitted unreadable current values and all
  probe, fallback, freshness, account/surface, confidence, assessment and mode details.
  Since no verifiable switch operation existed, it directed the user to `/model` and
  ended by asking them to reply “continue” after changing or retaining the setting.
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

Evidence: [sanitized native inventory](evidence/native-smoke.json) and
[metadata-probe summary](evidence/routing-probe.json), plus the
[Codex CLI R05 behavioral result](evidence/codex-cli-r05.json) and
[direct-selection result](evidence/codex-cli-direct-selection.json), plus the
[localized conversation-output result](evidence/codex-cli-localized-context.json) and
[App fallback-reference fixture](evidence/codex-app-fallback-reference.json), plus the
[deferred-permission challenge fixture](evidence/codex-app-permission-challenge.json).
Raw inventory is regenerated locally at build/native-smoke.json.
Host startup may update its own logs/caches or contact its provider.

The persistent personal plugin was updated and enabled as development build
`0.4.0+codex.20260912040629`. A new conversation is still required to load it. No user
model/effort setting was changed.
Native discovery is not behavioral execution, and no live App control socket was tested.

## Archive inventory and SHA-256

| Archive | Bytes |
|---|---:|
| adaptive-task-routing-openai-0.4.0.zip | 94181 |
| adaptive-task-routing-claude-0.4.0.zip | 92794 |
| adaptive-task-routing-gemini-0.4.0.zip | 92722 |

```text
4a530ae6bbc93cf789d68dd0813c6e61efaf3c8985c2185312b3b1629fea1c76  adaptive-task-routing-openai-0.4.0.zip
784a91a9c9b5cddc5488fba37a9eb701b89f656d8ed289bc68674660ccee19ea  adaptive-task-routing-claude-0.4.0.zip
cd85de753d5ce7cfb41ddc589731b8b6a2cd51cc2f2158f09422a4e9540f408c  adaptive-task-routing-gemini-0.4.0.zip
```

Each ZIP has manifests at its root without a wrapper. All three Skills, shared guides
and the single optional Codex helper are generated from canonical sources. The helper
does not run on installation or Skill loading; no startup hook or daemon is introduced.
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
   test Auto, actual thinking controls and sibling/shared-resource consent boundaries.
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
.release-backups/dist-u1nm3ofm/dist. It is recoverable and was not used as input.
No Git index/history/remotes, remote repository, push, release or submission was changed.
See [release and owner submission steps](release.md).
