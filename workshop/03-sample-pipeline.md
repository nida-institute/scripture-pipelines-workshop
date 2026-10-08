# Lesson 3 — The sample pipeline: reading it, checking it, and knowing what it costs

**Status:** proposed (2026-10-07)
**Amendments:** none yet.
**Track:** sp only. Human at the Helm participants skip this lesson.

**Audience.**
- *Scholars:* you will read a pipeline as a description of what happens to a passage — which texts
  are fetched, which analyses come with them, what a model is asked, and from what — and you will
  decide when it runs.
- *Technical participants:* the same, plus the step types, how outputs are named and passed on,
  and how to check a pipeline completely without spending anything.

**Vocabulary.**
- **Pipeline** — a YAML file listing steps in order; each step takes named inputs and produces
  named outputs. YAML is a plain-text format for structured settings.
- **Step** — one operation in a pipeline: fetch a text, save a file, ask a model.
- **Step type** — what kind of operation a step is, given by its `type:` line.
- **Resource** — a text Scripture Pipelines can open by name, such as `SBLGNT` (the Society of
  Biblical Literature Greek New Testament), `WLC` (the Westminster Leningrad Codex of the Hebrew
  Bible) or `BSB` (the Berean Standard Bible).
- **Model** — the large language model a step sends its prompt to, e.g. `gpt-4.1`. Calling one
  costs money.
- **Prompt** — the instructions a model step sends, kept in a `.gpt` file under `prompts/`.
- **Token** — the unit a model provider charges by: roughly three-quarters of an English word.
- **Lint** — checking a pipeline for mistakes without running it.
- **Dry run** — running a pipeline in a mode that resolves every name and path but calls no model.
- **Deliverable / intermediate** — the files a pipeline exists to produce, and the files it writes
  on the way there.

---

## 0. Why this lesson

A pipeline spends your money and writes files in your name, and Claude will happily offer to run
one. Before anyone runs it, you need to be able to say what it will do, which parts cost money,
and whether it is ready. Every one of those can be found out for free.

## 1. The core idea

**Only the model steps cost money, and you decide when they run.** Everything else in a pipeline —
fetching texts, attaching analyses, saving files — is free, and so are the checks (`sp lint`,
`--dry-run`). In the sample, two steps call a model and every other step is free. That ratio is
the point: the engine does the work of putting the right text in front of the model, so the model
is asked about what it was given rather than what it remembers.

## 2. What you start with

- Lessons 1 and 2 done: a project set up with `sp init`, on GitHub.
- The sample pipeline `sp init` wrote: `pipelines/readers-guide.yaml`, with its prompts
  `prompts/readers-guide.gpt` and `prompts/parallel-significance.gpt`, and `docs/tutorial.md`.
- A model API key set with `sp setup` (Lesson 1, 4.2).

The sample's model is `gpt-4.1`, set under `llm_config.model`. Any `gpt` model that `sp models`
lists will do; the workshop has been tested with OpenAI's models.

## 3. What you produce

- The sample's texts available on your machine, each under a licence you agreed to yourself.
- A short written account, in your own words, of what each step does and which steps cost money.
- A clean `sp lint` and a clean `--dry-run`.
- One run, on a passage you chose: a reader's guide and a parallel-significance note in
  `outputs/`, and their intermediates in `intermediate/`.

## 4. Steps

### 4.1 Make the sample's texts available — and agree to their licences yourself

The sample reads three named resources — `SBLGNT`, `WLC` and `BSB` — and the Macula syntax trees
registered on them (`docs/tutorial.md` §2). See what your machine has:

```sh
sp resource list
```

`sp lint` checks that every resource a pipeline names can be opened, and **offers to install what
is missing** (`docs/ai-context/sp/command-line.md`). Each install shows the text's licence and asks
you to agree.

**Agree to licences yourself, in your own terminal.** A licence is an agreement in your name. `sp`
has an option that agrees without asking (`--accept-terms`); Claude must not use it on your
behalf. If Claude proposes it, say no.

`sp resource terms` lists the licence each text was registered under, and whether you agreed.

### 4.2 Read the pipeline — with Claude

