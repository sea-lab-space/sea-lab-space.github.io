# Slack bot for the lab website

Lab members send a new paper from Slack. A website admin approves it with a button, and it goes live. This page is for whoever sets the bot up or keeps it running. How to use it is in the main [README](../README.md#add-pub-slack).

## How it works

1. A member types `/add-paper`, or mentions the bot in a channel and presses its button. A form asks for the paper's BibTeX (or a DOI or arXiv link) and its research directions.
2. The bot starts the workflow **Slack bot - propose a publication**. It runs `scripts/add_publication.py`, runs the two site checks, and opens a pull request from a branch named `bot/publication-<folder>`.
3. The bot posts a card in the admins' channel with the paper's details and three buttons: Approve and publish, Decline, View changes.
4. When an admin presses Approve, the workflow **Slack bot - approve or decline a publication** merges the pull request into `main`, starts the deploy, waits for it, and replies under the card and to the requester. Decline closes the pull request.

Nothing is stored anywhere but GitHub and Slack. The pieces:

| File | Runs on | What it does |
|---|---|---|
| `slack-bot/bot.py` | The lab server | Stays connected to Slack, shows the form, checks the admin list, starts the workflows. |
| `.github/workflows/slack-add-publication.yml` | GitHub Actions | Builds the pull request and posts the approval card. |
| `.github/workflows/slack-publication-decision.yml` | GitHub Actions | Merges or closes the pull request, deploys, reports back. |
| `scripts/add_publication.py` | GitHub Actions, or your computer | Adds one paper to the bib and to `content/publication/`. |
| `slack-bot/notify.py` | GitHub Actions | Writes the bot's Slack messages. |
| `slack-bot/manifest.yaml` | | The Slack app's settings, for creating the app. |

`bot.py` connects out to Slack (Slack calls this Socket Mode). The server needs no public address and no open port. It only needs to reach `slack.com`, `api.github.com` and `raw.githubusercontent.com`.

## Set it up

You need:

- An account on the lab server, with Python 3.8 or newer and `git`. `sudo` makes step 7 simpler but is not required.
- Permission to add an app to the lab's Slack workspace. A workspace admin may have to approve it.
- Write access to this repository, and someone who can add a secret and a variable to it (step 6). If you don't see **Settings > Secrets and variables**, ask Orson.

The two workflows must be on `main` before the bot can start them, so merge this folder and the workflows first.

1. **Create the Slack app.** Go to https://api.slack.com/apps, choose **Create New App > From a manifest**, pick the lab workspace, and paste all of `manifest.yaml`. Then choose **Install to Workspace**.
2. **Copy two tokens from the Slack app's settings.**
   - **OAuth & Permissions > Bot User OAuth Token.** It starts with `xoxb-`.
   - **Basic Information > App-Level Tokens > Generate Token and Scopes.** Give it any name, add the scope `connections:write`, and generate. It starts with `xapp-`.
3. **Create a GitHub token that can only start workflows.** On GitHub, go to **Settings > Developer settings > Personal access tokens > Fine-grained tokens > Generate new token**.
   - Resource owner: `sea-lab-space`. If the organization isn't offered, an owner has to allow fine-grained tokens first.
   - Repository access: **Only select repositories**, then this repository.
   - Repository permissions: **Actions: Read and write**. Nothing else.
   - Note the expiry date. The bot stops working on that day. See [When the token expires](#token).
4. **Collect the admins' Slack member IDs.** Open each admin's Slack profile, press the three dots, and choose **Copy member ID**. An ID looks like `U01ABCDEF`.
5. **Choose the admins' channel.** Create or pick the channel where approval cards should appear. Anyone in it can see the cards, but only the admins from step 4 can press Approve or Decline. In that channel, type `/invite @SEA Lab Website`. Copy the channel's ID from the bottom of its **About** panel. It looks like `C01ABCDEF`.
6. **Tell the workflows about Slack.** In this repository on GitHub, under **Settings > Secrets and variables > Actions**:
   - a **secret** named `SLACK_BOT_TOKEN`, with the `xoxb-` token from step 2,
   - a **variable** named `SLACK_ADMIN_CHANNEL`, with the channel ID from step 5.

   Or from a terminal:
   ```bash
   gh secret set SLACK_BOT_TOKEN --repo sea-lab-space/sea-lab-space.github.io
   gh variable set SLACK_ADMIN_CHANNEL --repo sea-lab-space/sea-lab-space.github.io --body C01ABCDEF
   ```
7. **Start the bot on the server.**
   ```bash
   git clone https://github.com/sea-lab-space/sea-lab-space.github.io.git
   cd sea-lab-space.github.io/slack-bot
   python3 -m venv venv
   venv/bin/pip install -r requirements.txt
   cp .env.example .env
   chmod 600 .env
   ```
   Fill in `.env` with the two tokens from step 2, the token from step 3, and the IDs from step 4. Then run `venv/bin/python bot.py`. It should print `Starting for sea-lab-space/sea-lab-space.github.io` and then `Bolt app is running!`. Try it (next section), then stop it with Ctrl+C and make it permanent:
   - **With `sudo`:** open `sea-lab-website-bot.service`, change `USERNAME` and the two paths to match the server, and run the three commands at the top of that file. `systemctl status sea-lab-website-bot` should say `active (running)`.
   - **Without `sudo`:** remove the `User=` line from that file, change `WantedBy=multi-user.target` to `WantedBy=default.target`, copy it to `~/.config/systemd/user/`, and run `systemctl --user daemon-reload` and `systemctl --user enable --now sea-lab-website-bot`. Then run `loginctl enable-linger $USER`, so the bot keeps running after you log out and starts after a reboot. If that command is refused, ask the server's administrator to run it for you.
8. **Invite the bot** to each channel where members should be able to mention it: `/invite @SEA Lab Website`. `/add-paper` works everywhere without this.

## Try it

- Type `/add-paper` and send a real paper that is not on the site yet. About a minute later the bot sends you a direct message, and a card appears in the admins' channel.
- Press **View changes** to see the pull request, then **Decline** to close it without publishing anything. Declining is the safe way to test: approving puts the paper on the live site.
- Then ask someone who is not an admin to press a button on a new card. They should see a private message saying only admins can.

## Keep it running

- **Is it running?** `systemctl status sea-lab-website-bot` on the server (add `--user` if you set it up without `sudo`). If Slack answers `/add-paper` with "dispatch_failed" or "this app is not responding", the bot is not running or cannot reach Slack.
- **Read its log.** `journalctl -u sea-lab-website-bot -n 100` (or `journalctl --user -u ...`). Problems before a workflow starts, such as the form not opening or a button doing nothing, show up here. Later problems are in the repository's Actions tab, under the two "Slack bot" workflows, and the bot's Slack message links to the log.
- <a name="token"></a>**When the token expires.** Members see "GitHub turned the bot away" in the form. Create a new token as in step 3, put it in `.env`, and restart the bot. Put the expiry date in the lab calendar.
- **Change who can approve.** Edit `ADMIN_SLACK_IDS` in `.env` and restart the bot.
- **Restart the bot.** `sudo systemctl restart sea-lab-website-bot` (or `systemctl --user restart sea-lab-website-bot`).
- **Change the research directions.** Nothing to do here. The form reads `data/research_directions.yaml` from `main` on GitHub, and picks up a change within five minutes.
- **Change the bot's code.** Edit `bot.py`, run `venv/bin/python -m unittest` in this folder, and merge the change. Then on the server run `git pull` and restart the bot. Merging on GitHub alone does not update the copy on the server. Changes to the workflows, `notify.py`, and `scripts/add_publication.py` take effect as soon as they are on `main`, with nothing to do on the server.
- **Run one copy only.** If a second copy runs with the same tokens, for example on a laptop during testing, Slack hands each request to one of the two at random.
- **Hand it over.** The server account, the Slack app, and the GitHub token each belong to a person. Before that person leaves the lab, move the bot to another account on the server, add a collaborator to the Slack app (**Collaborators** in its settings), and have someone else create a new GitHub token.

## Things to know

- **The bot merges with GitHub Actions' own permissions.** `main` has no branch protection today, so this works. If `main` is later protected so that every change needs a review, the Approve button will fail with a message under the card. The pull request stays open and can still be merged on GitHub. To keep the button working, the rule would have to let GitHub Actions bypass it.
- **The admin list is the only thing between a button press and the live site.** It is checked in `bot.py`. Anyone who can read `.env` on the server can start the bot's workflows and post as the bot, so keep that file readable only by its owner. Anyone who can push to this repository can already change the site without the bot.
- **The bot only merges its own pull requests.** The decision workflow refuses a pull request that is not on a `bot/publication-` branch, or that changes anything except `sea-lab-publication.bib` and `content/publication/`. If someone adds other changes to a bot pull request, approve it on GitHub instead.
- **Two papers approved in a row.** Each bot branch adds its paper to the end of the bib, so the second one conflicts with the first there. The decision workflow settles that itself by keeping both entries (`merge_bib` in `scripts/add_publication.py`). GitHub's own merge button will show a conflict on the second pull request. The Slack button still works.
- **What the public can see.** This repository is public, and so are its workflow logs. They show the submitted BibTeX, and the Slack member and channel IDs of the requester and the admin (IDs like `U01ABCDEF`, not names). Pull requests and commits name nobody.
- **What the bot does not do.** It adds new papers only. Award badges, a paper's `featured.png`, `selected` and `highlight`, `publication_short`, and fixes to papers already on the site are still done by hand, as the main README describes. An admin can push changes inside the paper's folder, such as a `featured.png`, to the bot's branch before pressing Approve.
- **Looked-up papers need a look.** For a DOI or arXiv link, the details come from doi.org. They usually have no abstract, and the venue name or the capital letters in the title can differ from the paper. The card says when a paper was looked up, and the form has a box for the abstract.
