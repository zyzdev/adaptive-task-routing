"""Local subprocess fixture only. No provider SDK, credentials or model invocation."""
import hashlib
import json
from pathlib import Path
import sys
import time


def deny_external_work(event, args):
    if event.startswith(("socket.", "subprocess.")) or event in ("os.system", "os.exec", "os.posix_spawn"):
        raise RuntimeError("Fake adapter forbids network and child processes")


sys.addaudithook(deny_external_work)
request = json.load(sys.stdin)
mode = sys.argv[1] if len(sys.argv) > 1 else "success"
if mode == "timeout":
    time.sleep(30)
elif mode == "invalid":
    print("not JSON")
    sys.exit(0)
elif mode == "exit":
    sys.exit(7)
elif mode == "oversize":
    print("x" * 4096)
    sys.exit(0)

# Never read the plan or expected outcomes. These fabricated observations test the
# transport and statistics only; they do not evaluate routing or any real task.
result = {
    "schema_version": 1, "plan_id": request["plan_id"], "job_id": request["job_id"],
    "request_sha256": hashlib.sha256(json.dumps(
        request, ensure_ascii=False, sort_keys=True, allow_nan=False).encode()).hexdigest(),
    "status": "completed", "response": "Synthetic adapter output; not a model answer.",
    "decision": {"routing_triggered": False},
    "observations": {"mutations_occurred": False, "fixtures_unchanged": True},
    "metrics": {"input_tokens": None, "output_tokens": None},
    "provenance": {"execution_scope": "synthetic_harness_fixture", "billing_basis": "unknown",
                   "model": "none", "reasoning_effort": "none",
                   "workspace_empty": not any(Path.cwd().iterdir()),
                   "received_top_level_keys": sorted(request)},
}
if mode == "wrong_hash":
    result["request_sha256"] = "incorrect"
if mode == "blocked":
    result["status"] = "blocked"
print(json.dumps(result))
