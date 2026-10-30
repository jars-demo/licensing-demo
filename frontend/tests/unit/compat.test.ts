import fs from 'node:fs'
import path from 'node:path'

import { describe, expect, it } from 'vitest'

import { FOUND, INTO, SAME_AS, verdict } from '@/lib/compat'

// The explorer and `nest compat` must give the same answer for every pair.

type Lab = {
  licenses: string[]
  found: string[]
  same_as: Record<string, string>
  verdicts: Record<string, Record<string, [string, string]>>
}

const lab: Lab = JSON.parse(
  fs.readFileSync(path.join(process.cwd(), '..', 'lab', 'nest', 'compat.json'), 'utf8'),
)

describe('compatibility table', () => {
  it('lists the same licenses as the lab', () => {
    expect([...INTO]).toEqual(lab.licenses)
    expect([...FOUND]).toEqual(lab.found)
    expect(SAME_AS).toEqual(lab.same_as)
  })

  it.each(FOUND.flatMap((found) => INTO.map((into) => [found, into] as const)))(
    '%s into %s matches the lab',
    (found, into) => {
      const key = lab.same_as[found] ?? found
      expect(verdict(found, into)).toEqual(lab.verdicts[key]?.[into])
    },
  )

  it('never lets GPL code into a permissive project', () => {
    expect(verdict('GPL-3.0', 'MIT')[0]).toBe('no')
    expect(verdict('AGPL-3.0', 'Apache-2.0')[0]).toBe('no')
    expect(verdict('none', 'GPL-3.0')[0]).toBe('no')
  })
})
