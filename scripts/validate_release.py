#!/usr/bin/env python3
"""Validate sources, links, manifests, staging trees, ZIP bytes and SHA-256."""
from __future__ import annotations

import argparse
import json
import posixpath
import re
import stat
import sys
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

import yaml

# Also support importlib-based callers, including the original regression tests.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from release_lib import (ROOT, PLATFORMS, SKILLS, SURFACES, SKILL_HELPER, MANIFESTS, COMMON_FILES, SCHEMA,
                         AUTO_ACTIVATION, GEMINI_COORDINATOR_DEPENDENCIES,
                         archive_name, digest, ignored, metadata, payload, stage_path)

SEMVER = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?\Z")


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def frontmatter(data, name):
    text = data.decode("utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    require(match, f"Invalid Skill frontmatter: {name}")
    fields = yaml.load(match.group(1), Loader=UniqueLoader)
    require(isinstance(fields, dict), f"Skill frontmatter must be a mapping: {name}")
    require(fields.get("name") == name, f"Skill name mismatch: {name}")
    require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) and len(name) <= 64,
            f"Invalid Skill name: {name}")
    description = fields.get("description")
    require(isinstance(description, str) and 0 < len(description) <= 1024,
            f"Invalid Skill description: {name}")
    require(text[match.end():].strip(), f"Empty Skill body: {name}")
    require(set(fields) <= {"name", "description", "license", "compatibility", "metadata", "allowed-tools"},
            f"Unsupported Skill frontmatter field: {name}")
    return fields


def anchors(text):
    result, seen = set(), {}
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        title = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", title).lower()
        slug = re.sub(r"[^\w\- ]", "", title, flags=re.UNICODE).replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        result.add(slug if not count else f"{slug}-{count}")
    result.update(re.findall(r'\bid=["\']([^"\']+)["\']', text))
    return result


def validate_links(entries, label="packaged"):
    for name, data in entries.items():
        if not name.endswith(".md"):
            continue
        text = data.decode("utf-8")
        # Code examples are literal, not navigable Markdown links.
        text = re.sub(r"^(`{3,}|~{3,}).*?^\1\s*$", "", text, flags=re.M | re.S)
        refs = {key.strip().casefold(): value for key, value in
                re.findall(r"^\s{0,3}\[([^]]+)\]:\s*(<[^>]+>|\S+)", text, re.M)}
        destinations = re.findall(r"!?\[[^]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+['\"][^\n]*?['\"])?\s*\)", text)
        destinations += list(refs.values())
        for title, key in re.findall(r"\[([^]\n]+)\]\[([^]\n]*)\]", text):
            key = (key or title).strip().casefold()
            require(key in refs, f"Undefined reference link in {name}: {key}")
        # HTML links and images are checked too.
        destinations += re.findall(r'(?:href|src)=["\']([^"\']+)["\']', text)
        for raw in destinations:
            url = urlsplit(raw.strip("<>"))
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            require(not path.startswith("/") and "\\" not in path,
                    f"Non-portable link in {name}: {raw}")
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), path)) if path else name
            require(resolved != ".." and not resolved.startswith("../"),
                    f"Escaping link in {name}: {raw}")
            exists = resolved in entries or any(p.startswith(resolved.rstrip("/") + "/") for p in entries)
            require(exists, f"broken {label} link in {name}: {raw}")
            if url.fragment and resolved.endswith(".md") and resolved in entries:
                require(unquote(url.fragment) in anchors(entries[resolved].decode()),
                        f"broken {label} anchor in {name}: {raw}")


