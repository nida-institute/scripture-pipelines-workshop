# Workshop — directing AI with Scripture Pipelines

**Status:** proposed (2026-10-07)
**Amendments:** each amendment is dated, gives its reason, and goes at the top of this list.
- **2026-10-07 — two tracks.** The same materials serve Human at the Helm and Scripture
  Pipelines, so every part of every lesson is labelled [Both], [sp only] or [Helm only].
- **2026-10-07 — two goals added.** Anyone who has taken the workshop must be able to teach it,
  and anyone who cannot attend must be able to work through it alone. So nothing may live only
  in an instructor's head: every lesson carries its own teaching notes (§7), and every step must
  make sense without being introduced.

**Audience:** a mixed room. Scholars who know the texts and data but are new to directing an AI,
and technical staff who are comfortable with a terminal, git and YAML. Every lesson serves both.

**Two tracks: Scripture Pipelines and Human at the Helm.** The same materials serve both.
[Human at the Helm](https://github.com/nida-institute/human-at-the-helm) is the methodology —
keeping the person in charge of an AI's work, in any project. Scripture Pipelines (`sp`) is an
engine for biblical and linguistic pipelines that ships the methodology with it. Every part of
every lesson is labelled:

- **[Both]** — for everyone.
- **[sp only]** — Scripture Pipelines participants only; Helm participants skip it.
- **[Helm only]** — Helm participants only, usually in place of an `sp only` part beside it.

A lesson's header says which track it serves; a step's label is at the start of its heading; a
single line or table row that differs is labelled inline.

**Terminal or app.** Every action can be done from the Claude Code command line or from the Code
tab of the Claude desktop app. Lesson 1 (§4.1, *Terminal or app*) has the table showing where each
action happens in each, including what "your own terminal" means in both — and every later lesson
relies on it.

**The two goals.**
1. **Anyone who has taken the workshop can teach it.** Everything an instructor needs is in the
   lesson files themselves.
2. **Anyone can work through it alone.** The materials do not depend on an instructor or a
   partner being in the room.

**How the lessons are written.** Each lesson follows the same template, modelled on the way
Scripture Pipelines writes its durable specifications: a stated audience, a vocabulary, numbered
sections, a check you can carry out yourself, an explicit list of what the lesson leaves out, and
notes for whoever teaches it.

**The language rule (applies to every lesson).** Jargon is never the only form of a point. Every
technical term is glossed in plain words the first time a lesson uses it, and every Greek or Hebrew
term is shown with a translation.

---

## How the workshop runs

The instructor introduces each section and is there to help throughout. Participants work in
pairs, discussing the materials, the pipelines, what Claude proposes and anything else that comes
up. Claude is used as a guide: when a step is unclear, participants ask it to explain or walk them
through it.

## Teaching the workshop

If you have taken the workshop, you can teach it. For each lesson:

1. **Before the day**, read the whole lesson, then its **§7 Teaching this lesson**, and do the
   setup it lists — participants who arrive without a paid Claude plan or a model API key cannot
   take part, so tell them in advance.
2. **On the day**, introduce each step with the sentences in §7, let pairs work, and walk the room.
   §7 lists where people usually get stuck and what gets them moving again.
3. **Before moving on**, run the **§5 checks** out loud with the room. A pair that fails a check
   catches up before the next section, because each step builds on the one before.
4. **Afterwards**, if something went differently from what §7 predicted, add it to §7 as a dated
   amendment, so the next instructor knows.

The times in §7 are estimates; correct them from experience.

## Working on your own

You can take the workshop without attending one.

- **Claude takes your partner's place.** Explain to Claude what you are about to do and ask it to
  question your understanding; ask it to explain anything you do not follow.
- **The §5 checks take the instructor's place.** Do not move on until every check in a lesson
  passes.
- **§7 is for you too.** Its introductions and its list of where people get stuck are written for
  instructors, but they are just as useful read alone.
- **You arrange your own prerequisites:** a paid Claude plan and a model API key (Lesson 1, §2).
- **If you are stuck,** open an issue on [the Scripture Pipelines repository](https://github.com/nida-institute/LLMFlow/issues)
  describing what you did, what you expected, and what happened instead.

---

## Lessons

| # | Lesson | Track | What you leave with |
|---|---|---|---|
| 1 | [Getting started](01-getting-started.md) | Both, with an install step for each | Claude and Scripture Pipelines installed, a project set up, and the commands that open and close a session safely |
| 2 | [Your project on GitHub](02-github.md) | Both | Your repository on GitHub, an AI agent account working under its own name, the Claude GitHub App, a board, issues, `TODO.md`, a CHANGELOG — and a reading of what the skills actually say |
| 3 | [The sample pipeline](03-sample-pipeline.md) | sp only | The sample pipeline read, checked for free, and run on a passage you chose — knowing which steps cost money and why |
| 4 | [The written record](04-written-record.md) | Both | Plans you rule on, specifications, audits without verdicts, issues you create, and `tmp/` — and where each lives |
| 5 | [Drift](05-drift.md) | Both | The drift patterns named, which of `sp`'s guards your machine actually enforces, and what to do when drift has happened |
| 6 | _(to come)_ — the catalog of biblical data | sp only | Finding, licensing and downloading datasets, and suggesting new ones |

---

## The lesson template

```markdown
# Lesson N — <title>

**Status:** proposed (<date>)
**Amendments:** (dated, with the reason, newest first)
**Track:** Both | sp only — every step heading starts with [Both], [sp only] or [Helm only]

**Audience:** what a scholar needs from this lesson / what a technical participant needs
**Vocabulary:** each term used, glossed once in plain words

## 0. Why this lesson        — the problem it solves, in the participant's terms
## 1. The core idea          — the one thing to take away
## 2. What you start with    — files, prerequisites, prior lessons
## 3. What you produce       — the concrete result at the end
## 4. Steps                  — each one understandable without an instructor
## 5. How you know it worked — a check you carry out, not one you take on trust
## 6. Non-goals              — what this lesson deliberately leaves out
## 7. Teaching this lesson   — setup beforehand, an introduction for each step,
                               where people get stuck, times, what to check before moving on
```

Open questions for the workshop's author are written as a question followed by a line holding
only `=>`; the answer goes after the `=>`. **A lesson is not ready to teach or to study alone while
it still holds an unanswered `=>`**, because whoever meets it has nobody to answer it.
