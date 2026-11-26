"""Tests for bot.py. Run in this folder with:  python -m unittest -v

Slack and GitHub are replaced by fakes, so nothing is sent anywhere.
"""

import io
import json
import logging
import os
import time
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

import yaml

import bot

logging.disable(logging.CRITICAL)  # The error paths below log on purpose.

DIRECTIONS_FILE = Path(__file__).resolve().parent.parent / "data" / "research_directions.yaml"
DIRECTION_IDS = [d["id"] for d in yaml.safe_load(DIRECTIONS_FILE.read_text(encoding="utf-8"))["directions"]]


class Recorder:
    """Stands in for Slack's ack() and respond(): remembers how it was called."""

    def __init__(self):
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append(kwargs if kwargs else {"args": args})

    @property
    def last(self):
        return self.calls[-1]


class FakeWeb:
    """Stands in for urllib: serves the directions file, records GitHub calls."""

    def __init__(self, github_status=204):
        self.github_status = github_status
        self.github = []
        self.directions_fetches = 0

    def __call__(self, request, timeout=None):
        url = request if isinstance(request, str) else request.full_url
        if "raw.githubusercontent.com" in url:
            self.directions_fetches += 1
            return io.BytesIO(DIRECTIONS_FILE.read_bytes())
        self.github.append({"url": url, "body": json.loads(request.data), "headers": dict(request.header_items())})
        if self.github_status >= 400:
            raise urllib.error.HTTPError(url, self.github_status, "no", {}, io.BytesIO(b"no"))
        return io.BytesIO(b"")


def submission(entry, directions=("personal-health-agents",), abstract=None, where=None):
    return {
        "callback_id": "publication_submit",
        "private_metadata": json.dumps(where or {}),
        "state": {
            "values": {
                "entry": {"value": {"value": entry}},
                "directions": {"value": {"selected_options": [{"value": d} for d in directions]}},
                "abstract": {"value": {"value": abstract}},
            }
        },
    }


def press(action_id, user):
    action = {
        "action_id": action_id,
        "value": json.dumps({"pr": 77, "title": "A Paper", "requester": "UMEMBER", "reply_channel": "UMEMBER", "reply_ts": ""}),
    }
    body = {
        "user": {"id": user},
        "container": {"channel_id": "CADMINS", "message_ts": "111.222"},
        "message": {
            "text": "New publication request: A Paper",
            "blocks": [{"type": "header"}, {"type": "section"}, {"type": "actions", "elements": []}],
        },
    }
    return body, action


