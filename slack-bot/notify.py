#!/usr/bin/env python3
"""Post the Slack bot's messages from the two bot workflows.

  review   The pull request is open. Post the approval card (Approve and
           Decline buttons) in the admin channel and tell the requester.
  failed   The request could not be turned into a pull request. Tell the
           requester why.
  outcome  An admin pressed a button and the workflow has finished. Reply
           under the approval card and tell the requester.

Needs SLACK_BOT_TOKEN, and SLACK_ADMIN_CHANNEL for `review`. BOT_CONTEXT is
the JSON that slack-bot/bot.py sent along with the request: who asked and
where to reply. Only the Python standard library is used.
"""

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

PUBLICATION_PAGE = "https://sea-lab.space/publication/"
MAX_AUTHORS = 8


def slack(method, **payload):
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        sys.exit("SLACK_BOT_TOKEN is not set. See slack-bot/README.md.")
    request = urllib.request.Request(
        f"https://slack.com/api/{method}",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    if not result.get("ok"):
        sys.exit(f"Slack {method} failed: {result.get('error')}")
    return result


def esc(text):
    """Escape text for Slack's mrkdwn."""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, TypeError, ValueError):
        return {}


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8").strip()
    except (OSError, TypeError):
        return ""


def context():
    try:
        value = json.loads(os.environ.get("BOT_CONTEXT") or "{}")
    except ValueError:
        value = {}
    return value if isinstance(value, dict) else {}


def tell_requester(ctx, text):
    """Reply where the request came from: a thread, or a direct message."""
    channel = ctx.get("reply_channel") or ctx.get("requester")
    if not channel:
        print("No requester to tell (the workflow was started by hand):\n" + text)
        return
    message = {"channel": channel, "text": text, "unfurl_links": False}
    if ctx.get("reply_ts"):
        message["thread_ts"] = ctx["reply_ts"]
    slack("chat.postMessage", **message)


def review_blocks(summary, pr_number, pr_url, ctx):
    authors = summary.get("authors") or []
    shown = ", ".join(authors[:MAX_AUTHORS])
    if len(authors) > MAX_AUTHORS:
        shown += f", and {len(authors) - MAX_AUTHORS} more"
    title = esc(summary.get("title", ""))
    if summary.get("link"):
        title = f"<{summary['link']}|{title}>"
    venue = " · ".join(esc(p) for p in (summary.get("venue"), summary.get("date")) if p)
    requester = f"<@{ctx['requester']}>" if ctx.get("requester") else "someone on GitHub"

    notes = []
    if summary.get("looked_up_doi"):
        notes.append(f"Details were looked up from the DOI {esc(summary['looked_up_doi'])}.")
    if not summary.get("has_abstract"):
        notes.append("No abstract.")
    notes.append("Nothing is published until you approve.")

    # What the buttons carry back to the bot. Slack allows 2000 characters.
    value = json.dumps(
        {
            "pr": int(pr_number),
            "title": summary.get("title", "")[:150],
            "requester": ctx.get("requester", ""),
            "reply_channel": ctx.get("reply_channel", ""),
            "reply_ts": ctx.get("reply_ts", ""),
        }
    )

    def confirm(title_text, body, button):
        return {
            "title": {"type": "plain_text", "text": title_text},
            "text": {"type": "plain_text", "text": body},
            "confirm": {"type": "plain_text", "text": button},
            "deny": {"type": "plain_text", "text": "Cancel"},
        }

    return [
        {"type": "header", "text": {"type": "plain_text", "text": "New publication request"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*{title}*\n{esc(shown)}\n_{venue}_"}},
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": "*Research directions*\n" + esc(", ".join(summary.get("direction_titles") or []))},
                {"type": "mrkdwn", "text": f"*Requested by*\n{requester}"},
            ],
        },
        {"type": "context", "elements": [{"type": "mrkdwn", "text": " ".join(notes)}]},
        {
            "type": "actions",
            "block_id": "publication_decision",
            "elements": [
                {
                    "type": "button",
                    "action_id": "publication_approve",
                    "style": "primary",
                    "text": {"type": "plain_text", "text": "Approve and publish"},
                    "value": value,
                    "confirm": confirm("Publish this paper?", "It goes on the lab website in a few minutes.", "Publish"),
                },
                {
                    "type": "button",
                    "action_id": "publication_decline",
                    "style": "danger",
                    "text": {"type": "plain_text", "text": "Decline"},
                    "value": value,
                    "confirm": confirm("Decline this request?", "The pull request is closed and the requester is told.", "Decline"),
                },
                {
                    "type": "button",
                    "action_id": "publication_view",
                    "text": {"type": "plain_text", "text": "View changes"},
                    "url": f"{pr_url}/files",
                },
            ],
        },
    ]


