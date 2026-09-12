#!/usr/bin/env python3
"""Load release metadata locally without model calls or persistent installation.

Claude and Gemini use temporary configuration directories. Codex reads an explicit
temporary marketplace through its app-server API; no install/write API is called.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import tempfile
import time

from release_lib import ROOT, SKILLS


def command(args, cwd, env):
    result = subprocess.run(args, cwd=cwd, env=env, input="", text=True,
                            capture_output=True, timeout=45)
    return {"command": args, "exit_code": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr}


def codex_read(marketplace, cwd):
    args = ["codex", "app-server", "--stdio", "-c", "analytics.enabled=false"]
    with tempfile.TemporaryFile(mode="w+") as error_log:
        process = subprocess.Popen(args, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=error_log, text=True, bufsize=1)
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        def send(value):
            process.stdin.write(json.dumps(value) + "\n")
            process.stdin.flush()
        def receive(identifier):
            deadline = time.monotonic() + 40
            while time.monotonic() < deadline:
                if selector.select(timeout=0.5):
                    line = process.stdout.readline()
                    if not line:
                        raise RuntimeError("Codex app-server closed its output")
                    value = json.loads(line)
                    if value.get("id") == identifier:
                        if "error" in value:
                            raise RuntimeError(json.dumps(value["error"]))
                        return value["result"]
            raise TimeoutError("Codex local plugin read timed out")
        try:
            send({"id": 1, "method": "initialize", "params": {
                "clientInfo": {"name": "atr-release-smoke", "version": "1.0.0"},
                "capabilities": {"experimentalApi": True}}})
            receive(1)
            send({"method": "initialized"})
            send({"id": 2, "method": "plugin/read", "params": {
                "pluginName": "adaptive-task-routing", "marketplacePath": str(marketplace)}})
            result = receive(2)
            plugin = result["plugin"]
            names = sorted(s["name"] for s in plugin["skills"])
            expected = sorted(f"adaptive-task-routing:{s}" for s in SKILLS)
            return {"command": args, "method": "plugin/read", "skills": names,
                    "status": "pass" if names == expected else "fail", "result": result}
        finally:
            selector.close()
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            process.stdin.close()
            process.stdout.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=("all", "openai", "claude", "gemini"), default="all")
    args = parser.parse_args()
    from validate_release import validate_dist
    validate_dist(ROOT, ROOT / "dist")
    report = {}
    with tempfile.TemporaryDirectory(prefix="atr-native-smoke-") as temporary:
        scratch = Path(temporary)
        for platform, executable in (("openai", "codex"), ("claude", "claude"), ("gemini", "gemini")):
            if args.platform not in ("all", platform):
                continue
            if not shutil.which(executable):
                report[platform] = {"status": "blocked", "reason": "CLI unavailable"}
                continue
            plugin = ROOT / "dist" / platform / "adaptive-task-routing"
            workspace = scratch / platform
            workspace.mkdir()
            environment = os.environ.copy()
            environment["NO_COLOR"] = "1"
            records = []
            try:
                if platform == "openai":
                    target = workspace / "plugins/adaptive-task-routing"
                    shutil.copytree(plugin, target)
                    marketplace = workspace / ".agents/plugins/marketplace.json"
                    marketplace.parent.mkdir(parents=True)
                    marketplace.write_text(json.dumps({"name": "atr-release-smoke", "plugins": [{
                        "name": "adaptive-task-routing",
                        "source": {"source": "local", "path": "./plugins/adaptive-task-routing"},
                        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        "category": "Productivity"}]}))
                    report[platform] = codex_read(marketplace, workspace)
                elif platform == "claude":
                    # Bare mode and no auth environment keep the inventory check offline.
                    environment = {k: v for k, v in environment.items()
                                   if k in {"PATH", "LANG", "LC_ALL", "TMPDIR", "NO_COLOR"}}
                    environment["CLAUDE_CONFIG_DIR"] = str(workspace / "config")
                    records.append(command([executable, "--setting-sources", "", "--plugin-dir",
                                            str(plugin), "plugin", "list", "--json"], workspace, environment))
                    output = records[-1]["stdout"]
                    found = "adaptive-task-routing" in output
                    records.append(command([executable, "--bare", "--setting-sources", "", "--plugin-dir",
                                            str(plugin), "plugin", "details", "adaptive-task-routing@inline"],
                                           workspace, environment))
                    inventory = records[-1]["stdout"]
                    found = found and all(s in inventory for s in SKILLS)
                    report[platform] = {"status": "pass" if found and all(r["exit_code"] == 0 for r in records) else "blocked",
                                        "scope": "plugin and Skill inventory discovery, not behavioral execution",
                                        "records": records}
                else:
                    environment["GEMINI_CLI_HOME"] = str(workspace / "config")
                    environment["GEMINI_CLI_NO_RELAUNCH"] = "1"
                    # Consent is limited to this audited plugin and disposable test workspace.
                    records.append(command([executable, "extensions", "link", str(plugin), "--consent"], workspace, environment))
                    records.append(command([executable, "extensions", "list"], workspace, environment))
                    records.append(command([executable, "skills", "list"], workspace, environment))
                    passed = all(r["exit_code"] == 0 for r in records)
                    passed = passed and all(s in records[-1]["stdout"] for s in SKILLS)
                    report[platform] = {"status": "pass" if passed else "blocked", "records": records}
            except (RuntimeError, TimeoutError, subprocess.TimeoutExpired, OSError) as error:
                report[platform] = {"status": "blocked", "reason": str(error), "records": records}
            print(f'{platform}: {report[platform]["status"]}', flush=True)
    output = ROOT / "build/native-smoke.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"Evidence: {output}")
    return 0 if all(r["status"] == "pass" for r in report.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