Open `pipelines/readers-guide.yaml` and read it with Claude:

> Walk me through `pipelines/readers-guide.yaml` one step at a time. For each step, tell me what it
> does, what it reads, what it produces, and whether it calls a model. Don't run anything.

Read it in this order:

1. **The `description:` at the top** — what the pipeline is for and how to run it.
2. **`llm_config`** — which model the model steps use, and how long an answer they may write.
3. **`variables`** — the settings you can change with `--var`, such as `greek_frequency_cutoff`.
4. **Each step's `description:`** — every step in the sample explains itself.

Then open the two prompts. Each begins with a header saying what it `requires`; check that the
step calling it supplies each one under `prompt.inputs`.

**With your partner** (or with Claude, on your own): each of you explains one step to the other
without looking at Claude's explanation.

### 4.3 The kinds of step

The sample uses six step types. The full list of types, and every key each accepts, is in
`docs/cli-api.json`; `docs/llmflow-language-quickref.md` describes the common ones.

| Type | What it does in the sample | Calls a model? |
|---|---|---|
| `scripture` | Fetches a passage from a named resource — English, Greek or Hebrew — with any analyses asked for under `include:` (morphology, senses, glosses, syntax, frequency) | No — free |
| `save` | Writes something already in hand to a file | No — free |
| `parallel-passages` | Looks the passage up in the UBS Parallel Passages database | No — free |
| `for-each` | Repeats the steps inside it once for each item in a list — here, each parallel, then each chapter | No — free, unless a step inside it calls a model |
| `json` | Assembles a structured record from values already in hand | No — free |
| `llm` | Sends a prompt and its inputs to the model and keeps the answer | **Yes — costs money** |

Two more things you will see:

- **`condition:`** skips a step unless something is true. The sample uses it to fetch the Greek
  *or* the Hebrew, never both, depending on the testament.
- **`output:`** names what a step produces, so a later step can use it as `${name}`. Nothing
  passes between steps any other way.

### 4.4 What costs money — and how much

Only the two `llm` steps cost anything: `reader_guide` and `significance`. Each sends its prompt
and inputs to `gpt-4.1` and pays for the tokens in and the tokens out.

For Matthew 19:1-11, the pipeline's own comment records **13,331 input tokens** for the guide and
**18,699** for the significance. A longer passage, or one with more parallels, sends more. Your
provider's price page turns tokens into money; your provider's usage page shows what a run
actually cost.

**Watch the `for-each` steps when you write your own pipelines.** A model step inside a loop is
paid once per item: a passage with twenty parallels would call it twenty times.

**`sp run` is never run on Claude's initiative.** It is the one command here that costs money, so
it runs only when you say so, each time. A previous "run it" does not cover the next run.

### 4.5 Check it for free: `sp lint` and `--dry-run`

```sh
sp lint --pipeline pipelines/readers-guide.yaml
sp run --pipeline pipelines/readers-guide.yaml --var passage="MAT 19:1-11" --dry-run
```

`sp lint` catches an undeclared variable, an output a step type does not offer, a prompt whose
inputs do not match its header, and a resource this machine cannot open. `--dry-run` resolves
every path and variable and **calls no model**. Claude may run both whenever it likes.

### 4.6 Run it — when you decide to

Choose a passage. References are written with a book code: `MAT 19:1-11`, `MRK 1:40-2:12`,
`PSA 23`. (`docs/ai-context/sp/passage-references.md` lists the forms that work.) An Old Testament
reference runs the Hebrew branch.

Then either run it yourself, or tell Claude explicitly — *"Run the readers-guide pipeline on
MAT 19:1-11."*

```sh
sp run --pipeline pipelines/readers-guide.yaml --var passage="MAT 19:1-11"
```

The two `*_frequency_cutoff` variables set how much help the guide gives: a word is explained when
its lemma (dictionary form) is among the least frequent N% in that corpus. Set them for your own
reading with `--var greek_frequency_cutoff=60`.

### 4.7 Read what it produced

