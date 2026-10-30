# One license, three places

> The license file is the law. The README and the manifests describe it, and they must say the same thing.

**Time:** 15 minutes

## Goal

Know the three places a project declares its license and who reads each one, write license names as SPDX identifiers, and catch the defaults that quietly declare the wrong license.

## The case

```bash
uv run python -m nest run 2
```

```text
nest scan case02_disagree/

LICENSE               Apache-2.0 · word for word
                      (no copyright line)
README                MIT, so do what you like.
pyproject.toml        MIT License
web/package.json      ISC
notices               (none)

  ✗ README's License section names MIT, LICENSE is Apache-2.0
  ✗ README's License section does not link to LICENSE
  ✗ pyproject.toml: "MIT License" is not an SPDX identifier (use "MIT")
  ✗ web/package.json says ISC, LICENSE is Apache-2.0
```

Robin moved Starling to Apache-2.0 and replaced `LICENSE`. Everything else still says something different. One project, three answers.

## Three places, three readers

| Where                                          | Who reads it                                          | What it must hold                                               |
| ---------------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------- |
| `LICENSE`                                      | Courts, GitHub, license scanners                      | The full license text, unmodified                               |
| `README.md`                                    | People deciding whether to use the project            | A License section naming the same license, linking to `LICENSE` |
| `pyproject.toml`, `package.json`, `Cargo.toml` | PyPI, npm, crates.io and every scanner a company runs | The license's SPDX identifier                                   |

`LICENSE` is the legal one. When the three disagree, a careful user has to stop and ask which is true, and most will simply pick another project. A company's license scanner reads only the manifests. If `package.json` says ISC, the scanner records ISC, whatever the license file says.

## SPDX identifiers

SPDX is a standard list of short license names. Tools match these exactly, so `MIT License`, `Apache 2`, and `apache2` are all wrong to a machine, even though a person understands them.

| License                          | SPDX identifier    |
| -------------------------------- | ------------------ |
| MIT                              | `MIT`              |
| Apache License 2.0               | `Apache-2.0`       |
| BSD 3-Clause                     | `BSD-3-Clause`     |
| GNU GPL 3.0, only that version   | `GPL-3.0-only`     |
| GNU GPL 3.0 or any later version | `GPL-3.0-or-later` |
| Mozilla Public License 2.0       | `MPL-2.0`          |

The older `GPL-3.0` id is deprecated because it does not say whether later versions are allowed. Write `-only` or `-or-later`.

## The defaults that lie

Two common ways a project ends up declaring a license nobody chose:

- **npm's default.** `npm init` writes `"license": "ISC"` into every new `package.json`. Unless you change it, your frontend says ISC.
- **Copied manifests.** A `pyproject.toml` copied from another project brings its license with it.

Private packages need the field too. `"private": true` stops npm publishing the package, but scanners still read the license of everything in the repository.

## How to write each one

In `pyproject.toml`, under `[project]`. This form comes from PEP 639 and needs hatchling 1.27 or setuptools 77 or later to build:

```toml
license = "Apache-2.0"
```

In `package.json`:

```json
"license": "Apache-2.0"
```

In the README, as the last section, with a link people can follow:

```text
## License

[Apache License 2.0](LICENSE) © 2026 Robin Vale
```

## Fix the case

Robin chose Apache-2.0, so `LICENSE` is the truth. Leave it alone and bring the other three into line:

1. In `pyproject.toml`, write the SPDX identifier for Apache 2.0.
2. In `web/package.json`, replace npm's `ISC`.
3. Rewrite the README's License section to name Apache 2.0, and only that, and link to `LICENSE`.

## Check it works

```bash
uv run python -m nest check 2
```

```text
  PASS  LICENSE is still Apache-2.0, the license Robin chose
  PASS  pyproject.toml declares the SPDX id Apache-2.0
  PASS  web/package.json declares Apache-2.0
  PASS  the README's License section names Apache 2.0, and only that
  PASS  the README's License section links to LICENSE
```

## Exercise

Change `LICENSE` to the MIT text instead, so it matches the old README, and run the check. Why is that the wrong fix, even though everything would then agree?

### More to try

- Search your own repositories for `"license": "ISC"` and ask whether you meant it.
- Look at the "About" box of a large GitHub project. GitHub shows the license it detected from the `LICENSE` file, not from the README.
