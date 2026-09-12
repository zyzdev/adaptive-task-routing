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


def manifests(config, platform):
    common = {key: config[key] for key in
              ("name", "version", "description", "author", "license", "keywords")}
    for key in ("homepage", "repository"):
        if key in config:
            common[key] = config[key]
    if platform == "openai":
        return {
            "plugin.json": json_bytes({"$schema": SCHEMA, **common,
                                      "extensions": {"com.openai": {"interface": config["interface"]}}}),
            ".codex-plugin/plugin.json": json_bytes({**common, "skills": "./skills/",
                                                     "interface": config["interface"]}),
        }
    if platform == "claude":
        return {".claude-plugin/plugin.json": json_bytes(common)}
    if platform == "gemini":
        return {"gemini-extension.json": json_bytes({key: config[key] for key in
                                                     ("name", "version", "description")})}
    raise ValueError(f"Unknown platform: {platform}")


def payload(root, platform):
    config = metadata(root)
    result = {}
    for folder in ("skills", "shared"):
        result.update({f"{folder}/{name}": data for name, data in read_tree(root / folder).items()})
    for name in COMMON_FILES:
        result[name] = (root / name).read_bytes()
    # Installation text is also the packaged README: one maintained copy per platform.
    readme = (root / f"packaging/{platform}/README.md").read_text(encoding="utf-8")
    # Source READMEs link two levels up; rebasing keeps both source and ZIP links valid.
    result["README.md"] = re.sub(r"(\]\()\.\./\.\./", r"\1", readme).encode("utf-8")
    result.update(manifests(config, platform))
    return result


def archive_name(config, platform):
    return f'{config["name"]}-{platform}-{config["version"]}.zip'


def stage_path(dist, config, platform):
    return dist / platform / config["name"]
