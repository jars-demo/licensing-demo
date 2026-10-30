# AGENTS.md

Guidance for coding agents and developers. Humans: start with [README.md](README.md).

## What this is

"Whose code is it anyway?": eight chapters, each a licensing idea explained in depth and a real mistake in Starling, a small open source project, that shows it. `lab/` holds the cases and the checker; `workshop/` the chapters; `frontend/` the site.

## Map

```text
lab/cases/caseNN_*/         one small project with one deliberate licensing mistake each
lab/nest/licenses.py        recognise a license from its exact words; copyright lines
lab/nest/project.py         what a project declares: LICENSE, README section, manifests, notices
lab/nest/scan.py            `nest scan PATH`, which works on any folder
lab/nest/checks.py          check_NN(root) -> [(label, ok)]; reads the project like a scanner
lab/nest/runs.py            `nest run N`: each case's symptom
lab/nest/deps.py            resolves case 07's requirements against its index.json
lab/nest/compat.json        the table behind `nest compat` and the site's explorer
lab/tests/                  each case fails as shipped, passes with tests/solutions/,
                            rejects plausible wrong fixes (test_mutations.py), and every
                            output quoted in a chapter is real (test_chapters.py)
frontend/src/lib/site.ts    cases and quoted output: a unit test finds each line in the chapters
frontend/src/lib/compat.ts  mirrors lab/nest/compat.json; a unit test keeps them equal
frontend/src/lib/maggie.ts  Maggie's note and quiz for each page
frontend/src/lib/tokens.ts  colour pairs; a test checks them against globals.css and WCAG AA
vercel.json                 one Vercel service, frontend/ (Next.js static export), public at /
```

## Commands

```bash
cd lab && uv sync && uv run pytest && uv run ruff check . && uv run ruff format --check .
cd frontend && npm ci && npm run verify
cd frontend && npx serve out -l 3115   # then, in another shell:
E2E_BASE_URL=http://localhost:3115 npm run test:e2e
```

Set `CHROMIUM_PATH` to use an installed Chromium if Playwright's own is missing.

## Rules

1. **The mistakes are the product.** Never fix a case in `lab/cases/`. Change a case, its check and its solution together, and keep `test_case_is_broken_as_shipped` passing.
2. **Checks test the promise.** Recognise licenses by their exact words, read the notices that actually ship, resolve the real dependency tree. Add a wrong fix to `test_mutations.py` when you find one that slips through.
3. **License texts are canonical.** `lab/nest/texts/` holds the texts from `gh api licenses/<id>`. Never edit them.
4. **Standard library only** in `lab/`. Pin exact versions everywhere else.
5. **Every output is real.** Output in chapters and on the site comes from real runs, and tests compare them. Rerun and update both together.
6. **Colours mean one thing.** Green is allowed or a pass, blue is allowed with conditions, red is not allowed or a failure, teal is where you are. Always pair colour with an icon and a word.
7. **Not legal advice.** Teach practice, name the uncertainty, and send legal questions to a lawyer.
8. **Writing style.** Plain English, short sentences, no em dashes. Conventional Commits with imperative, capitalised subjects.