def review(args):
    ctx = context()
    summary = read_json(args.summary)
    channel = os.environ.get("SLACK_ADMIN_CHANNEL")
    if not channel:
        sys.exit("SLACK_ADMIN_CHANNEL is not set. See slack-bot/README.md.")
    slack(
        "chat.postMessage",
        channel=channel,
        text=f"New publication request: {summary.get('title', '')}",
        blocks=review_blocks(summary, args.pr_number, args.pr_url, ctx),
        unfurl_links=False,
    )
    tell_requester(
        ctx,
        f"*{esc(summary.get('title', ''))}* is ready and waiting for a website "
        "admin to approve it. I will tell you here when they decide.",
    )


def failed(args):
    ctx = context()
    summary = read_json(args.summary)
    problem = read_text(args.problem)
    checks = read_text(args.checks)
    if summary.get("ok") is False:
        text = f"I could not add that paper. {esc(summary.get('error', ''))}"
    elif problem:
        text = f"I could not add that paper. {esc(problem)}"
    elif args.checks_outcome == "failure":
        tail = "\n".join(checks.splitlines()[-15:])
        text = (
            "I could not add that paper, because the site checks did not pass. "
            f"Please show this to a website admin:\n```{esc(tail)}```\n<{args.run_url}|Full log>"
        )
    else:
        text = (
            "Something went wrong on my side while adding that paper. Please "
            f"tell a website admin. <{args.run_url}|Log>"
        )
    tell_requester(ctx, text)


def outcome(args):
    ctx = context()
    title = esc(ctx.get("title") or "the paper")
    actor = f"<@{ctx['actor']}>" if ctx.get("actor") else "A website admin"
    detail = esc(read_text(args.problem)) or "See the log."
    pr = f"<{args.pr_url}|pull request>" if args.pr_url else "pull request"
    log = f"<{args.run_url}|Log>"

    if args.status == "live":
        admins = f":white_check_mark: Published. It is on the <{PUBLICATION_PAGE}|Publications page> now."
        requester = f":tada: *{title}* was approved and is on the <{PUBLICATION_PAGE}|Publications page> now."
    elif args.status == "declined":
        admins = f"Declined. The {pr} is closed."
        requester = f"{actor} declined *{title}*. Ask them what to change, then send it again."
    elif args.status == "deploy_failed":
        admins = (
            f":warning: The paper is merged, but the site did not deploy, so it is not live yet. {detail} {log}\n"
            "Fix the cause, then run *Deploy website to GitHub Pages* from the Actions tab."
        )
        requester = f"*{title}* was approved, but the site did not update. The admins have been told."
    else:
        admins = (
            f":warning: I could not finish this. {detail} {log}\n"
            f"Nothing changed on the site. You can still handle the {pr} on GitHub."
        )
        requester = f"{actor} answered your request for *{title}*, but I hit a problem. The admins have been told."

    if ctx.get("admin_channel") and ctx.get("admin_ts"):
        slack(
            "chat.postMessage",
            channel=ctx["admin_channel"],
            thread_ts=ctx["admin_ts"],
            text=admins,
            unfurl_links=False,
        )
    else:
        print(admins)
    # A second press on a card that was already handled is no news to the
    # requester, who has heard the first outcome.
    if "already handled" not in detail:
        tell_requester(ctx, requester)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)

    p = commands.add_parser("review")
    p.add_argument("--summary", required=True)
    p.add_argument("--pr-number", required=True)
    p.add_argument("--pr-url", required=True)
    p.set_defaults(run=review)

    p = commands.add_parser("failed")
    p.add_argument("--summary")
    p.add_argument("--problem")
    p.add_argument("--checks", help="what the site checks printed")
    p.add_argument("--checks-outcome", default="", help="'failure' when the site checks step failed")
    p.add_argument("--pr-url", default="")
    p.add_argument("--run-url", default="")
    p.set_defaults(run=failed)

    p = commands.add_parser("outcome")
    p.add_argument("--status", required=True, choices=["live", "declined", "deploy_failed", "failed"])
    p.add_argument("--problem")
    p.add_argument("--pr-url", default="")
    p.add_argument("--run-url", default="")
    p.set_defaults(run=outcome)

    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
