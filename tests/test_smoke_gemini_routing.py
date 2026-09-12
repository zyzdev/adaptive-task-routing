"""Offline fixtures for the opt-in CLI smoke checker; no inference or subprocess calls."""
import importlib.util
from pathlib import Path
import unittest


SPEC = importlib.util.spec_from_file_location(
    "gemini_smoke", Path(__file__).resolve().parents[1] / "scripts/smoke_gemini_routing.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

KEEP = """### Adaptive Task Routing

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
        note = KEEP.replace("維持目前設定", "暫時沿用設定").replace(
            "目前設定足以完成核對。", "切換成本與效益仍不明確。")
        note += "任務適配設定：fixture-strong / high。\n"
        self.assertTrue(all(MODULE.routing_output_checks(note).values()))

    def test_rejects_unknown_current_field_but_accepts_uncertainty_in_prose(self):
        note = KEEP.replace("維持目前設定", "暫時沿用設定").replace(
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
