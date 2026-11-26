#!/usr/bin/env python3
"""The Slack side of the lab's website bot. Runs on the lab server.

It holds no state and never touches the site itself. It keeps one connection
open to Slack (Socket Mode, so the server needs no public address), shows the
"Add a publication" form, and starts one of two GitHub Actions workflows in
the website repository:

    slack-add-publication.yml       a member sent a paper
    slack-publication-decision.yml  an admin pressed Approve or Decline

Those workflows do the work and post the results (slack-bot/notify.py).
Setup, settings and the whole flow: slack-bot/README.md.

Run it with:  python bot.py     (settings come from .env in this folder)
"""

import json
import logging
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ADD_WORKFLOW = "slack-add-publication.yml"
DECISION_WORKFLOW = "slack-publication-decision.yml"
DOI = re.compile(r"\b10\.\d{4,9}/\S+")
ARXIV = re.compile(r"arxiv(\.org/(abs|pdf)/|:)\s*\d{4}\.\d{4,5}", re.I)
REQUIRED = ("SLACK_BOT_TOKEN", "SLACK_APP_TOKEN", "GITHUB_TOKEN", "ADMIN_SLACK_IDS")
FIVE_MINUTES = 5 * 60

log = logging.getLogger("website-bot")


# --------------------------------------------------------------- settings

def load_env(path=None):
    """Read KEY=value lines from .env. Values already set in the environment win."""
    path = Path(path) if path else Path(__file__).with_name(".env")
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def repo():
    return os.environ.get("GITHUB_REPO", "sea-lab-space/sea-lab-space.github.io")


def ref():
    return os.environ.get("GITHUB_REF", "main")


def admins():
    return [a for a in re.split(r"[\s,]+", os.environ.get("ADMIN_SLACK_IDS", "")) if a]


def parse(text):
    try:
        value = json.loads(text or "{}")
    except ValueError:
        return {}
    return value if isinstance(value, dict) else {}


# --------------------------------------------------------------- handlers

def on_command(ack, body, client, respond):
    """/add-paper: open the form. Updates go to the person as a direct message."""
    ack()
    problem = open_form(client, body["trigger_id"], {"reply_channel": body["user_id"]})
    if problem:
        respond(text=problem, response_type="ephemeral")


def on_mention(event, client):
    """"@bot ..." in a channel: reply in the thread with a button that opens
    the form. Slack only lets a form open from a button or a slash command."""
    thread = event.get("thread_ts") or event["ts"]
    text = "Have a new paper for the lab website? Press the button and paste its BibTeX or DOI."
    client.chat_postMessage(
        channel=event["channel"],
        thread_ts=thread,
        text=text,
        blocks=[
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "action_id": "publication_open",
                        "style": "primary",
                        "text": {"type": "plain_text", "text": "Add a publication"},
                        "value": json.dumps({"reply_channel": event["channel"], "reply_ts": thread}),
                    }
                ],
            },
        ],
    )


def on_open(ack, body, action, client, respond):
    """The button from on_mention."""
    ack()
    problem = open_form(client, body["trigger_id"], parse(action.get("value")))
    if problem:
        respond(text=problem, response_type="ephemeral", replace_original=False)