def validate_manifests(entries, platform, config):
    all_manifests = set().union(*MANIFESTS.values())
    present = all_manifests.intersection(entries)
    require(present == MANIFESTS[platform], f"Wrong manifests for {platform}: {present}")
    for name in entries:
        parts = PurePosixPath(name).parts
        require(not any(p in {".claude-plugin", ".codex-plugin"} for p in parts)
                or name in MANIFESTS[platform], f"Foreign or misplaced manifest: {name}")
        require(not name.endswith("gemini-extension.json") or name in MANIFESTS[platform],
                f"Foreign or misplaced manifest: {name}")
    for name in present:
        value = json.loads(entries[name])
        require(value.get("name") == config["name"], f"Manifest name mismatch: {name}")
        require(value.get("version") == config["version"], f"Manifest version mismatch: {name}")
    if platform == "openai":
        portable = json.loads(entries["plugin.json"])
        legacy = json.loads(entries[".codex-plugin/plugin.json"])
        require(portable.get("$schema") == SCHEMA, "Portable schema missing")
        require("skills" not in portable and "interface" not in portable, "Legacy fields in portable manifest")
        require(portable["extensions"]["com.openai"] == {"interface": legacy["interface"]},
                "OpenAI overlay mismatch")
        require(legacy.get("skills") == "./skills/", "Codex skills path mismatch")
        expected_hook = {"hooks": {"UserPromptSubmit": [{"hooks": [{
            "type": "command",
            "command": f"printf '%s\\n' '{AUTO_ACTIVATION['openai']}'",
            "commandWindows": f"Write-Output '{AUTO_ACTIVATION['openai']}'",
            "async": False,
            "timeoutSec": 5,
            "additionalContextLimit": 0,
        }]}]}}
        require(legacy.get("hooks") == expected_hook, "Codex automatic routing hook mismatch")
        import jsonschema
        schema = json.loads((Path(__file__).resolve().parent.parent / "tests/schemas/plugin.schema.json").read_text())
        jsonschema.Draft202012Validator(schema).validate(portable)
    if platform == "claude":
        hook = json.loads(entries.get("hooks/hooks.json", b"{}"))
        handlers = hook.get("hooks", {}).get("UserPromptSubmit", [])
        require(hook.get("description") and len(handlers) == 1
                and handlers[0].get("hooks") == [{
                    "type": "command",
                    "command": f'echo "{AUTO_ACTIVATION["claude"]}"',
                    "timeout": 5,
                }], "Claude automatic routing hook mismatch")
    if platform == "gemini":
        manifest = json.loads(entries["gemini-extension.json"])
        require(manifest.get("contextFileName") == "GEMINI.md",
                "Gemini automatic context is not configured")
        expected = [
            "# Adaptive Task Routing startup instruction\n\n",
            AUTO_ACTIVATION["gemini"],
            "\n\n## Embedded automatic coordinator contract\n",
        ]
        for name in GEMINI_COORDINATOR_DEPENDENCIES:
            expected.extend((f"\n### Embedded dependency: `{name}`\n\n",
                             entries[name].decode("utf-8").rstrip(), "\n"))
        require(entries.get("GEMINI.md", b"").decode("utf-8") == "".join(expected),
                "Gemini automatic routing context mismatch")
        require("## Embedded automatic coordinator contract" in
                entries["GEMINI.md"].decode("utf-8"),
                "Gemini automatic coordinator contract missing")
        coordinator = entries["skills/adaptive-task-routing/SKILL.md"].decode("utf-8")
        require("## Generated Gemini dependency appendix" in coordinator
                and all(f"### Embedded dependency: `{name}`" in coordinator
                        for name in GEMINI_COORDINATOR_DEPENDENCIES),
                "Gemini coordinator dependency appendix mismatch")
    # The optional model probe is the only executable source. Automatic activation uses
    # a declarative Gemini context and small host-native command hooks.
    executables = {n for n in entries if PurePosixPath(n).suffix in
                   {".py", ".sh", ".js", ".ts", ".ps1", ".exe", ".so", ".dylib"}}
    require(executables == {SKILL_HELPER}, "Unexpected or missing Skill helper")
    allowed_roots = {"hooks"} if platform == "claude" else set()
    require(not any(PurePosixPath(n).parts[0] in {"scripts", "hooks", "commands", "agents"} - allowed_roots
                    for n in entries), "Unexpected startup/build component")
    allowed_runtime = {"GEMINI.md"} if platform == "gemini" else set()
    require(not any(n in entries for n in ({".mcp.json", "mcp.json", ".app.json", "GEMINI.md", "CLAUDE.md"}
                                             - allowed_runtime)),
            "Unexpected runtime component")


