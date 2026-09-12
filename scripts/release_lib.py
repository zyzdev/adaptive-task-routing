"""Shared deterministic release inputs. No platform payload is maintained by hand."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = ("openai", "claude", "gemini")
SKILLS = ("adaptive-task-routing", "task-context-router", "research-model-router")
SURFACES = ("chatgpt-web", "chatgpt-desktop", "chatgpt-mobile", "codex-app", "codex-cli", "claude-code", "gemini-cli")
SKILL_HELPER = "skills/research-model-router/scripts/probe_codex.py"
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
COMMON_FILES = (
    "LICENSE", "CHANGELOG.md", "docs/architecture.md", "docs/architecture.zh-TW.md",
    "docs/full-example.md", "docs/full-example.zh-TW.md",
    "tests/behavioral-cases.md", "tests/behavioral-matrix.json", "tests/surface-matrix.json",
)
MANIFESTS = {
    "openai": {"plugin.json", ".codex-plugin/plugin.json"},
    "claude": {".claude-plugin/plugin.json"},
    "gemini": {"gemini-extension.json"},
}
AUTO_ACTIVATION = {
    "openai": (
        "First complete any requested analysis or planning deliverable and present its useful "
        "content before routing advice. When the result defines a substantial next phase, or the "
        "user requested execution, decide whether that next phase constitutes substantial "
        "multi-step coding, debugging, architecture, validation, research, or analysis work. "
        "For every qualifying next phase you MUST invoke $adaptive-task-routing after the plan and "
        "before that phase begins, then follow its routing gate. In user-facing output, put the "
        "requested plan or findings before the routing note. In ask mode stop after the note and "
        "wait for the user's natural response; only auto mode may continue automatically. Skip "
        "ordinary chat, status checks, "
        "tiny operations, questions only about this plugin, and an unchanged phase whose gate "
        "already completed."
    ),
    "claude": (
        "First complete any requested analysis or planning deliverable and present its useful "
        "content before routing advice. When the result defines a substantial next phase, or the "
        "user requested execution, decide whether that next phase constitutes substantial "
        "multi-step coding, debugging, architecture, validation, research, or analysis work. "
        "For every qualifying next phase you MUST invoke "
        "/adaptive-task-routing:adaptive-task-routing after the plan and before that phase begins, "
        "then follow its routing gate. In user-facing output, put the requested plan or findings "
        "before the routing note. In ask mode stop after the note and wait for the user's natural "
        "response; only auto mode may continue automatically. Skip ordinary chat, status checks, "
        "tiny operations, questions only about this plugin, and an unchanged phase whose gate "
        "already completed."
    ),
    "gemini": (
        "First complete any requested analysis or planning deliverable and present its useful "
        "content before routing advice. When the result defines a substantial next phase, or the "
        "user requested execution, decide whether that next phase constitutes substantial "
        "multi-step coding, debugging, architecture, validation, research, or analysis work. "
        "For every qualifying next phase you MUST call activate_skill with name "
        "adaptive-task-routing after the plan and before that phase begins, then follow its routing "
        "gate. In user-facing output, put the requested plan or findings before the routing note. "
        "In ask mode stop after the note and wait for the user's natural response; only auto mode "
        "may continue automatically. Skip ordinary chat, status checks, tiny operations, questions "
        "only about this extension, and an unchanged phase whose gate already completed."
    ),
}
GEMINI_COORDINATOR_DEPENDENCIES = (
    "shared/gemini-coordinator-runtime.md",
)
FORBIDDEN_PARTS = {".DS_Store", "__MACOSX", "__pycache__", ".git", "dist", "node_modules", ".venv"}


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def metadata(root=ROOT):
    return json.loads((root / "release.json").read_text(encoding="utf-8"))


def ignored(path):
    return any(p in FORBIDDEN_PARTS for p in path.parts) or path.suffix in {".pyc", ".pyo"}


def read_tree(directory):
    result = {}
    for path in sorted(directory.rglob("*")):
        if ignored(path.relative_to(directory)):
            continue
        if path.is_symlink():
            raise ValueError(f"Symlink not allowed in source: {path}")
        if path.is_file():
            result[path.relative_to(directory).as_posix()] = path.read_bytes()
    return result


def gemini_coordinator(root, base):
    parts = [
        base.decode("utf-8").rstrip(),
        "\n\n## Generated Gemini dependency appendix",
        "\nThis build-generated appendix is authoritative for this invocation. It keeps the "
        "complete compact Gemini routing contract inside the one directory authorized by "
        "activating this Skill. Follow it as the coordinator-delegated result of both child "
        "routers. Do not output until both enabled decisions are complete.\n",
    ]
    for name in GEMINI_COORDINATOR_DEPENDENCIES:
        content = (root / name).read_text(encoding="utf-8").rstrip()
        # Embedded dependencies are instructions, not navigable files in the coordinator's
        # Skill directory. Remove Markdown link wrappers so Gemini does not follow a path that
        # sits outside the directory authorized by this one Skill activation.
        content = re.sub(r"\[([^\]]+)\]\([^\n)]+\)", r"\1", content)
        parts.extend((f"\n### Embedded dependency: `{name}`\n\n",
                      content, "\n"))
    return "".join(parts).encode("utf-8")


def manifests(config, platform):
    common = {key: config[key] for key in
              ("name", "version", "description", "author", "license", "keywords")}
    for key in ("homepage", "repository"):
        if key in config:
            common[key] = config[key]
    if platform == "openai":
        reminder = AUTO_ACTIVATION["openai"]
        hooks = {"hooks": {"UserPromptSubmit": [{"hooks": [{
            "type": "command",
            "command": f"printf '%s\\n' '{reminder}'",
            "commandWindows": f"Write-Output '{reminder}'",
            "async": False,
            "timeoutSec": 5,
            "additionalContextLimit": 0,
        }]}]}}
        return {
            "plugin.json": json_bytes({"$schema": SCHEMA, **common,
                                      "extensions": {"com.openai": {"interface": config["interface"]}}}),
            ".codex-plugin/plugin.json": json_bytes({**common, "skills": "./skills/",
                                                     "hooks": hooks,
                                                     "interface": config["interface"]}),
        }
    if platform == "claude":
        return {".claude-plugin/plugin.json": json_bytes(common)}
    if platform == "gemini":
        return {"gemini-extension.json": json_bytes({key: config[key] for key in
                                                     ("name", "version", "description")}
                                                     | {"contextFileName": "GEMINI.md"})}
    raise ValueError(f"Unknown platform: {platform}")


def payload(root, platform):
    config = metadata(root)
    result = {}
    for folder in ("skills", "shared"):
        result.update({f"{folder}/{name}": data for name, data in read_tree(root / folder).items()})
    if platform == "gemini":
        coordinator = "skills/adaptive-task-routing/SKILL.md"
        result[coordinator] = gemini_coordinator(root, result[coordinator])
    for name in COMMON_FILES:
        result[name] = (root / name).read_bytes()
    # Installation text is also the packaged README: one maintained copy per platform.
    readme = (root / f"packaging/{platform}/README.md").read_text(encoding="utf-8")
    # Source READMEs link two levels up; rebasing keeps both source and ZIP links valid.
    result["README.md"] = re.sub(r"(\]\()\.\./\.\./", r"\1", readme).encode("utf-8")
    if platform == "claude":
        result["hooks/hooks.json"] = json_bytes({
            "description": "Remind Claude to route qualifying substantial work.",
            "hooks": {"UserPromptSubmit": [{"hooks": [{
                "type": "command",
                "command": f'echo "{AUTO_ACTIVATION["claude"]}"',
                "timeout": 5,
            }]}]},
        })
    if platform == "gemini":
        result["GEMINI.md"] = (
            "# Adaptive Task Routing startup instruction\n\n"
            + AUTO_ACTIVATION["gemini"] + "\n"
        ).encode("utf-8")
    result.update(manifests(config, platform))
    return result


def archive_name(config, platform):
    return f'{config["name"]}-{platform}-{config["version"]}.zip'


def stage_path(dist, config, platform):
    return dist / platform / config["name"]
