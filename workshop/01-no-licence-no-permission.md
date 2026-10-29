# No licence, no permission

> Code with no licence is not free to use. It belongs to its author, and everyone else needs permission.

**Time:** 15 minutes

## Goal

Understand what copyright gives an author by default, why a public repository is not open source on its own, what a licence actually does, and how to add one properly: the exact text, a real copyright line and the right identifier.

## The case

```bash
uv run python -m nest run 1
```

```text
nest scan case01_no_licence/

LICENSE               (none)
README                (no License section)
pyproject.toml        (none)
notices               (none)

  ✗ no LICENSE file: the code is 'all rights reserved' and nobody may reuse it
  ✗ README has no License section
  ✗ pyproject.toml declares no licence
```

Robin Vale wrote Starling, a tiny command-line notebook, and put it on GitHub. The README says "Starling is open source, so use it however you like!" Nothing else does. Open `lab/cases/case01_no_licence/` and look for a licence. There is none.

## Copyright is automatic

In almost every country, the moment you write code, you own the copyright in it. You do not register anything or add a © sign. Copyright gives the author, and only the author, the right to copy the work, change it and share it.

So the default for any code is **all rights reserved**. Nobody else may copy, modify or redistribute it, even if they can see it.

## Public is not open source

Publishing a repository lets people read the code. GitHub's terms of service add a little more: other users may view and fork a public repository on GitHub. That is all. They may not copy the code into their own project, ship it in a product or publish a changed version elsewhere.

A sentence in a README such as "use it however you like" does not fix this. It is vague: may people sell it, change it, remove your name? Lawyers at the companies who might use Starling will not guess, and careful developers will not touch it.

## What a licence does

A licence is the author giving permission in advance, in writing, on conditions everyone can read. Open source licences give everyone the same permission: use, copy, change and share, including commercially. They differ in what they ask in return.

| Licence    | In one line                                                     | Choose it when                                                |
| ---------- | --------------------------------------------------------------- | ------------------------------------------------------------- |
| MIT        | Do anything, keep the notice                                    | You want the most people to use it with the least friction    |
| Apache-2.0 | MIT plus a patent licence, a NOTICE file and stated changes     | Companies will adopt it, or patents worry you                 |
| GPL-3.0    | If you share changed versions, share their source under GPL too | You want improvements to stay open                            |
| AGPL-3.0   | GPL, and running it as a web service counts as sharing          | It is a server and you want the same rule for hosted versions |

There is no wrong answer here, only a choice. Robin wants MIT: short, well known and easy to follow.

## The exact text, not from memory

Tools and lawyers recognise a licence by its exact words. Never type one from memory or "tidy it up". Get the canonical text:

```bash
gh api licenses/mit --jq .body
```

You can also copy it from [choosealicense.com](https://choosealicense.com/licenses/mit/) or the [SPDX licence list](https://spdx.org/licenses/MIT.html). The case uses the same text, in `lab/nest/texts/MIT.txt`.

## The copyright line

The MIT text starts with a template line: `Copyright (c) [year] [fullname]`. Fill it in with the year the code was first published and the name of whoever owns it, then leave every other word alone.

- **Whose name?** The author's, or their employer's if they wrote it as part of their job. For a project with many contributors, `Robin Vale and contributors` is common.
- **Which year?** The year of first publication. Some projects write a range, such as `2024-2026`. Both are fine. A missing year is not.

## The identifier

Every licence has a short, exact name from the SPDX list: `MIT`, `Apache-2.0`, `GPL-3.0-only`. Package managers read it from the manifest. In `pyproject.toml` it is one line under `[project]`:

```toml
license = "MIT"
```

Chapter 02 is all about these identifiers.

## Fix the case

In `lab/cases/case01_no_licence/`:

1. Create `LICENSE` with the MIT text, and fill in the copyright line for Robin Vale and 2026.
2. Add `license = "MIT"` to `pyproject.toml`, under `[project]`.

## Check it works

```bash
uv run python -m nest check 1
```

```text
  PASS  a LICENSE file at the root of the project
  PASS  LICENSE is the MIT licence, word for word
  PASS  its copyright line names Robin Vale and a year
  PASS  pyproject.toml declares license = "MIT"
```

Then run `nest run 1` again. The scan now has one complaint left: the README has no License section. Chapter 02 deals with it.

## Exercise

Add a sentence to the end of the MIT text in your fix, such as "Not for commercial use.", and run the check. Why does a single extra sentence mean the file is no longer the MIT licence? Then remove it again.

### More to try

- Run `uv run python -m nest scan ..` from `lab/` to scan this workshop itself, then scan a repository of your own.
- Find a project you use that has no licence. Open an issue that asks, politely, which licence the author intends.