def validate_matrix(root):
    matrix = json.loads((root / "tests/behavioral-matrix.json").read_text())
    cases = matrix["cases"]
    require(len({c["id"] for c in cases}) == len(cases), "Duplicate behavioral case ID")
    for polarity, count in (("positive", 5), ("negative", 3)):
        require(sum(c["kind"] == polarity and c.get("openai_submission", False) for c in cases) >= count,
                f"Need {count} submission {polarity} cases")
    for case in cases:
        require(case["prompt"] and case["expected"] and case["setup"], f"Incomplete case: {case['id']}")
        require(set(case["results"]) == {"chatgpt", "codex", "claude", "gemini"}, "Missing platform result")
        for result in case["results"].values():
            require(result["status"] in {"not_run", "pass", "fail", "blocked"}, "Invalid result status")
            if result["status"] != "not_run":
                require(result.get("evidence"), "Executed case requires evidence")
    surface_matrix = json.loads((root / "tests/surface-matrix.json").read_text())
    extra = surface_matrix["cases"]
    ids = [case["id"] for case in cases + extra]
    require(len(set(ids)) == len(ids), "Duplicate surface case ID")
    require({f"R{i:02}" for i in range(1, 11)} <= {c["id"] for c in extra}, "Missing discovery cases")
    require({f"S{i:02}" for i in range(1, 13)} <= {c["id"] for c in extra}, "Missing switching cases")
    for case in extra:
        require(case["prompt"] and case["setup"] and case["expected"], "Incomplete discovery case")
    require(set(surface_matrix["surfaces"]) == set(SURFACES), "Missing test surface")
    for results in surface_matrix["surfaces"].values():
        require(set(results) == set(ids), "Missing surface case result")
        for result in results.values():
            require(result["status"] in {"not_run", "pass", "fail", "blocked"}, "Invalid surface status")
            if result["status"] != "not_run":
                require(result.get("evidence"), "Executed surface case requires evidence")


