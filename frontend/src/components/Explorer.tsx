'use client'

import { useState } from 'react'

import { FOUND, type Found, INTO, type Into, type Verdict, verdict, WORDS } from '@/lib/compat'

// "Can I use it?": pick the licence of the code you found and the licence of your project, and
// see whether they combine. Every verdict pairs its colour with an icon and a word.

const LOOK: Record<Verdict, string> = {
  yes: 'border-ok bg-ok-wash text-ok',
  cond: 'border-cond bg-cond-wash text-cond',
  no: 'border-no bg-no-wash text-no',
}

const LABEL: Record<Found, string> = {
  MIT: 'MIT',
  'BSD-3-Clause': 'BSD-3-Clause',
  ISC: 'ISC',
  'Apache-2.0': 'Apache-2.0',
  'MPL-2.0': 'MPL-2.0',
  'GPL-2.0-only': 'GPL-2.0-only',
  'GPL-3.0': 'GPL-3.0',
  'AGPL-3.0': 'AGPL-3.0',
  none: 'No licence',
}

export function Mark({ kind, size = 14 }: { kind: Verdict; size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 14 14" aria-hidden="true" className="shrink-0">
      {kind === 'yes' ? (
        <path d="M2.5 7.5l3 3 6-7" fill="none" stroke="currentColor" strokeWidth="2.2" />
      ) : kind === 'cond' ? (
        <path d="M7 2v6.5M7 10.5v1.8" stroke="currentColor" strokeWidth="2.2" />
      ) : (
        <path d="M3 3l8 8M11 3l-8 8" stroke="currentColor" strokeWidth="2.2" />
      )}
    </svg>
  )
}

function Choices<T extends string>({
  legend,
  options,
  value,
  label,
  onChange,
}: {
  legend: string
  options: readonly T[]
  value: T
  label: (option: T) => string
  onChange: (option: T) => void
}) {
  return (
    <fieldset className="flex flex-col gap-2.5">
      <legend className="eyebrow mb-2.5">{legend}</legend>
      <div className="flex flex-wrap gap-2">
        {options.map((option) => (
          <button
            key={option}
            type="button"
            aria-pressed={option === value}
            onClick={() => onChange(option)}
            className={`inline-flex min-h-10 items-center border px-3 font-mono text-[13px] ${
              option === value
                ? 'border-ink bg-signal font-medium text-ink'
                : 'border-rule-strong bg-surface text-ink-2 hover:border-ink hover:text-ink'
            }`}
          >
            {label(option)}
          </button>
        ))}
      </div>
    </fieldset>
  )
}

export function Explorer() {
  const [found, setFound] = useState<Found>('GPL-3.0')
  const [into, setInto] = useState<Into>('MIT')
  const [kind, why] = verdict(found, into)

  return (
    <div className="panel flex min-w-0 flex-col border-2 border-ink">
      <div className="flex flex-col gap-6 p-4 sm:p-5">
        <Choices
          legend="1. The code you found is under"
          options={FOUND}
          value={found}
          label={(option) => LABEL[option]}
          onChange={setFound}
        />
        <Choices
          legend="2. Your project is under"
          options={INTO}
          value={into}
          label={(option) => option}
          onChange={setInto}
        />
      </div>
      <div
        role="status"
        aria-live="polite"
        key={`${found}-${into}`}
        className={`stamp mx-4 mb-4 flex flex-col gap-2 border-2 p-4 sm:mx-5 ${LOOK[kind]}`}
      >
        <p className="flex items-center gap-2 font-sans text-[13px] font-bold tracking-[0.1em] uppercase">
          <Mark kind={kind} size={16} />
          <span data-testid="verdict">{WORDS[kind]}</span>
        </p>
        <p className="display text-[19px] leading-snug text-ink">
          {LABEL[found]} code in {/^[AM]/.test(into) ? 'an' : 'a'} {into} project
        </p>
        <p className="text-[15px] leading-relaxed text-ink-2">{why}</p>
      </div>
      <div className="border-t border-rule px-4 py-4 sm:px-5">
        <p className="eyebrow mb-3">{LABEL[found]} code, into every licence</p>
        <ul className="grid grid-cols-2 gap-2 sm:grid-cols-3">
          {INTO.map((target) => {
            const [each] = verdict(found, target)
            return (
              <li
                key={target}
                className={`flex min-h-10 items-center justify-between gap-2 border px-3 text-[13px] ${LOOK[each]}`}
              >
                <span className="font-mono">{target}</span>
                <span className="flex items-center gap-1 font-semibold">
                  <Mark kind={each} size={12} />
                  {each === 'cond' ? 'With conditions' : WORDS[each]}
                </span>
              </li>
            )
          })}
        </ul>
      </div>
    </div>
  )
}
