# Fonts, icons and images

> A font file is software, an icon set is code, and a photo has an author. Each one ships with its own license.

**Time:** 15 minutes

## Goal

Treat assets like code: find their license before using them, ship the license alongside them, and know the rules of the licenses you will meet most, the SIL Open Font License, the permissive icon licenses and Creative Commons.

## The case

```bash
uv run python -m nest run 5
```

```text
file                                  license   license shipped
assets/fonts/WrenSans-Regular.woff2   OFL-1.1   no
assets/icons/ (3 icons, Feathery)     ISC       no

Starling's LICENSE: MIT · Copyright (c) 2026 Robin Vale
```

Starling's web view is set in Wren Sans, an open font, and uses three icons from Feathery, an open icon set. Both are free to use. Neither came with its license. The originals, with their licenses, are in `upstream/`.

## Assets have authors

People treat a font or an icon as decoration, not code. Copyright does not. Someone designed every glyph and drew every icon, and they own them unless they gave them away. "Free download" on a website is not a license. Look for the license file, or the license on the project's page, before you add the asset.

## The SIL Open Font License

Most open fonts, including most Google Fonts, use the OFL. It is generous:

- You may use the font anywhere, embed it in documents and apps, and bundle it with software, including commercial software.
- You may change it. A changed version must stay under the OFL.
- You may not sell the font on its own.
- Every copy must include the font's copyright notice and the license. Put the license next to the font files, usually as `OFL.txt`.
- If the authors declared a **Reserved Font Name**, a modified version may not use that name. Subsetting a font for the web can count as modifying it, so check before you ship a subset under the original name.

Loading a font from a font service such as Google Fonts means the service distributes it, not you. Bundling the file in your repository means you do.

## Icon sets

Icon sets use ordinary software licenses, and their conditions are the same as for code: keep the notice.

| Icon set     | License | What you keep                                                   |
| ------------ | ------- | --------------------------------------------------------------- |
| Lucide       | ISC     | Copyright and permission notice                                 |
| Heroicons    | MIT     | Copyright and permission notice                                 |
| Feather      | MIT     | Copyright and permission notice                                 |
| Simple Icons | CC0-1.0 | Nothing, but the logos inside are still trademarks (chapter 06) |

## Images and Creative Commons

Photos, illustrations and documentation often use Creative Commons licenses:

- **CC0** gives the work to the public domain. No conditions.
- **CC-BY** asks for credit: the author, the source, the license and whether you changed it.
- **CC-BY-SA** adds share-alike: changed versions must use the same license.
- **NC** (non-commercial) and **ND** (no derivatives) versions forbid commercial use or changes. They do not suit most software projects.

Creative Commons licenses are for content, not code. For code, use a software license.

## Fix the case

In `lab/cases/case05_assets/`:

1. Copy `upstream/wren-sans/OFL.txt` to `assets/fonts/OFL.txt`, next to the font. Its copyright line must stay as the authors wrote it.
2. Copy `upstream/feathery/LICENSE` to `assets/icons/LICENSE`. A `THIRD_PARTY_NOTICES.md` with the same text also works.
3. Leave Starling's own `LICENSE` alone. The font's license covers the font, not Starling.

## Check it works

```bash
uv run python -m nest check 5
```

```text
  PASS  the Wren Sans license (OFL-1.1) ships next to the font
  PASS  and it carries the font's copyright line
  PASS  the Feathery icons' ISC license and copyright ship with Starling
  PASS  Starling's own LICENSE is still MIT, and still Robin's
```

## Exercise

Copy the blank OFL template from `lab/nest/texts/OFL-1.1.txt` into `assets/fonts/` instead of the real one, and run the check. Why does the copyright line matter as much as the license words?

### More to try

- List every font, icon and image in a project of yours. Can you name the license of each one?
- Open a font on Google Fonts and find its license. Does it declare a Reserved Font Name?
