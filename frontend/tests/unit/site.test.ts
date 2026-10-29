import fs from 'node:fs'
import path from 'node:path'

import { describe, expect, it } from 'vitest'

import { CASE_SEVEN, CASE_TWO, CASES, CHECKLIST } from '@/lib/site'
import { CHAPTERS } from '@/lib/workshop'

// Every line the site quotes is real lab output, and the lab's tests prove the chapters quote
// real output. So each line on the site must appear, word for word, in its chapter.

const chapter = (number: string) => CHAPTERS.find((c) => c.number === number)?.body ?? ''

describe('site facts', () => {
  it('has one case per chapter, in order', () => {
    expect(CASES.map((c) => c.number)).toEqual(CHAPTERS.map((c) => c.number))
    expect(CHAPTERS).toHaveLength(8)
  })

  it.each(CASES)('case $number shows a symptom from its chapter', (item) => {
    expect(chapter(item.number)).toContain(item.symptom)
  })

  it('quotes case 07 exactly as chapter 07 does', () => {
    for (const line of [...CASE_SEVEN.tree, CASE_SEVEN.verdict, CASE_SEVEN.culprit]) {
      expect(chapter('07')).toContain(line)
    }
  })

  it('quotes case 02 exactly as chapter 02 does', () => {
    for (const line of [...CASE_TWO.run, ...CASE_TWO.check]) {
      expect(chapter('02')).toContain(line)
    }
  })

  it('has the same checklist as the last chapter', () => {
    const items = [...chapter('08').matchAll(/^\d+\. (.+)$/gm)].map((m) => m[1])
    expect(items.slice(-10)).toEqual(CHECKLIST)
  })

  it('names every case in the lab CLI with the same title', () => {
    const cli = fs.readFileSync(
      path.join(process.cwd(), '..', 'lab', 'nest', '__main__.py'),
      'utf8',
    )
    for (const item of CASES) {
      expect(cli).toContain(`"${item.title}"`)
    }
  })
})
