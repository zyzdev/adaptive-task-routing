"""Local routing experiments. Standard library only; provider access lives in adapters.

Planning, importing, scoring and preparing blind reviews never launch a process.
Only execute_jobs can do so, and the CLI requires an explicit execution opt-in.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import random
import re
import signal
import statistics
import subprocess
import tempfile
import time


VERSION = 1
IDENTIFIER = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}$")
METRICS = ("elapsed_seconds", "input_tokens", "output_tokens", "cached_input_tokens",
           "tool_calls", "retries", "model_switches", "context_switches",
           "human_interventions", "cost_usd")
MISSING = object()


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     allow_nan=False).encode()).hexdigest()


def parse_json(raw):
    def reject_constant(value):
        raise ValueError(f"Non-finite JSON value: {value}")

    def finite_float(value):
        parsed = float(value)
        if not math.isfinite(parsed):
            raise ValueError("JSON floating-point value overflowed")
        return parsed

    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(raw, parse_constant=reject_constant, parse_float=finite_float,
                      object_pairs_hook=unique_object)


def read_json(path):
    return parse_json(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    """Refuse overwrite; partial writes cannot become accepted experiment records."""
    serialized = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(serialized)


def identifier(value):
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise ValueError(f"Invalid identifier: {value!r}")
    return value


def require_object(value, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def require_schema(value, label):
    require_object(value, label)
    if type(value.get("schema_version")) is not int or value["schema_version"] != VERSION:
        raise ValueError(f"Unsupported {label} schema_version")


def positive_int(value, label):
    if type(value) is not int or value < 1:
        raise ValueError(f"{label} must be a positive integer")
    return value


def validate_suite(suite):
    require_schema(suite, "suite")
    identifier(suite.get("id"))
    for key in ("strategies", "cases"):
        if not isinstance(suite.get(key), list) or not suite[key]:
            raise ValueError(f"suite.{key} must be a nonempty list")
        ids = [identifier(require_object(row, key).get("id")) for row in suite[key]]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate {key} identifier")
    strategy_ids = {s["id"] for s in suite["strategies"]}
    for strategy in suite["strategies"]:
        if not isinstance(strategy.get("instructions"), str) or not strategy["instructions"].strip():
            raise ValueError("Each strategy needs instructions")
    prompts = set()
    for case in suite["cases"]:
        if case.get("track") not in ("routing_decision", "task_outcome"):
            raise ValueError("case.track must be routing_decision or task_outcome")
        if case.get("split") not in ("development", "holdout"):
            raise ValueError("case.split must be development or holdout")
        inputs = require_object(case.get("input"), "case.input")
        if not isinstance(inputs.get("prompt"), str) or not inputs["prompt"].strip():
            raise ValueError("case.input.prompt must be nonempty")
        # Catch exact normalized duplicates. Semantic deduplication remains human work.
        fingerprint = digest(" ".join(inputs["prompt"].split()).casefold())
        if fingerprint in prompts:
            raise ValueError("Duplicate normalized prompt; use distinct cases")
        prompts.add(fingerprint)
        rules = case.get("checks", [])
        if not isinstance(rules, list):
            raise ValueError("case.checks must be a list")
        check_ids = set()
        for rule in rules:
            require_object(rule, "check")
            rule_id = identifier(rule.get("id"))
            if rule_id in check_ids:
                raise ValueError("Duplicate check id within case")
            check_ids.add(rule_id)
            if rule.get("op") not in ("eq", "in", "contains", "absent"):
                raise ValueError("Unknown check operator")
            if not isinstance(rule.get("path"), str) or not rule["path"]:
                raise ValueError("Each check needs a dotted object path")
            if rule["op"] != "absent" and "value" not in rule:
                raise ValueError("Check needs value")
            if rule["op"] == "in" and not isinstance(rule["value"], list):
                raise ValueError("in check needs a list value")
            if rule["op"] == "contains" and not isinstance(rule["value"], str):
                raise ValueError("contains check needs a string value")
            if "strategies" in rule and (not isinstance(rule["strategies"], list)
                    or not rule["strategies"] or not set(rule["strategies"]) <= strategy_ids):
                raise ValueError("Check references unknown strategies")
            if type(rule.get("critical", False)) is not bool:
                raise ValueError("check.critical must be boolean")
    return suite


def create_plan(suite_path, output, *, repetitions=3, seed=0, split="development",
                cases=None, strategies=None, contract_root=None):
    positive_int(repetitions, "repetitions")
    if type(seed) is not int or split not in ("development", "holdout", "all"):
        raise ValueError("Invalid seed or split")
    suite = validate_suite(read_json(suite_path))
    selected_cases = [c for c in suite["cases"] if (split == "all" or c["split"] == split)
                      and (not cases or c["id"] in cases)]
    selected_strategies = [s for s in suite["strategies"] if not strategies or s["id"] in strategies]
    if cases and set(cases) != {c["id"] for c in selected_cases}:
        raise ValueError("Unknown cases or cases excluded by split")
    if strategies and set(strategies) != {s["id"] for s in selected_strategies}:
        raise ValueError("Unknown strategies")
    if not selected_cases or not selected_strategies:
        raise ValueError("Selection is empty")
    contracts = {}
    if contract_root is not None:
        root = Path(contract_root)
        paths = ["skills/adaptive-task-routing/SKILL.md", "skills/task-context-router/SKILL.md",
                 "skills/research-model-router/SKILL.md", "shared/runtime-routing-policy.md",
                 "shared/defaults.yaml", "shared/routing-ux.md"]
        contracts = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in paths}
    payload = {"schema_version": VERSION, "suite_id": suite["id"], "suite_sha256": digest(suite),
               "seed": seed, "repetitions": repetitions, "split": split,
               "cases": selected_cases, "strategies": selected_strategies,
               "contract_sha256": contracts}
    plan_id = digest(payload)[:24]
    jobs = make_jobs(payload, plan_id)
    plan = {**payload, "plan_id": plan_id, "created_at": now(), "jobs": jobs,
            "status": "not_run", "estimated_adapter_invocations": len(jobs)}
    output = Path(output)
    if output.exists():
        raise ValueError("Choose a new plan directory; existing output is never overwritten")
    write_json(output / "plan.json", plan)
    # Requests contain no expected outcomes or gold checks.
    for job in jobs:
        write_json(output / "requests" / (job["id"] + ".json"), job["request"])
    return plan


def make_jobs(payload, plan_id):
    """Reconstruct the complete schedule, including requests, from pinned inputs."""
    jobs = []
    for case in payload["cases"]:
        for repeat in range(payload["repetitions"]):
            for strategy in payload["strategies"]:
                job_id = digest([plan_id, case["id"], repeat, strategy["id"]])[:24]
                request = {"schema_version": VERSION, "plan_id": plan_id, "job_id": job_id,
                           "case_id": case["id"], "track": case["track"], "repeat": repeat,
                           "sampling_seed": payload["seed"] + repeat, "strategy": strategy,
                           "input": case["input"], "contract_sha256": payload["contract_sha256"]}
                jobs.append({"id": job_id, "case_id": case["id"], "strategy_id": strategy["id"],
                             "repeat": repeat, "request": request, "request_sha256": digest(request)})
    random.Random(payload["seed"]).shuffle(jobs)
    return jobs


def load_plan(directory):
    plan = require_object(read_json(Path(directory) / "plan.json"), "plan")
    require_schema(plan, "plan")
    payload_keys = ("schema_version", "suite_id", "suite_sha256", "seed", "repetitions",
                    "split", "cases", "strategies", "contract_sha256")
    payload = {k: plan[k] for k in payload_keys}
    if digest(payload)[:24] != plan["plan_id"]:
        raise ValueError("Plan contents changed; create a new plan")
    expected_jobs = make_jobs(payload, plan["plan_id"])
    if digest(plan["jobs"]) != digest(expected_jobs):
        raise ValueError("Schedule or requests changed; create a new plan")
    if type(plan.get("estimated_adapter_invocations")) is not int or plan["estimated_adapter_invocations"] != len(expected_jobs):
        raise ValueError("Planned invocation count changed")
    return plan


def validate_result(result, job, plan):
    require_schema(result, "result")
    for key, value in (("schema_version", VERSION), ("plan_id", plan["plan_id"]),
                       ("job_id", job["id"]), ("request_sha256", job["request_sha256"])):
        if result.get(key) != value:
            raise ValueError(f"Result {key} mismatch")
    if result.get("status") not in ("completed", "failed", "blocked"):
        raise ValueError("Result status must be completed, failed or blocked")
    if not isinstance(result.get("response", ""), str):
        raise ValueError("response must be a string")
    for key in ("decision", "observations", "metrics", "provenance"):
        require_object(result.get(key, {}), key)
    metrics = result.get("metrics", {})
    for metric, value in metrics.items():
        if metric not in METRICS:
            raise ValueError(f"Unknown metric {metric}")
        if value is not None and (type(value) not in (int, float) or not math.isfinite(value) or value < 0):
            raise ValueError(f"Invalid nonnegative metric {metric}")
    success = result.get("observations", {}).get("task_success")
    if success is not None and type(success) is not bool:
        raise ValueError("observations.task_success must be boolean or null")
    evidence = result.get("observations", {}).get("task_success_evidence")
    if success is not None and (not isinstance(evidence, str) or not evidence.strip()):
        raise ValueError("task_success needs a nonempty evidence reference string")
    if result["status"] != "completed" and success is True:
        raise ValueError("An incomplete run cannot claim task success")
    if metrics.get("cost_usd") is not None and result.get("provenance", {}).get("billing_basis") != "api":
        raise ValueError("cost_usd requires billing_basis=api; do not price subscription usage")
    for field in ("surface", "host_version", "model", "reasoning_effort", "execution_scope", "billing_basis", "adapter_sha256"):
        value = result.get("provenance", {}).get(field)
        if value is not None and not isinstance(value, str):
            raise ValueError(f"provenance.{field} must be a string or null")
    return result


def import_result(directory, source):
    plan = load_plan(directory)
    result = require_object(read_json(source), "result")
    jobs = {j["id"]: j for j in plan["jobs"]}
    if result.get("job_id") not in jobs:
        raise ValueError("Unknown result job_id")
    validate_result(result, jobs[result["job_id"]], plan)
    write_json(Path(directory) / "results" / (result["job_id"] + ".json"), result)
    return result


def read_results(directory, plan):
    results = {}
    jobs = {j["id"]: j for j in plan["jobs"]}
    for path in sorted((Path(directory) / "results").glob("*.json")):
        result = require_object(read_json(path), "result")
        job_id = result.get("job_id")
        if job_id not in jobs or path.stem != job_id:
            raise ValueError(f"Unexpected result file {path.name}")
        results[job_id] = validate_result(result, jobs[job_id], plan)
    return results


def stop_process(process):
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    else:
        process.kill()
    process.wait()


def execute_jobs(directory, adapter_path, *, allow_execution=False, max_jobs=None):
    """Explicit external adapter only. No providers, installed-host discovery or retries."""
    if not allow_execution:
        raise ValueError("Execution requires --allow-execution; it may consume account usage")
    positive_int(max_jobs, "max_jobs")
    plan = load_plan(directory)
    existing = read_results(directory, plan)
    adapter = require_object(read_json(adapter_path), "adapter")
    adapter_hash = digest(adapter)
    if any(r.get("provenance", {}).get("adapter_sha256") not in (None, adapter_hash)
           for r in existing.values()):
        raise ValueError("Adapter configuration changed; use a new experiment directory")
    argv = adapter.get("argv")
    if not isinstance(argv, list) or not argv or not all(isinstance(s, str) and s for s in argv):
        raise ValueError("adapter.argv must be a nonempty array of literal arguments")
    if not Path(argv[0]).is_absolute():
        raise ValueError("adapter executable must be an absolute path")
    timeout = positive_int(adapter.get("timeout_seconds", 180), "timeout_seconds")
    output_limit = positive_int(adapter.get("max_output_bytes", 2_000_000), "max_output_bytes")
    pending = [j for j in plan["jobs"] if j["id"] not in existing][:max_jobs]
    for job in pending:
        started = time.monotonic()
        result = {"schema_version": VERSION, "plan_id": plan["plan_id"], "job_id": job["id"],
                  "request_sha256": job["request_sha256"], "status": "failed"}
        with tempfile.TemporaryDirectory(prefix="atr-eval-") as temporary:
            with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
                process = None
                try:
                    # The adapter receives a request, never the suite or its expected answers.
                    process = subprocess.Popen(argv, cwd=temporary, stdin=subprocess.PIPE,
                        stdout=stdout, stderr=stderr, start_new_session=(os.name == "posix"))
                    process.communicate(json.dumps(job["request"], ensure_ascii=False).encode(), timeout=timeout)
                    if process.returncode:
                        result.update(status="failed", error_type="adapter_exit",
                                      exit_code=process.returncode)
                    else:
                        stdout.seek(0)
                        raw = stdout.read(output_limit + 1)
                        if len(raw) > output_limit:
                            raise ValueError("Adapter output exceeded limit")
                        parsed = parse_json(raw)
                        validate_result(parsed, job, plan)
                        result = parsed
                except subprocess.TimeoutExpired:
                    stop_process(process)
                    result.update(status="blocked", error_type="timeout")
                except (OSError, ValueError, TypeError, KeyError) as error:
                    result.update(status="failed", error_type=type(error).__name__)
                except BaseException as error:
                    if process is not None:
                        stop_process(process)
                    # Preserve an interrupted attempt so resume cannot silently resubmit
                    # a remote job whose billing/cancellation state may be unknown.
                    result.update(status="blocked", error_type=type(error).__name__)
                    result["metrics"] = {"elapsed_seconds": round(time.monotonic() - started, 6)}
                    result["provenance"] = {"adapter_sha256": adapter_hash, "collected_at": now(),
                                            "execution_scope": "interrupted_attempt"}
                    write_json(Path(directory) / "results" / (job["id"] + ".json"), result)
                    raise
        # Includes routing and adapter setup; provider timing can stay in provenance.
        provenance = result.setdefault("provenance", {})
        if result.get("metrics", {}).get("elapsed_seconds") is not None:
            provenance["adapter_reported_elapsed_seconds"] = result["metrics"]["elapsed_seconds"]
        result.setdefault("metrics", {})["elapsed_seconds"] = round(time.monotonic() - started, 6)
        provenance.update(adapter_sha256=adapter_hash, collected_at=now())
        write_json(Path(directory) / "results" / (job["id"] + ".json"), result)
        yield result
        # Do not burn the remaining invocation budget on a broken adapter.
        if result["status"] != "completed":
            break


def lookup(value, path):
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return MISSING
        value = value[part]
    return value


def evaluate_check(rule, result):
    actual = lookup(result, rule["path"])
    if rule["op"] == "absent":
        return "pass" if actual is MISSING else "fail"
    if actual is MISSING or actual is None:
        return "unknown"
    expected = rule["value"]
    if rule["op"] == "eq":
        passed = type(actual) is type(expected) and actual == expected
    elif rule["op"] == "in":
        passed = any(type(actual) is type(item) and actual == item for item in expected)
    else:
        passed = isinstance(actual, str) and expected in actual
    return "pass" if passed else "fail"


def interval(successes, count):
    """Descriptive Wilson 95% interval; repeats of one case are not independent tasks."""
    if not count:
        return None
    z = 1.959963984540054
    p = successes / count
    denominator = 1 + z * z / count
    midpoint = (p + z * z / (2 * count)) / denominator
    margin = z * math.sqrt(p * (1 - p) / count + z * z / (4 * count * count)) / denominator
    return [max(0, midpoint - margin), min(1, midpoint + margin)]


def measurements(values, total):
    return {"observed": len(values), "missing": total - len(values),
            "mean": statistics.mean(values) if values else None,
            "median": statistics.median(values) if values else None,
            "sum_observed": sum(values) if values else None}


def score(directory):
    plan = load_plan(directory)
    results = read_results(directory, plan)
    cases = {c["id"]: c for c in plan["cases"]}
    rows = []
    for job in plan["jobs"]:
        result = results.get(job["id"])
        case = cases[job["case_id"]]
        row = {"job_id": job["id"], "case_id": case["id"], "strategy_id": job["strategy_id"],
               "track": case["track"], "repeat": job["repeat"],
               "status": result["status"] if result else "not_run", "checks": []}
        for rule in case.get("checks", []):
            if job["strategy_id"] not in rule.get("strategies", [job["strategy_id"]]):
                continue
            status = (evaluate_check(rule, result) if result and result["status"] == "completed" else "unknown")
            row["checks"].append({"id": rule["id"], "critical": rule.get("critical", False), "status": status})
        states = [c["status"] for c in row["checks"]]
        row["contract_status"] = ("fail" if "fail" in states else "unknown" if not states or "unknown" in states else "pass")
        row["task_success"] = result.get("observations", {}).get("task_success") if result else None
        row["metrics"] = result.get("metrics", {}) if result else {}
        row["provenance"] = result.get("provenance", {}) if result else {}
        rows.append(row)
    groups = defaultdict(list)
    for row in rows:
        groups[(row["track"], row["strategy_id"])].append(row)
    summaries = []
    for (track, strategy), group in sorted(groups.items()):
        states = Counter(r["status"] for r in group)
        checks = Counter(r["contract_status"] for r in group)
        observed_success = [r["task_success"] for r in group if r["task_success"] is not None]
        summaries.append({"track": track, "strategy_id": strategy, "planned": len(group),
            "status_counts": dict(states), "contract_counts": dict(checks),
            "execution_scopes": dict(Counter(r["provenance"].get("execution_scope") or "unknown" for r in group)),
            "observed_configurations": dict(Counter(
                (r["provenance"].get("model") or "unknown") + " / " +
                (r["provenance"].get("reasoning_effort") or "unknown") for r in group)),
            "critical_failures": sum(c["critical"] and c["status"] == "fail" for r in group for c in r["checks"]),
            "critical_unknown": sum(c["critical"] and c["status"] == "unknown" for r in group for c in r["checks"]),
            "task_success": {"observed": len(observed_success), "missing": len(group) - len(observed_success),
                "successes": sum(observed_success),
                "rate_observed": statistics.mean(observed_success) if observed_success else None,
                "wilson_95_descriptive": interval(sum(observed_success), len(observed_success))},
            "metrics": {m: measurements([r["metrics"][m] for r in group if r["metrics"].get(m) is not None], len(group))
                        for m in METRICS}})
    comparisons = []
    strategy_ids = [s["id"] for s in plan["strategies"]]
    by_key = {(r["case_id"], r["repeat"], r["strategy_id"]): r for r in rows}
    for index, left in enumerate(strategy_ids):
        for right in strategy_ids[index + 1:]:
            for track in sorted({r["track"] for r in rows}):
                matched = [(r, by_key[(r["case_id"], r["repeat"], right)]) for r in rows
                           if r["strategy_id"] == left and r["track"] == track]
                both_success = [(a["task_success"], b["task_success"]) for a, b in matched
                                if a["task_success"] is not None and b["task_success"] is not None]
                comparisons.append({"track": track, "left": left, "right": right,
                    "planned_pairs": len(matched), "observed_success_pairs": len(both_success),
                    "success_rate_delta_left_minus_right": statistics.mean([int(a) - int(b) for a, b in both_success]) if both_success else None,
                    "metric_deltas_left_minus_right": {m: measurements([
                        a["metrics"][m] - b["metrics"][m] for a, b in matched
                        if a["metrics"].get(m) is not None and b["metrics"].get(m) is not None], len(matched)) for m in METRICS}})
    return {"schema_version": VERSION, "plan_id": plan["plan_id"], "generated_at": now(),
            "result_sha256": {job_id: digest(result) for job_id, result in sorted(results.items())},
            "summaries": summaries, "paired_comparisons": comparisons, "jobs": rows,
            "limitations": ["Contract checks examine submitted structured fields, not verified host behavior.",
                "Task success is externally assessed and requires an evidence reference; references are not verified here.",
                "Missing observations remain unknown; completed is not synonymous with task success.",
                "Repeated cases are correlated; intervals are descriptive, not statistical significance or release certification.",
                "Metrics mix neither tracks nor currencies; adapter invocation caps are not token or money caps."]}


def blind_packet(directory, output, *, left, right, seed=0, mirror=False):
    if left == right:
        raise ValueError("Choose two distinct strategies")
    plan = load_plan(directory)
    strategy_ids = {s["id"] for s in plan["strategies"]}
    if not {left, right} <= strategy_ids:
        raise ValueError("Unknown review strategy")
    results = read_results(directory, plan)
    cases = {c["id"]: c for c in plan["cases"]}
    by_key = {(j["case_id"], j["repeat"], j["strategy_id"]): j for j in plan["jobs"]}
    rng = random.Random(seed)
    items, keys = [], []
    skipped = 0
    for case in plan["cases"]:
        for repeat in range(plan["repetitions"]):
            jobs = [by_key[(case["id"], repeat, s)] for s in (left, right)]
            pair = [results.get(j["id"]) for j in jobs]
            if not all(r and r["status"] == "completed" and r.get("response", "").strip() for r in pair):
                skipped += 1
                continue
            rng.shuffle(jobs)
            orientations = [jobs, list(reversed(jobs))] if mirror else [jobs]
            for order, oriented in enumerate(orientations):
                item_id = digest([plan["plan_id"], left, right, case["id"], repeat, seed, order])[:24]
                items.append({"id": item_id, "track": case["track"], "input": cases[case["id"]]["input"],
                    "A": results[oriented[0]["id"]]["response"], "B": results[oriented[1]["id"]]["response"]})
                keys.append({"id": item_id, "case_id": case["id"], "repeat": repeat,
                    "pair_id": digest([case["id"], repeat, left, right])[:24],
                    "A": {"strategy_id": oriented[0]["strategy_id"], "job_id": oriented[0]["id"]},
                    "B": {"strategy_id": oriented[1]["strategy_id"], "job_id": oriented[1]["id"]}})
    rng.shuffle(items)
    rubric = {"criteria": ["correctness", "instruction_following", "action_clarity"],
        "scores": "Each criterion: integer 0 (unacceptable) to 4 (fully meets requirements), or null if unassessable.",
        "winner": "A, B, tie, or unassessable. Judge correctness and requirements before style.",
        "bias_control": "Do not reward length alone. Do not infer model identity. Return a concise evidence-based reason.",
        "review_format": "One object per item and judge: id, judge_id, winner, scores {A:{criterion:score},B:{criterion:score}}, reason."}
    key = {"schema_version": VERSION, "plan_id": plan["plan_id"],
           "left": left, "right": right, "mirror": mirror, "skipped_pairs": skipped, "items": keys}
    packet = {"schema_version": VERSION, "rubric": rubric, "items": items,
              "key_binding_version": 2, "mapping_sha256": digest(key)}
    packet_id = digest(packet)
    packet["packet_id"] = packet_id
    key["packet_id"] = packet_id
    output = Path(output)
    if output.exists():
        raise ValueError("Choose a new blind-review directory")
    write_json(output / "review.json", packet)
    write_json(output / "private-key.json", key)
    return packet, key


def summarize_reviews(packet_path, key_path, reviews_path):
    packet, key, reviews = (require_object(read_json(path), label) for path, label in
                           ((packet_path, "packet"), (key_path, "key"), (reviews_path, "reviews")))
    for label, value in (("packet", packet), ("key", key), ("reviews", reviews)):
        require_schema(value, label)
    packet_id = packet.get("packet_id")
    if digest({k: v for k, v in packet.items() if k != "packet_id"}) != packet_id or key.get("packet_id") != packet_id:
        raise ValueError("Review packet/key mismatch")
    if reviews.get("packet_id") != packet_id:
        raise ValueError("Review input must identify the exact packet")
    if type(packet.get("key_binding_version")) is not int or packet["key_binding_version"] != 2:
        raise ValueError("Regenerate legacy review packets to bind the complete private key")
    if packet.get("mapping_sha256") != digest({k: v for k, v in key.items() if k != "packet_id"}):
        raise ValueError("Private review mapping changed")
    items = {i["id"]: i for i in packet["items"]}
    keys = {i["id"]: i for i in key["items"]}
    if set(items) != set(keys) or len(items) != len(packet["items"]) or len(keys) != len(key["items"]):
        raise ValueError("Review key has missing or extra items")
    if not isinstance(reviews.get("reviews"), list):
        raise ValueError("reviews must contain a list of review objects")
    criteria = packet["rubric"]["criteria"]
    seen, rows = set(), []
    for vote in reviews["reviews"]:
        require_object(vote, "review")
        item_id, judge = vote.get("id"), identifier(vote.get("judge_id"))
        if item_id not in items or (item_id, judge) in seen:
            raise ValueError("Unknown or duplicate review")
        seen.add((item_id, judge))
        winner = vote.get("winner")
        if winner not in ("A", "B", "tie", "unassessable"):
            raise ValueError("Unknown review winner")
        if not isinstance(vote.get("reason"), str) or not vote["reason"].strip():
            raise ValueError("Review needs an evidence-based reason")
        scores = require_object(vote.get("scores"), "scores")
        for side in ("A", "B"):
            side_scores = require_object(scores.get(side), side)
            if set(side_scores) != set(criteria):
                raise ValueError("Each side needs every rubric criterion")
            if any(v is not None and (type(v) is not int or not 0 <= v <= 4) for v in side_scores.values()):
                raise ValueError("Scores must be integers 0..4 or null")
        mapping = keys[item_id]
        rows.append({**vote, "track": items[item_id]["track"], "pair_id": mapping["pair_id"],
            "winner_strategy": mapping[winner]["strategy_id"] if winner in ("A", "B") else winner,
            "character_counts": {s: len(items[item_id][s]) for s in ("A", "B")}})
    summaries = []
    for track in sorted({i["track"] for i in items.values()}):
        group = [r for r in rows if r["track"] == track]
        grouped = defaultdict(list)
        for row in group:
            grouped[(row["judge_id"], row["pair_id"])].append(row)
        consistent, inconsistent, incomplete = [], 0, 0
        for votes in grouped.values():
            if key["mirror"] and len(votes) != 2:
                incomplete += 1
            elif len({v["winner_strategy"] for v in votes}) != 1:
                inconsistent += 1
            else:
                consistent.append(votes[0])
        # Average the two orientations before aggregating scores; never inflate sample count.
        criterion_values = defaultdict(list)
        for votes in grouped.values():
            if key["mirror"] and len(votes) != 2:
                continue
            for strategy in (key["left"], key["right"]):
                for criterion in criteria:
                    values = [v["scores"][side][criterion] for v in votes for side in ("A", "B")
                              if keys[v["id"]][side]["strategy_id"] == strategy]
                    if values and all(v is not None for v in values):
                        criterion_values[(strategy, criterion)].append(statistics.mean(values))
        # Agreement is computed per independent pair, after excluding inconsistent mirrored votes.
        by_pair = defaultdict(list)
        for vote in consistent:
            if vote["winner_strategy"] != "unassessable":
                by_pair[vote["pair_id"]].append(vote["winner_strategy"])
        agreements = [a == b for votes in by_pair.values() for index, a in enumerate(votes) for b in votes[index + 1:]]
        decisive = [r for r in group if r["winner"] in ("A", "B")]
        unequal = [r for r in decisive if r["character_counts"]["A"] != r["character_counts"]["B"]]
        summaries.append({"track": track, "review_rows": len(group),
            "criterion_scores": {strategy: {criterion: measurements(
                criterion_values[(strategy, criterion)], len(grouped)) for criterion in criteria}
                for strategy in (key["left"], key["right"])},
            "consistent_pair_votes": dict(Counter(r["winner_strategy"] for r in consistent)),
            "order_inconsistent_pair_votes": inconsistent, "incomplete_mirrored_pair_votes": incomplete,
            "judge_agreement": {"comparisons": len(agreements), "rate": statistics.mean(agreements) if agreements else None},
            "A_selection_rate_descriptive": statistics.mean(r["winner"] == "A" for r in decisive) if decisive else None,
            "longer_answer_selection_rate_descriptive": statistics.mean(
                r["character_counts"][r["winner"]] == max(r["character_counts"].values()) for r in unequal) if unequal else None})
    return {"schema_version": VERSION, "packet_id": packet_id, "plan_id": key["plan_id"],
        "items": len(items), "items_without_review": len(set(items) - {r["id"] for r in rows}),
        "reviewer_coverage": {judge: {"reviewed": sum(r["judge_id"] == judge for r in rows),
            "missing": len(items) - sum(r["judge_id"] == judge for r in rows)} for judge in sorted({r["judge_id"] for r in rows})},
        "summaries": summaries, "reviews": rows,
        "limitations": ["Preference is not objective correctness. Order/length diagnostics are not causal bias estimates.",
            "Mirrored answers are the same experiment, not independent extra wins. Judges also share the same task sample.",
            "Responses may disclose their strategy; inspect/redact before distributing a new versioned packet."]}


def markdown_report(report):
    lines = ["# Routing evaluation report", "", f"Plan: `{report['plan_id']}`", "",
             "Adapter completion, contract checks and task success are separate observations.", "",
             "| Track | Strategy | Planned | Completed | Contract pass / fail / unknown | Task success / observed |",
             "| --- | --- | ---: | ---: | --- | --- |"]
    for summary in report["summaries"]:
        counts, success = summary["contract_counts"], summary["task_success"]
        lines.append(f"| {summary['track']} | {summary['strategy_id']} | {summary['planned']} | "
                     f"{summary['status_counts'].get('completed', 0)} | "
                     f"{counts.get('pass', 0)} / {counts.get('fail', 0)} / {counts.get('unknown', 0)} | "
                     f"{success['successes']} / {success['observed']} |")
    lines += ["", "## Paired comparisons", "", "Deltas are left minus right using only matched observations.", ""]
    for comparison in report["paired_comparisons"]:
        delta = comparison["success_rate_delta_left_minus_right"]
        lines += [f"- {comparison['track']}: {comparison['left']} vs {comparison['right']}: "
                  f"success delta {delta if delta is not None else 'unknown'} "
                  f"({comparison['observed_success_pairs']}/{comparison['planned_pairs']} observed pairs)."]
        for metric in ("elapsed_seconds", "cost_usd", "retries", "human_interventions"):
            data = comparison["metric_deltas_left_minus_right"][metric]
            lines.append(f"  - {metric}: {data['mean'] if data['mean'] is not None else 'unknown'} "
                         f"({data['observed']} observed, {data['missing']} missing).")
    lines += ["", "## Limits", ""] + [f"- {note}" for note in report["limitations"]]
    return "\n".join(lines) + "\n"
