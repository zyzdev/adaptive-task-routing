#!/usr/bin/env python3
"""Plan routing experiments, import results and score locally. No execution by default."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from routing_eval import (blind_packet, create_plan, execute_jobs, import_result,
                          markdown_report, score, summarize_reviews, write_json)


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan", help="Write a seeded experiment plan; never invokes adapters")
    plan.add_argument("--suite", type=Path, default=Path(__file__).resolve().parents[1] / "tests/routing-eval-cases.json")
    plan.add_argument("--output", type=Path, required=True)
    plan.add_argument("--repetitions", type=int, default=3)
    plan.add_argument("--seed", type=int, default=0)
    plan.add_argument("--split", choices=("development", "holdout", "all"), default="development")
    plan.add_argument("--case", action="append", dest="cases")
    plan.add_argument("--strategy", action="append", dest="strategies")
    plan.add_argument("--contract-root", type=Path, help="Hash the six canonical routing contract files")
    execute = commands.add_parser("run", help="Opt-in external adapter execution; MAY CONSUME ACCOUNT USAGE")
    execute.add_argument("--plan", type=Path, required=True)
    execute.add_argument("--adapter", type=Path, required=True)
    execute.add_argument("--allow-execution", action="store_true")
    execute.add_argument("--max-jobs", type=int, required=True,
                         help="Invocation cap for THIS command, not a token/money cap")
    ingest = commands.add_parser("import", help="Import one existing result; no inference")
    ingest.add_argument("--plan", type=Path, required=True)
    ingest.add_argument("--result", type=Path, required=True)
    evaluate = commands.add_parser("score", help="Score existing records; no inference")
    evaluate.add_argument("--plan", type=Path, required=True)
    evaluate.add_argument("--output", type=Path, required=True)
    evaluate.add_argument("--markdown", type=Path)
    blind = commands.add_parser("blind", help="Prepare randomized review packet and separate private key")
    blind.add_argument("--plan", type=Path, required=True)
    blind.add_argument("--left", required=True)
    blind.add_argument("--right", required=True)
    blind.add_argument("--seed", type=int, default=0)
    blind.add_argument("--mirror", action="store_true", help="Include swapped copies to measure order consistency")
    blind.add_argument("--output", type=Path, required=True)
    reviews = commands.add_parser("review-report", help="Aggregate previously collected human/LLM reviews")
    reviews.add_argument("--packet", type=Path, required=True)
    reviews.add_argument("--key", type=Path, required=True)
    reviews.add_argument("--reviews", type=Path, required=True)
    reviews.add_argument("--output", type=Path, required=True)
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "plan":
            result = create_plan(args.suite, args.output, repetitions=args.repetitions, seed=args.seed,
                                 split=args.split, cases=args.cases, strategies=args.strategies,
                                 contract_root=args.contract_root)
            print(f"Plan {result['plan_id']}: {len(result['jobs'])} jobs planned; none executed.")
        elif args.command == "run":
            for result in execute_jobs(args.plan, args.adapter, allow_execution=args.allow_execution,
                                       max_jobs=args.max_jobs):
                print(f"{result['job_id']}: {result['status']}", flush=True)
                if result["status"] != "completed":
                    return 1
        elif args.command == "import":
            result = import_result(args.plan, args.result)
            print(f"Imported {result['job_id']}: {result['status']}")
        elif args.command == "score":
            if args.markdown and (args.markdown.exists() or args.markdown.resolve() == args.output.resolve()):
                raise ValueError("Choose a new, distinct Markdown output path")
            result = score(args.plan)
            write_json(args.output, result)
            if args.markdown:
                args.markdown.parent.mkdir(parents=True, exist_ok=True)
                with args.markdown.open("x", encoding="utf-8") as stream:
                    stream.write(markdown_report(result))
            print(f"Scored {len(result['jobs'])} planned jobs; no model calls.")
        elif args.command == "blind":
            packet, key = blind_packet(args.plan, args.output, left=args.left, right=args.right,
                                      seed=args.seed, mirror=args.mirror)
            print(f"Prepared {len(packet['items'])} review items; {key['skipped_pairs']} incomplete pairs skipped.")
            print("Share review.json only. Keep private-key.json away from reviewers.")
        else:
            result = summarize_reviews(args.packet, args.key, args.reviews)
            write_json(args.output, result)
            print(f"Aggregated {len(result['reviews'])} existing reviews; no model calls.")
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
