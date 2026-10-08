# Lesson 4 — The written record: plans, specifications, audits, issues and `tmp/`

**Status:** proposed (2026-10-07)
**Amendments:** none yet.
**Track:** Both. The audit step has a version for each track.

**Audience.**
- *Scholars:* you will know where each kind of decision and finding is written down, which of them
  authorise work, and which are yours to make.
- *Technical participants:* the same, plus the naming and lifecycle conventions `sp` ships, and
  where they disagree.

**Vocabulary.**
- **Plan** — a working document describing a piece of work before it is done:
  `project/plans/<topic>-plan.md`.
- **Specification (spec)** — a durable statement of what something must do, consulted every time
  it is rebuilt. Unlike a plan, it does not expire when the work is done.
- **Example** — a worked input and output that shows a model what is wanted. A wrong one teaches
  the wrong thing on every run, so it is treated like a specification.
- **AI context** — `docs/ai-context/`, the documents Claude reads to learn the project. Your
  project's own half is `docs/ai-context/project/`.
- **Status** — the line at the top of a plan saying whether it is `proposed` (thinking aloud) or
  `ruled` (decided by a person, on a date).
- **Ruling** — a decision a person has made. It is permanent until overruled, and lives in
  `CHANGELOG.md`, or in the project's rules when it binds future work.
- **Audit** — a structured check that reports what it found, with evidence. It never gives a
  verdict.
- **Audit record** — the file an audit writes its findings to, under `project/audits/`.
- **Checklist** — a short procedure for auditing one kind of artifact, written by the project.
- **`tmp/`** — the project's folder for throwaway files: drafts, commit messages, scratch notes.
- **`=>`** — the marker under a question in a document, where the person deciding writes the answer.

---

## 0. Why this lesson

An AI produces documents faster than anyone can read them. Without conventions, a project fills up
with plans nobody approved, findings nobody checked and drafts nobody can tell from decisions — and
the next session reads all of them as if they were authoritative. This lesson is about writing
things down in a way that keeps clear what was *proposed*, what was *found*, and what was *decided*,
and by whom.

## 1. The core idea

**Every document says whether it is a proposal, a finding or a decision — and only a person turns a
proposal into a decision.** A plan marked `proposed` is never authorisation to build. An audit
reports; you decide what to do about it. An issue records a decision about what to work on, and
only you create one. What lasts is the ruling, in `CHANGELOG.md`; the working documents that led to
it are scratch.

## 2. What you start with

- Lessons 1 and 2 done: your project on GitHub.
- **[sp only]** Lesson 3 done: the sample pipeline run once, its output in `outputs/`.
- The `project/plans/README.md` and `project/audits/README.md` that `sp init` or `/install` wrote.
  Read both.

## 3. What you produce

- One plan, written by Claude, answered by you, and marked `ruled`.
- One short specification, drafted by Claude, approved by you, and moved into
  `docs/ai-context/project/`.
- One audit record, with every finding located — of your sample pipeline's output **[sp only]**,
  or of a file in your own project **[Helm only]**.
- One issue created by you, linked from `project/TODO.md`.
- A `tmp/` folder you understand, and nothing in it you did not mean to keep there.

## 4. Steps

### 4.1 [Both] Before any change: `/authorize`

Before Claude edits anything that matters, `/authorize` makes it stop and say:

1. **what authorises the change** — an issue, your own instruction quoted exactly, or an audit
   finding;
2. **exactly which files will change**, and what will not;
3. then it asks you: **a plan file, an issue, or neither?**

and it waits for your answer and your sign-off. Ask for a small change to your project — say, a
different default passage in the sample **[sp only]**, or a new section in your project's
`docs/ai-context/project/overview.md` **[Helm only]** — and run `/authorize` first. Notice what it asks you.

### 4.2 [Both] Plans — proposals, until you rule them

Ask Claude to write a plan for a small change, in `project/plans/<topic>-plan.md`. Every plan:

- opens with **`Status: proposed (<date>)`**. *Proposed* means thinking aloud; it is **never
  authorisation to build**;
- asks its questions in the document, each followed by a line holding only **`=>`**. **You write the
  answers after the `=>`**, in the file; Claude never fills one in. Your words there are the ruling,
  and are quoted, never reworded;
- becomes **`ruled (<date>)`** only when you say so. Only then does work start.

Answer the plan's questions after their `=>` lines and change its status yourself.

**Plans are temporary.** After about eight days a plan is either done or obsolete, and either way it
goes — its rulings are already in `CHANGELOG.md`, because writing that entry is part of finishing the
work. Claude lists the plans past eight days and asks; **deleting one is always your decision**
(`project/plans/README.md`; **[sp only]** `plans-are-temporary` in `docs/ai-context/sp/rules.md`).

### 4.3 [Both] Specifications — the design that outlasts the work

A plan describes one piece of work and then expires. A **specification** describes what something
must *always* do, and is consulted every time it is rebuilt. A model of one is the reader
specification in the Ears-to-Hear project, which this workshop's own lessons are patterned on:

- a status line, and **dated amendments, each with its reason**, newest first;
- the audience, and a vocabulary;
- numbered sections stating requirements, each with **why** — often the failure that produced it;
- **non-goals**: what it deliberately does not do;
- how compliance is **checked**, preferably by a test.

When a spec and the code disagree, the spec wins and the code is wrong.

**Claude drafts; you approve; then Claude moves it into the AI context.** Claude is encouraged to
draft specifications — and examples for prompts, which work the same way. A draft is only a
proposal. Once you have approved it, Claude moves it into `docs/ai-context/project/`, where every
later session reads it as part of the project. Nothing enters the AI context unapproved, because
whatever is there is what Claude will treat as true.

Ask Claude to draft a one-page specification for something small in your project — what a file
must contain, say. Read it, change what is wrong, approve it, and have Claude move it.

### 4.4 [Both] Audits — findings, never verdicts

**[sp only]** Run `/audit-output` on the reader's guide your sample pipeline produced in Lesson 3.
It traces each statement in the output back to what the model was given, and grades how much
latitude the model had to invent (`docs/ai-context/sp/audits-pattern.md`). It writes its record to
`project/audits/`.

**[Helm only]** Human at the Helm ships no audit skills; an audit starts from a checklist you
write. Write three checks for one file in your project — for example, that every rule in
`docs/ai-context/project/rules.md` says *why* — and ask Claude to audit the file against them and
write the record to `project/audits/`, with the date in its filename.

Then read the record. A good record:

- quotes **exact text and locations** for every finding, so you can check each in one step;
- says **how deep the audit went** — what was read in full, what was sampled, what was not examined;
- carries **no verdict**. "Approved", "needs attention" and "production ready" are decisions, and
  decisions are yours.

**Audits are diagnostic, not gates.** You run one when you want to know something; its findings
often become the plan or the issue that authorises the next change.

**[sp only]** The four audit skills, by what you are looking at:

| Looking at | Skill |
|---|---|
| generated output — did the model use what it was given? | `/audit-output` |
| prompts and pipeline YAML | `/audit-prompts` |
| the contracts between steps | `/audit-pipeline` |
| Python plugins | `/audit-code` |

### 4.5 [Both] Issues — a decision about what to work on

An issue is where a piece of work is proposed, discussed and tracked, and its thread keeps the whole
history of a design decision. **Only you create issues** (Lesson 2, 4.5): Claude drafts one into
`tmp/`, you edit it and create it with `gh issue create --body-file`.

Turn one finding from your audit into an issue. Then link it from `project/TODO.md` as `→ #N` — a
link, not a copy.

### 4.6 [Both] `tmp/` — throwaway, but not anyone's to sweep

