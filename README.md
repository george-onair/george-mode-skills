# george-mode

**Skills that make coding agents prove their work: every "done" is split into separate, checkable evidence lines instead of one vague claim.**

- **Who it's for:** people running Claude Code, Codex, Cursor or similar agents on real repos who are tired of "done" meaning "I wrote a file".
- **Works with:** any host that loads `SKILL.md` folders (Claude Code, OpenAI Codex, Cursor, oh-my-pi, Grok CLI, Google Antigravity).
- **Requires:** Python 3, standard library only. MIT licensed.

## 30-second quickstart

```sh
git clone https://github.com/george-onair/george-mode-skills.git
cd george-mode-skills
python3 scripts/install.py           # dry run: prints the symlinks it would create
python3 scripts/install.py --apply   # install (never overwrites existing paths)
```

Then start a task with `/george-mode` (or `$george-mode`, depending on your host).

## What you get back

Instead of "Done!", the agent reports each acceptance layer on its own line and may not claim a higher layer from a lower one. The shape of a report (illustrative format, not real project data):

```text
Result: login redirect fixed.
- File exists:      src/auth/redirect.ts changed
- Checks pass:      unit tests for auth run and pass
- Real run:         not done (no staging host available)
- External state:   not applicable
Open: verify on staging before release.
```

A real command you can run right now, from the repo root:

```sh
$ python3 scripts/verify_package.py
{
  "passed": true,
  "errors": [],
  "scope": "package integrity, not host runtime"
}
```

Note the `scope` line: even the integrity check says what it does *not* prove.

**Related:** for small standalone skills (a `SKILL.md` debugger, a minimal MCP server plan, a repo license preflight), see [george-onair/claude-code-skills](https://github.com/george-onair/claude-code-skills).
**Updates:** [@George_ONair on X](https://x.com/George_ONair).

The full set is 11 skills that run a **decide, act, verify, reflect** loop: register goals, assumptions, falsifiers, predictions and stop conditions before high-stakes choices, and verify real behavior before claiming "done".

## Skills

| Skill | Purpose |
|---|---|
| `george-mode` | Entry point. Routes a task by weight; holds the authorization and evidence rules. Invoke explicitly (`/george-mode`, `$george-mode`). |
| `george-investigate` | Read-only investigation: project survey, raw-evidence checks. |
| `george-decide` | Decision loop for important/irreversible choices (goal, assumptions, falsifiers, predictions, stop conditions). |
| `george-design` | Structural investigation, competing designs, adversarial review. |
| `george-engineer` | Features, bugs, refactors, performance, forensics, visual parity, PRs. |
| `george-evaluate` | Blind tests, perf-number audits, skill behavior checks. |
| `george-orchestrate` | Multi-phase plans, PR babysitting/landing, pausing and resuming; per-host sub-agent adapters. |
| `george-deliver` | Build and configure an already-decided deliverable to completion. |
| `george-verify` | Acceptance on the real surface, host adaptation, platform read-back. |
| `george-reflect` | Compare predictions with outcomes, extract bounded lessons. |
| `george-resume` | Resume long tasks and handoffs without losing goal or scope. |

Self-contained method references: [`decision-loop.md`](skills/george-mode/references/decision-loop.md) and [`verify-before-deliver.md`](skills/george-mode/references/verify-before-deliver.md).

## Theory toolkit

[`theory/`](theory/) holds the full method behind the skills: *Reflexive Practice: Private Canon* (the complete theory text), a loop operating manual, AI collaboration instructions, nine blank project-dossier templates, a field and numbering specification, sources and revision notes, and a blank eight-sheet loop workbook (`.xlsx`). Start with [theory/00_getting-started.md](theory/00_getting-started.md). The templates and workbook are blank; no real project data is included.

## Install

Requires Python 3 (standard library only). From the package root:

```sh
python3 scripts/verify_package.py        # integrity check against PACKAGE-MANIFEST.json
python3 scripts/install.py               # dry run: shows planned symlinks
python3 scripts/install.py --apply       # create symlinks
python3 scripts/install.py --remove --apply   # uninstall (only links pointing here)
```

The installer symlinks each `skills/george-*` folder into `~/.agents/skills`, `~/.codex/skills`, `~/.cursor/skills`, `~/.gemini/config/skills`, and adds an OMP command alias. It never overwrites an existing path. Use `--home DIR` to target a different home.

Manual install (e.g. **Claude Code**): copy or symlink all `skills/george-*` folders together into `~/.claude/skills/` (or a project's `.claude/skills/`). Keep them as siblings — skills link to each other with relative paths.

Optional: the GitHub PR watcher in `skills/george-orchestrate/tools/pstack/` needs Bun and `gh`; run `bun install --frozen-lockfile` there first.

## Tests

```sh
python3 -m unittest discover -s tests
cd skills/george-orchestrate/tools/pstack && bun install --frozen-lockfile && bun test
```

## Attribution

Large parts (the 24 engineering principles, engineer/design/evaluate/orchestrate playbooks, and the watch-pr tool) are adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (@poteto), MIT License. See [NOTICE.md](NOTICE.md) and [third_party/pstack-LICENSE.txt](third_party/pstack-LICENSE.txt).

## License

MIT. See [LICENSE](LICENSE). Portions adapted from pstack keep their original MIT notice in [NOTICE.md](NOTICE.md).
