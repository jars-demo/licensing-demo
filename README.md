# Whose code is it anyway?

A hands-on open source licensing workshop. Eight chapters, each explaining one idea in depth, each with a real licensing mistake in Starling, a small open source notebook, for you to fix: no licence, a licence declared three different ways, a template's missing name, a copied Apache file, a font with no papers, a borrowed logo, a GPL package two levels down and a hosted AGPL fork. **Maggie**, the magpie who collects shiny things and keeps their papers, quizzes you along the way.

**Workshop site:** [licensing.jishanahmed.in](https://licensing.jishanahmed.in)

> This workshop teaches engineering practice, not law. For anything that matters legally, ask a lawyer.

## Quick start

You need [uv](https://docs.astral.sh/uv/) and git. uv installs Python 3.13 for you. The lab uses the Python standard library only: no accounts, no API keys, no Docker.

```bash
git clone https://github.com/jars-demo/licensing-demo.git
cd licensing-demo/lab
uv sync
uv run python -m nest run 1
```

## How a case works

| Command                              | What it does                                                |
| ------------------------------------ | ----------------------------------------------------------- |
| `uv run python -m nest list`         | every case, and which ones are fixed                        |
| `uv run python -m nest run N`        | show case N's mistake, the way a scanner sees it            |
| `uv run python -m nest check N`      | check your fix                                              |
| `uv run python -m nest hint N`       | a nudge from Maggie                                         |
| `uv run python -m nest scan PATH`    | scan any project on disk: LICENSE, README and manifests     |
| `uv run python -m nest compat [A B]` | can code under licence A go into a project under licence B? |

Each case is a folder in `lab/cases/`: a tiny project with one mistake. Fix the files in it. `upstream/` inside a case stands in for the other projects Starling borrowed from. Start a case over with `git restore cases/` from `lab/`.

Every check reads the project the way a licence scanner would: the exact licence words, the notices that ship, the packages that get installed. A plausible but wrong fix does not pass.

## The chapters

| #   | Chapter                                                               | The case                                |
| --- | --------------------------------------------------------------------- | --------------------------------------- |
| 01  | [No licence, no permission](workshop/01-no-licence-no-permission.md)  | The repo nobody could use               |
| 02  | [One licence, three places](workshop/02-one-licence-three-places.md)  | Three answers to one question           |
| 03  | [Keep their name](workshop/03-keep-their-name.md)                     | The name that went missing              |
| 04  | [Copying Apache code](workshop/04-copying-apache-code.md)             | The file that forgot where it came from |
| 05  | [Fonts, icons and images](workshop/05-fonts-icons-and-images.md)      | The font with no papers                 |
| 06  | [Names and logos](workshop/06-names-and-logos.md)                     | The partner nobody signed up            |
| 07  | [What you ship](workshop/07-what-you-ship.md)                         | The copyleft two levels down            |
| 08  | [Copyleft over the network](workshop/08-copyleft-over-the-network.md) | The fork that hid its source            |

About two and a quarter hours in all. The last chapter ends with a checklist.

## Layout

```text
lab/cases/            the eight cases: one small project with one licensing mistake each
lab/nest/             the CLI, the scanner, the checks and the compatibility table
lab/nest/texts/       canonical licence texts the scanner compares against
lab/tests/            every case fails as shipped, passes with tests/solutions/, rejects wrong
                      fixes, and every output quoted in a chapter is real
workshop/             the chapters, in Markdown
frontend/             the workshop site (Next.js, static export), which renders workshop/
```

Run the lab's tests with `cd lab && uv run pytest`. The solutions are in `lab/tests/solutions/`: peek only when truly stuck.

## Run the site locally

```bash
cd frontend
npm ci
npm run dev
```

`npm run verify` runs lint, type checks, formatting, unit tests and a production build. For the browser tests, serve the build with `npx serve out -l 3115`, then run `E2E_BASE_URL=http://localhost:3115 npm run test:e2e`.

## Deploy

The site is a static export. Import the repository in [Vercel](https://vercel.com/new) and deploy: the root `vercel.json` declares one service, `frontend` (Next.js in `frontend/`), routes every path to it, and sets clean URLs and the security headers. The lab and the cases are Python you run on your own machine, not services, so Vercel never builds them. There are no settings to change.

## License

[MIT](LICENSE) © 2026 Jishanahmed AR Shaikh. Starling, Kestrel Labs, Gustwind, Wren Sans, Feathery, Driftwood and inkpot are made up for the cases.