`tmp/` holds only throwaway files: issue drafts, commit messages from `/stage-commits`, scratch
notes. It is normally kept out of git, so nothing in it reaches a commit by accident.

Two things follow:

- **Nothing that must survive belongs in `tmp/`.** A draft you want to keep becomes a plan, an
  issue, or a document the project's map names.
- **Never clear `tmp/` with a wildcard.** It may hold another session's only copy of a draft.
  Files are deleted by name, by whoever made them, once they have done their job.

### 4.7 [Both] Where everything lives

| What | Where | Lifetime |
|---|---|---|
| Plans | `project/plans/<topic>-plan.md` | about eight days, then deleted on your word |
| Specifications and examples, once approved | `docs/ai-context/project/` | until replaced |
| Audit records | `project/audits/`, with the date in the filename | one per audit |
| Audit checklists | wherever the project keeps its own documents, named in `docs/ai-context/project/index.md` | until replaced |
| Work to do | GitHub issues, linked from `project/TODO.md` | until closed |
| Rulings | `CHANGELOG.md`, or the project's `rules.md` | permanent |
| Throwaway files | `tmp/` | deleted by name when done |

## 5. How you know it worked

- `/authorize` stopped before editing and asked you: plan, issue, or neither.
- Your plan has your answers after its `=>` lines, in your words, and its status is
  `ruled (<date>)` — set by you.
- Your specification is in `docs/ai-context/project/`, and you approved it before it got there.
- Your audit record quotes a location for every finding and contains no verdict.
- Your issue is authored by you and linked from `project/TODO.md` as `→ #N`.
- `CHANGELOG.md` carries the ruling from your plan, dated.

## 6. Non-goals

- Writing an audit checklist of your own.
- Testing prompt changes with `sp tools replay`.
- Deleting plans: the eight-day rule is introduced here, and practised as plans age.

## 7. Teaching this lesson

### Before the day

- **[sp only]** Make sure every participant has a sample-pipeline output from Lesson 3 to audit.
  If some do not, keep a copy of yours they can use.
- **[Helm only]** Have an example three-item checklist ready for participants who cannot think of
  one.
- Read `project/plans/README.md` and `project/audits/README.md` yourself — and, **[sp only]**,
  `docs/ai-context/sp/audits-pattern.md`; participants' questions come from them.

### Introducing each step

| Step | Say | Rough time |
|---|---|---|
| — | "AI writes faster than anyone reads. Today is about writing things down so it stays clear what was proposed, what was found, and what was decided — and by whom." | 5 min |
| 4.1 | "Before Claude changes anything, it should tell you what authorises it and exactly what it will touch — and ask how you want it recorded." | 10 min |
| 4.2 | "A plan is a proposal until you rule on it. You answer its questions after the `=>`, in your own words." | 25 min |
| 4.3 | "A spec is a plan that never expires: the standing description of what something must do. These lessons are written as one." | 10 min |
| 4.4 | "An audit reports what it found, with evidence. It never tells you whether it's good — that's yours." | 25 min |
| 4.5 | "A finding becomes work when you decide it should. That's an issue, and you create it." | 10 min |
| 4.6–4.7 | "`tmp/` is scratch. And here is where everything else lives." | 10 min |

The times are estimates, about an hour and a half in all; correct them from experience.

### Where people get stuck

- **Claude answers its own question after a `=>`.** Delete its answer, and point to the rule: only
  the person deciding writes there.
- **Claude starts building from a `proposed` plan.** Stop it. The status is the point of 4.2.
- **The audit record says "looks good" or "approved".** That is a verdict; ask Claude to remove it
  and state findings only.
- **Someone asks Claude to clean up `tmp/`.** It should delete by name only, files it made itself.
- **Plans pile up.** Show that deleting one loses nothing: `git log` and `git show` still have it.

### Before moving the room on

Run the §5 checks out loud. Ask one pair to read a question from their plan and the answer they
wrote after its `=>`, and another to read a finding from their audit with the location it cites.
