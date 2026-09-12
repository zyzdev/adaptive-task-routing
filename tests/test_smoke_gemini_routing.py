"""Offline fixtures for the opt-in CLI smoke checker; no inference or subprocess calls."""
import importlib.util
from pathlib import Path
import unittest


SPEC = importlib.util.spec_from_file_location(
    "gemini_smoke", Path(__file__).resolve().parents[1] / "scripts/smoke_gemini_routing.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

PLAN = """## 改善計畫
1. 統一 manifest 與 release.py 的版號來源。
2. 以發布結果取代 assert True，加入失敗案例。
3. 核對產物與 manifest 的版本一致。

---

"""

KEEP = PLAN + """### Adaptive Task Routing

✓ 維持目前設定

目前設定足以完成核對。
對話：留在目前對話，不需開新對話。
目前 AI：fixture-balanced / medium。
接著執行已授權核對。
"""


class GeminiCompactSmokeTests(unittest.TestCase):
    def test_accepts_keep_with_conversation_sentence(self):
        self.assertTrue(all(MODULE.routing_output_checks(KEEP).values()))

    def test_rejects_task_fit_alternative_in_verified_keep(self):
        result = MODULE.routing_output_checks(KEEP + "任務適配設定：fixture-strong / high。\n")
        self.assertFalse(result["verified_keep_current_only"])

    def test_accepts_provisional_keep_with_known_current_and_uncertain_cost(self):
        note = KEEP.replace("✓ 維持目前設定", "暫時沿用設定").replace(
            "目前設定足以完成核對。", "切換成本與效益仍不明確。")
        note += "任務適配設定：fixture-strong / high。\n"
        self.assertTrue(all(MODULE.routing_output_checks(note).values()))

    def test_rejects_unknown_current_field_but_accepts_uncertainty_in_prose(self):
        note = KEEP.replace("✓ 維持目前設定", "暫時沿用設定").replace(
            "目前 AI：fixture-balanced / medium。", "目前設定尚無法確認。\n任務適配設定：fixture-balanced / high。")
        self.assertTrue(all(MODULE.routing_output_checks(note).values()))
        self.assertFalse(MODULE.routing_output_checks(note + "\n目前 AI：Unknown")["no_unknown_current_field"])

    def test_rejects_old_subtitle_and_window_field(self):
        note = KEEP.replace("### Adaptive Task Routing", "### Adaptive Task Routing｜任務資源建議")
        self.assertFalse(MODULE.routing_output_checks(note)["plain_heading"])
        note = KEEP.replace("不需開新對話", "是否切換視窗：否")
        checks = MODULE.routing_output_checks(note)
        self.assertFalse(checks["no_window_field"])
        self.assertFalse(checks["conversation_visibility"])

    def test_context_off_omits_the_conversation_assessment(self):
        note = KEEP.replace("對話：留在目前對話，不需開新對話。\n", "")
        self.assertTrue(all(MODULE.routing_output_checks(note, context_enabled=False).values()))
        self.assertFalse(MODULE.routing_output_checks(KEEP, context_enabled=False)["conversation_visibility"])

    def test_rejects_reported_gemini_reversal_and_default_only_model(self):
        note = KEEP[len(PLAN):].replace("目前 AI：fixture-balanced / medium。", "目前 AI：使用模型預設。")
        note = note.replace("接著執行已授權核對。", "不需操作，以下為專案文件一致性與測試缺口改善計畫。")
        checks = MODULE.routing_output_checks(note + PLAN)
        self.assertFalse(checks["plan_before_routing"])
        self.assertFalse(checks["no_default_only_current"])

    def test_rejects_greeting_before_note_with_plan_after_note(self):
        checks = MODULE.routing_output_checks("好的，我會先檢查。\n" + KEEP[len(PLAN):] + PLAN)
        self.assertFalse(checks["plan_before_routing"])

    def test_rejects_plan_split_around_routing_and_duplicate_note(self):
        self.assertFalse(MODULE.routing_output_checks(KEEP + "\n## 補充改善計畫\n1. 核對產物。")['plan_before_routing'])
        self.assertFalse(MODULE.routing_output_checks(KEEP + KEEP)['plain_heading'])

    def test_routing_only_needs_no_invented_plan(self):
        self.assertTrue(all(MODULE.routing_output_checks(KEEP[len(PLAN):], require_plan=False).values()))

    def test_accepts_named_model_with_native_default_reasoning(self):
        note = KEEP.replace("fixture-balanced / medium", "Pro / Reasoning：使用模型預設")
        self.assertTrue(all(MODULE.routing_output_checks(note).values()))

    def test_rejects_synonym_or_action_merged_with_reason(self):
        for action in ["保留現況", "✓ 維持目前設定：目前設定足夠。"]:
            with self.subTest(action=action):
                self.assertFalse(MODULE.routing_output_checks(KEEP.replace("✓ 維持目前設定", action))["canonical_action_line"])

    def test_accepts_canonical_context_and_blocker_actions_without_ai_fields(self):
        for action, conversation in [
            ("→ 建議交接", "建議開新對話並交接必要脈絡，待你確認。"),
            ("↻ 全新開始", "建議開啟全新對話，不帶入目前脈絡，待你確認。"),
            ("? 需要你的決定", "目的地仍待確認。"),
        ]:
            note = KEEP.replace("✓ 維持目前設定", action).replace(
                "目前 AI：fixture-balanced / medium。\n", "").replace(
                "留在目前對話，不需開新對話。", conversation)
            with self.subTest(action=action):
                self.assertTrue(all(MODULE.routing_output_checks(note).values()))

    def test_accepts_provisional_without_task_fit_or_current_field(self):
        note = KEEP.replace("✓ 維持目前設定", "暫時沿用設定").replace(
            "目前 AI：fixture-balanced / medium。\n", "")
        self.assertTrue(all(MODULE.routing_output_checks(note).values()))
