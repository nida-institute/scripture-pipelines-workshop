# Lesson 2 — Your project on GitHub, with an AI agent that works under its own name

**Status:** proposed (2026-10-07)
**Amendments:** none yet.
**Track:** Both. Where a file's location differs between the tracks, both are given.

**Audience.**
- *Scholars:* you will put your project on GitHub, see exactly which actions are the AI's and which
  are yours, and keep track of the work in issues, a board and a task list Claude reads.
- *Technical participants:* the same, plus how the agent's identity is configured, why a push is
  always yours, and how to check what the skills and AI-context files actually instruct.

**Vocabulary.**
- **git** — the tool that records a project's history on your computer.
- **GitHub** — a website that holds a copy of that history and adds issues, boards and sharing.
- **Repository (repo)** — a project folder whose history git tracks.
- **Commit** — a saved, named point in that history. It carries an author's name.
- **Push** — sending your commits to GitHub. It is done with *your* login, so GitHub records *you*
  as the person who pushed, whoever wrote the change.
- **Issue** — a numbered GitHub page for one piece of work or one question, with a discussion
  thread. Written `#12`.
- **Project board** — a GitHub page showing issues as cards in columns.
- **Agent account** — a second GitHub account that belongs to you but is used only by the AI, so
  anything it writes on GitHub, such as a comment, is labelled as the AI's.
- **Claude GitHub App** — lets anyone write `@claude` in an issue or pull request and have Claude
  respond on GitHub itself.
- **`gh`** — GitHub's command-line tool.
- **`TODO.md`** — `project/TODO.md`, the project's task list, which Claude reads at the start of a
  session.
- **CHANGELOG** — `CHANGELOG.md`, the dated record of what changed and why.

---

## 0. Why this lesson

Once an AI can create issues, write commit messages and prepare your work for saving, you need to
be able to tell afterwards **who did what**. Without that, an issue the AI opened reads as one you
wrote, and a change it made reads as your decision. This lesson sets up the identities that keep
those apart, and the files that keep the work's state outside any one session.

## 1. The core idea

**The AI's actions carry the AI's name; the acts that carry your name are yours.** The agent
account labels what the AI writes on GitHub. **Only you create issues, commit, push and open pull
requests** — Claude drafts and prepares them and hands you the command. Everything else in this lesson — issues, the
board, `TODO.md`, the CHANGELOG — is where the work is recorded so that the next session, and the
next person, can find it.

## 2. What you start with