def validate_source(root):
    required = list(COMMON_FILES) + ["release.json", "shared/defaults.yaml",
               "shared/runtime-routing-policy.md", "shared/runtime-routing-policy.zh-TW.md",
               "tests/trigger-contract.json", "scripts/build_release.py", "scripts/validate_release.py",
               "shared/host-discovery.md", "shared/hosts/openai.md", "shared/hosts/claude.md",
               "shared/hosts/gemini.md", "shared/gemini-coordinator-runtime.md",
               "shared/model-catalogs/openai-codex-cli.json", SKILL_HELPER]
    for name in required:
        require((root / name).is_file(), f"Missing required file: {name}")
    config = metadata(root)
    require(config.get("name") == "adaptive-task-routing", "Release name mismatch")
    require(isinstance(config.get("description"), str) and config["description"].strip(), "Missing description")
    require(isinstance(config.get("author"), dict) and config["author"].get("name"), "Missing author")
    interface = config.get("interface", {})
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        require(isinstance(interface.get(key), str) and interface[key].strip(), f"Missing interface.{key}")
    require(isinstance(interface.get("capabilities"), list)
            and all(isinstance(c, str) for c in interface["capabilities"]), "Invalid capabilities")
    prompts = interface.get("defaultPrompt", [])
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3
            and all(isinstance(p, str) and 0 < len(p) <= 128 for p in prompts), "Invalid starter prompts")
    for key in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        if key in interface:
            value = urlsplit(interface[key])
            require(value.scheme == "https" and value.netloc, f"Invalid interface URL: {key}")
    for key in ("composerIcon", "logo", "logoDark", "screenshots"):
        if key in interface:
            values = interface[key] if key == "screenshots" else [interface[key]]
            require(isinstance(values, list), f"Invalid assets: {key}")
            for value in values:
                require(isinstance(value, str) and value.startswith("./assets/")
                        and ".." not in PurePosixPath(value).parts, f"Invalid asset path: {value}")
                # Add assets to the explicit release inputs before advertising them.
                require(value[2:] in payload(root, "openai"), f"Asset not in release payload: {value}")
    match = SEMVER.fullmatch(config.get("version", ""))
    require(match, "Invalid semantic version")
    if match.group(4):
        require(not any(p.isdigit() and len(p) > 1 and p.startswith("0") for p in match.group(4).split(".")),
                "Invalid numeric prerelease version")
    require(f'## [{config["version"]}]' in (root / "CHANGELOG.md").read_text(), "Changelog version missing")
    require(all("A cross-file release-flow, cross-platform consistency, or test-gap scan qualifies" in
                AUTO_ACTIVATION[platform] for platform in PLATFORMS),
            "Automatic activation may misclassify a substantial audit as informational")
    require(all("resource-guidance heading" in AUTO_ACTIVATION[platform]
                for platform in PLATFORMS),
            "Automatic activation does not preserve the branded routing-note boundary")
    require(all("configuration commands" in AUTO_ACTIVATION[platform]
                and "mode change affects both" in AUTO_ACTIVATION[platform]
                for platform in PLATFORMS),
            "Automatic activation does not route conversational mode commands")
    require(all(token in AUTO_ACTIVATION["gemini"] for token in (
                "before responding or using task tools",
                "automatic adaptive-task-routing coordinator",
                "embedded coordinator contract below directly",
                "Compose one final user response")),
            "Gemini automatic routing can depend on unavailable Skill activation")
    contract = json.loads((root / "tests/trigger-contract.json").read_text())
    actual = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    require(actual == set(SKILLS), f"Expected exactly three Skills: {actual}")
    for skill in SKILLS:
        path = root / "skills" / skill / "SKILL.md"
        require(not path.is_symlink(), f"Symlink Skill: {skill}")
        fields = frontmatter(path.read_bytes(), skill)
        require(fields == yaml.load(contract[skill], Loader=UniqueLoader), f"Trigger definition changed: {skill}")
        require((path.parent / "references/zh-TW.md").is_file(), f"Missing translation: {skill}")
    defaults = yaml.load((root / "shared/defaults.yaml").read_text(), Loader=UniqueLoader)
    require(defaults["user_policy"] == {"context_mode": "ask", "model_mode": "ask"}, "Default modes changed")
    require(defaults.get("schema_version") == 3, "Discovery defaults schema mismatch")
    require(defaults.get("recommendation", {}).get("require_switch_assessment") is True
            and defaults.get("switching") == {
                "granularity": "meaningful_phase_boundary",
                "prefer_stickiness_when_suitable": True,
                "quality_floor_overrides_stickiness": True,
                "unknown_cost_is_zero": False,
                "automatic_change_requires": "justified_switch",
                "observations_scope": "session_only",
            }, "Unsafe switching defaults")
    require(defaults["discovery"]["persisted_settings_are_live"] is False
            and defaults["discovery"]["unknown_does_not_skip_task_requirements"] is True,
            "Unsafe discovery defaults")
    permission_escalation = defaults["discovery"].get("permission_escalation", {})
    require(permission_escalation == {
                "recommendation_default": "fallback_without_prompt",
                "ask_after_user_challenge": True,
                "requires_matching_surface_read_path": True,
                "maximum_requests_per_unchanged_condition": 1,
                "after_decline": "continue_with_fallback",
            }, "Invalid permission escalation defaults")
    registry_map = defaults["model_catalog"].get("bundled_fallback_registries", {})
    require(registry_map == {
                "openai": "shared/model-catalogs/openai-codex-cli.json",
                "gemini-cli": "shared/model-catalogs/gemini-cli.json",
            }, "Unexpected bundled fallback registries")
    registry_rel = registry_map["openai"]
    registry = json.loads((root / registry_rel).read_text())
    require(registry.get("schema_version") == 3 and registry.get("product") == "codex-cli"
            and registry.get("surface") == "codex-cli"
            and registry.get("catalog_kind") == "versioned_expiring_fallback",
            "Invalid bundled fallback registry scope")
    require(set(registry.get("reference_surfaces", [])) == {
                "chatgpt-desktop", "chatgpt-web", "codex-app", "codex-cli",
                "codex-ide-extension", "codex-cloud"}
            and registry.get("fallback_use", {}).get("ask_for_selector_before_recommendation") is False
            and isinstance(registry.get("fallback_use", {}).get("recommendation_scope"), str)
            and isinstance(registry.get("fallback_use", {}).get("availability_scope"), str),
            "Invalid fallback cross-surface reference scope")
    observed = datetime.fromisoformat(registry["observed_at"])
    expires = datetime.fromisoformat(registry["expires_at"])
    require(observed.tzinfo and expires.tzinfo and observed < expires <= observed + timedelta(days=7)
            and expires > datetime.now(timezone.utc), "Bundled fallback registry is stale")
    models = registry.get("models")
    require(isinstance(models, list) and models, "Empty bundled fallback registry")
    require(registry.get("catalog_complete") is True
            and registry.get("visible_model_count") == len(models),
            "Incomplete bundled fallback registry")
    capability_source = registry.get("capability_source", {})
    capability_url = urlsplit(capability_source.get("url", ""))
    require(capability_source.get("type") == "official_documentation"
            and capability_url.scheme == "https"
            and capability_url.netloc in {"learn.chatgpt.com", "developers.openai.com"}
            and isinstance(capability_source.get("checked_at"), str)
            and isinstance(capability_source.get("scope"), str),
            "Invalid fallback capability source")
    guidance = registry.get("reasoning_guidance", {})
    require(isinstance(guidance.get("principle"), str)
            and all(isinstance(guidance.get(value), str)
                    for value in ("low", "medium", "high", "xhigh", "max", "ultra")),
            "Incomplete fallback reasoning guidance")
    identifiers = []
    for model in models:
        require(isinstance(model, dict) and isinstance(model.get("model"), str)
                and all(isinstance(model.get(key), str) and model[key].strip()
                        for key in ("display_name", "runtime_description",
                                    "official_description", "selection_guidance")),
                "Invalid fallback model")
        efforts = model.get("supported_reasoning_efforts")
        require(isinstance(efforts, list) and efforts
                and all(isinstance(value, str) and value for value in efforts)
                and len(efforts) == len(set(efforts)), "Invalid fallback effort options")
        require(model.get("default_reasoning_effort") in efforts, "Invalid fallback default effort")
        identifiers.append(model["model"])
    require(len(identifiers) == len(set(identifiers)), "Duplicate fallback model")
    gemini_registry = json.loads((root / registry_map["gemini-cli"]).read_text())
    require(gemini_registry.get("schema_version") == 1
            and gemini_registry.get("product") == "gemini-cli"
            and gemini_registry.get("surface") == "gemini-cli"
            and gemini_registry.get("catalog_kind") == "versioned_expiring_fallback",
            "Invalid Gemini fallback registry scope")
    gemini_observed = datetime.fromisoformat(gemini_registry["observed_at"])
    gemini_expires = datetime.fromisoformat(gemini_registry["expires_at"])
    require(gemini_observed.tzinfo and gemini_expires.tzinfo
            and gemini_observed < gemini_expires <= gemini_observed + timedelta(days=7)
            and gemini_expires > datetime.now(timezone.utc),
            "Gemini fallback registry is stale")
    gemini_models = gemini_registry.get("models")
    require(isinstance(gemini_models, list)
            and gemini_registry.get("catalog_complete") is True
            and gemini_registry.get("visible_model_count") == len(gemini_models)
            and {item.get("model") for item in gemini_models}
                == {"auto", "pro", "flash", "flash-lite"}
            and all(isinstance(item.get("display_name"), str)
                    and isinstance(item.get("official_description"), str)
                    and isinstance(item.get("selection_guidance"), str)
                    for item in gemini_models)
            and not any("1.5" in json.dumps(item) for item in gemini_models),
            "Invalid Gemini fallback models")
    gemini_capability_url = urlsplit(
        gemini_registry.get("capability_source", {}).get("url", ""))
    reasoning_control = gemini_registry.get("reasoning_control", {})
    require(gemini_registry.get("source", {}).get("host_version") == "gemini-cli 0.59.0"
            and gemini_capability_url.scheme == "https"
            and gemini_capability_url.netloc == "geminicli.com"
            and gemini_registry.get("fallback_use", {}).get(
                "ask_for_selector_before_recommendation") is False
            and reasoning_control.get("kind") == "model_native"
            and reasoning_control.get("fallback_display_value") == "model-default"
            and all(isinstance(reasoning_control.get(key), str)
                    for key in ("selection_rule", "forbidden_inference")),
            "Invalid Gemini fallback evidence")
    gemini_runtime = (root / "shared/gemini-coordinator-runtime.md").read_text()
    require(all(token in gemini_runtime for token in (
                "A fresh one-prompt session is focused",
                "### Adaptive Task Routing｜任務資源建議",
                "以下建議是根據上述計畫的下一階段",
                "【最低足夠 AI 設定】", "【建議 AI 設定】",
                "Reasoning：使用模型預設", "Never output Gemini 1.5",
                "如需採用建議，可用 /model 選擇模型",
                "Complete and present the requested findings or plan",
                "The note is incomplete if that final paragraph is omitted",
                "In `auto`, apply any callable")),
            "Gemini compact coordinator contract missing")
    model_skill = (root / "skills/research-model-router/SKILL.md").read_text()
    evidence_schema = (root / "skills/research-model-router/references/evidence-schema.md").read_text()
    # These checks protect instruction payloads, not measured host behavior.
    shared_policy = (root / "shared/runtime-routing-policy.md").read_text()
    for label, instruction in (("shared policy", shared_policy),
                               ("model skill", model_skill),
                               ("Gemini projection", gemini_runtime)):
        require(all(token in instruction for token in (
                    "Route at task boundaries, not every prompt",
                    "switch_assessment", "switch_value", "decision: change",
                    "quality", "Unknown", "remaining", "reasoning-only")),
                f"Switching contract missing: {label}")
    require(all(token in evidence_schema for token in (
                "switch_assessment:", "baseline: current_configuration",
                "target: recommended_setting", "cache_evidence:",
                "switching_cost: low | medium | high | unknown",
                "switch_value: low | medium | high | unknown",
                "decision: retain | change | defer")),
            "Switching evidence schema missing")
    require("Lower the setting again after the demanding phase ends" not in model_skill,
            "Automatic downgrade conflicts with switching assessment")
    require("### Select the action paragraph" in gemini_runtime
            and "For `retain` or `defer`, do not append `/model`" in gemini_runtime
            and "目前保留設定；我先停在這裡" in gemini_runtime
            and "Whenever the recommended model may differ" not in gemini_runtime,
            "Gemini retention action conflicts with switch assessment")
    require("### Select the action paragraph" in model_skill
            and "For `retain` or `defer`, do not append `/model`" in model_skill
            and "目前保留設定；我先停在這裡" in model_skill,
            "Model retention action selection missing")
    require(all(token in model_skill for token in
                ("minimum_sufficient_setting", "recommended_setting",
                 "upgrade_value", "upgrade_reason")),
            "Model router two-tier recommendation contract missing")
    require("never print `Current: unknown / unknown`" in model_skill
            and "### Adaptive Task Routing｜任務資源建議" in model_skill
            and "never emit a second divider or heading" in model_skill
            and "do not require a fixed confirmation word" in model_skill
            and "如需採用建議，可使用介面中的模型與推理強度選單調整" in model_skill
            and "do not include the CLI-only `/model` command" in model_skill
            and "Do not ask the user to transcribe selector options" in model_skill
            and "Never output bare Codex-style `low`, `medium`, or `high` as a Gemini setting" in model_skill
            and "* Reasoning：使用模型預設" in model_skill
            and "Traditional Chinese must use the exact literal headings" in model_skill
            and "目前環境無法代為切換模型；Reasoning 使用模型預設" in model_skill
            and "Put the requested plan or preceding findings before these blocks" in model_skill
            and "In `ask`, stop after the blocks" in model_skill
            and "In `auto`, continue authorized downstream work" in model_skill
            and "reply “continue”" not in model_skill
            and "回覆「繼續」" not in model_skill
            and "Never render the schema or internal evidence in ordinary compact output" in model_skill
            and "## When the user questions a recommendation" in model_skill
            and "ask once for narrowly scoped read permission only when the current host exposes a concrete path" in model_skill
            and "do not mention the probe, fallback/registry source" in model_skill
            and "## Direct-selection dispatch guard" in model_skill
            and "delegated_from: research-model-router" in model_skill,
            "Model router compact action contract missing")
    require(all(token in evidence_schema for token in
                ("current_configuration:", "model_catalog:", "assessment:",
                 "minimum_sufficient_setting:", "recommended_setting:",
                 "runtime_capabilities:", "execution:")),
            "Model router evidence schema missing")
    coordinator = (root / "skills/adaptive-task-routing/SKILL.md").read_text()
    require("### Adaptive Task Routing｜任務資源建議" in coordinator
            and "以下建議是根據上述計畫的下一階段" in coordinator
            and "【對話設定】" in coordinator and "* 建議：留在目前對話" in coordinator
            and "是否切換視窗" in coordinator
            and "For a plan-only or analysis-only request" in coordinator
            and "Present the requested findings and plan before one compact routing note" in coordinator
            and "If model mode is `ask`, stop after the routing note" in coordinator
            and "Do not require a fixed confirmation word" in coordinator
            and "Localize every label and description to the user's language" in coordinator
            and "never show those English enum tokens" in coordinator
            and "never surface the probe, fallback/registry source" in coordinator
            and "coordinator-delegated" in coordinator,
            "Coordinator localized conversation-output contract missing")
    context_skill = (root / "skills/task-context-router/SKILL.md").read_text()
    require("## Direct-selection dispatch guard" in context_skill
            and "delegated_from: task-context-router" in context_skill,
            "Context router direct-selection guard missing")
    validate_matrix(root)
    source_entries = {}
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if ignored(rel) or any(p in {"build", ".release-backups"} for p in rel.parts):
            continue
        require(not path.is_symlink(), f"Symlink in source: {rel}")
        if path.is_file():
            source_entries[rel.as_posix()] = path.read_bytes()
    validate_links(source_entries, "source")
    for platform in PLATFORMS:
        entries = payload(root, platform)
        validate_manifests(entries, platform, config)
        validate_links(entries)
    return config