class BotTest(unittest.TestCase):
    def setUp(self):
        self.web = FakeWeb()
        self.client = mock.Mock()
        self.ack = Recorder()
        self.respond = Recorder()
        bot._directions.update(at=0.0, list=None)
        for patch in (
            mock.patch.object(bot.urllib.request, "urlopen", self.web),
            mock.patch.dict(os.environ, {"GITHUB_TOKEN": "github-test", "ADMIN_SLACK_IDS": "UADMIN1, UADMIN2"}),
        ):
            patch.start()
            self.addCleanup(patch.stop)

    # ------------------------------------------------------------ the form

    def test_add_paper_opens_the_form_with_every_direction(self):
        bot.on_command(self.ack, {"trigger_id": "TRIGGER", "user_id": "UMEMBER"}, self.client, self.respond)
        self.assertEqual(len(self.ack.calls), 1)
        self.assertEqual(self.respond.calls, [])
        sent = self.client.views_open.call_args.kwargs
        self.assertEqual(sent["trigger_id"], "TRIGGER")
        self.assertEqual(json.loads(sent["view"]["private_metadata"]), {"reply_channel": "UMEMBER"})
        options = sent["view"]["blocks"][2]["element"]["options"]
        self.assertEqual([o["value"] for o in options], DIRECTION_IDS)
        self.assertEqual(options[0]["text"]["text"], "Personal Health Agents")
        self.assertTrue(all(len(o["text"]["text"]) <= 75 for o in options))

    def test_directions_are_fetched_once_within_five_minutes(self):
        bot.load_directions()
        bot.load_directions()
        self.assertEqual(self.web.directions_fetches, 1)
        bot._directions["at"] = time.time() - 6 * 60
        bot.load_directions()
        self.assertEqual(self.web.directions_fetches, 2)

    def test_a_form_that_cannot_open_says_so(self):
        self.client.views_open.side_effect = RuntimeError("expired_trigger_id")
        bot.on_command(self.ack, {"trigger_id": "T", "user_id": "UMEMBER"}, self.client, self.respond)
        self.assertIn("expired_trigger_id", self.respond.last["text"])

    def test_a_mention_gets_a_button_in_the_thread(self):
        bot.on_mention({"channel": "CLAB", "ts": "5.6", "user": "UMEMBER"}, self.client)
        sent = self.client.chat_postMessage.call_args.kwargs
        self.assertEqual((sent["channel"], sent["thread_ts"]), ("CLAB", "5.6"))
        button = sent["blocks"][1]["elements"][0]
        self.assertEqual(button["action_id"], "publication_open")
        self.assertEqual(json.loads(button["value"]), {"reply_channel": "CLAB", "reply_ts": "5.6"})

    def test_the_button_opens_the_form_and_remembers_the_thread(self):
        action = {"value": json.dumps({"reply_channel": "CLAB", "reply_ts": "5.6"})}
        bot.on_open(self.ack, {"trigger_id": "T2"}, action, self.client, self.respond)
        sent = self.client.views_open.call_args.kwargs
        self.assertEqual(json.loads(sent["view"]["private_metadata"]), {"reply_channel": "CLAB", "reply_ts": "5.6"})

    # ------------------------------------------------------- sending a paper

    def test_sending_the_form_starts_the_add_workflow_and_confirms_in_the_thread(self):
        view = submission(
            "@article{x, title={T}}",
            directions=("adaptive-interventions", "beyond-health"),
            abstract="Some abstract.",
            where={"reply_channel": "CLAB", "reply_ts": "5.6"},
        )
        bot.on_submit(self.ack, {"user": {"id": "UMEMBER"}}, view, self.client)
        self.assertEqual(self.ack.calls, [{"args": ()}])
        (call,) = self.web.github
        self.assertTrue(call["url"].endswith("/repos/sea-lab-space/sea-lab-space.github.io/actions/workflows/slack-add-publication.yml/dispatches"))
        self.assertEqual(call["headers"]["Authorization"], "Bearer github-test")
        self.assertEqual(call["body"]["ref"], "main")
        inputs = call["body"]["inputs"]
        self.assertEqual(inputs["entry"], "@article{x, title={T}}")
        self.assertEqual(inputs["directions"], "adaptive-interventions,beyond-health")
        self.assertEqual(inputs["abstract"], "Some abstract.")
        self.assertEqual(json.loads(inputs["context"]), {"requester": "UMEMBER", "reply_channel": "CLAB", "reply_ts": "5.6"})
        sent = self.client.chat_postMessage.call_args.kwargs
        self.assertEqual((sent["channel"], sent["thread_ts"]), ("CLAB", "5.6"))

    def test_a_doi_is_accepted_and_from_add_paper_the_confirmation_is_a_direct_message(self):
        view = submission("https://doi.org/10.1145/3613904.3642000", where={"reply_channel": "UMEMBER"})
        bot.on_submit(self.ack, {"user": {"id": "UMEMBER"}}, view, self.client)
        self.assertNotIn("abstract", self.web.github[0]["body"]["inputs"])
        sent = self.client.chat_postMessage.call_args.kwargs
        self.assertEqual(sent["channel"], "UMEMBER")
        self.assertNotIn("thread_ts", sent)

    def test_bibtex_pasted_as_a_code_block_and_an_arxiv_link_are_accepted(self):
        for entry in ("```@article{x, title={T}}```", "arxiv.org/abs/2605.21295"):
            self.web.github.clear()
            bot.on_submit(self.ack, {"user": {"id": "UMEMBER"}}, submission(entry), self.client)
            self.assertEqual(len(self.web.github), 1, entry)

    def test_text_that_is_neither_bibtex_nor_a_doi_is_sent_back_with_an_error(self):
        bot.on_submit(self.ack, {"user": {"id": "UMEMBER"}}, submission("my new CHI paper!"), self.client)
        self.assertEqual(self.ack.last["response_action"], "errors")
        self.assertIn("entry", self.ack.last["errors"])
        self.assertEqual(self.web.github, [])
        self.client.chat_postMessage.assert_not_called()

    def test_when_github_refuses_the_token_the_form_says_so(self):
        self.web.github_status = 401
        bot.on_submit(self.ack, {"user": {"id": "UMEMBER"}}, submission("@article{x, title={T}}"), self.client)
        self.assertIn("token", self.ack.last["errors"]["entry"])
        self.client.chat_postMessage.assert_not_called()

    # ------------------------------------------------- approve and decline

    def test_someone_who_is_not_an_admin_cannot_approve(self):
        body, action = press("publication_approve", "UMEMBER")
        bot.on_decision(self.ack, body, action, self.respond)
        self.assertEqual(self.web.github, [])
        self.assertEqual(self.respond.last["response_type"], "ephemeral")
        self.assertIs(self.respond.last["replace_original"], False)
        self.assertIn("<@UADMIN1>, <@UADMIN2>", self.respond.last["text"])

    def test_an_admins_approval_starts_the_decision_workflow_and_removes_the_buttons(self):
        body, action = press("publication_approve", "UADMIN2")
        bot.on_decision(self.ack, body, action, self.respond)
        (call,) = self.web.github
        self.assertIn("/slack-publication-decision.yml/dispatches", call["url"])
        inputs = call["body"]["inputs"]
        self.assertEqual((inputs["pr_number"], inputs["decision"]), ("77", "approve"))
        self.assertEqual(
            json.loads(inputs["context"]),
            {
                "title": "A Paper",
                "requester": "UMEMBER",
                "reply_channel": "UMEMBER",
                "reply_ts": "",
                "actor": "UADMIN2",
                "admin_channel": "CADMINS",
                "admin_ts": "111.222",
            },
        )
        update = self.respond.last
        self.assertIs(update["replace_original"], True)
        self.assertNotIn("actions", [b["type"] for b in update["blocks"]])
        self.assertIn("<@UADMIN2> approved", update["blocks"][-1]["elements"][0]["text"])

    def test_an_admins_decline_is_passed_on_as_a_decline(self):
        body, action = press("publication_decline", "UADMIN1")
        bot.on_decision(self.ack, body, action, self.respond)
        self.assertEqual(self.web.github[0]["body"]["inputs"]["decision"], "decline")
        self.assertIn("declined", self.respond.last["blocks"][-1]["elements"][0]["text"])

    def test_when_the_decision_cannot_start_the_buttons_stay_and_the_admin_is_told(self):
        self.web.github_status = 500
        body, action = press("publication_approve", "UADMIN1")
        bot.on_decision(self.ack, body, action, self.respond)
        self.assertIs(self.respond.last["replace_original"], False)
        self.assertIn("error 500", self.respond.last["text"])

    # ------------------------------------------------------------ settings

    def test_env_file_is_read_without_overriding_the_environment(self):
        path = Path(self.id() + ".env")
        self.addCleanup(path.unlink)
        path.write_text("# comment\nGITHUB_TOKEN=from-file\nSLACK_APP_TOKEN = 'xapp-from-file'\n", encoding="utf-8")
        with mock.patch.dict(os.environ):
            os.environ.pop("SLACK_APP_TOKEN", None)
            bot.load_env(path)
            self.assertEqual(os.environ["GITHUB_TOKEN"], "github-test")
            self.assertEqual(os.environ["SLACK_APP_TOKEN"], "xapp-from-file")