def on_submit(ack, body, view, client):
    """A member pressed "Send for approval"."""
    values = view["state"]["values"]
    entry = (values["entry"]["value"].get("value") or "").strip()
    directions = [o["value"] for o in values["directions"]["value"].get("selected_options") or []]
    abstract = (values["abstract"]["value"].get("value") or "").strip()
    where = parse(view.get("private_metadata"))
    user = body["user"]["id"]

    unwrapped = entry.strip("`").strip()
    is_bibtex = unwrapped.startswith("@") and "{" in unwrapped
    if not (is_bibtex or DOI.search(entry) or ARXIV.search(entry)):
        ack(
            response_action="errors",
            errors={"entry": "Paste a BibTeX entry (it starts with @), a DOI such as 10.1145/3613904.3642000, or an arXiv link."},
        )
        return

    inputs = {
        "entry": entry,
        "directions": ",".join(directions),
        "context": json.dumps(
            {
                "requester": user,
                "reply_channel": where.get("reply_channel") or user,
                "reply_ts": where.get("reply_ts") or "",
            }
        ),
    }
    if abstract:
        inputs["abstract"] = abstract
    problem = start_workflow(ADD_WORKFLOW, inputs)
    if problem:
        ack(response_action="errors", errors={"entry": problem})
        return

    ack()  # An empty answer closes the form.
    message = {
        "channel": where.get("reply_channel") or user,
        "text": f"Got it, <@{user}>. I am preparing the paper and will ask the website admins to approve it. That takes about a minute.",
    }
    if where.get("reply_ts"):
        message["thread_ts"] = where["reply_ts"]
    client.chat_postMessage(**message)


def on_decision(ack, body, action, respond):
    """Someone pressed Approve or Decline on a request card."""
    ack()
    user = body["user"]["id"]
    if user not in admins():
        who = ", ".join(f"<@{a}>" for a in admins()) or "nobody yet (ADMIN_SLACK_IDS is empty)"
        respond(
            text=f"Only website admins can approve or decline a publication. The admins are {who}.",
            response_type="ephemeral",
            replace_original=False,
        )
        return

    request = parse(action.get("value"))
    approve = action["action_id"] == "publication_approve"
    container = body.get("container") or {}
    problem = start_workflow(
        DECISION_WORKFLOW,
        {
            "pr_number": str(request.get("pr") or ""),
            "decision": "approve" if approve else "decline",
            "context": json.dumps(
                {
                    "title": request.get("title", ""),
                    "requester": request.get("requester", ""),
                    "reply_channel": request.get("reply_channel", ""),
                    "reply_ts": request.get("reply_ts", ""),
                    "actor": user,
                    "admin_channel": container.get("channel_id", ""),
                    "admin_ts": container.get("message_ts", ""),
                }
            ),
        },
    )
    if problem:
        respond(text=problem, response_type="ephemeral", replace_original=False)
        return

    # Replace the buttons with who decided, so nobody presses them twice.
    if approve:
        note = f":hourglass_flowing_sand: <@{user}> approved this. Publishing takes about five minutes. I will reply here when it is live."
    else:
        note = f"<@{user}> declined this."
    message = body.get("message") or {}
    blocks = [b for b in message.get("blocks") or [] if b.get("type") != "actions"]
    blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text": note}]})
    respond(text=message.get("text") or note, blocks=blocks, replace_original=True)


def on_view_changes(ack):
    """"View changes" is a link. Slack still reports the press, and wants an answer."""
    ack()


# --------------------------------------------------------------- the form

def open_form(client, trigger_id, where):
    """Open the form. Returns None, or a sentence saying why it did not open."""
    try:
        directions = load_directions()
    except Exception:
        log.exception("Could not load the research directions")
        return "I could not load the research directions from GitHub. Try again in a minute."
    try:
        client.views_open(trigger_id=trigger_id, view=form(directions, where))
    except Exception as error:
        log.exception("Could not open the form")
        return f"I could not open the form ({error}). Try again."
    return None