def validate_package(archive, expected):
    with zipfile.ZipFile(archive) as package:
        infos = package.infolist()
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)), f"Duplicate ZIP entry: {archive}")
        for info in infos:
            path = PurePosixPath(info.filename)
            require(not info.is_dir() and not path.is_absolute() and ".." not in path.parts
                    and "\\" not in info.filename and path.as_posix() == info.filename
                    and not ignored(path) and not stat.S_ISLNK(info.external_attr >> 16),
                    f"Unsafe ZIP entry: {info.filename}")
            require(info.file_size <= 5_000_000, f"Oversized ZIP entry: {info.filename}")
        require(set(names) == set(expected),
                f"ZIP content mismatch: missing={set(expected)-set(names)}, unexpected={set(names)-set(expected)}")
        for name, data in expected.items():
            require(package.read(name) == data, f"stale or modified payload: {name}")
        require(package.testzip() is None, f"Bad ZIP CRC: {archive}")
    validate_links(expected)


def validate_checksums(dist, archives):
    path = dist / "SHA256SUMS"
    require(path.is_file(), "Missing SHA256SUMS")
    found = {}
    for line in path.read_text().splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\]+\.zip)", line)
        require(match, f"Invalid checksum line: {line}")
        checksum, name = match.groups()
        require(name not in found, f"Duplicate checksum: {name}")
        found[name] = checksum
    require(set(found) == {p.name for p in archives}, "Checksum file set mismatch")
    for archive in archives:
        require(found[archive.name] == digest(archive.read_bytes()), f"SHA-256 does not match: {archive.name}")


