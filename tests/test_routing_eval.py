"""Offline harness contracts and CLI integration. Only the local fake adapter runs."""
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("routing_eval", ROOT / "scripts/routing_eval.py")
EVAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVAL)
# Load the CLI without changing sys.path for other test modules.
CLI_SPEC = importlib.util.spec_from_file_location("routing_eval_cli", ROOT / "scripts/evaluate_routing.py")
CLI = importlib.util.module_from_spec(CLI_SPEC)
with patch.dict(sys.modules, {"routing_eval": EVAL}):
    CLI_SPEC.loader.exec_module(CLI)
FAKE = ROOT / "tests/fixtures/routing_eval_fake_adapter.py"


class RoutingEvalTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="atr-eval-tests-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        # Fail if offline library paths accidentally acquire network access.
        for method in ("socket", "create_connection"):
            guard = patch.object(socket, method, side_effect=AssertionError("Network is forbidden"))
            guard.start()
            self.addCleanup(guard.stop)
        self.suite = EVAL.read_json(ROOT / "tests/routing-eval-cases.json")
        self.suite_path = self.root / "suite.json"
        EVAL.write_json(self.suite_path, self.suite)
        self.directory = self.root / "plan"

    def plan(self, **kwargs):
        options = {"cases": ["release_audit", "evidence_synthesis"],
                   "strategies": ["adaptive", "sticky"], "repetitions": 1, "seed": 13}
        options.update(kwargs)
        return EVAL.create_plan(self.suite_path, self.directory, **options)

    def result(self, plan, job, **changes):
        result = {"schema_version": 1, "plan_id": plan["plan_id"], "job_id": job["id"],
                  "request_sha256": job["request_sha256"], "status": "completed",
                  "response": "Synthetic answer for offline tests.", "decision": {},
                  "observations": {"mutations_occurred": False, "fixtures_unchanged": True},
                  "metrics": {}, "provenance": {"execution_scope": "synthetic_harness_fixture"}}
        result.update(changes)
        return result

    def put(self, result):
        source = self.root / ("source-" + result["job_id"] + ".json")
        EVAL.write_json(source, result)
        EVAL.import_result(self.directory, source)

    def adapter(self, mode="success", **changes):
        value = {"argv": [sys.executable, "-S", str(FAKE), mode], "timeout_seconds": 5}
        value.update(changes)
        path = self.root / ("adapter-" + mode + ".json")
        EVAL.write_json(path, value)
        return path

    def cli(self, *args):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return CLI.main([str(a) for a in args])

    def packet(self, mirror=True):
        plan = self.plan(cases=["release_audit"])
        for job in plan["jobs"]:
            self.put(self.result(plan, job, response="brief" if job["strategy_id"] == "adaptive" else "a much longer answer"))
        output = self.root / "blind"
        packet, key = EVAL.blind_packet(self.directory, output, left="adaptive", right="sticky", mirror=mirror, seed=7)
        return output, packet, key

    def review(self, packet, key, judge="reviewer-1", prefer="adaptive"):
        reviews = []
        for item in key["items"]:
            winner = next(side for side in ("A", "B") if item[side]["strategy_id"] == prefer)
            reviews.append({"id": item["id"], "judge_id": judge, "winner": winner,
                "scores": {side: {c: 4 if side == winner else 2 for c in packet["rubric"]["criteria"]}
                           for side in ("A", "B")}, "reason": "Synthetic review of fixture content."})
        return {"schema_version": 1, "packet_id": packet["packet_id"], "reviews": reviews}

    def summarize(self, output, reviews):
        path = self.root / ("reviews-" + str(len(list(self.root.glob("reviews-*")))) + ".json")
        EVAL.write_json(path, reviews)
        return EVAL.summarize_reviews(output / "review.json", output / "private-key.json", path)

    def test_plan_reproducible_and_export_has_no_gold(self):
        with patch.object(EVAL.subprocess, "Popen", side_effect=AssertionError("No execution")):
            first = self.plan(contract_root=ROOT)
            second = EVAL.create_plan(self.suite_path, self.root / "second", cases=["release_audit", "evidence_synthesis"],
                strategies=["adaptive", "sticky"], repetitions=1, seed=13, contract_root=ROOT)
        self.assertEqual(first["plan_id"], second["plan_id"])
        self.assertEqual(first["jobs"], second["jobs"])
        self.assertEqual(len(first["jobs"]), 4)
        self.assertEqual(len(first["contract_sha256"]), 6)
        self.assertFalse((self.directory / "results").exists())
        for job in first["jobs"]:
            request = EVAL.read_json(self.directory / "requests" / (job["id"] + ".json"))
            self.assertEqual(request, job["request"])
            self.assertNotIn("checks", request)
            self.assertNotIn("success_rubric", request)

    def test_plan_rejects_reuse_invalid_selection_and_empty_holdout(self):
        self.plan()
        with self.assertRaises(ValueError):
            self.plan()
        for options in ({"cases": ["missing"]}, {"strategies": ["missing"]},
                        {"repetitions": 0}, {"repetitions": True}, {"split": "holdout"}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.plan(**options)

    def test_suite_duplicates_and_invalid_schema_are_rejected(self):
        duplicate = deepcopy(self.suite)
        duplicate["cases"][1]["input"]["prompt"] = "  " + duplicate["cases"][0]["input"]["prompt"].upper()
        with self.assertRaises(ValueError):
            EVAL.validate_suite(duplicate)
        for version in (True, 1.0, 0, "1"):
            invalid = deepcopy(self.suite)
            invalid["schema_version"] = version
            with self.subTest(version=version), self.assertRaises(ValueError):
                EVAL.validate_suite(invalid)

    def test_schedule_tampering_is_rejected(self):
        self.plan()
        original = (self.directory / "plan.json").read_text()
        for mutation in ("delete", "request", "schedule"):
            altered = json.loads(original)
            if mutation == "delete":
                altered["jobs"].pop()
            elif mutation == "request":
                altered["jobs"][0]["request"]["input"]["prompt"] = "changed"
            else:
                altered["jobs"].reverse()
            (self.directory / "plan.json").write_text(json.dumps(altered))
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                EVAL.load_plan(self.directory)

    def test_import_binding_and_overwrite_protection(self):
        plan = self.plan()
        result = self.result(plan, plan["jobs"][0])
        for field in ("plan_id", "job_id", "request_sha256"):
            bad = {**result, field: "wrong"}
            source = self.root / (field + ".json")
            EVAL.write_json(source, bad)
            with self.subTest(field=field), self.assertRaises(ValueError):
                EVAL.import_result(self.directory, source)
        self.put(result)
        before = (self.directory / "results" / (result["job_id"] + ".json")).read_bytes()
        with self.assertRaises(FileExistsError):
            EVAL.import_result(self.directory, self.root / ("source-" + result["job_id"] + ".json"))
        self.assertEqual(before, (self.directory / "results" / (result["job_id"] + ".json")).read_bytes())

    def test_success_evidence_billing_and_metric_validation(self):
        plan = self.plan()
        job = plan["jobs"][0]
        variants = [
            {"status": "failed", "observations": {"task_success": True, "task_success_evidence": "synthetic"}},
            {"observations": {"task_success": True}},
            {"observations": {"task_success": 1, "task_success_evidence": "synthetic"}},
            {"metrics": {"cost_usd": 1}, "provenance": {"billing_basis": "subscription"}},
            {"metrics": {"input_tokens": -1}}, {"metrics": {"input_tokens": True}},
            {"metrics": {"cost_usd": float("inf")}}, {"metrics": {"invented_metric": 1}},
            {"schema_version": True}, {"schema_version": 1.0},
        ]
        for changes in variants:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                EVAL.validate_result(self.result(plan, job, **changes), job, plan)
        valid = self.result(plan, job, metrics={"cost_usd": 0, "input_tokens": None}, provenance={"billing_basis": "api"})
        EVAL.validate_result(valid, job, plan)

    def test_invalid_json_never_becomes_missing_or_zero(self):
        for raw in ('{"x":NaN}', '{"x":Infinity}', '{"x":1e999}', '{"x":0,"x":1}'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                EVAL.parse_json(raw)

    def test_score_counts_missing_and_failed_costs_and_matches_pairs(self):
        plan = self.plan()
        for job in plan["jobs"]:
            if job["strategy_id"] == "sticky" and job["case_id"] == "evidence_synthesis":
                continue
            failed = job["case_id"] == "evidence_synthesis"
            success = job["strategy_id"] == "adaptive" and not failed
            self.put(self.result(plan, job, status="failed" if failed else "completed",
                observations={"task_success": success, "task_success_evidence": "synthetic verifier",
                              "mutations_occurred": False, "fixtures_unchanged": True},
                metrics={"cost_usd": 3 if failed else 1 if success else 2}, provenance={"billing_basis": "api"}))
        report = EVAL.score(self.directory)
        adaptive = next(s for s in report["summaries"] if s["strategy_id"] == "adaptive")
        sticky = next(s for s in report["summaries"] if s["strategy_id"] == "sticky")
        self.assertEqual(adaptive["metrics"]["cost_usd"]["sum_observed"], 4)
        self.assertEqual(adaptive["task_success"]["rate_observed"], .5)
        self.assertEqual(adaptive["status_counts"], {"completed": 1, "failed": 1})
        self.assertEqual(sticky["metrics"]["cost_usd"]["missing"], 1)
        self.assertIsNone(sticky["metrics"]["input_tokens"]["sum_observed"])
        pair = report["paired_comparisons"][0]
        self.assertEqual(pair["observed_success_pairs"], 1)
        self.assertEqual(pair["success_rate_delta_left_minus_right"], 1)
        self.assertEqual(pair["metric_deltas_left_minus_right"]["cost_usd"]["mean"], -1)
        failed_row = next(r for r in report["jobs"] if r["status"] == "failed")
        self.assertEqual(failed_row["contract_status"], "unknown")
        self.assertIn("unknown", EVAL.markdown_report(report))

    def test_completed_is_not_success_and_tracks_stay_separate(self):
        plan = self.plan(cases=["brief_question", "release_audit"])
        for job in plan["jobs"]:
            self.put(self.result(plan, job))
        report = EVAL.score(self.directory)
        self.assertEqual(len(report["summaries"]), 4)
        for summary in report["summaries"]:
            self.assertIsNone(summary["task_success"]["rate_observed"])
        self.assertEqual(len(report["paired_comparisons"]), 2)

    def test_check_types_missing_absence_and_strategy_filters(self):
        result = {"a": {"value": True, "null": None}, "response": "hello world"}
        for rule, expected in [
            ({"path": "a.value", "op": "eq", "value": 1}, "fail"),
            ({"path": "a.value", "op": "in", "value": [1]}, "fail"),
            ({"path": "a.missing", "op": "eq", "value": False}, "unknown"),
            ({"path": "a.null", "op": "absent"}, "fail"),
            ({"path": "a.missing", "op": "absent"}, "pass"),
            ({"path": "response", "op": "contains", "value": "world"}, "pass"),
        ]:
            with self.subTest(rule=rule):
                self.assertEqual(EVAL.evaluate_check(rule, result), expected)
        self.plan(cases=["short_phase_retention"])
        report = EVAL.score(self.directory)
        sticky = next(r for r in report["jobs"] if r["strategy_id"] == "sticky")
        self.assertEqual(sticky["checks"], [])
        self.assertEqual(sticky["contract_status"], "unknown")

    def test_run_requires_opt_in_and_positive_limit_before_process_creation(self):
        with patch.object(EVAL.subprocess, "Popen") as launch:
            for kwargs in ({"allow_execution": False, "max_jobs": 1},
                           {"allow_execution": True, "max_jobs": 0}):
                with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                    list(EVAL.execute_jobs(self.directory, self.root / "nonexistent", **kwargs))
            launch.assert_not_called()

    def test_fake_runner_cap_resume_and_isolation(self):
        plan = self.plan()
        adapter = self.adapter()
        first = list(EVAL.execute_jobs(self.directory, adapter, allow_execution=True, max_jobs=1))
        self.assertEqual(len(first), 1)
        result = first[0]
        self.assertEqual(result["status"], "completed")
        self.assertTrue(result["provenance"]["workspace_empty"])
        self.assertNotIn("checks", result["provenance"]["received_top_level_keys"])
        self.assertEqual(result["provenance"]["execution_scope"], "synthetic_harness_fixture")
        self.assertGreaterEqual(result["metrics"]["elapsed_seconds"], 0)
        rest = list(EVAL.execute_jobs(self.directory, adapter, allow_execution=True, max_jobs=20))
        self.assertEqual(len(rest), len(plan["jobs"]) - 1)
        with patch.object(EVAL.subprocess, "Popen") as launch:
            self.assertEqual(list(EVAL.execute_jobs(self.directory, adapter, allow_execution=True, max_jobs=1)), [])
            launch.assert_not_called()

    def test_runner_failures_stop_without_automatic_retry(self):
        for mode in ("invalid", "exit", "wrong_hash", "oversize", "blocked", "timeout"):
            with self.subTest(mode=mode):
                self.directory = self.root / ("plan-" + mode)
                self.plan()
                adapter = self.adapter(mode, timeout_seconds=1, max_output_bytes=2048)
                results = list(EVAL.execute_jobs(self.directory, adapter, allow_execution=True, max_jobs=4))
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["status"], "blocked" if mode in ("blocked", "timeout") else "failed")
                next_results = list(EVAL.execute_jobs(self.directory, adapter, allow_execution=True, max_jobs=1))
                self.assertNotEqual(next_results[0]["job_id"], results[0]["job_id"])

    def test_changed_adapter_rejected_before_execution(self):
        self.plan()
        list(EVAL.execute_jobs(self.directory, self.adapter(), allow_execution=True, max_jobs=1))
        changed = self.adapter("blocked")
        with patch.object(EVAL.subprocess, "Popen") as launch, self.assertRaises(ValueError):
            list(EVAL.execute_jobs(self.directory, changed, allow_execution=True, max_jobs=1))
        launch.assert_not_called()

    def test_interruption_preserves_attempt_so_resume_does_not_silently_retry(self):
        plan = self.plan()
        adapter = self.adapter()
        process = Mock()
        process.communicate.side_effect = KeyboardInterrupt
        with patch.object(EVAL.subprocess, "Popen", return_value=process), patch.object(EVAL, "stop_process") as stop:
            with self.assertRaises(KeyboardInterrupt):
                list(EVAL.execute_jobs(self.directory, adapter, allow_execution=True, max_jobs=1))
            stop.assert_called_once_with(process)
        results = EVAL.read_results(self.directory, plan)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[plan["jobs"][0]["id"]]["status"], "blocked")

    def test_blind_mirror_anonymity_and_no_double_count(self):
        output, packet, key = self.packet()
        self.assertEqual(len(packet["items"]), 2)
        first, second = packet["items"]
        self.assertEqual(first["A"], second["B"])
        self.assertEqual(first["B"], second["A"])
        for item in packet["items"]:
            self.assertNotIn("strategy_id", item)
            self.assertNotIn("job_id", item)
        summary = self.summarize(output, self.review(packet, key))["summaries"][0]
        self.assertEqual(summary["consistent_pair_votes"], {"adaptive": 1})
        self.assertEqual(summary["criterion_scores"]["adaptive"]["correctness"]["observed"], 1)
        self.assertEqual(summary["criterion_scores"]["adaptive"]["correctness"]["mean"], 4)
        self.assertEqual(summary["A_selection_rate_descriptive"], .5)
        self.assertEqual(summary["longer_answer_selection_rate_descriptive"], 0)

    def test_order_bias_missing_votes_and_interjudge_agreement(self):
        output, packet, key = self.packet()
        reviews = self.review(packet, key)
        reviews["reviews"].extend(self.review(packet, key, judge="reviewer-2")["reviews"])
        report = self.summarize(output, reviews)
        self.assertEqual(report["summaries"][0]["judge_agreement"], {"comparisons": 1, "rate": 1})
        biased = self.review(packet, key)
        for row in biased["reviews"]:
            row["winner"] = "A"
        result = self.summarize(output, biased)["summaries"][0]
        self.assertEqual(result["order_inconsistent_pair_votes"], 1)
        self.assertEqual(result["consistent_pair_votes"], {})
        biased["reviews"].pop()
        report = self.summarize(output, biased)
        self.assertEqual(report["items_without_review"], 1)
        self.assertEqual(report["reviewer_coverage"]["reviewer-1"]["missing"], 1)
        self.assertEqual(report["summaries"][0]["incomplete_mirrored_pair_votes"], 1)

    def test_review_duplicate_invalid_score_and_packet_mismatch(self):
        output, packet, key = self.packet()
        for mutation in ("duplicate", "score", "packet"):
            reviews = self.review(packet, key)
            if mutation == "duplicate":
                reviews["reviews"].append(reviews["reviews"][0])
            elif mutation == "score":
                reviews["reviews"][0]["scores"]["A"]["correctness"] = True
            else:
                reviews["packet_id"] = "wrong"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.summarize(output, reviews)

    def test_review_key_metadata_is_bound(self):
        output, packet, key = self.packet()
        reviews = self.review(packet, key)
        key["plan_id"] = "another-plan"
        (output / "private-key.json").write_text(json.dumps(key))
        with self.assertRaises(ValueError):
            self.summarize(output, reviews)

    def test_incomplete_pairs_are_skipped_not_wins(self):
        self.plan()
        packet, key = EVAL.blind_packet(self.directory, self.root / "empty", left="adaptive", right="sticky")
        self.assertEqual(packet["items"], [])
        self.assertEqual(key["skipped_pairs"], 2)
        report = self.summarize(self.root / "empty", {"schema_version": 1, "packet_id": packet["packet_id"], "reviews": []})
        self.assertEqual(report["summaries"], [])

    def test_cli_offline_pipeline_and_report_outputs(self):
        with patch.object(EVAL.subprocess, "Popen", side_effect=AssertionError("Offline commands spawned a process")):
            self.assertEqual(self.cli("plan", "--suite", self.suite_path, "--output", self.directory,
                "--case", "release_audit", "--strategy", "adaptive", "--strategy", "sticky", "--repetitions", 1), 0)
            plan = EVAL.load_plan(self.directory)
            for job in plan["jobs"]:
                source = self.root / (job["id"] + ".json")
                EVAL.write_json(source, self.result(plan, job))
                self.assertEqual(self.cli("import", "--plan", self.directory, "--result", source), 0)
            report = self.root / "report.json"
            markdown = self.root / "report.md"
            self.assertEqual(self.cli("score", "--plan", self.directory, "--output", report, "--markdown", markdown), 0)
            self.assertTrue(markdown.read_text().startswith("# Routing evaluation report"))
            self.assertEqual(self.cli("score", "--plan", self.directory, "--output", report), 2)
            output = self.root / "review"
            self.assertEqual(self.cli("blind", "--plan", self.directory, "--left", "adaptive", "--right", "sticky",
                "--mirror", "--output", output), 0)
            packet, key = EVAL.read_json(output / "review.json"), EVAL.read_json(output / "private-key.json")
            votes = self.root / "votes.json"
            EVAL.write_json(votes, self.review(packet, key))
            self.assertEqual(self.cli("review-report", "--packet", output / "review.json", "--key", output / "private-key.json",
                "--reviews", votes, "--output", self.root / "judged.json"), 0)

    def test_real_cli_process_with_fake_adapter_only(self):
        # Minimal environment excludes user Python startup paths and provider settings.
        env = {"PATH": os.defpath, "PYTHONIOENCODING": "utf-8"}
        if "SYSTEMROOT" in os.environ:
            env["SYSTEMROOT"] = os.environ["SYSTEMROOT"]
        self.plan()
        command = [sys.executable, "-S", str(ROOT / "scripts/evaluate_routing.py"), "run",
                   "--plan", str(self.directory), "--adapter", str(self.adapter()), "--max-jobs", "1"]
        refused = subprocess.run(command, capture_output=True, text=True, env=env, timeout=10)
        self.assertEqual(refused.returncode, 2)
        self.assertFalse((self.directory / "results").exists())
        completed = subprocess.run(command + ["--allow-execution"], capture_output=True, text=True, env=env, timeout=10)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(len(list((self.directory / "results").glob("*.json"))), 1)


if __name__ == "__main__":
    unittest.main()
