# Names and logos

> Copyright covers the logo file. Trademark covers what the logo means. No open source license grants the second.

**Time:** 15 minutes

## Goal

Tell copyright and trademark apart, use another product's name and logo to say what yours works with, word it so it never suggests they made or back your project, and record it in a NOTICE.

## The case

```bash
uv run python -m nest run 6
```

```text
claim:   README.md: The official Driftwood DB notebook, endorsed by Driftwood Data
claim:   templates/header.html: Official Driftwood partner
logo:    assets/logos/driftwood.svg, the mark of Driftwood Data
notice:  none
```

Starling for Driftwood keeps notes in a Driftwood DB database. Robin wanted people to recognise the integration, so he put Driftwood's logo in the header, and then went further. Driftwood Data never endorsed Starling, and Starling is not a partner.

## Two different rights

|                      | Copyright                     | Trademark                        |
| -------------------- | ----------------------------- | -------------------------------- |
| Protects             | A work: code, text, a drawing | A sign of origin: a name, a logo |
| Answers              | Who may copy this?            | Who does this come from?         |
| Open source licenses | Grant it, on conditions       | Do not grant it                  |

Apache-2.0 says it outright in section 6: the license does not let you use the licensor's trade names or marks. MIT says nothing about trademarks, and GPL-3.0 mentions them only to let authors refuse trademark rights explicitly. None of them grants one. Even when a logo's file is under an open license, the mark it shows is not.

## What you may say

Trademark law in many countries lets you name another product to say what yours works with, as long as you do not suggest that its owner made, sponsors or endorses yours. "Works with Driftwood DB" names a product. "Official Driftwood partner" claims a relationship.

| Says what it works with           | Claims a relationship      |
| --------------------------------- | -------------------------- |
| Works with Driftwood DB           | Official Driftwood client  |
| A notebook for Driftwood DB       | Driftwood-certified        |
| Connects to Driftwood DB          | Endorsed by Driftwood Data |
| Integrations: [logo] Driftwood DB | Driftwood partner          |

Many companies publish brand guidelines that add rules: minimum sizes, colours, no changes to the logo, sometimes no use in product names at all. Read them before using a logo, and follow them. This chapter is not legal advice: when a name is central to a product or money is involved, ask a lawyer.

## Do not put their name in yours

Calling the project "Driftwood Notes" makes the confusion permanent: every mention of your project uses their mark. Prefer your own name with a description: "Starling for Driftwood DB" is a common pattern, and "Starling, a notebook for Driftwood DB" is safer still.

## The notice

A trademark notice in `NOTICE` (or `THIRD_PARTY_NOTICES.md`) says three things: which file is whose mark, why you use it, and that you are not endorsed.

```text
assets/logos/driftwood.svg is the logo of Driftwood DB. Driftwood DB and its logo are
trademarks of Driftwood Data. They are used only to show which database Starling works
with. Starling is not an official Driftwood project and is not endorsed by Driftwood Data.
```

Good projects add one more line: how to ask for removal. It shows good faith and gives the owner a quiet way to raise a concern.

## Fix the case

In `lab/cases/case06_logo/`:

1. Rewrite the README's description and the header's text so they say what Starling works with, and claim nothing more.
2. Keep the logo in the header. People should recognise the integration.
3. Add a `NOTICE` naming the logo file, Driftwood Data as the trademark owner, and stating that Starling is not official or endorsed.

## Check it works

```bash
uv run python -m nest check 6
```

```text
  PASS  README and the header make no claim to be official, endorsed or a partner
  PASS  the header still shows Driftwood's logo, so people recognise it
  PASS  a NOTICE names the logo file and Driftwood Data's trademark
  PASS  the NOTICE says Starling is not official or endorsed
```

## Exercise

Add the notice, but leave "Official Driftwood partner" in the header, and run the check. Why can a notice not undo a claim made somewhere else?

### More to try

- Find the brand guidelines of a product your project integrates with. What do they say about using the logo?
- Read the trademark section of the Apache License 2.0. It is three lines long.
