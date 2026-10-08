# Lesson 5 — Drift: how an AI ends up in charge, and how `sp` guards against it

**Status:** proposed (2026-10-07)
**Amendments:** none yet.
**Track:** Both. Step 4.3 has a version for each track; lines that differ are labelled.

**Audience.**
- *Scholars:* you will recognise the ways an AI quietly takes decisions that are yours, name them
  when they happen, and know what to do next.
- *Technical participants:* the same, plus which of `sp`'s guards are enforced by the machine and
  which hold only while the model pays attention to them.

**Vocabulary.**
- **Drift** — the gradual shift of control from you to the AI, one helpful-looking step at a time.
- **Drift pattern** — one named, recognisable way drift happens, such as *scope expansion* or
  *false memory*.
- **Guard** — anything that prevents or exposes a drift pattern.
- **Gate** — a guard that stops an act *before* it happens, such as a permission rule that makes
  Claude ask before running a command.
- **Instruction** — a guard that is only text the model is asked to follow: `CLAUDE.md`, the rules,
  a skill. It works only while the model attends to it.
- **Human at the Helm** — the methodology these guards come from, published at
  [github.com/nida-institute/human-at-the-helm](https://github.com/nida-institute/human-at-the-helm).

---

## 0. Why this lesson

None of the drift patterns looks like a failure while it is happening. Each looks like help:
fixing something nearby, offering the best option, reporting that everything passed, recalling
what you agreed earlier. You have spent four lessons using guards against them without naming
them. This lesson names the patterns, so you can see them, and shows which guards actually stop
them and which only ask the model to behave.

## 1. The core idea

**Drift looks like helpfulness, and most guards against it are instructions, not locks.** A rule
in `CLAUDE.md` holds only while the model attends to it; a long session, a compacted context or a
different tool can lose it without anyone noticing. So the last guard is always you: knowing the
patterns, keeping the acts that carry your name in your own hands, and checking claims against
the files rather than taking them on trust.

## 2. What you start with

- Lessons 1–4 done.
- [`drift-patterns.md`](https://github.com/nida-institute/human-at-the-helm/blob/main/drift-patterns.md)
  from Human at the Helm. Read it before the lesson if you can; it takes about twenty minutes.
  **[Helm only]** `/install` put a copy in your project at `docs/ai-context/helm/drift-patterns.md`.
- Your project's rules, which you first read in Lesson 2: **[sp only]** `docs/ai-context/sp/rules.md`;
  **[Helm only]** `docs/ai-context/project/rules.md` and `docs/ai-context/helm/disciplines/`.

## 3. What you produce

- A written example, from your own sessions in Lessons 1–4, of at least one drift pattern, with
  the guard that caught it — or that should have.
- A list, for your own machine, of which `sp` rules are enforced and which are instructions only.
- One use of `/stand-down`.

## 4. Steps

### 4.1 [Both] The patterns

`drift-patterns.md` groups them into six families. One line each:

| Family | What happens | Examples |
|---|---|---|
| **Authority fabrication** | The AI invents reasons to be trusted | treats its own old comment as a design decision; "as we agreed earlier…" about something never agreed; misquotes a file and defends the misquote |
| **Framing** | The AI substitutes its idea of your goal for your goal | restates your question narrower; offers "the best approach" instead of options; renames your concepts |
| **Scope and momentum** | The AI does more than was asked | "while I'm here I also…"; adds things you'll "probably need"; "now is a good time to…" |
| **Reporting** | The AI misstates what was done | "tests pass" when some ran; "it works" when the happy path worked |
| **Overwhelm** | Volume replaces evaluation | a wall of options you approve unread; "should I go ahead?" after it already has |
| **Persona** | The AI performs experience or feeling | "in my experience…"; "most scholars think…"; apologies and promises in place of a correction |

**With your partner** (on your own, with Claude): each choose one family and explain it to the
other with an example of your own.

### 4.2 [Both] The guards you have already used

Every lesson so far put a guard against one or more patterns in your hands:

| Pattern | Guard | Lesson |
|---|---|---|
| The AI working from habit instead of the project's rules | `/load-context` at the start of every session | 1 |
| Context loss, unnoticed | `/health-check`, which lists every correction one by one | 1 |
| False memory between sessions | `/handoff` — what the next session knows is what is written | 1 |
| Optimism in reporting | `/stage-commits` shows the actual staged diff; §5 checks you carry out yourself | 1, every lesson |
| Acts carrying your name done for you | only you create issues, commit, push and open pull requests | 2 |
| **[sp only]** Spending and agreeing in your name | only you agree to licences and decide when `sp run` runs | 3 |
| AI work indistinguishable from yours | the agent account and author name | 2 |
| **[sp only]** Ungrounded output | trace the guide back to its input; `/audit-output` | 3, 4 |
| Scope expansion, the helpful addition | `/authorize`: what authorises this, exactly what changes, what does not | 4 |
| Decision laundering, circular authority | `Status: proposed` until you rule; your answers after `=>`; audits carry no verdict | 4 |

### 4.3 [Both] Enforced, or only asked?

**[Both] Neither installer adds any gates.** `sp init` and Helm's `/install` write rules, AI
context and skills — instructions, all of them. Whether anything on your machine actually stops an
act depends on your own `~/.claude/settings.json`. Ask Claude to read yours and list which
commands, if any, it must ask you about before running.

**[Helm only]** Read `docs/ai-context/helm/disciplines/README.md`. It separates the short
operational rules a session is held to from the longer essays explaining the failures behind them.
Every one of them is an instruction unless your settings gate it.

**[sp only]** `docs/ai-context/sp/rules.md` sorts its own rules into three groups. Open it and find
them:

1. **Rules a gate stops before the act** — e.g. `commit-authority`, `issues-need-approval`. These are
   the strongest: the act is refused or put in front of you first. But read the note at the top of
   that section: **the gate lives in your own Claude Code settings, not in the project.** On a
   machine where nobody configured it, the rule is only an instruction.
2. **Rules a test can catch** — checked by Scripture Pipelines' own test suite, and some of them by
   `sp lint` in your project.
3. **Rules no test can catch** — the file's own words: "they hold only while they are actually in
   attention." These are the ones to carry yourself.

*Adding gates of your own: this part of the lesson is still to be written.*

### 4.4 [Both] Where the guards do not reach

Recall Lesson 1, 4.10: **Cowork reads a project's `CLAUDE.md` and nothing else** — not your
settings, not your hooks, not your skills. Chat reads none of it. The same is true of any other tool
that edits your files. Outside Claude Code, every guard in this lesson is at most an instruction,
and most are absent.

The acts that are yours stay yours there too, and for a mechanical reason: they need your own
credentials, in your own terminal.

### 4.5 [Both] When drift has happened: `/stand-down`

When you notice the AI has been steering — deciding things you did not ask it to, narrowing your
options, running ahead — type `/stand-down`. It names what happened and resets who is in charge.

What does *not* work, according to `drift-patterns.md`:

- **accepting an apology and carrying on** — the model has no way to keep the promise;
- **arguing** — each defence adds more of the wrong position to the conversation.

What does: redirect ("set that aside; here is what I want"), paste the actual file when the dispute
is about what it says, or **start a fresh session** — `/handoff`, `/exit`, restart, `/load-context`.
That cycle from Lesson 1 is also the strongest reset there is.

### 4.6 [Both] Find one in your own sessions

Look back over your sessions in Lessons 1–4 — Claude Code keeps them: `claude --resume` lists them
in the terminal, and the sidebar lists them in the app. Find one moment that matches a pattern in 4.1. Write down:

- what the AI said or did, quoted;
- which pattern it is;
- which guard caught it — or which would have.

If you find none, ask Claude to propose a change to your project with no `/authorize`, and watch
what it does.

## 5. How you know it worked

- You can name the six families, and give an example of one from your own sessions, quoted.
- You can say which of your project's rules are enforced on *your* machine, and how you know —
  from your own `settings.json`, not from what the rules say about themselves.
- You can say why Cowork and Chat are outside these guards.
- You have used `/stand-down` once and can say what it changed.

## 6. Non-goals

- Writing rules, skills or hooks of your own.
- The full Human at the Helm methodology — `adopting.md` in that repository covers it.
- Changing what Scripture Pipelines ships. Disagreements between its files are reported to it, not
  worked around (Lesson 2, 4.9).

## 7. Teaching this lesson

### Before the day

- Ask participants to read `drift-patterns.md` beforehand.
- Collect two or three examples of drift from your own sessions, quoted, to show the room. Real
  examples land far better than described ones.
- Know what your own `~/.claude/settings.json` gates, so you can show one that does and contrast a
  fresh one that does not.

### Introducing each step

| Step | Say | Rough time |
|---|---|---|
| — | "Every drift pattern looks like help while it's happening. Today we name them." | 5 min |
| 4.1 | "Six families. You've probably already seen most of them this week." | 25 min |
| 4.2 | "Every lesson so far gave you a guard. Here's what each one was guarding against." | 10 min |
| 4.3 | "Most guards are instructions the model is asked to follow. Let's find out which ones on your machine actually stop anything." | 20 min |
| 4.4 | "Outside Claude Code, almost none of this applies." | 5 min |
| 4.5 | "When it has happened: redirect, paste the file, or start fresh. Don't accept the apology." | 10 min |
| 4.6 | "Find one in your own sessions. Quote it." | 20 min |

The times are estimates, about an hour and a half in all; correct them from experience.

### Where people get stuck

- **"Claude never did any of that to me."** Usually it did, gently. Point them at the
  smallest patterns: a summary longer than the question, "great question", an option menu with one
  option clearly preferred.
- **Treating the rules file as proof of enforcement.** The file says what is *meant* to be
  gated; only `settings.json` says what is. Have them read their own.
- **Expecting `/stand-down` to fix the model.** It resets the working relationship in this session;
  it does not change the model. A fresh session is often the better reset.

### Before moving the room on

Run the §5 checks out loud. Ask two pairs to read out their quoted example and name its pattern; let
the room say whether they agree.
