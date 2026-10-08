# Open decisions

**How it works.** Answer inline after a `=>`. **Only the Captain writes after a `=>`.** Once
answered, the answer is applied to the workshop materials in his words and the item leaves this
file.

**What belongs here.** Only decisions the Captain has to make for the workshop. Anything answerable
from the rules, from a prior ruling, or by checking is answered and not posed here.

---

## G1 — gates in Lesson 5

Lesson 5 (`workshop/05-drift.md`, 4.3) teaches that neither `sp init` nor Helm's `/install` adds
any gates, so on a participant's machine every rule is only an instruction. The question is
whether participants should add gates themselves in that lesson.

**Concretely, this is what they would add** to the `permissions` block of
`~/.claude/settings.json` — the file they already edit in Lesson 2 for the agent's `env` block:

```json
"permissions": {
  "deny": [
    "Bash(git commit:*)",
    "Bash(git push:*)",
    "Bash(gh issue create:*)",
    "Bash(gh pr create:*)",
    "Bash(gh pr merge:*)"
  ],
  "ask": [
    "Bash(sp run:*)"
  ]
}
```

**What each does.**

- **`deny`** — Claude cannot run the command at all. These five are the acts ruled the human's
  alone: issues (A), commits and pushes (B), pull requests (F), and merging. A permission rule
  governs only what *Claude* runs, so the participant's own terminal is untouched; that is where
  they run these themselves.
- **`ask`** — Claude must show you the command and wait. `sp run` goes here rather than under
  `deny` because `CLAUDE.md` allows Claude to run a pipeline when explicitly told to; the prompt
  makes each run a decision. Helm participants leave this line out.

**What it costs.** One edit to a file participants already have open, and about ten minutes of the
lesson. The exercise becomes concrete: add the block, restart, ask Claude to push, and watch it be
refused.

**What it does not do.** A rule matches the way a command begins, so a command written differently
may not match; and `--accept-terms` on `sp resource add` cannot be singled out this way, so
agreeing to licences stays an instruction. The gates close the common path, not every path.

**Bearing on it.** `docs/ai-context/sp/rules.md`, "Rules a gate stops before the act", names
`Bash(gh issue create:*)`, `Bash(git push:*)` and `Bash(gh pr merge:*)` as `ask` gates. `deny` is
stricter, to match rulings A, B and F, under which the AI does not do these at all rather than
does them after asking.

=>

---

## N1 — the catalog's name and link, for Lesson 6

The catalog lesson needs one name and one link. Three are in use:

- **"Awesome Bible Resources"** — the Captain's name for it in this session;
- **"Awesome Biblical Data"** and `github.com/nida-institute/awesome-biblical-data` — the
  repository's own README title and its git remote;
- **"Awesome Biblical Resources"** and `github.com/nida-institute/awesome-biblical-resources` —
  `LLMFlow/docs/why-scripture-pipelines.md:67,290`.

If the current one is `awesome-biblical-data`, the LLMFlow document is stale and goes in the
collab note.

=>