- Lesson 1 done: Claude Code working in your `sp init` project, and the session commands.
- A GitHub account of your own.
- `gh` installed and signed in **as you**, in your own terminal: `gh auth login`. If you do not
  have `gh`, ask Claude to walk you through installing it from [cli.github.com](https://cli.github.com).
- Admin rights on the repository you create (you have them, since you create it).

The way of working is the same as Lesson 1 (§4.0): in pairs at a workshop, with Claude as your
guide — or on your own, with Claude as your partner and the §5 checks as your instructor.

## 3. What you produce

- Your project as a private GitHub repository, created and pushed by you.
- A second GitHub account for the AI, added to that repository, and Claude Code configured to use
  it — while your own terminal still uses yours.
- The Claude GitHub App installed on the repository.
- A project board with four columns, an issue on it, and that issue linked from `TODO.md`.
- A first CHANGELOG entry.
- Notes from reading the skills and AI-context files, including where they disagree.

## 4. Steps

### 4.1 [Both] Make the project a repository, with Claude's guidance

Ask Claude to make the folder a git repository and prepare a first commit. It runs `git init`,
checks what should and should not be tracked (**[sp only]** generated intermediate files should
not be — see `separate-output-from-intermediates` in `docs/ai-context/sp/rules.md`), runs `/commit-ready` to
check the work against the definition of done, then runs `/stage-commits`: it groups the files, asks you to confirm them, stages them, shows you the
staged diff and hands you the commit command.

**You run the commit.** Read the diff it showed you first.

### 4.2 [Both] Put it on GitHub — in your own terminal

Create the GitHub repository **from your own terminal, not from inside Claude**. Inside Claude,
`gh` will shortly be signed in as the agent (4.4), and the repository would then belong to the
agent account instead of to you.

```sh
cd ~/workshop-project
gh repo create workshop-project --source . --private --push
```

`--source .` uses this folder, `--private` keeps it private, and `--push` sends your commits.
([gh repo create](https://cli.github.com/manual/gh_repo_create))

### 4.3 [Both] Install the Claude GitHub App

Claude Code has a command, `/install-github-app`, that does this for you — but it pushes a branch
to GitHub, and only you push. So install it by hand, which takes three steps:
([GitHub Actions — manual setup](https://code.claude.com/docs/en/github-actions))

1. **Install the app** on your repository from [github.com/apps/claude](https://github.com/apps/claude),
   signed in as you.
2. **Add a credential as a repository secret** (the repository's Settings → Secrets and
   variables → Actions): either an API key from the Claude Console, stored as
   `ANTHROPIC_API_KEY`, or a token from your Claude subscription, made in your own terminal with
   `claude setup-token` and stored as `CLAUDE_CODE_OAUTH_TOKEN`.
3. **Add the workflow file.** Ask Claude to write `.github/workflows/claude.yml` from the example
   in the documentation; then `/commit-ready`, `/stage-commits`, and you commit and push it.

After that, writing `@claude` in an issue or pull request comment starts Claude on GitHub. Its
comments appear as `claude[bot]`.

**It costs something each time it runs:** GitHub Actions minutes from your account's allowance,
plus Claude usage against the API key or subscription you gave it.

Commits, pushes and pull requests in your repository remain yours, however the work was prepared.
GitHub's automatic checks run on the pull request you open.

### 4.4 [Both] Give the AI its own GitHub account

1. **Create a second GitHub account** for the agent, e.g. `yourname-ai-agent`. GitHub allows one
   free machine account per person, used only for automation.
   ([Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service))
2. **Add it to your repository** as a collaborator with the **Triage** role — enough to open
   issues, comment and label, not enough to change code.
   ([roles](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization))
   Accept the invitation while signed in as the agent.
3. **Tell Claude Code to use it.** In `~/.claude/settings.json`, the `env` block sets variables
   for the commands Claude runs — and only those, so your own terminal is unaffected:

   ```json
   {
     "env": {
       "GH_CONFIG_DIR": "/Users/you/.config/gh-agent",
       "GIT_AUTHOR_NAME": "Claude (AI agent)",
       "GIT_AUTHOR_EMAIL": "you+agent@example.com",
       "GIT_COMMITTER_NAME": "Claude (AI agent)",
       "GIT_COMMITTER_EMAIL": "you+agent@example.com"
     }
   }
   ```

   `GH_CONFIG_DIR` makes `gh` keep a separate login in that folder
   ([gh environment](https://cli.github.com/manual/gh_help_environment)). The `GIT_*` variables set
   the author name on any commit made from inside Claude
   ([git environment variables](https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables)).
   Use an absolute path.
4. **Sign `gh` in as the agent, into that folder** — in your own terminal:

   ```sh
   GH_CONFIG_DIR=/Users/you/.config/gh-agent gh auth login
   ```

   Sign in with the agent account, not yours.
5. **Do not run `gh auth setup-git`.** It would make git use a `gh` login for pushing. Pushing
   stays with your own credentials, in your own terminal.
   ([gh auth setup-git](https://cli.github.com/manual/gh_auth_setup-git))

**Check it:** restart Claude, then ask it to run `gh auth status`. It should name the agent
account. In your own terminal, `gh auth status` should still name you.

### 4.5 [Both] Issues — drafted by Claude, created by you

**Only you create issues.** Ask Claude to draft one for the next piece of work. It writes the
title and body to a file in `tmp/` and shows them to you. Edit until it says what you mean, then
create it yourself, in your own terminal:

```sh
gh issue create --title "<title>" --body-file tmp/issue.md
```

The issue appears under your name, because it is yours.

Issues are also where design discussion belongs: the thread keeps the whole history of a decision,
where a separate document would drift (**[sp only]** `docs/ai-context/sp/github-workflow.md`).

### 4.6 [Both] A project board with four columns

Every board uses the same four columns, in order: **Backlog → Todo → Doing → Done**
(**[sp only]** `project-boards` in `docs/ai-context/sp/rules.md`; a Helm project adopts the same
four).

In your own terminal, give your login the scope it needs, create the board and link it:

```sh
gh auth refresh -s project
gh project create --owner @me --title "your-project"
gh project link <number> --owner @me --repo <you>/your-project
```

Then open the board on GitHub and set the Status column options to the four above — the columns
are edited in the web page. Add your issue to the board.
([gh project](https://cli.github.com/manual/gh_project))

### 4.7 [Both] `TODO.md` — the task list Claude reads first

`project/TODO.md` has three sections: **Active** (in flight), **Backlog** (next) and **Done**
(recent). Link an issue as `→ #N` rather than copying its text — the issue is the full record, the
list is the short version (**[sp only]** `todo-is-the-session-cache` in
`docs/ai-context/sp/rules.md`).

Add your issue to it. Notice the difference from Lesson 1's handoff: `HANDOFF.md` holds only what
disappears once work is committed; `TODO.md` holds everything that outlasts the session.

### 4.8 [Both] CHANGELOG — the dated record of what changed

Add `CHANGELOG.md` with a first entry: a dated heading, then one line per change, each naming the
issue it closes as `(Issue #N)`. `/stage-commits` checks that a change in behaviour has a
CHANGELOG entry before it stages anything.

**Head each entry with the date only** — `## 2026-10-07`. **[sp only]**
`docs/ai-context/sp/github-workflow.md` numbers versions in four parts (`0.2.1.14`), taken from a
`pyproject.toml` that a workshop project does not have; a date is all a workshop project needs.

### 4.9 [Both] Read what the skills and AI context actually say

A skill is only a text file, and so are the project's rules. Reading them is how you find out what
Claude has been told to do — and whether the instructions agree with each other.

Open these:

**[Both]**
- `.claude/skills/stage-commits/SKILL.md`
- `.claude/skills/commit-ready/SKILL.md`

**[sp only]**
- `docs/ai-context/sp/rules.md` — the rules every session is held to
- `docs/ai-context/sp/github-workflow.md`
- `~/.sp/disciplines/github-authority.md`

**[Helm only]**
- `docs/ai-context/project/rules.md` — your project's own rules
- `docs/ai-context/helm/disciplines/github-authority.md`

Then answer three questions, first by reading and then by asking Claude to check your answer
against the files:

1. **Who creates a GitHub issue, and does a person see it first?**
2. **Who commits, and who pushes?**
3. **Who opens a pull request?**

Write down which file says what, quoting the line. Where the files disagree, note it.

The answers in this workshop: **only you create issues, commit, push and open pull requests.**
Ruled 2026-10-07. Where a shipped file says otherwise, that is a disagreement worth reporting to
the project that ships it — not working around. Disagreements found on 2026-10-07 were reported,
and some may be fixed by the time you read this; if every file now agrees, say so.

## 5. How you know it worked

- On GitHub, the repository is owned by **your** account, and its first commit is authored by you.
- Inside Claude, `gh auth status` names the agent account; in your own terminal it names you.
- The issue from 4.5 shows **you** as its author.
- The board has exactly the four columns, with the issue on it.
- `project/TODO.md` links the issue as `→ #N`.
- You can say, with a quoted line from each file in 4.9, what it says about issues, commits,
  pushes and pull requests — and where any of them disagree with the workshop's answer.

## 6. Non-goals

- Branches and pull requests, beyond knowing that opening one is yours.
- Writing or changing skills.
- Organisation accounts and permissions.

## 7. Teaching this lesson

### Before the day

- Tell participants ahead of time to **create the second GitHub account for the AI** before they
  arrive (4.4, step 1). It needs a separate email address, and a confirmation email can be slow; a
  `you+agent@…` address works with many providers.
- Ask them to **install `gh`** and sign in as themselves beforehand, if they can.
- Decide which credential participants will give the GitHub App (4.3): an API key from the Claude
  Console, or a token from their Claude subscription. Tell them which, and that each `@claude` run
  costs Actions minutes and Claude usage.
- Work through the lesson yourself shortly before, including the board's columns in the web page —
  GitHub's screens change.

### Introducing each step

| Step | Say | Rough time |
|---|---|---|
| — | "The theme today: you should always be able to tell afterwards who did what. The AI's actions carry the AI's name; anything that carries your name, you do yourself." | 5 min |
| 4.1 | "Claude prepares the first save and shows you exactly what's in it. You read it, then you run the commit." | 15 min |
| 4.2 | "Create the GitHub repository from your own terminal. Inside Claude, `gh` is about to become the agent, and the repository must belong to you." | 10 min |
| 4.3 | "The GitHub App lets people ask Claude for help on GitHub itself. We install it by hand, because the automatic installer pushes — and pushing is yours." | 20 min |
| 4.4 | "Now the AI gets its own GitHub account, so what it writes there is labelled as the AI's. Your own terminal stays you." | 25 min |
| 4.5 | "Claude drafts issues; you create them. An issue is a decision about what to work on, and that's yours." | 10 min |
| 4.6 | "A board shows the issues as cards. Every board here has the same four columns." | 15 min |
| 4.7–4.8 | "`TODO.md` is the short list Claude reads at the start of every session. The CHANGELOG is the dated record of what changed." | 15 min |
| 4.9 | "Skills are just text files. Let's read what Claude has actually been told — and find where the files disagree." | 25 min |

The times are estimates, about two and a half hours in all; correct them from experience.

### Where people get stuck

- **The repository was created under the agent account.** It was created from inside Claude after
  4.4. Delete it on GitHub and create it again from the participant's own terminal.
- **`gh auth status` inside Claude still names the participant.** Claude was not restarted after
  `settings.json` changed, or `GH_CONFIG_DIR` is a relative path. Use an absolute path and restart.
- **`gh auth status` in their own terminal names the agent.** They signed in without
  `GH_CONFIG_DIR=…` in front of `gh auth login`, so the agent replaced their own login. Sign in
  again as themselves, then redo 4.4 step 4.
- **A participant's own commit is authored as the AI, or their issue appears under the agent.** In
  the terminal version they ran it with Claude's `!` prefix, which uses Claude's settings. Run it
  again from a separate terminal window — or, in the app, from the Terminal pane (Lesson 1, 4.1).
- **The agent cannot comment on the repository.** The collaborator invitation has not been
  accepted. Sign in to GitHub as the agent and accept it.
- **`gh project create` is refused.** The login lacks the `project` scope: `gh auth refresh -s project`.
- **`@claude` does nothing.** The workflow file is not on GitHub yet, or the secret's name does not
  match the one the workflow expects. Check the repository's Actions tab for a failed run.
- **`settings.json` will not load after editing.** A missing comma or brace. Ask Claude to check
  the file — it is a quick fix and a good example of letting Claude read before it writes.

### Before moving the room on

Run the §5 checks out loud. After 4.4, have every pair run `gh auth status` in both places and say
which account each one names; the rest of the lesson depends on it. In 4.9, ask pairs to read out
one disagreement they found, quoting the line.
