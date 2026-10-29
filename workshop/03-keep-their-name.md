# Keep their name

> When you build on someone else's code, their copyright notice comes with it. Add your name; never remove theirs.

**Time:** 15 minutes

## Goal

Read the one condition of the MIT licence, see why starter templates and forks carry their authors' notices forever, and put more than one copyright holder in a project correctly.

## The case

```bash
uv run python -m nest run 3
```

```text
nest scan case03_template/

LICENSE               MIT · word for word
                      Copyright (c) 2026 Robin Vale
README                [MIT](LICENSE) © 2026 Robin Vale
pyproject.toml        MIT
notices               (none)

  ✓ the licence file, README and manifests agree

starling/cli_base.py          from kestrel-template
kestrel-template is           MIT · Copyright (c) 2019 Kestrel Labs
that notice, in Starling      nowhere
```

Everything agrees, and the scan is happy. But Robin started Starling from kestrel-template, a starter kit by Kestrel Labs, and `starling/cli_base.py` is still their code. Starling's `LICENSE` came from the template too, and Robin replaced Kestrel Labs' name with his own. Open `upstream/kestrel-template/LICENSE` to see what it said.

## MIT's one condition

The MIT licence grants almost everything, then asks one thing:

```text
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
```

The copyright notice is the line with the name on it. Kestrel Labs gave Robin permission on the condition that their notice stays with every copy of their code, including copies inside Starling. Replace the name, and Robin no longer meets the condition, so he no longer has the permission.

ISC and the BSD licences have the same condition in different words. So do most permissive licences.

## Templates, forks and starters

This mistake is common because it feels like housekeeping. You start a project from a template, a fork or a generator, and the first thing you do is put your own name in `LICENSE`. But the template's code is still in your project:

- **A fork** keeps every line of the original until you rewrite it.
- **A starter template** often keeps its scaffolding, its build files and its helpers for years.
- **A generator** may add its own licence notice to the files it writes. Read it before deleting it.

If you rewrite every line the template gave you, its notice can go. Until then, it stays.

## Two names in one licence

The fix is to add, not replace. A licence can carry several copyright lines, one per owner, oldest first:

```text
MIT License

Copyright (c) 2019 Kestrel Labs
Copyright (c) 2026 Robin Vale

Permission is hereby granted, ...
```

Both lines sit above the same permission text, so one licence covers both owners' code. This works when both are under the same licence. When they are not, keep each one's notice in a third-party notices file instead, as chapter 04 does.

## Notices in their own file

Some projects keep their own `LICENSE` to themselves and list everything they borrowed in `THIRD_PARTY_NOTICES.md`: for each source, its name, where it came from, its copyright line and its full licence text. That satisfies MIT too, as long as the notices file ships with the code. The check accepts either way.

A sentence in the README, such as "based on kestrel-template", is a kind credit. It is not the notice the licence asks for.

## Fix the case

In `lab/cases/case03_template/LICENSE`, put Kestrel Labs' copyright line back, above Robin's. Do not remove Robin's: he owns everything he wrote since 2026.

## Check it works

```bash
uv run python -m nest check 3
```

```text
  PASS  LICENSE is still the MIT licence, word for word
  PASS  Robin Vale's copyright line is still there
  PASS  kestrel-template's notice, Copyright (c) 2019 Kestrel Labs, ships with the code
```

## Exercise

Undo your fix, then add a `THIRD_PARTY_NOTICES.md` holding only the line `Copyright (c) 2019 Kestrel Labs`. Run the check. What else does the notice need, and why?

### More to try

- Open a project you started from a template. Is the template's notice still in it?
- Look at the `LICENSE` of a long-lived fork on GitHub. How many copyright lines does it have?
