# Copying Apache code

> Apache-2.0 asks for four things when you share its code: the license, the notices, a note of your changes, and its NOTICE file.

**Time:** 20 minutes

## Goal

Read section 4 of the Apache License 2.0 and turn it into a short list you can follow, understand the NOTICE file and the patent license, and copy a file from an Apache project into an MIT project correctly.

## The case

```bash
uv run python -m nest run 4
```

```text
upstream backoff.py       # Copyright 2023 The Gustwind Authors
                          # SPDX-License-Identifier: Apache-2.0
starling/backoff.py       (no header)
what changed              jitter added, not recorded
Apache 2.0 text           not shipped
Gustwind NOTICE lines     none
```

Starling retries syncs with a backoff function copied from Gustwind, an Apache-2.0 library. Robin added random jitter to it, and on the way he dropped its two header lines. Compare `starling/backoff.py` with `upstream/gustwind/gustwind/backoff.py`, and read `upstream/gustwind/NOTICE`.

## Section 4, as a list

When you share Apache-2.0 code, changed or not, section 4 of the license asks you to:

1. **Give a copy of the license** to everyone who receives the code.
2. **Mark changed files**: any file you modified must carry a prominent notice saying you changed it.
3. **Keep the notices**: every copyright, patent, trademark and attribution notice in the source stays.
4. **Carry the NOTICE file**: if the project you copied has a `NOTICE` file, its attribution lines go into a `NOTICE` file of yours.

Your own project keeps its own license. Starling stays MIT. Only the copied file is Apache-2.0, which makes Starling "MIT, with one file under Apache-2.0". Say so in the README.

## The NOTICE file

`NOTICE` is Apache's place for attribution that must travel with the code: who wrote it, and credits the authors require. It is plain text, and it is not the license.

Two rules keep it useful. Copy the upstream attribution lines exactly. And add only attribution: no license terms, no marketing, no changelog.

## Saying what you changed

"Prominent notice" means somewhere a reader of that file will see it. A comment at the top is the usual place:

```python
# Copyright 2023 The Gustwind Authors
# SPDX-License-Identifier: Apache-2.0
# Modified by Robin Vale in 2026: added full jitter to every delay.
```

One line is enough. It tells readers that a bug in this file may be Robin's, not Gustwind's.

## SPDX headers and the LICENSES folder

`SPDX-License-Identifier: Apache-2.0` is a one-line way to say which license a file is under. It does not replace the license text, which must still ship with the project. The [REUSE](https://reuse.software) convention keeps one copy of each license in a `LICENSES/` folder, named by its identifier, such as `LICENSES/Apache-2.0.txt`. Scanners and people both understand it.

## The patent license

Apache-2.0 has something MIT does not. Section 3 gives you a license to any patents the contributors hold that cover their contributions. And if you sue someone claiming the code infringes your patent, your patent license from that project ends. This is the main reason companies prefer Apache-2.0, and it is why GPL-2.0, which has no such terms and forbids extra ones, cannot be combined with it.

## Fix the case

In `lab/cases/case04_apache_copy/`:

1. Put Gustwind's two header lines back at the top of `starling/backoff.py`, and add a third that says what Robin changed.
2. Add the full Apache 2.0 text as `LICENSES/Apache-2.0.txt`. Copy it from `upstream/gustwind/LICENSE`.
3. Create `NOTICE`: name Starling, say that `starling/backoff.py` comes from Gustwind and was changed, and include Gustwind's NOTICE lines.
4. Leave Starling's own `LICENSE` as it is.

## Check it works

```bash
uv run python -m nest check 4
```

```text
  PASS  Starling's own LICENSE is still MIT
  PASS  starling/backoff.py keeps Gustwind's copyright line
  PASS  starling/backoff.py says it is under Apache-2.0
  PASS  starling/backoff.py says what was changed
  PASS  the full Apache License 2.0 text ships with Starling
  PASS  Starling's NOTICE carries Gustwind's NOTICE lines
```

## Exercise

Change the SPDX line in your fix to `SPDX-License-Identifier: MIT`, so the whole project looks like one license, and run the check. Who is allowed to change the license of Gustwind's code?

### More to try

- Run `uv run python -m nest compat Apache-2.0 GPL-2.0-only` and read why.
- Find a project you use that has a `NOTICE` file. What does it hold?