```
outputs/
├── 40019001-40019011-readers-guide.md
└── 40019001-40019011-parallel-significance.md
intermediate/
└── 40019001-40019011/
    ├── english.txt
    ├── greek.json
    ├── greek-analysis.txt
    ├── parallels.json
    └── parallels/
```

`outputs/` holds the deliverables; `intermediate/` holds everything fetched on the way, one folder
per passage, saved so each stage can be read. Commit `outputs/`; `intermediate/` is for reading.

**Check the guide against what it was given.** Pick three statements in the reader's guide — a
parsed form, a gloss, what a participle attaches to — and find the evidence for each in
`greek-analysis.txt` (or `hebrew-analysis.txt`). A statement you cannot trace to the input is the
model speaking from memory.

**The output is a draft.** It has not been reviewed by anyone who knows the text, and it is not
ready for use until a person who does has read and corrected it.

## 5. How you know it worked

- `sp resource list` shows `SBLGNT`, `WLC` and `BSB`, and `sp resource terms` shows that **you**
  agreed to each licence.
- You can name the two steps that cost money, and say why every other step is free.
- `sp lint` reports no errors, and the dry run completes without calling a model.
- `outputs/` holds the guide and the significance note for the passage you chose, with its
  reference in the filenames.
- You traced three statements in the guide to lines in the analysis file — or found one you could
  not trace, and can say what that means.

## 6. Non-goals

- Writing or changing a pipeline or a prompt.
- Choosing between models, or tuning their settings.
- Finding and downloading other datasets — Lesson 4.
- Reviewing the guide as a scholar would. That is the work the guide exists to support, not part
  of this lesson.

## 7. Teaching this lesson

### Before the day

- Remind participants to bring an OpenAI API key (Lesson 1, §2).
- Run `sp lint` on the sample on a clean machine shortly before, so you know how long the text
  installs take and what the licence prompts look like.
- Run the pipeline once on the passage you will demonstrate, and note what it cost from your
  provider's usage page, so you can tell the room a real figure.
- Pick two passages for the room: one New Testament with parallels (Matthew 19:1-11 is the
  documented example) and one Old Testament.

### Introducing each step

| Step | Say | Rough time |
|---|---|---|
| — | "A pipeline spends your money and writes files in your name. Today you'll learn to say exactly what one will do before it does it." | 5 min |
| 4.1 | "The sample reads three texts. Installing them means agreeing to their licences — and that agreement is yours, not Claude's." | 15 min |
| 4.2 | "Read the pipeline the way you'd read a method section: what goes in, what's done to it, what comes out. Ask Claude to walk you through it — and tell it not to run anything." | 25 min |
| 4.3 | "Six kinds of step. Only one of them calls a model." | 10 min |
| 4.4 | "Two steps cost money. Here is roughly how much, and here is the trap: a model step inside a loop." | 10 min |
| 4.5 | "Two checks that cost nothing. Run them every time before you run the real thing." | 10 min |
| 4.6 | "Now you choose a passage and decide to run it. Notice that you have to say so — Claude won't do it on its own." | 15 min |
| 4.7 | "Read the guide against what the model was given. Anything you can't trace to the input came from its memory." | 20 min |

The times are estimates, about two hours in all; correct them from experience.

### Where people get stuck

- **`sp lint` reports a resource it cannot open.** The text is not installed. Let `sp lint` offer
  to install it, in the participant's own terminal, so they see and agree to the licence.
- **The run fails to authenticate with the model.** The OpenAI key is missing or mistyped. `sp setup`
  in the participant's own terminal.
- **A reference is not recognised.** Book names must be codes (`MAT`, not `Matthew`), and a range
  may cross a chapter but not a book — see `passage-references.md`.
- **Claude offers to run the pipeline.** Good: it should offer. It should not run it until told.
  If it runs one unasked, stop and discuss it in the room — it is the failure this lesson is about.
- **`outputs/` is empty after a run.** Read the run's last lines: a failure in an earlier step stops
  the run before the model steps write anything. The `intermediate/` folder shows how far it got.

### Before moving the room on

Run the §5 checks out loud. Before 4.6, have one pair state which steps will cost money and why the
rest are free. After 4.7, ask a pair to read out one statement from their guide and the line in the
analysis file that supports it.
