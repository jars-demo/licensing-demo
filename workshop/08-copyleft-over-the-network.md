# Copyleft over the network

> The AGPL closes the web service gap: change an AGPL program and let people use it online, and you must offer them its source.

**Time:** 20 minutes

## Goal

Understand why the GPL does not reach a program that only runs on your server, what the AGPL adds, when it applies and when it does not, and how to meet it: keep the licence, and link to the source of the exact version you run.

## The case

```bash
uv run python -m nest run 8
```

```text
vendor/inkpot/LICENSE     MIT · Copyright (c) 2026 Robin Vale
upstream/inkpot/LICENSE   AGPL-3.0
vendor/inkpot/CHANGES.md  modified by Robin Vale
deploy/site.toml          source_url = ""
templates/footer.html     no link to the source
```

Starling Cloud is Starling in the browser. Its notes sync through a copy of inkpot, an AGPL-3.0 sync server, in `vendor/inkpot/`. Robin changed it (see `CHANGES.md`) and, to keep the repository tidy, replaced its licence with MIT and his own name. The site gives users no way to get the source.

## You cannot change someone else's licence

Only the copyright owner can relicense code. Robin owns his changes to inkpot, but not inkpot. Putting MIT on the folder does not make it MIT; it only misleads everyone who reads it, and it breaks the AGPL's own conditions, which require keeping its licence and notices. The first fix is to put the real licence back.

## The gap the GPL leaves

The GPL's conditions apply when you **convey** the program: give someone a copy. A web service gives nobody a copy. Users send requests and get pages back, while the program stays on the server. So a company can change GPL software, run it as a service, and never share its changes. Many people call this the SaaS loophole.

## What the AGPL adds

The AGPL is the GPL plus one section. Section 13 says that if you **modify** the program, and users **interact with it remotely** over a network, your modified version must offer those users its complete source code.

| Situation                                                                    | AGPL source offer needed?                                          |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| You run unmodified AGPL software, such as a database server, behind your app | No. You changed nothing, and your app's own code is not part of it |
| You change AGPL software and run it only for yourself                        | No. Nobody else interacts with it                                  |
| You change AGPL software and users reach it over the network                 | Yes. Offer them the source of your version                         |
| You distribute AGPL software, changed or not                                 | Yes, as with the GPL                                               |

Starling Cloud is the third row.

## Meeting section 13

The offer must be prominent and must lead to the source of the version users are actually talking to:

- **Link to your source, not upstream's.** Upstream does not have Robin's changes. The link must reach the code with the batching and the health endpoint in it.
- **Keep it current.** A tag or commit for each deployed version is ideal: the source must match what runs.
- **Put it where users are.** A footer link on every page, or a "Source" item in the app's menu, is the common way.
- **Keep the AGPL on the AGPL code.** Robin's own code in Starling Cloud can stay MIT. The combined service is covered by the AGPL where it includes inkpot, so publish the source of the whole service if the parts cannot be separated.

## Fix the case

In `lab/cases/case08_agpl/`:

1. Copy `upstream/inkpot/LICENSE` back over `vendor/inkpot/LICENSE`.
2. In `deploy/site.toml`, set `source_url` to the public repository of Robin's version. Any public `https` repository will do for the lab, but not upstream inkpot.
3. In `templates/footer.html`, add a link whose `href` is `{{ source_url }}`, so every page offers the source.
4. Leave Starling Cloud's own `LICENSE` as MIT.

## Check it works

```bash
uv run python -m nest check 8
```

```text
  PASS  vendor/inkpot/ is under AGPL-3.0 again, word for word
  PASS  deploy/site.toml points source_url at the source of your version
  PASS  every page footer links to that source
  PASS  the rest of Starling Cloud keeps its MIT licence
```

Then run `uv run python -m nest list`. All eight should say `fixed`.

## The checklist

Take these with you. Each one is a chapter.

1. Every repository gets a licence file with the exact, canonical text. No licence means no permission.
2. Fill in the copyright line with a real name and year, and leave every other word alone.
3. Declare the same licence in `LICENSE`, the README and every manifest, as an SPDX identifier.
4. When you build on someone's code, keep their copyright notice. Add your name; never replace theirs.
5. Copying Apache-2.0 code: ship the licence, keep the headers, say what you changed, and carry their NOTICE lines.
6. Fonts, icons and images have licences. Ship each licence next to the asset it covers.
7. A licence never grants a trademark. Use other products' names and logos to say what you work with, never to claim endorsement.
8. Read the licence of every dependency you ship, including the ones two levels down, and check them in CI.
9. GPL code in something you distribute makes the whole thing GPL. AGPL code you change and run online must offer its source.
10. Only the owner can change a licence. When in doubt, ask the author, and for anything that matters legally, ask a lawyer.

## Exercise

Set `source_url` to `https://github.com/inkpot-sync/inkpot` and run the check. Upstream's source is public, so why is it not enough?

### More to try

- Run `uv run python -m nest compat AGPL-3.0 MIT` and `uv run python -m nest compat` to see the whole table.
- Find a well-known AGPL project and look at its hosted version. Where does it link to its source?
