// Facts shown on the site. Every symptom and output line is real output from the lab:
// `uv run python -m nest run N` and `nest check N`. A unit test finds each one in the chapters.

export const REPO_URL = 'https://github.com/jars-demo/licensing-demo'
export const SITE_URL = 'https://licensing.jishanahmed.in'

export type Case = {
  number: string
  title: string
  topics: string
  symptom: string
}

export const CASES: readonly Case[] = [
  {
    number: '01',
    title: 'The repo nobody could use',
    topics: 'copyright, choosing a licence',
    symptom: "✗ no LICENSE file: the code is 'all rights reserved' and nobody may reuse it",
  },
  {
    number: '02',
    title: 'Three answers to one question',
    topics: 'SPDX ids, manifests, README',
    symptom: '✗ web/package.json says ISC, LICENSE is Apache-2.0',
  },
  {
    number: '03',
    title: 'The name that went missing',
    topics: "MIT's condition, templates, forks",
    symptom: 'that notice, in Starling      nowhere',
  },
  {
    number: '04',
    title: 'The file that forgot where it came from',
    topics: 'Apache-2.0, NOTICE, stated changes',
    symptom: 'starling/backoff.py       (no header)',
  },
  {
    number: '05',
    title: 'The font with no papers',
    topics: 'OFL, icon sets, Creative Commons',
    symptom: 'assets/fonts/WrenSans-Regular.woff2   OFL-1.1   no',
  },
  {
    number: '06',
    title: 'The partner nobody signed up',
    topics: 'trademarks, logos, endorsement',
    symptom: 'claim:   templates/header.html: Official Driftwood partner',
  },
  {
    number: '07',
    title: 'The copyleft two levels down',
    topics: 'dependencies, copyleft, CI gates',
    symptom: 'colorwheel 1.4.0: GPL-3.0-only, pulled in by prettyout',
  },
  {
    number: '08',
    title: 'The fork that hid its source',
    topics: 'AGPL, network use, source offers',
    symptom: 'deploy/site.toml          source_url = ""',
  },
]

/** Case 07 from `nest run 7`, for the hero. */
export const CASE_SEVEN = {
  tree: [
    'prettyout 2.1.0       MIT             tables',
    '  colorwheel 1.4.0    GPL-3.0-only    colour   ✗ not permissive',
    'click-lite 3.0.2      BSD-3-Clause    commands',
  ],
  verdict: 'Starling is MIT. Packages it ships that are not permissive: 1',
  culprit: '  colorwheel 1.4.0: GPL-3.0-only, pulled in by prettyout',
}

/** Case 02 from start to finish: what the scan says, the fix, and the check. */
export const CASE_TWO = {
  run: [
    "✗ README's License section names MIT, LICENSE is Apache-2.0",
    '✗ pyproject.toml: "MIT License" is not an SPDX identifier (use "MIT")',
    '✗ web/package.json says ISC, LICENSE is Apache-2.0',
  ],
  fix: [
    '- license = "MIT License"',
    '+ license = "Apache-2.0"',
    '- "license": "ISC"',
    '+ "license": "Apache-2.0"',
  ],
  check: [
    'PASS  pyproject.toml declares the SPDX id Apache-2.0',
    'PASS  web/package.json declares Apache-2.0',
    "PASS  the README's License section names Apache 2.0, and only that",
  ],
}

export const LEARN = [
  {
    title: 'No licence, no permission',
    text: 'Why public code is still all rights reserved, and how to add a licence with the exact text and a real copyright line.',
  },
  {
    title: 'One licence, three places',
    text: 'LICENSE, the README and every manifest, saying the same thing in SPDX identifiers that tools understand.',
  },
  {
    title: 'Borrowing properly',
    text: "Keeping a template's notice, and the four things Apache-2.0 asks when you copy and change its code.",
  },
  {
    title: 'Assets and trademarks',
    text: "Licences for fonts, icons and images, and how to show another product's logo without claiming its endorsement.",
  },
  {
    title: 'What you ship',
    text: 'Permissive, copyleft and source-available dependencies, and the GPL package hiding two levels down.',
  },
  {
    title: 'Copyleft over the network',
    text: 'What the AGPL adds for web services, when it applies, and how to offer the source of the version you run.',
  },
]

export const CHECKLIST = [
  'Every repository gets a licence file with the exact, canonical text. No licence means no permission.',
  'Fill in the copyright line with a real name and year, and leave every other word alone.',
  'Declare the same licence in `LICENSE`, the README and every manifest, as an SPDX identifier.',
  "When you build on someone's code, keep their copyright notice. Add your name; never replace theirs.",
  'Copying Apache-2.0 code: ship the licence, keep the headers, say what you changed, and carry their NOTICE lines.',
  'Fonts, icons and images have licences. Ship each licence next to the asset it covers.',
  "A licence never grants a trademark. Use other products' names and logos to say what you work with, never to claim endorsement.",
  'Read the licence of every dependency you ship, including the ones two levels down, and check them in CI.',
  'GPL code in something you distribute makes the whole thing GPL. AGPL code you change and run online must offer its source.',
  'Only the owner can change a licence. When in doubt, ask the author, and for anything that matters legally, ask a lawyer.',
]

export const QUICKSTART = `git clone https://github.com/jars-demo/licensing-demo.git
cd licensing-demo/lab
uv sync
uv run python -m nest run 1`

export const SCAN_COMMAND = 'uv run python -m nest scan ~/code/your-project'
