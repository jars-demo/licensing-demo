// Can code under one license go into a project under another? The same table as the lab's
// `nest compat` (lab/nest/compat.json). A unit test checks that the two never drift apart.

export type Verdict = 'yes' | 'cond' | 'no'

export const INTO = ['MIT', 'Apache-2.0', 'MPL-2.0', 'GPL-2.0-only', 'GPL-3.0', 'AGPL-3.0'] as const
export type Into = (typeof INTO)[number]

export const FOUND = [
  'MIT',
  'BSD-3-Clause',
  'ISC',
  'Apache-2.0',
  'MPL-2.0',
  'GPL-2.0-only',
  'GPL-3.0',
  'AGPL-3.0',
  'none',
] as const
export type Found = (typeof FOUND)[number]

type Row = Record<Into, readonly [Verdict, string]>

const KEEP = 'Keep its copyright line and license text with the code.'
const ASK = 'No license means no permission. Ask the author, or write your own.'
const MPL_FILES =
  'File-level copyleft: the copied files stay MPL-2.0 and their source must stay available. Your other files keep your license.'
const MPL_GPL = "Allowed unless the files are marked 'Incompatible With Secondary Licenses'."
const AGPL_WHOLE =
  'The whole work would become AGPL-3.0, including offering the source to users over a network.'

export const SAME_AS: Partial<Record<Found, Found>> = { 'BSD-3-Clause': 'MIT', ISC: 'MIT' }

export const VERDICTS: Record<Exclude<Found, 'BSD-3-Clause' | 'ISC'>, Row> = {
  MIT: {
    MIT: ['yes', KEEP],
    'Apache-2.0': ['yes', KEEP],
    'MPL-2.0': ['yes', KEEP],
    'GPL-2.0-only': ['yes', KEEP],
    'GPL-3.0': ['yes', KEEP],
    'AGPL-3.0': ['yes', KEEP],
  },
  'Apache-2.0': {
    MIT: [
      'cond',
      'The copied files stay Apache-2.0: keep the license, the NOTICE lines and a note of what you changed. Your project becomes MIT and Apache-2.0.',
    ],
    'Apache-2.0': [
      'yes',
      'Keep the license, carry its NOTICE lines into yours, and say what you changed.',
    ],
    'MPL-2.0': [
      'cond',
      'The copied files stay Apache-2.0, with their NOTICE lines and a note of what you changed.',
    ],
    'GPL-2.0-only': [
      'no',
      "Apache-2.0's patent terms are extra restrictions GPL-2.0 does not allow.",
    ],
    'GPL-3.0': [
      'yes',
      'GPL-3.0 was written to accept Apache-2.0 code. The combined work is GPL-3.0.',
    ],
    'AGPL-3.0': ['yes', 'AGPL-3.0 accepts Apache-2.0 code. The combined work is AGPL-3.0.'],
  },
  'MPL-2.0': {
    MIT: ['cond', MPL_FILES],
    'Apache-2.0': ['cond', MPL_FILES],
    'MPL-2.0': ['yes', 'Keep the notices, and keep the source of changed MPL files available.'],
    'GPL-2.0-only': ['cond', MPL_GPL],
    'GPL-3.0': ['cond', MPL_GPL],
    'AGPL-3.0': ['cond', MPL_GPL],
  },
  'GPL-2.0-only': {
    MIT: [
      'no',
      'Distributing it would make the whole work GPL-2.0. Only if you relicense your project.',
    ],
    'Apache-2.0': [
      'no',
      'Distributing it would make the whole work GPL-2.0, which cannot take Apache-2.0 terms.',
    ],
    'MPL-2.0': ['no', 'Distributing it would make the whole work GPL-2.0.'],
    'GPL-2.0-only': [
      'yes',
      'Same license. Keep the notices and share the source when you distribute.',
    ],
    'GPL-3.0': [
      'no',
      "'Only' means no later version: GPL-2.0-only and GPL-3.0 cannot be combined.",
    ],
    'AGPL-3.0': [
      'no',
      "'Only' means no later version: GPL-2.0-only cannot be combined with AGPL-3.0.",
    ],
  },
  'GPL-3.0': {
    MIT: [
      'no',
      'Distributing it would make the whole work GPL-3.0. Only if you relicense your project.',
    ],
    'Apache-2.0': [
      'no',
      'Distributing it would make the whole work GPL-3.0. Only if you relicense your project.',
    ],
    'MPL-2.0': ['no', 'Distributing it would make the whole work GPL-3.0.'],
    'GPL-2.0-only': ['no', 'GPL-3.0 code cannot go into a GPL-2.0-only work.'],
    'GPL-3.0': ['yes', 'Same license. Keep the notices and share the source when you distribute.'],
    'AGPL-3.0': [
      'yes',
      'Section 13 of both licenses allows combining them. The combined work is AGPL-3.0.',
    ],
  },
  'AGPL-3.0': {
    MIT: ['no', AGPL_WHOLE],
    'Apache-2.0': ['no', AGPL_WHOLE],
    'MPL-2.0': ['no', 'The whole work would become AGPL-3.0.'],
    'GPL-2.0-only': ['no', 'AGPL-3.0 code cannot go into a GPL-2.0-only work.'],
    'GPL-3.0': [
      'cond',
      'Section 13 allows combining them, but the AGPL part keeps its network clause.',
    ],
    'AGPL-3.0': [
      'yes',
      'Same license. Offer the source of your modified version to everyone who uses it, including over a network.',
    ],
  },
  none: {
    MIT: ['no', ASK],
    'Apache-2.0': ['no', ASK],
    'MPL-2.0': ['no', ASK],
    'GPL-2.0-only': ['no', ASK],
    'GPL-3.0': ['no', ASK],
    'AGPL-3.0': ['no', ASK],
  },
}

export function verdict(found: Found, into: Into): readonly [Verdict, string] {
  const key = (SAME_AS[found] ?? found) as keyof typeof VERDICTS
  return VERDICTS[key][into]
}

export const WORDS: Record<Verdict, string> = {
  yes: 'Yes',
  cond: 'Yes, with conditions',
  no: 'No',
}
