# Lesson 1 — Getting started: installing Claude, and opening and closing a session safely

**Status:** proposed (2026-10-07)
**Amendments:** none yet.
**Track:** Both. Step 4.2 has one version for each track; lines that differ are labelled.

**Audience.**
- *Scholars:* you will be able to start Claude on a project, have it read that project's rules
  before it does anything, and end a session without losing what it knew.
- *Technical participants:* the same, plus where the configuration lives, which parts of it are
  enforced and which are only instructions, and why the desktop app's Cowork mode is a different
  thing from Claude Code.

**Vocabulary.**
- **Claude Code** — Claude working on files on your computer: reading them, editing them, running
  commands. It runs either in a terminal or in the Code tab of the Claude desktop app.
- **Terminal** — the text window where you type commands (Terminal on a Mac).
- **Session** — one conversation with Claude, from start to exit. Claude forgets everything when a
  session ends; only what is written in files survives.
- **Context** — what Claude has in front of it during a session: the files it has read and the
  conversation so far. It is limited, and a long session gets condensed ("compacted"), losing detail.
- **Slash command** — a command typed into Claude starting with `/`, such as `/exit`.
- **Skill** — a written procedure that Claude follows when you type its slash command. Skills are
  files on your computer, so you can read exactly what each one tells Claude to do.
- **[sp only] `sp`** — the Scripture Pipelines command. `sp init` sets up a project and installs
  the skills this workshop uses.
- **[Helm only] `/install`** — Human at the Helm's installer, run from a copy of its repository. It
  sets up a project and installs the same skills.
- **Repository (repo)** — a project folder whose history is tracked by git. Lesson 2.
- **Commit** — a saved, named point in a repository's history. Lesson 2.

---

## 0. Why this lesson

An AI session starts with no memory of your project and ends by forgetting everything it learned.
Left alone, it fills the first gap by guessing and loses the second without telling you. The
commands in this lesson close both gaps: one makes Claude read the project's own rules before it
starts, and the others make sure what it knows is written down before it stops.

## 1. The core idea

**A session is temporary; the files are what last.** Start every session by having Claude read the
project's rules (`/load-context`). End it by writing down what matters (`/handoff`) and leaving
the saving of your work in your own hands (`/stage-commits`). Restarting is cheap and normal — a
fresh session that reads a good handoff usually works better than a long, tired one.

## 2. What you start with