def form(directions, where):
    return {
        "type": "modal",
        "callback_id": "publication_submit",
        "private_metadata": json.dumps(where or {}),
        "title": {"type": "plain_text", "text": "Add a publication"},
        "submit": {"type": "plain_text", "text": "Send for approval"},
        "close": {"type": "plain_text", "text": "Cancel"},
        "blocks": [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "A website admin approves the paper before it goes on the site."},
            },
            {
                "type": "input",
                "block_id": "entry",
                "label": {"type": "plain_text", "text": "BibTeX or DOI"},
                "hint": {
                    "type": "plain_text",
                    "text": "One paper: its BibTeX entry, a DOI, or an arXiv link. This box holds 3000 characters. If the BibTeX is longer, leave its abstract out and paste the abstract below.",
                },
                "element": {
                    "type": "plain_text_input",
                    "action_id": "value",
                    "multiline": True,
                    "max_length": 3000,
                    "placeholder": {"type": "plain_text", "text": "@inproceedings{...}  or  10.1145/3613904.3642000"},
                },
            },
            {
                "type": "input",
                "block_id": "directions",
                "label": {"type": "plain_text", "text": "Research directions"},
                "hint": {
                    "type": "plain_text",
                    "text": "Pick every direction that fits, the main one first. Use Beyond Health for work outside health.",
                },
                "element": {
                    "type": "multi_static_select",
                    "action_id": "value",
                    "placeholder": {"type": "plain_text", "text": "Choose one or more"},
                    "options": [
                        {"text": {"type": "plain_text", "text": d["title"][:75]}, "value": d["id"]}
                        for d in directions
                    ],
                },
            },
            {
                "type": "input",
                "block_id": "abstract",
                "optional": True,
                "label": {"type": "plain_text", "text": "Abstract"},
                "hint": {"type": "plain_text", "text": "Only needed when you sent a DOI, or BibTeX without an abstract."},
                "element": {"type": "plain_text_input", "action_id": "value", "multiline": True, "max_length": 3000},
            },
        ],
    }


# The form's choices come from data/research_directions.yaml on main, the
# same file the site and its checks use, so they can never drift apart. It is
# read from GitHub, so the server's copy of the repository can be out of date.
_directions = {"at": 0.0, "list": None}


def load_directions():
    if _directions["list"] and time.time() - _directions["at"] < FIVE_MINUTES:
        return _directions["list"]
    url = f"https://raw.githubusercontent.com/{repo()}/{ref()}/data/research_directions.yaml"
    with urllib.request.urlopen(url, timeout=10) as response:
        data = yaml.safe_load(response.read().decode("utf-8"))
    found = [{"id": d["id"], "title": str(d.get("title") or d["id"])} for d in data["directions"]]
    if not found:
        raise ValueError(f"No directions in {url}")
    _directions.update(at=time.time(), list=found)
    return found


# ----------------------------------------------------------------- GitHub

def start_workflow(workflow, inputs):
    """Start a workflow. Returns None, or a sentence saying why it did not start."""
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo()}/actions/workflows/{workflow}/dispatches",
        data=json.dumps({"ref": ref(), "inputs": inputs}).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN', '')}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "sea-lab-website-bot",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=10):
            return None
    except urllib.error.HTTPError as error:
        log.error("GitHub %s dispatch answered %s: %s", workflow, error.code, error.read()[:500])
        if error.code in (401, 403, 404):
            return (
                "GitHub turned the bot away, most likely because its access token "
                "expired. Please tell a website admin (see slack-bot/README.md)."
            )
        return f"GitHub could not start the job (error {error.code}). Please tell a website admin."
    except (urllib.error.URLError, TimeoutError):
        log.exception("Could not reach GitHub")
        return "I could not reach GitHub. Try again in a minute."


# ------------------------------------------------------------------- main

def build_app(**options):
    from slack_bolt import App

    app = App(token=os.environ.get("SLACK_BOT_TOKEN"), **options)
    app.command("/add-paper")(on_command)
    app.event("app_mention")(on_mention)
    app.action("publication_open")(on_open)
    app.view("publication_submit")(on_submit)
    app.action("publication_approve")(on_decision)
    app.action("publication_decline")(on_decision)
    app.action("publication_view")(on_view_changes)
    return app


def main():
    from slack_bolt.adapter.socket_mode import SocketModeHandler

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    load_env()
    missing = [name for name in REQUIRED if not os.environ.get(name)]
    if missing:
        sys.exit(f"Missing settings: {', '.join(missing)}. Put them in slack-bot/.env (see .env.example).")
    log.info("Starting for %s, admins: %s", repo(), ", ".join(admins()))
    # Reconnects by itself when the connection to Slack drops.
    SocketModeHandler(build_app(), os.environ["SLACK_APP_TOKEN"]).start()


if __name__ == "__main__":
    main()
