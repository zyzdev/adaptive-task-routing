# Release procedure

The repository root is source, not an installable plugin. Edit skills/ and shared/ once.
Set release.json's version and update CHANGELOG.md. The current release candidate is
0.4.2; no remote release or platform submission is created by any script.

## Build and validate

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_release.py --source-only
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build_release.py
.venv/bin/python scripts/validate_release.py --require-archives
claude plugin validate dist/claude/adaptive-task-routing --strict
gemini extensions validate dist/gemini/adaptive-task-routing
.venv/bin/python scripts/smoke_local.py
(cd dist && shasum -a 256 -c SHA256SUMS)
```

The build creates exactly three root-layout ZIPs, SHA256SUMS, and three unpacked plugin
trees at dist/{openai,claude,gemini}/adaptive-task-routing. ZIPs contain no wrapper
directory. File names use release.json's version. Stable ordering, timestamps, modes
and compression settings make rebuilds reproducible within the same Python/zlib toolchain.

Each build validates a temporary release first. Previous dist contents, including old
versions or unrelated files placed there, are moved into an ignored .release-backups/
directory before the new dist is installed. Nothing from old dist is used as build input.
Do not edit staging files: they are regenerated. The portable validator rejects stale
staging data, foreign manifests, extra/missing ZIP entries, traversal, symlinks,
duplicate entries, invalid links/anchors/frontmatter, changed triggers and bad digests.

Source tests and build code are excluded from runtime packages. Behavioral cases,
architecture, examples, shared files, license, changelog and platform-specific README
are explicitly included. README source lives in packaging/<platform>/README.md and is
placed at each package root with its repository-relative links rebased by the builder.
Both source and packaged links are checked. Codex and Claude packages include fixed-output
prompt hooks; Gemini includes startup context. They remind the host to complete and present a
requested analysis or plan first, then invoke the Skill for any substantial next phase before
that phase begins. For an execution request, the host presents an actionable plan before the
gate. They do not run the router or metadata helper themselves.

The sole packaged executable source is the optional Python 3.10+ Codex metadata helper
inside the model Skill. Its read-only RPC tests run in the Python suite. To check it
locally from Codex CLI, run `python3 dist/openai/adaptive-task-routing/skills/research-model-router/scripts/probe_codex.py --surface auto --cwd "$PWD"`.
It returns evidence, not a switch or proof of App applicability; host cache/log activity
may occur. Do not run it on Claude/Gemini or a ChatGPT sandbox as an App-settings probe.
In a project-only Codex sandbox it may return `codex_state_unwritable`; the routing
Skill stops after that read and immediately uses the matching unexpired bundled registry
to produce minimum-sufficient and recommended settings. It does not print unreadable
current fields. In `ask`, it presents the applicable selector or `/model` control and stops for
the user's natural decision. In `auto`, it applies only through independently verified model and
effort controls; otherwise it shows the control as optional, retains the current setting, and
continues.
`/status` can provide current settings as user-reported evidence.
Installing a release enables the packaged host-native reminder where the host supports it.
Codex can require one-time hook trust. No status line, daemon, or Python environment is configured.

This source build does not replace existing personal plugin installations. Use the
confirmed local marketplace's update/reinstall flow and a new thread to test changes;
keep development cachebusters out of the canonical three-platform release version.
The generated OpenAI tree contains both the agent-plugins root `plugin.json` and the
Codex `.codex-plugin/plugin.json`. During local cachebuster installation, synchronize
the same development version into both manifests before `codex plugin add`; current
Codex CLI installation keys its cache from the root manifest. Validate the resulting
local tree before reinstalling.

## Owner actions before public submission

Run [the behavioral matrix](../tests/behavioral-cases.md) on ChatGPT, Codex, Claude Code
and Gemini CLI. Store actual evidence and observed model/effort in
tests/behavioral-matrix.json and tests/surface-matrix.json; not_run is not a pass.
The latter is the per-surface authority: 34 cases across seven surfaces (238 cells),
including discovery regressions R01–R10. Keep ChatGPT web/desktop/mobile and Codex App/CLI
results separate. Rebuild after recording evidence.

Choose the real publisher, contact, repository/website, support, privacy/terms URLs,
logo, screenshots if requested and country availability. Those are not fabricated in
the manifest. OpenAI listing identity must match the verified identity. Publisher
metadata remains a manual release prerequisite.

## OpenAI / ChatGPT / Codex submission

1. Confirm organization identity verification and Apps Management Write access.
2. Open [OpenAI Platform Plugins](https://platform.openai.com/plugins).
3. Create plugin → Skills only. Supply the generated OpenAI ZIP, not the monorepo
   or a marketplace bundle. Inspect the portal's imported three Skills and shared files.
4. Complete listing, developer identity, logo/category, public website/support/privacy/
   terms URLs, starter prompts, regions and attestations. Use P01–P05 and N01–N03 plus
   actual observed results for the required five positive and three negative tests.
5. Review the concrete draft, then the owner chooses Submit. After approval, choose
   Publish separately. Public publication is shared by ChatGPT and Codex.

If the portal reports an ingestion error, preserve the error and follow the current
[submission error reference](https://developers.openai.com/plugins/deploy/submission-errors);
do not drop shared dependencies just to make an upload pass.

## Claude Code submission

1. After approval, publish the generated Claude tree to a dedicated repository root
   or a plugin subdirectory referenced by a real marketplace entry.
2. Validate the published checkout, locally load it with --plugin-dir, then test
   installation from the marketplace in a fresh session.
3. Open the submission form linked by the current
   [official guide](https://code.claude.com/docs/en/plugins):
   https://platform.claude.com/plugins/submit (also available to individual authors), or
   https://claude.ai/admin-settings/directory/submissions/plugins/new for Team/Enterprise
   organizations with directory management access.
4. Supply the actual repository/plugin path, release version, publisher details and
   test evidence. The owner submits and follows review status. Third-party approvals
   land in claude-community, with the reviewed commit pinned in the catalog. Users add
   anthropics/claude-plugins-community, then install adaptive-task-routing@claude-community.
   claude-plugins-official is curated separately by Anthropic and has no application process.

## Gemini CLI distribution and gallery

1. After approval, publish the generated Gemini tree to a dedicated public GitHub
   repository, with gemini-extension.json at the absolute root.
2. Add topic gemini-cli-extension to the repository About section. The gallery crawls
   eligible repositories; tagging and validation do not guarantee a listing.
3. Users can run gemini extensions install with that repository URL and --ref.
4. If publishing a GitHub Release, attach the Gemini ZIP and its checksum. Keep the
   other platforms' ZIPs off this extension release to avoid multiple generic assets.
5. Test installation from the actual remote URL/tag after publication.

All repository creation, pushes, tags/releases, catalog submissions, topic edits and
publishing are owner actions still awaiting confirmation. See
[verification results](release-verification.md) and [specification sources](platform-specs.md).
