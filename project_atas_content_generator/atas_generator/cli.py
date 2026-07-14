from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .generator import export_api_seed, generate_thread, merge_mailbox
from .io import read_json
from .prompts import build_thread_prompt
from .providers import MockProvider, OpenAICompatibleProvider
from .scenario import Scenario
from .validation import validate_generation


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="atas-generate", description="Project ATaS mailbox authoring pipeline")
    p.add_argument("--scenario", type=Path, default=Path("scenario"), help="Scenario data directory")
    p.add_argument("--generated", type=Path, default=Path("generated"), help="Generated content directory")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("list-threads")

    prompt_cmd = sub.add_parser("prompt")
    prompt_cmd.add_argument("thread_id")
    prompt_cmd.add_argument("--output", type=Path)

    gen = sub.add_parser("generate")
    gen.add_argument("thread_id")
    gen.add_argument("--provider", choices=["mock", "openai-compatible"], default="openai-compatible")

    validate = sub.add_parser("validate")
    validate.add_argument("thread_id")

    status = sub.add_parser("status")

    merge = sub.add_parser("merge")
    merge.add_argument("--output", type=Path, default=Path("generated/emails.json"))
    merge.add_argument("--allow-incomplete", action="store_true")

    api_seed = sub.add_parser("export-api-seed")
    api_seed.add_argument("--output", type=Path, default=Path("../fake-email-api/data/atas_seed_emails.json"))
    api_seed.add_argument("--allow-incomplete", action="store_true")
    api_seed.add_argument("--thread-id", action="append", help="Export only this reviewed thread; repeat as needed")
    return p


def main() -> None:
    args = parser().parse_args()
    scenario = Scenario.load(args.scenario)

    if args.command == "list-threads":
        for thread in scenario.threads:
            print(f"{thread['thread_id']:10} {thread['email_count']:3}  {thread['importance']:8}  {thread['purpose']}")
        return

    if args.command == "prompt":
        text = build_thread_prompt(scenario, args.thread_id)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text)
        return

    if args.command == "generate":
        messages = scenario.thread_messages(args.thread_id)
        provider = MockProvider(messages) if args.provider == "mock" else OpenAICompatibleProvider.from_environment()
        path = generate_thread(scenario, args.thread_id, provider, args.generated)
        print(path)
        return

    if args.command == "validate":
        path = args.generated / "threads" / args.thread_id / "emails.json"
        if not path.exists():
            raise SystemExit(f"Not generated: {args.thread_id}")
        errors = validate_generation(scenario.thread_messages(args.thread_id), read_json(path))
        if errors:
            print("\n".join(f"ERROR: {error}" for error in errors))
            raise SystemExit(1)
        print(f"{args.thread_id}: valid")
        return

    if args.command == "status":
        for thread in scenario.threads:
            tid = thread["thread_id"]
            path = args.generated / "threads" / tid / "emails.json"
            state = "generated" if path.exists() else "pending"
            print(f"{tid:10} {state}")
        return

    if args.command == "merge":
        result = merge_mailbox(scenario, args.generated, args.output, args.allow_incomplete)
        print(json.dumps(result, indent=2))
        return

    if args.command == "export-api-seed":
        result = export_api_seed(scenario, args.generated, args.output, args.allow_incomplete, args.thread_id)
        print(json.dumps(result, indent=2))
        return


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
