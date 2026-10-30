# What you ship

> Your dependencies' licenses become your problem the moment you ship them, including the ones you never chose.

**Time:** 20 minutes

## Goal

Know when a dependency's license applies to you, tell permissive, weak copyleft, strong copyleft and source-available licenses apart, find the package two levels down that nobody chose, and fix it without losing the feature.

## The case

```bash
uv run python -m nest run 7
```

```text
prettyout 2.1.0       MIT             tables
  colorwheel 1.4.0    GPL-3.0-only    colour   ✗ not permissive
click-lite 3.0.2      BSD-3-Clause    commands

Starling is MIT. Packages it ships that are not permissive: 1
  colorwheel 1.4.0: GPL-3.0-only, pulled in by prettyout
```

`starling --table` shows notes as a coloured table. Robin asked for prettyout, which is MIT. Its newest version pulls in colorwheel, which is GPL-3.0. Robin ships Starling as a single download with its dependencies inside. The packages, their licenses and what they need are in `index.json`.

## When a dependency's license applies

Most open source licenses set their conditions on **distribution**: giving a copy to someone else. If Starling only lists `prettyout` in `requirements.txt` and users install it themselves, Starling distributes none of it. When Starling ships as a single executable, a Docker image or a bundled frontend, it distributes every dependency inside, and must meet every one of their conditions.

That is why a JavaScript bundle, a desktop app and a container image need a license review, and a library on PyPI mostly does not.

## Four families

| Family           | Examples                        | What shipping it asks                                    |
| ---------------- | ------------------------------- | -------------------------------------------------------- |
| Permissive       | MIT, BSD, ISC, Apache-2.0       | Keep the notices                                         |
| Weak copyleft    | MPL-2.0, LGPL-3.0               | Share the source of that component, and changes to it    |
| Strong copyleft  | GPL-2.0, GPL-3.0, AGPL-3.0      | Share the whole program's source, under the same license |
| Source-available | BUSL-1.1, SSPL-1.0, Elastic-2.0 | Not open source: limits on production or hosted use      |

And one more: **no license, or UNKNOWN**. That means no permission at all (chapter 01). Treat it as a blocker until you find the real license.

## Transitive dependencies

Nobody chose colorwheel. Robin chose prettyout, and prettyout 2.1.0 chose colorwheel. A real project has hundreds of these. You are responsible for all of them, so read the full tree, not just your own requirements:

```bash
uvx pip-licenses --from=mixed --order=license
npx --yes license-checker-rseidelsohn --summary
```

Run them in CI, and fail the build when a new license appears outside the list you have approved. A lockfile makes the tree exact, so the check is repeatable.

## Your options

When a dependency's license does not fit, you have four ways out:

1. **Pin a version** that does not bring it in, if that version still does the job.
2. **Swap the package** for one with a license that fits.
3. **Stop shipping it**: let users install it themselves, if that is honest about how the program works.
4. **Change your license** to one that fits the dependency, if you own all your code and want to.

Starling wants to stay MIT and keep coloured tables, so options 1 and 2 are the candidates. Read `index.json` carefully: some packages that give tables and colour have licenses that would only move the problem.

## Fix the case

Edit `lab/cases/case07_deps/requirements.txt`. Starling must still get both `tables` and `colour`, every requirement must be pinned to a version in the index, and nothing it ships may be copyleft, source-available or unlicensed.

## Check it works

```bash
uv run python -m nest check 7
```

```text
  PASS  every requirement is pinned and found in the index
  PASS  nothing Starling ships is copyleft, source-available or unlicensed
  PASS  Starling still gets its tables and colour
  PASS  Starling's LICENSE is still MIT
```

## Exercise

Try `prettyout==1.9.0`, then `richgrid==5.0.0`, and run the check after each. Write down in one line why each one fails.

### More to try

- Run `pip-licenses` or `license-checker` on a project of yours. How many licenses appear? Do you recognise them all?
- Read the license of a package marked BUSL-1.1. What is its "change date", and what happens then?