- A Mac (Windows and Linux are noted where they differ).
- A paid Claude plan. Claude Code is included in **Pro, Max, Team and Enterprise**, and through the
  **Claude Console** (pay-as-you-go API credits). It is **not** in the Free plan.
  ([quickstart](https://code.claude.com/docs/en/quickstart), [pricing](https://claude.com/pricing))
- **[sp only]** An **OpenAI** API key. Scripture Pipelines calls models with it, separately from
  your Claude plan; the workshop has been tested with OpenAI's models.
- **[Helm only]** `git`, to copy the Human at the Helm repository.
- A partner, if you are at a workshop — you work in pairs throughout. On your own, Claude takes
  the partner's place (4.0).

At a workshop, the instructor will have told you in advance what to arrange. On your own, arrange
it before you start: without the plan nothing in this lesson works, and on the sp track nothing
runs without the key.

## 3. What you produce

- Claude Code running, in the terminal or the desktop app's Code tab.
- **[sp only]** Scripture Pipelines installed, and a project folder set up with `sp init`.
- **[Helm only]** A project folder set up with Human at the Helm's `/install`.
- One complete session cycle: start → `/load-context` → `/health-check` → `/handoff` → `/exit` →
  restart → `/load-context`.
- A `project/HANDOFF.md` file written by Claude, which you have read.

## 4. Steps

### 4.0 [Both] How the workshop runs

- **The instructor introduces each section** before you start it, and is there to help
  throughout. Ask whenever you are stuck.
- **Work in pairs.** Talk through what you are doing with your partner: the workshop materials,
  the pipelines, what Claude proposes and why, and anything else that comes up. Two people
  reading Claude's report catch more than one.
- **Use Claude as your guide.** When a step is unclear, ask Claude to explain it or walk you
  through it. Reading what it proposes before approving it is part of the lesson, not a delay.

**On your own.** Claude takes your partner's place: before each step, tell Claude what you are
about to do and why, and ask it to question your understanding. The §5 checks take the
instructor's place — do not move on until they pass. §7 below is written for instructors, but its
introductions and its list of where people get stuck are just as useful read alone.

### 4.1 [Both] Install Claude — choose one

**In the terminal.** Run the installer:

```sh
curl -fsSL https://claude.ai/install.sh | bash
```

On Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`. This version updates itself.
([setup](https://code.claude.com/docs/en/setup))

Then make a new, empty folder for your workshop project and start Claude *in it* — the folder is
how Claude knows which project it is working on:

```sh
mkdir ~/workshop-project
cd ~/workshop-project
claude
```

The first time, it asks you to sign in with your Claude account.

**In the desktop app.** Download the Claude app
([Mac](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect),
[Windows](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect)), sign in, and click the
**Code** tab at the top. Choose **Local**, select your project folder, and start typing.
([desktop quickstart](https://code.claude.com/docs/en/desktop-quickstart))

**The two are the same Claude Code.** They read the same settings, the same project instructions
and the same skills, so everything below works in both. The app also has a **Chat** and a
**Cowork** mode, and those are different — see 4.10.

#### Terminal or app: where each action happens

Every action in this workshop can be done either way. The lessons say what to do; this table says
where, and applies to every lesson.

| Action | Terminal (Claude Code CLI) | Desktop app (Code tab) |
|---|---|---|
| Start Claude in your project | `cd ~/workshop-project`, then `claude` | **Local** → choose the folder → start typing |
| Start a second, fresh session | a new terminal window, `claude` | Cmd+N (Ctrl+N on Windows) |
| Run a slash command or skill | type `/` and choose | type `/` and choose — the same menu |
| Approve or refuse what Claude proposes | answer the prompt in the terminal | the approval card in the session |
| Change the permission mode | Shift+Tab | the mode selector next to the send button |
| See what Claude changed | ask Claude to show the diff, or `/diff` | click the `+12 −1` indicator to open the diff view |
| Read a file | open it in your editor, or ask Claude to show it | click its path in the conversation |
| **Run a command as yourself** — commit, push, create an issue, sign in, enter a key | **a separate terminal window, outside Claude** | the **Terminal** pane: Ctrl+\` or **Terminal** in the title bar |
| End the session | `/exit` | Cmd+W, or close it in the sidebar |
| Resume an earlier session | `claude --continue` (latest) or `claude --resume` (choose) | click it in the sidebar; `/resume` also lists terminal sessions |
| Change Claude Code's settings | edit `~/.claude/settings.json` in an editor; `/config` for some | edit `~/.claude/settings.json` in an editor; **Settings → Claude Code** for some |

([desktop](https://code.claude.com/docs/en/desktop),
[permission modes](https://code.claude.com/docs/en/permission-modes),
[sessions](https://code.claude.com/docs/en/sessions))

**"Your own terminal" means the row in bold above.** When a lesson says to do something in your own
terminal, it means a shell that is *you*, not Claude:

- **In the terminal version, do not use Claude's `!` prefix for these.** A command typed after `!`
  runs inside Claude's session, with Claude's settings — so after Lesson 2 it would commit under the
  AI's name and sign in to GitHub as the AI's account. Use a separate terminal window.
- **In the app, the Terminal pane is your own shell.** It does not take Claude's settings, so it
  acts as you. (This is described in Claude Code's issue tracker rather than its documentation;
  check it in Lesson 2 with `gh auth status`, which names the account in use.)

### 4.2 [sp only] Install Scripture Pipelines — with Claude walking you through it

The instructions are in Scripture Pipelines' own
[`INSTALL.md`](https://github.com/nida-institute/LLMFlow/blob/main/INSTALL.md). Rather than
following them alone, ask Claude to take you through them:

> Read https://github.com/nida-institute/LLMFlow/blob/main/INSTALL.md and walk me through
> installing Scripture Pipelines on this computer, one step at a time. Explain each step before
> we do it.

This is the first chance to practise the way of working the whole workshop teaches: Claude
explains and proposes, you decide and approve. Ask it why whenever a step is unclear — that is
what it is there for.

Along the way:

- **`sp --version`** confirms the install worked.
- **Your API key is yours to type.** `sp setup` asks for the key Scripture Pipelines uses to call
  a model — your OpenAI key. Run it **in your own terminal**, not through
  Claude, and never paste the key into the conversation — anything typed there becomes part of
  the session.
- **`sp init`**, run in your project folder, sets the project up: its `CLAUDE.md`, its
  `docs/ai-context/` and its starter pipeline — and installs the skills this lesson uses.

Then **exit and restart Claude** in the project folder (4.8 and 4.9 show how). Claude reads a
project's `CLAUDE.md` when a session starts, so the session that ran `sp init` has not seen it.

### 4.2 [Helm only] Install Human at the Helm into your project

Human at the Helm installs from a copy of its own repository. Its installer is a skill that lives
there, so starting Claude in that copy makes `/install` available
([README](https://github.com/nida-institute/human-at-the-helm#getting-started)):

```sh
git clone https://github.com/nida-institute/human-at-the-helm
cd human-at-the-helm
claude
```

Then, inside Claude:

```
/install ~/workshop-project
```

**Read what it proposes before you approve it.** The installer lists every file it will write into
your project and every file it will leave alone, then waits. That is the discipline the whole
workshop teaches, applied to its own installation: Claude explains, you decide. Everything it
installs — skills, the AI context, a `CLAUDE.md` — is plain text, declared in the repository's
`manifest.yaml`.

Then **exit, and start Claude again in your project folder** (4.8 and 4.9 show how). The skills and
the `CLAUDE.md` belong to the project, so a session started there is the one that sees them.

### 4.3 [Both] `/load-context` — have Claude read the project's rules first

Type `/load-context` at the start of every session, before asking for anything else.

Claude reads the project's `CLAUDE.md`, the documents under `docs/ai-context/`, the project's
rules and the shared disciplines, then reports: which project and branch it is in, the commands it
may use, what is changed and not yet saved, and that it is ready.

*Why it matters:* without it, Claude works from general habits rather than from this project's
rules. Read its report — if it names the wrong project, or says it could not find the rules, stop
there.

### 4.4 [Both] `/health-check` — is this session still working well?

Ask at any point, and especially after a long stretch of work. Claude reports on five things:

1. whether the session has been compacted (condensed, losing detail);
2. whether it is re-deriving things it already established;
3. every correction you have had to make, listed one by one with what was claimed and what was true;
4. how much work is unsaved, naming the files;
5. whether the next step is waiting on a decision from you.

It opens and closes with two answers — **handoff: yes/no** and **exit: yes/no** — and the decision
is yours. "Handoff yes, exit no" is common: write things down, keep working.

### 4.5 [Both] `/handoff` — write down what the next session needs

Claude writes `project/HANDOFF.md`, leading with **the single next action**, then the work in
progress, the decisions made and why, and what not to touch. The test it is held to: a fresh
session reading only that file and the project must be able to start the next step without
guessing.

**Read it.** It is the only thing the next session will know about this one.

### 4.6 [Both] `/commit-ready` — is the work ready to be saved?

Before anything is saved, `/commit-ready` checks it against the project's definition of done, in
order, stopping at the first thing that fails: an issue exists for the work; tests were written
first and pass; the CHANGELOG is updated; the commit message names its issue; and, once you have
opened a pull request, GitHub's automatic checks on it pass.

It decides **whether** a commit may happen. `/stage-commits` is **how**. Where its checklist says
the AI commits, pushes, opens a pull request or merges, those steps are yours: **only you commit,
push and open pull requests.**

**[sp only]** Its gates were written for the Scripture Pipelines engine itself — a Python test suite, a version
in `pyproject.toml`, a TypeScript interface. Where a gate cannot apply to your project, expect
Claude to say so rather than pass it silently.

### 4.7 [Both] `/stage-commits` — Claude prepares the save; you make it

In a git repository, Claude groups the changed files, asks you to confirm whose each change is,
writes the commit message to a file, stages the files, shows you exactly what is staged, and hands
you the one command that saves it. **Claude never commits or pushes** — those carry your name, so
they are yours to do.

You will use this from Lesson 2 onwards, once you have your own repository.

### 4.8 [Both] `/exit` — end the session

- **Terminal:** type `/exit` (or press Ctrl+D twice).
- **Desktop app:** press Cmd+W (Ctrl+W on Windows), or close the session in the sidebar.

([quickstart](https://code.claude.com/docs/en/quickstart),
[desktop](https://code.claude.com/docs/en/desktop))

### 4.9 [Both] Restart

- **Terminal:** `claude` in the project folder starts fresh. `claude --continue` reopens the most
  recent conversation in that folder; `claude --resume` lets you pick an older one.
- **Desktop app:** Cmd+N (Ctrl+N) starts a fresh session in the same folder; clicking a previous
  session in the sidebar resumes it.

([sessions](https://code.claude.com/docs/en/sessions))

**Prefer a fresh start after a handoff.** Then type `/load-context` again.

`/load-context` reads `project/HANDOFF.md`, so the fresh session starts from the handoff the last
one wrote.

### 4.10 [Both] The other modes of the app: Chat and Cowork

**Chat** reads none of your project's files or settings. It is a separate assistant.

**Cowork** gives Claude access to folders you grant it, but it is not Claude Code, and it does not
follow most of what this workshop sets up.

**What Cowork reads**
- It reads `CLAUDE.md` files inside a folder you grant it, so a project's `CLAUDE.md` reaches it,
  along with its instruction to read `docs/ai-context/`.
- It does **not** read anything in `~/.claude`, the folder where Claude Code keeps your personal
  configuration. The Cowork overview says so plainly
  ([Cowork overview](https://claude.com/docs/cowork/overview)). That leaves out:
  - your personal `~/.claude/CLAUDE.md`, with any rules you keep for every project;
  - `settings.json`, both yours and the project's, so no allow / deny / ask permission rules apply;
  - hooks — checks that run automatically, such as at the start of a session;
  - the `env` block in your settings, such as a separate git author name for the AI;
  - Claude Code's memory files and the skills in `~/.claude/skills` — so none of this lesson's
    five commands exists in Cowork.
- Its settings and skills come from your claude.ai account, added through the app's Customize
  screen.

**Where Cowork can read, write and run**
- It can only reach the folders you grant it.
- Reading and writing files happens directly on your computer. Shell commands run in an isolated
  Linux virtual machine on your computer.
- So `git` and `gh` there should not have your saved credentials, and a push would most likely
  fail. *This comes from a third-party blog post, not Anthropic's own documentation.*
- Commit authorship is a risk: without your settings, a commit made there would not carry the
  author name you set for the AI. What name it would use instead has not been confirmed.

**What this means for you:** in Cowork, the rules in a project's `CLAUDE.md` are only text the
model is asked to follow. Nothing enforces them, and your personal rules do not reach it at all.
Use the **Code** tab for this workshop.

## 5. How you know it worked

- `claude` starts in your project folder, or the app's Code tab shows that folder.
- **[sp only]** `sp --version` prints a version number.
- The project folder holds a `CLAUDE.md`, a `docs/ai-context/` folder and a `.claude/skills/`
  folder, written by `sp init` or by `/install`.
- `/load-context` names **your** project folder and lists its rules. If it names a different
  folder, you started Claude in the wrong place.
- Typing `/` shows `load-context`, `health-check`, `handoff`, `commit-ready` and `stage-commits`
  in the menu. If any is missing, the install in 4.2 did not reach this folder.
- `project/HANDOFF.md` exists, carries today's date, and its first item is a next action you
  could start yourself.
- After restarting, the fresh session can state that next action correctly without you telling it.

## 6. Non-goals

- Git, repositories and commits — Lesson 2. `/commit-ready` and `/stage-commits` are introduced
  here and practised there.
- Running pipelines (`sp run`), which costs money and is only ever done on your instruction.
- Chat and Cowork beyond knowing why this workshop does not use them.
- Customising settings, permissions or hooks.

## 7. Teaching this lesson

### Before the day

- Tell participants, at least a week ahead, that they need **a paid Claude plan** (Pro, Max, Team
  or Enterprise, or Claude Console credits) — and, **[sp only]**, **an OpenAI API key** — the
  workshop has been tested with OpenAI's models. Neither can be arranged quickly in the room.
- Ask them to bring a laptop they can install software on. A managed work machine may block the
  installers, or **[sp only]** the unsigned `sp` binary.
- Work through this lesson yourself on a clean account shortly before, so you meet any change in
  the installers before the room does.
- Plan the pairs so that, where you can, each pair has one person comfortable in a terminal.

### Introducing each step

| Step | Say | Rough time |
|---|---|---|
| 4.0 | "You'll work in pairs, and Claude is your guide. Reading what it proposes before you approve it is the skill we're learning today." | 5 min |
| 4.1 | "Claude Code is Claude working on the files on your own computer. It runs in a terminal or in the desktop app's Code tab — they're the same thing, so pick whichever you prefer." | 15 min |
| 4.2 [sp only] | "Now let Claude walk you through installing Scripture Pipelines. Notice the pattern: it explains, you decide. One rule: your API key never goes into the conversation." | 25 min |
| 4.2 [Helm only] | "The installer tells you every file it will write before it writes any. Read the list before you approve it — that's the whole method in one step." | 15 min |
| 4.3 | "Claude starts every session knowing nothing about your project. `/load-context` makes it read the project's rules first. Read its report — it's telling you what it understood." | 10 min |
| 4.4 | "Sessions get tired. `/health-check` tells you whether this one still knows what it knows, with the evidence." | 10 min |
| 4.5 | "Everything Claude knows vanishes when the session ends, unless it's written down. `/handoff` writes it down — and you read it." | 15 min |
| 4.6–4.7 | "Two commands you'll use in Lesson 2: one checks whether work is ready to save, the other prepares the save. Saving itself is always yours." | 10 min |
| 4.8–4.9 | "Ending and restarting is normal and cheap. A fresh session with a good handoff often works better than a long one." | 15 min |
| 4.10 | "The app has two other modes. This is why we don't use them for this work." | 10 min |

The times are estimates, about two hours in all; correct them from experience.

### Where people get stuck

- **Claude started in the wrong folder.** `/load-context` reports a different project, or finds no
  rules. Exit, `cd` into the project folder, start again.
- **[Helm only] `/install` is not in the `/` menu.** Claude was started somewhere other than the
  copy of the Human at the Helm repository. Start it there.
- **[sp only] `sp: command not found`.** The folder it was installed into is not on the PATH, or the
  terminal was opened before the install. Open a new terminal; if that fails, `INSTALL.md`'s
  troubleshooting table covers it.
- **[sp only] macOS refuses to open `sp`** ("unidentified developer"). *System Settings → Privacy &
  Security → Allow Anyway*, then run it again — described in `INSTALL.md`.
- **[sp only] On Windows, `sp` gives an odd parameter error.** PowerShell's own `sp` alias ran instead. Use
  `sp.exe`, or Command Prompt — `INSTALL.md` explains.
- **A slash command is missing from the `/` menu.** Both installers put the skills in the
  project's own `.claude/skills/` folder, so check that the install targeted *this* folder.
  **[sp only]** `sp doctor` restores any that are missing. Then restart Claude.
- **[sp only] Someone pastes their API key into Claude.** Have them create a new key with the provider and
  revoke the old one; then run `sp setup` in their own terminal.
- **Someone is on the Free Claude plan.** Claude Code is not included. Pair them with someone
  who has a plan for the rest of the lesson.

### Before moving the room on

Run the §5 checks out loud. In particular, after 4.9 ask one pair to show that their fresh session
can state the next action from their handoff — it is the point of the whole lesson.
