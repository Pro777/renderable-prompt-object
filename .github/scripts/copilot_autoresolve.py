#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from typing import Any

COPILOT_LOGIN = "copilot-pull-request-reviewer"


def _parse_ts(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def _run_json(cmd: list[str], stdin: str | None = None) -> dict[str, Any]:
    proc = subprocess.run(cmd, text=True, input=stdin, capture_output=True)
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        raise RuntimeError(stderr or f"command failed: {' '.join(cmd)}")
    return json.loads(proc.stdout)


def _gh_graphql(query: str, fields: dict[str, str], stdin_query: bool = False) -> dict[str, Any]:
    cmd = ["gh", "api", "graphql"]
    if stdin_query:
        cmd += ["-F", "query=@-"]
    else:
        cmd += ["-F", f"query={query}"]
    for k, v in fields.items():
        cmd += ["-F", f"{k}={v}"]
    return _run_json(cmd, stdin=query if stdin_query else None)


def _pr_meta(repo: str, number: int) -> tuple[set[str], dt.datetime]:
    payload = _run_json([
        "gh",
        "pr",
        "view",
        str(number),
        "--repo",
        repo,
        "--json",
        "files,commits",
    ])
    files = {f["path"] for f in payload.get("files", [])}
    commits = payload.get("commits", [])
    if not commits:
        return files, dt.datetime.now(dt.timezone.utc)
    head_ts = max(_parse_ts(c["committedDate"]) for c in commits)
    return files, head_ts


def _fetch_threads(owner: str, repo: str, number: int) -> list[dict[str, Any]]:
    query = """
query($owner:String!, $repo:String!, $number:Int!, $cursor:String) {
  repository(owner:$owner, name:$repo) {
    pullRequest(number:$number) {
      reviewThreads(first:100, after:$cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          comments(first:100) {
            nodes {
              author { login }
              createdAt
              body
            }
          }
        }
      }
    }
  }
}
""".strip()

    threads: list[dict[str, Any]] = []
    cursor: str | None = None
    while True:
        fields = {"owner": owner, "repo": repo, "number": str(number)}
        if cursor:
            fields["cursor"] = cursor
        payload = _gh_graphql(query, fields, stdin_query=True)
        data = payload["data"]["repository"]["pullRequest"]["reviewThreads"]
        nodes = data.get("nodes") or []
        threads.extend(nodes)
        if not data["pageInfo"]["hasNextPage"]:
            break
        cursor = data["pageInfo"]["endCursor"]

    return threads


def _resolve_thread(thread_id: str) -> bool:
    mutation = "mutation($id:ID!){ resolveReviewThread(input:{threadId:$id}) { thread { id isResolved } } }"
    try:
        _gh_graphql(mutation, {"id": thread_id})
        return True
    except RuntimeError as exc:
        msg = str(exc)
        if "Resource not accessible by integration" in msg:
            print(f"WARN: skipping thread {thread_id}: {msg}")
            return False
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--number", required=True, type=int)
    parser.add_argument("--fail-on-unresolved", action="store_true")
    args = parser.parse_args()

    gh_token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not gh_token:
        print("GH_TOKEN or GITHUB_TOKEN is required", file=sys.stderr)
        return 2

    full_repo = f"{args.owner}/{args.repo}"
    changed_files, head_ts = _pr_meta(full_repo, args.number)
    threads = _fetch_threads(args.owner, args.repo, args.number)

    resolved = 0
    skipped = 0
    unresolved = 0
    considered = 0

    for thread in threads:
        if thread.get("isResolved"):
            continue
        comments = (thread.get("comments") or {}).get("nodes") or []
        copilot_comments = [c for c in comments if (c.get("author") or {}).get("login") == COPILOT_LOGIN]
        if not copilot_comments:
            continue

        considered += 1
        latest_copilot_ts = max(_parse_ts(c["createdAt"]) for c in copilot_comments)
        path = thread.get("path")

        can_resolve = False
        if thread.get("isOutdated"):
            can_resolve = True
        elif path and path in changed_files and head_ts > latest_copilot_ts:
            can_resolve = True

        if can_resolve:
            if _resolve_thread(thread["id"]):
                resolved += 1
            else:
                skipped += 1
        else:
            unresolved += 1

    print(f"Copilot threads considered: {considered}")
    print(f"Resolved this run: {resolved}")
    print(f"Skipped due to token limits: {skipped}")
    print(f"Still unresolved: {unresolved}")

    if args.fail_on_unresolved and unresolved:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
