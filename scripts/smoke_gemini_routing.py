#!/usr/bin/env python3
"""Opt-in live Gemini calls against the installed extension; does not install it.

Uses the CLI's configured model, read-only plan mode and disposable task fixtures.
Requires a configured/authenticated Gemini CLI. Calls may consume account usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import time


FIXTURES = {
    "manifest.json": '{"version":"1.2.0"}\n',
    "release.py": 'from pathlib import Path\nVERSION = "1.1.0"\n'
                  'def release():\n    Path("artifact.txt").write_text(VERSION)\n',
    "test_release.py": 'def test_release():\n    assert True\n',
}
AUDIT = ("請檢查這個目錄的 manifest.json、release.py、test_release.py，指出發布流程與測試的問題，"
         "提出三點具體改善計畫。先不要修改檔案。請用繁體中文。")
PROMPTS = {
    "audit": AUDIT,
    "next_phase": ("初步盤點已完成：發布版號有兩個來源，測試只有 assert True。"
                   "下一階段計畫做文件一致性審核與測試覆蓋率檢查，涵蓋 manifest.json、"
                   "release.py、test_release.py。請先評估下一階段的路由，先不要執行計畫。請用繁體中文。"),
    "context_off": "這次將 Context 路由設為 off，Model 路由維持 ask。" + AUDIT,
}


CANONICAL_ACTIONS = (
    "✓ 維持目前設定", "暫時沿用設定", "→ 建議交接", "↻ 全新開始",
    "↑ 建議調整 AI 設定", "? 需要你的決定",
)


def routing_output_checks(response, *, context_enabled=True, require_plan=True):
    """Check Chinese compact smoke fixtures, not model identity or quality evidence.

    Plan checks target AUDIT's three-point plan. They are structural guards, not a
    general prose evaluator. A passing result still requires semantic review.
    """
    headings = list(re.finditer(r"^### Adaptive Task Routing[ \t]*$", response, re.MULTILINE))
    heading = headings[0] if headings else None
    before = response[:heading.start()] if heading else ""
    note = response[heading.end():] if heading else ""
    lines = [line.strip() for line in note.splitlines() if line.strip()]
    action = lines[0] if lines else ""
    setting = re.search(r"任務適配設定|目前 AI|目前設定[：:]|Model[：:]", note)
    conversation = re.search(r"^\s*(?:[-*]\s*)?對話[：:]([^\n]+)", note, re.MULTILINE)
    explicit_conversation = bool(conversation and re.search(
        r"不需開新對話|無需開新對話|建議開新對話|建議開啟全新對話|目的地.*待確認", conversation[1]))
    current = re.search(r"^(?:目前 AI|目前設定)[：:]\s*([^\n]+)", note, re.MULTILINE)
    # A concrete-looking name is necessary for verified keep, never proof of observation.
    default_only = bool(current and re.fullmatch(
        r"(?:使用)?(?:模型|平台)?預設(?:值|設定)?[。.]?|(?:model |platform )?default[。.]?|Auto[。.]?",
        current[1].strip(), re.IGNORECASE))
    verified_keep = action == CANONICAL_ACTIONS[0]
    provisional_keep = action == CANONICAL_ACTIONS[1]
    plan_items = re.findall(r"^\s*(?:#{1,6}\s+)?(?:[-*]|[1-3][.、)])\s+\S.*$", before, re.MULTILINE)
    # A plan-only note is last; numbered task sections after it reveal reversal/splitting.
    later_plan = re.search(r"以下(?:為|是).*計畫|^\s*(?:#{1,6}\s+|[1-3][.、)]\s+)\S", note, re.MULTILINE)
    return {
        "plain_heading": len(headings) == 1,
        "canonical_action_line": action in CANONICAL_ACTIONS,
        "plan_before_routing": not require_plan or (len(plan_items) >= 3 and later_plan is None),
        "action_before_setting": action in CANONICAL_ACTIONS and (
            setting is None or note.find(action) < setting.start()),
        "conversation_visibility": explicit_conversation if context_enabled else conversation is None,
        "no_window_field": "是否切換視窗" not in note,
        "verified_keep_current_only": not verified_keep or (current is not None and "任務適配設定" not in note),
        "no_default_only_current": not default_only,
        "no_unknown_current_field": not re.search(
            r"(?:目前 AI|目前設定|Current AI)[：:]\s*(?:Unknown|unknown|未知|無法確認)", note),
        "retention_action_consistent": not ((verified_keep or provisional_keep) and "/model" in note),
        "no_artificial_retention_hold": "等你決定是否沿用目前設定" not in note,
    }


def run(case):
    started = time.monotonic()
    result = {"case": case, "prompt": PROMPTS[case]}
    with tempfile.TemporaryDirectory(prefix="atr-gemini-routing-") as temporary:
        workspace = Path(temporary)
        for name, content in FIXTURES.items():
            (workspace / name).write_text(content)
        # No workspace GEMINI.md or explicit Skill/output template in the prompt.
        command = ["gemini", "--skip-trust", "--approval-mode", "plan",
                   "--extensions", "adaptive-task-routing", "--output-format", "json",
                   "-p", PROMPTS[case]]
        try:
            completed = subprocess.run(command, cwd=workspace, input="", capture_output=True,
                                       text=True, timeout=180)
            data = json.loads(completed.stdout)
            response = data.get("response", "")
            checks = {
                **routing_output_checks(response, context_enabled=case != "context_off",
                                        require_plan=case != "next_phase"),
                "successful_response": completed.returncode == 0 and bool(response),
                "fixtures_unchanged": all((workspace / name).read_text() == content
                    for name, content in FIXTURES.items()),
                "no_execution_artifact": not (workspace / "artifact.txt").exists(),
            }
            result.update(response=response, checks=checks,
                          observed_models=list(data.get("stats", {}).get("models", {})),
                          semantic_review_required=True,
                          status="pass" if all(checks.values()) else "fail")
        except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as error:
            result.update(status="blocked", error_type=type(error).__name__)
    result["elapsed_seconds"] = round(time.monotonic() - started, 2)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=tuple(PROMPTS) + ("all",), default="all")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    installed = Path.home() / ".gemini/extensions/adaptive-task-routing/GEMINI.md"
    startup = installed.read_bytes()
    report = {"scope": "Installed extension in fresh CLI sessions; no workspace GEMINI.md; "
              "configured model; no real model/context switch. Output checks also require semantic review.",
              "startup_sha256": hashlib.sha256(startup).hexdigest(), "results": []}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for case in PROMPTS if args.case == "all" else (args.case,):
        result = run(case)
        report["results"].append(result)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        print(f'{case}: {result["status"]} ({result["elapsed_seconds"]}s)', flush=True)
    return 0 if all(r["status"] == "pass" for r in report["results"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