def validate_dist(root, dist):
    require(dist.is_dir() and not dist.is_symlink(), "Invalid dist directory")
    config = metadata(root)
    archives = [dist / archive_name(config, p) for p in PLATFORMS]
    expected_top = set(PLATFORMS) | {p.name for p in archives} | {"SHA256SUMS"}
    require({p.name for p in dist.iterdir()} == expected_top, "Unexpected/stale dist files")
    require(not any(p.is_symlink() for p in dist.iterdir()), "Symlink in dist")
    for platform, archive in zip(PLATFORMS, archives):
        entries = payload(root, platform)
        stage = stage_path(dist, config, platform)
        require(stage.is_dir() and not stage.is_symlink(), f"Missing or symlink stage: {stage}")
        require({p.name for p in (dist / platform).iterdir()} == {config["name"]}, "Extra staging directory")
        actual = {}
        for path in stage.rglob("*"):
            require(not path.is_symlink(), f"Symlink in stage: {path}")
            rel = path.relative_to(stage)
            require(not ignored(rel), f"Junk in stage: {rel}")
            if path.is_dir():
                require(any(n.startswith(rel.as_posix() + "/") for n in entries),
                        f"Extra staging directory: {rel}")
            if path.is_file():
                actual[path.relative_to(stage).as_posix()] = path.read_bytes()
        require(actual == entries, f"Stale or extra staging payload: {platform}")
        validate_manifests(actual, platform, config)
        require(archive.is_file(), f"Missing archive: {archive}")
        validate_package(archive, entries)
    validate_checksums(dist, archives)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--source-only", action="store_true")
    group.add_argument("--require-archives", action="store_true")
    args = parser.parse_args()
    config = validate_source(ROOT)
    if not args.source_only and ((ROOT / "dist").exists() or args.require_archives):
        require((ROOT / "dist").is_dir(), "Missing dist; run scripts/build_release.py")
        validate_dist(ROOT, ROOT / "dist")
        print("PASS: all three staging trees, ZIP contents and SHA-256")
    print(f'PASS: source, manifests, links, triggers and version {config["version"]}')
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, yaml.YAMLError, zipfile.BadZipFile) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
