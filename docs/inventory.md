# Pre-refactor inventory

Audit date: 2026-09-11. Git had no commits and all inputs were untracked; no AGENTS.md was present in the project or checked parent directories. There were 69 text files across three platform folders, plus two .DS_Store files. Each platform contained 22 byte-identical common files and one platform manifest, all at version 0.3.1. No scripts/ or dist/ existed. Six validator tests referenced a missing scripts/validate_release.py.

The 22 common files were consolidated at the project root. All Skill bodies, descriptions, translations, shared policy/defaults, LICENSE, and full examples were preserved byte-for-byte. Platform manifests are now generated from release.json. README, architecture, installation, contribution, security and release documents are maintained here; old versions remain in the pre-change snapshot.

Complete pre-change backup (including Finder metadata): /tmp/adaptive-task-routing-before.k9GeGR/original.tar.gz

SHA-256: bd863ae5baba2900d7bbe9a64473f8fdca09eab6b23ab967db3e121045ca330c

This is a local temporary recovery copy, not a release artifact; preserve it elsewhere if long-term recovery is needed.

## Original file inventory

- adaptive-task-routing-openai/.codex-plugin/plugin.json
- adaptive-task-routing-openai/CHANGELOG.md
- adaptive-task-routing-openai/CONTRIBUTING.md
- adaptive-task-routing-openai/LICENSE
- adaptive-task-routing-openai/README.md
- adaptive-task-routing-openai/README.zh-TW.md
- adaptive-task-routing-openai/SECURITY.md
- adaptive-task-routing-openai/docs/architecture.md
- adaptive-task-routing-openai/docs/architecture.zh-TW.md
- adaptive-task-routing-openai/docs/full-example.md
- adaptive-task-routing-openai/docs/full-example.zh-TW.md
- adaptive-task-routing-openai/packaging/INSTALL-CODEX-LOCAL.md
- adaptive-task-routing-openai/shared/defaults.yaml
- adaptive-task-routing-openai/shared/runtime-routing-policy.md
- adaptive-task-routing-openai/shared/runtime-routing-policy.zh-TW.md
- adaptive-task-routing-openai/skills/adaptive-task-routing/SKILL.md
- adaptive-task-routing-openai/skills/adaptive-task-routing/references/zh-TW.md
- adaptive-task-routing-openai/skills/research-model-router/SKILL.md
- adaptive-task-routing-openai/skills/research-model-router/references/zh-TW.md
- adaptive-task-routing-openai/skills/task-context-router/SKILL.md
- adaptive-task-routing-openai/skills/task-context-router/references/zh-TW.md
- adaptive-task-routing-openai/tests/behavioral-cases.md
- adaptive-task-routing-openai/tests/test_validate_release.py
- adaptive-task-routing-claude/.claude-plugin/plugin.json
- adaptive-task-routing-claude/CHANGELOG.md
- adaptive-task-routing-claude/CONTRIBUTING.md
- adaptive-task-routing-claude/LICENSE
- adaptive-task-routing-claude/README.md
- adaptive-task-routing-claude/README.zh-TW.md
- adaptive-task-routing-claude/SECURITY.md
- adaptive-task-routing-claude/docs/architecture.md
- adaptive-task-routing-claude/docs/architecture.zh-TW.md
- adaptive-task-routing-claude/docs/full-example.md
- adaptive-task-routing-claude/docs/full-example.zh-TW.md
- adaptive-task-routing-claude/packaging/INSTALL-CODEX-LOCAL.md
- adaptive-task-routing-claude/shared/defaults.yaml
- adaptive-task-routing-claude/shared/runtime-routing-policy.md
- adaptive-task-routing-claude/shared/runtime-routing-policy.zh-TW.md
- adaptive-task-routing-claude/skills/adaptive-task-routing/SKILL.md
- adaptive-task-routing-claude/skills/adaptive-task-routing/references/zh-TW.md
- adaptive-task-routing-claude/skills/research-model-router/SKILL.md
- adaptive-task-routing-claude/skills/research-model-router/references/zh-TW.md
- adaptive-task-routing-claude/skills/task-context-router/SKILL.md
- adaptive-task-routing-claude/skills/task-context-router/references/zh-TW.md
- adaptive-task-routing-claude/tests/behavioral-cases.md
- adaptive-task-routing-claude/tests/test_validate_release.py
- adaptive-task-routing-gemini/CHANGELOG.md
- adaptive-task-routing-gemini/CONTRIBUTING.md
- adaptive-task-routing-gemini/LICENSE
- adaptive-task-routing-gemini/README.md
- adaptive-task-routing-gemini/README.zh-TW.md
- adaptive-task-routing-gemini/SECURITY.md
- adaptive-task-routing-gemini/docs/architecture.md
- adaptive-task-routing-gemini/docs/architecture.zh-TW.md
- adaptive-task-routing-gemini/docs/full-example.md
- adaptive-task-routing-gemini/docs/full-example.zh-TW.md
- adaptive-task-routing-gemini/gemini-extension.json
- adaptive-task-routing-gemini/packaging/INSTALL-CODEX-LOCAL.md
- adaptive-task-routing-gemini/shared/defaults.yaml
- adaptive-task-routing-gemini/shared/runtime-routing-policy.md
- adaptive-task-routing-gemini/shared/runtime-routing-policy.zh-TW.md
- adaptive-task-routing-gemini/skills/adaptive-task-routing/SKILL.md
- adaptive-task-routing-gemini/skills/adaptive-task-routing/references/zh-TW.md
- adaptive-task-routing-gemini/skills/research-model-router/SKILL.md
- adaptive-task-routing-gemini/skills/research-model-router/references/zh-TW.md
- adaptive-task-routing-gemini/skills/task-context-router/SKILL.md
- adaptive-task-routing-gemini/skills/task-context-router/references/zh-TW.md
- adaptive-task-routing-gemini/tests/behavioral-cases.md
- adaptive-task-routing-gemini/tests/test_validate_release.py
- .DS_Store
- adaptive-task-routing-claude/.DS_Store