class RoutingTest(unittest.TestCase):
    """Each kind of Slack request reaches a handler, through Slack's own library."""

    def test_every_request_the_bot_expects_has_a_handler(self):
        from slack_bolt import BoltRequest
        from slack_sdk import WebClient

        handled = []

        def stub(name):
            def handler(ack):
                handled.append(name)
                ack()
            return handler

        names = ("on_command", "on_open", "on_submit", "on_decision", "on_view_changes")
        # What Slack answers to "who am I?", which the library asks first.
        identity = mock.MagicMock(headers={})
        identity.get = {"ok": True, "team_id": "T1", "user_id": "UBOT", "bot_id": "BBOT"}.get
        with mock.patch.multiple(bot, **{name: stub(name) for name in names}), \
                mock.patch.object(WebClient, "auth_test", return_value=identity), \
                mock.patch.dict(os.environ, {"SLACK_BOT_TOKEN": "xoxb-test"}):
            app = bot.build_app(token_verification_enabled=False)
            requests = [
                {"command": "/add-paper", "trigger_id": "T", "user_id": "U", "team_id": "T1"},
                {"type": "view_submission", "team": {"id": "T1"}, "user": {"id": "U"}, "view": {"type": "modal", "callback_id": "publication_submit"}},
            ] + [
                {"type": "block_actions", "team": {"id": "T1"}, "user": {"id": "U"}, "actions": [{"type": "button", "action_id": action_id}]}
                for action_id in ("publication_open", "publication_approve", "publication_decline", "publication_view")
            ]
            for body in requests:
                response = app.dispatch(BoltRequest(body=body, mode="socket_mode"))
                self.assertEqual(response.status, 200, body)
        self.assertEqual(handled, ["on_command", "on_submit", "on_open", "on_decision", "on_decision", "on_view_changes"])


if __name__ == "__main__":
    unittest.main()
