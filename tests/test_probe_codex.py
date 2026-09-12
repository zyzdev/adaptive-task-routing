from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("probe_codex", ROOT / "skills/research-model-router/scripts/probe_codex.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class FakeRpc:
    def __init__(self, pages=None, thread=None, errors=()):
        self.pages = list(pages if pages is not None else [{"data": [{
            "model": "fixture-model", "description": "Fixture capability", "secret": "NEVER_PRINT",
            "supportedReasoningEfforts": [{"reasoningEffort": "fixture-effort"}]}]}])
        self.thread = thread or {"id": "fixture-thread", "model": "saved-model", "reasoningEffort": "saved-effort",
                                 "status": {"type": "notLoaded"}, "source": "cli",
                                 "preview": "NEVER_PRINT"}
        self.errors = errors
        self.calls = []

    def call(self, method, params):
        self.calls.append((method, params))
        if method in self.errors:
            raise probe.ProbeError("rpc_error")
        if method == "model/list":
            return self.pages.pop(0)
        if method == "config/read":
            return {"config": {"model": "default-model", "model_reasoning_effort": "default-effort",
                               "api_key": "NEVER_PRINT"}}
        return {"thread": self.thread}


class ProbeTests(unittest.TestCase):
    def test_filters_secrets_and_does_not_promote_defaults_or_saved_settings(self):
        client = FakeRpc()
        result = probe.collect(client, ROOT, "fixture-thread")
        self.assertNotIn("NEVER_PRINT", json.dumps(result))
        self.assertEqual(result["current_configuration"]["model"], "unknown")
        self.assertEqual(result["thread_configuration"]["evidence"], "persisted_or_unverified")
        self.assertEqual(result["disk_defaults"]["model"], "default-model")
        self.assertEqual(result["catalog"]["applicability"], "unverified")
        self.assertEqual(client.calls[-1], ("thread/read", {"threadId": "fixture-thread", "includeTurns": False}))
        self.assertEqual(result["switch_capability"], "not_tested")

    def test_cli_surface_scopes_only_the_candidate_catalog(self):
        result = probe.collect(FakeRpc(), ROOT, "fixture-thread", surface="codex-cli")
        self.assertEqual(result["catalog"]["scope"], "current_cli_environment")
        self.assertEqual(result["catalog"]["applicability"], "verified")
        self.assertEqual(result["catalog"]["applicability_basis"],
                         "caller_identified_codex_cli")
        self.assertEqual(result["disk_defaults"]["applicability"], "unverified")
        self.assertEqual(result["thread_configuration"]["applicability"], "unverified")
        self.assertEqual(result["current_configuration"],
                         {"model": "unknown", "reasoning_effort": "unknown"})

    def test_app_surface_does_not_promote_a_separate_cli_catalog(self):
        result = probe.collect(FakeRpc(), ROOT, surface="codex-app")
        self.assertEqual(result["catalog"]["applicability"], "unverified")
        self.assertEqual(result["catalog"]["applicability_basis"],
                         "separate_cli_process_does_not_establish_app_catalog")

    def test_surface_detection_uses_positive_process_evidence(self):
        fixtures = [
            (["/bin/zsh -lc python3 probe_codex.py", "/opt/homebrew/bin/codex --yolo"],
             ("codex-cli", "process_ancestry_codex_cli")),
            (["node /usr/local/lib/codex.js exec"],
             ("codex-cli", "process_ancestry_codex_cli")),
            (["/Applications/Codex.app/Contents/MacOS/Codex"],
             ("codex-app", "process_ancestry_codex_app")),
            (["/Applications/ChatGPT.app/Contents/MacOS/ChatGPT"],
             ("unknown", "process_ancestry_chatgpt_app")),
            (["/bin/zsh", "python3 probe_codex.py"],
             ("unknown", "no_positive_surface_evidence")),
        ]
        for commands, expected in fixtures:
            with self.subTest(commands=commands):
                self.assertEqual(probe.detect_surface(commands), expected)

    def test_auto_surface_uses_exact_thread_cli_origin_when_ancestry_is_isolated(self):
        result = probe.collect(FakeRpc(), ROOT, "fixture-thread")
        detection = probe.resolve_auto_surface(result, "unknown", "no_positive_surface_evidence")
        self.assertEqual(detection,
                         {"requested": "auto", "detected": "codex-cli",
                          "basis": "thread_read_source_cli"})
        self.assertEqual(result["catalog"]["applicability"], "verified")
        self.assertEqual(result["catalog"]["scope"], "current_cli_environment")
        self.assertEqual(result["thread_configuration"]["thread_source"], "cli")

    def test_pagination_and_hidden_models(self):
        client = FakeRpc(pages=[{"data": [{"model": "one"}], "nextCursor": "next"},
                               {"data": [{"model": "two"}, {"model": "hidden", "hidden": True}]}])
        result = probe.collect(client, ROOT)
        self.assertEqual([m["model"] for m in result["catalog"]["models"]], ["one", "two"])
        self.assertEqual(client.calls[1][1]["cursor"], "next")
        self.assertNotIn("thread/read", [m for m, _ in client.calls])

    def test_cyclic_pagination_retains_partial_evidence(self):
        client = FakeRpc(pages=[{"data": [{"model": "one"}], "nextCursor": "loop"},
                               {"data": [], "nextCursor": "loop"}])
        result = probe.collect(client, ROOT)
        self.assertEqual(result["catalog"]["status"], "partial")
        self.assertEqual(result["catalog"]["reason"], "invalid_pagination")

    def test_catalog_failure_does_not_hide_other_observations(self):
        result = probe.collect(FakeRpc(errors={"model/list"}), ROOT, "fixture-thread")
        self.assertEqual(result["catalog"]["status"], "error")
        self.assertEqual(result["disk_defaults"]["status"], "available")
        self.assertEqual(result["current_configuration"]["reasoning_effort"], "unknown")

    def test_wrong_thread_is_rejected(self):
        result = probe.collect(FakeRpc(), ROOT, "other-thread", via_socket=True)
        self.assertEqual(result["thread_configuration"]["status"], "scope_mismatch")
        self.assertNotIn("model", result["thread_configuration"])

    def test_loaded_thread_requires_explicit_transport_and_still_not_execution_telemetry(self):
        client = FakeRpc(thread={"id": "fixture-thread", "status": {"type": "idle"}, "model": "configured"})
        result = probe.collect(client, ROOT, "fixture-thread", via_socket=True)
        self.assertEqual(result["thread_configuration"]["evidence"], "live_configured")
        self.assertEqual(result["thread_configuration"]["applicability"], "unverified")
        self.assertEqual(result["current_configuration"]["model"], "unknown")

    def test_malformed_and_duplicate_catalogs(self):
        for data in ({}, [{"description": "no identifier"}], [{"model": "one"}, {"model": "one"}]):
            with self.subTest(data=data):
                result = probe.collect(FakeRpc(pages=[{"data": data}]), ROOT)
                self.assertIn(result["catalog"]["status"], {"error", "partial"})

    def test_rpc_timeout_is_bounded(self):
        client = probe.Rpc([sys.executable, "-c", "import time; time.sleep(10)"], ROOT, .1)
        started = time.monotonic()
        try:
            with self.assertRaisesRegex(probe.ProbeError, "timeout"):
                client.initialize()
        finally:
            client.close()
        self.assertLess(time.monotonic() - started, 3)

    def test_rpc_rejects_writes_and_history_before_sending(self):
        client = probe.Rpc([sys.executable, "-c", "import time; time.sleep(10)"], ROOT, .2)
        try:
            for method in ("turn/start", "thread/resume", "config/value/write", "thread/settings/update"):
                with self.assertRaisesRegex(probe.ProbeError, "method_not_allowed"):
                    client.call(method, {})
            with self.assertRaisesRegex(probe.ProbeError, "history_not_allowed"):
                client.call("thread/read", {"includeTurns": True})
        finally:
            client.close()

    def test_rpc_malformed_or_oversized_output_is_sanitized(self):
        for code, reason in [("print('private invalid data')", "invalid_protocol"),
                             ("print('x'*1048577)", "output_limit")]:
            with self.subTest(reason=reason):
                client = probe.Rpc([sys.executable, "-c", code], ROOT, 2)
                try:
                    with self.assertRaisesRegex(probe.ProbeError, reason):
                        client.call("model/list", {})
                finally:
                    client.close()

    def test_rpc_classifies_sandboxed_state_failure_without_leaking_stderr(self):
        private = "NEVER_PRINT_PRIVATE_PATH"
        code = ("import sys; "
                f"sys.stderr.write('Operation not permitted {private}\\n'"
                "+ 'failed to initialize sqlite state runtime\\n'); "
                "raise SystemExit(1)")
        client = probe.Rpc([sys.executable, "-c", code], ROOT, 2)
        try:
            with self.assertRaises(probe.ProbeError) as raised:
                client.initialize()
        finally:
            client.close()
        self.assertEqual(str(raised.exception), "codex_state_unwritable")
        self.assertNotIn(private, str(raised.exception))


if __name__ == "__main__":
    unittest.main()
