import Link from 'next/link'

import { ChapterList } from '@/components/ChapterList'
import { CopyButton } from '@/components/CopyButton'
import { Explorer, Mark } from '@/components/Explorer'
import { Maggie } from '@/components/Maggie'
import { Markdown } from '@/components/Markdown'
import {
  CASE_SEVEN,
  CASE_TWO,
  CHECKLIST,
  LEARN,
  QUICKSTART,
  REPO_URL,
  SCAN_COMMAND,
} from '@/lib/site'
import { CHAPTERS } from '@/lib/workshop'

function SectionHead({
  id,
  eyebrow,
  title,
  children,
}: {
  id: string
  eyebrow: string
  title: string
  children?: React.ReactNode
}) {
  return (
    <div className="flex max-w-2xl flex-col gap-3">
      <span className="eyebrow">{eyebrow}</span>
      <h2 id={id} className="display text-[30px] leading-[1.08] text-ink sm:text-[40px]">
        {title}
      </h2>
      {children ? (
        <p className="font-serif text-[18px] leading-relaxed text-ink-2">{children}</p>
      ) : null}
    </div>
  )
}

export default function Home() {
  const minutes = CHAPTERS.reduce((sum, chapter) => sum + chapter.minutes, 0)
  return (
    <>
      <section className="border-b border-rule">
        <div className="mx-auto grid max-w-6xl gap-12 px-4 pt-12 pb-16 lg:grid-cols-[minmax(0,1.15fr)_minmax(0,1fr)] lg:items-end lg:gap-16 lg:pt-20 lg:pb-20">
          <div className="flex min-w-0 flex-col gap-6">
            <span className="eyebrow">
              A hands-on workshop · {CHAPTERS.length} chapters · {minutes} minutes
            </span>
            <h1 className="display text-[44px] leading-[0.98] text-balance text-ink sm:text-[68px]">
              Whose code is it{' '}
              <span className="bg-signal px-1.5 box-decoration-clone">anyway?</span>
            </h1>
            <p className="max-w-xl font-serif text-[20px] leading-relaxed text-ink-2 sm:text-[21px]">
              Every project borrows: a template, a snippet, a font, a logo, three hundred packages.
              Learn what each one lets you do and what it asks in return, one real licensing mistake
              at a time, in one small open source project.
            </p>
            <div className="flex flex-wrap gap-3 pt-1">
              <Link
                href={`/workshop/${CHAPTERS[0]?.slug ?? ''}`}
                className="inline-flex h-12 items-center border-2 border-ink bg-signal px-6 text-[15.5px] font-bold text-ink shadow-[4px_4px_0_0_var(--ink)] hover:bg-signal-hover"
              >
                Start chapter 01
              </Link>
              <a
                href={REPO_URL}
                className="inline-flex h-12 items-center border-2 border-ink bg-surface px-6 text-[15.5px] font-bold text-ink hover:bg-surface-2"
              >
                Read the source
              </a>
            </div>
          </div>
          <figure className="code min-w-0 border-2 border-ink">
            <figcaption className="flex items-center justify-between gap-3 border-b border-code-rule px-4 py-2.5 text-[12px] text-code-muted">
              <span>uv run python -m nest run 7</span>
              <span className="hidden font-sans font-bold tracking-[0.1em] uppercase sm:inline">
                real output
              </span>
            </figcaption>
            <pre className="overflow-x-auto px-4 py-4 text-[12px] leading-relaxed sm:text-[12.5px]">
              <span>{CASE_SEVEN.tree[0]}</span>
              {'\n'}
              <span className="text-code-no">{CASE_SEVEN.tree[1]}</span>
              {'\n'}
              <span>{CASE_SEVEN.tree[2]}</span>
              {'\n\n'}
              <span className="text-code-muted">{CASE_SEVEN.verdict}</span>
              {'\n'}
              <span className="text-code-no">{CASE_SEVEN.culprit}</span>
            </pre>
            <p className="border-t border-code-rule px-4 py-3 font-sans text-[14px] leading-snug text-code-ink">
              Robin asked for one MIT package. It brought a GPL one along, two levels down, inside
              an app Robin ships as MIT. Chapter 07 finds a way out that keeps the coloured tables.
            </p>
          </figure>
        </div>
      </section>

      <section
        aria-labelledby="learn"
        className="mx-auto flex max-w-6xl flex-col gap-10 px-4 pt-20"
      >
        <SectionHead
          id="learn"
          eyebrow="What you will learn"
          title="From your first LICENSE to the AGPL"
        >
          A licence is permission in writing, with conditions. Each chapter takes one kind of
          permission, shows a project that broke its conditions, and fixes it.
        </SectionHead>
        <ol className="grid gap-x-10 gap-y-8 sm:grid-cols-2 lg:grid-cols-3">
          {LEARN.map((item, index) => (
            <li key={item.title} className="ruled flex min-w-0 flex-col gap-2 pt-3">
              <span className="font-mono text-[13px] text-muted">
                {String(index + 1).padStart(2, '0')}
              </span>
              <span className="display text-[20px] leading-snug text-ink">{item.title}</span>
              <span className="text-[15.5px] leading-relaxed text-ink-2">{item.text}</span>
            </li>
          ))}
        </ol>
      </section>

      <section
        id="explorer"
        aria-labelledby="explorer-title"
        className="mx-auto grid max-w-6xl scroll-mt-6 gap-10 px-4 pt-24 lg:grid-cols-[minmax(0,20rem)_minmax(0,1fr)] lg:gap-12 [&>*]:min-w-0"
      >
        <div className="flex flex-col gap-5">
          <SectionHead id="explorer-title" eyebrow="Try it" title="Can I use it?">
            You found some code you want. Pick its licence and your project&apos;s licence, and see
            whether they combine, and on what conditions.
          </SectionHead>
          <ul className="flex flex-col gap-1.5 border-t border-rule pt-4 text-[13.5px] text-ink-2">
            <li className="flex items-center gap-2 text-ok">
              <Mark kind="yes" />{' '}
              <span className="text-ink-2">Green means yes: keep the notices.</span>
            </li>
            <li className="flex items-center gap-2 text-cond">
              <Mark kind="cond" />{' '}
              <span className="text-ink-2">Blue means yes, with conditions to follow.</span>
            </li>
            <li className="flex items-center gap-2 text-no">
              <Mark kind="no" />{' '}
              <span className="text-ink-2">Red means no, not as things stand.</span>
            </li>
          </ul>
          <p className="text-[14px] leading-relaxed text-muted">
            The same table as <code className="font-mono text-[13px] text-ink">nest compat</code> in
            the lab, for the common case of distributing the combined code. It is a guide, not legal
            advice.
          </p>
        </div>
        <Explorer />
      </section>

      <section
        aria-labelledby="chapters"
        className="mx-auto flex max-w-6xl flex-col gap-10 px-4 pt-24"
      >
        <SectionHead id="chapters" eyebrow="The index" title="Eight chapters, eight mistakes">
          Each chapter explains one idea in depth, then hands you a small project that gets it wrong
          in exactly that way. You fix it, and the checker reads the project like a scanner would.
        </SectionHead>
        <ChapterList />
      </section>

      <section
        aria-labelledby="method"
        className="mx-auto flex max-w-6xl flex-col gap-10 px-4 pt-24"
      >
        <SectionHead id="method" eyebrow="How a case works" title="Run it, fix it, prove it">
          Every case is a folder: a tiny project with one licensing mistake in it. Nothing to
          install beyond uv. Here is case 02 from start to finish.
        </SectionHead>
        <ol className="grid gap-6 lg:grid-cols-3 [&>*]:min-w-0">
          {[
            {
              step: 'Run it',
              command: 'uv run python -m nest run 2',
              lines: CASE_TWO.run,
              tone: 'text-code-no',
              note: 'One licence file, three different answers around it.',
            },
            {
              step: 'Fix it',
              command: 'pyproject.toml, web/package.json',
              lines: CASE_TWO.fix,
              tone: 'text-code-ink',
              note: 'LICENSE is the truth. Bring the descriptions into line.',
            },
            {
              step: 'Prove it',
              command: 'uv run python -m nest check 2',
              lines: CASE_TWO.check,
              tone: 'text-code-ok',
              note: 'Every place names the same licence, in words tools understand.',
            },
          ].map((card, index) => (
            <li key={card.step} className="flex flex-col gap-3">
              <div className="flex items-center gap-3">
                <span className="folio text-[14px]">{index + 1}</span>
                <span className="display text-[18px] text-ink">{card.step}</span>
              </div>
              <div className="code flex flex-1 flex-col overflow-hidden">
                <div className="truncate border-b border-code-rule px-3.5 py-2 text-[12px] text-code-muted">
                  {card.command}
                </div>
                <pre
                  className={`px-3.5 py-3 text-[12.5px] leading-relaxed whitespace-pre-wrap [overflow-wrap:anywhere] ${card.tone}`}
                >
                  {card.lines.join('\n')}
                </pre>
              </div>
              <p className="text-[14.5px] text-ink-2">{card.note}</p>
            </li>
          ))}
        </ol>
      </section>

      <section
        aria-labelledby="start"
        className="mx-auto grid max-w-6xl gap-10 px-4 pt-24 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)] lg:items-start [&>*]:min-w-0"
      >
        <div className="flex flex-col gap-6">
          <SectionHead id="start" eyebrow="Quick start" title="Four commands to the first case">
            You need git and uv. uv installs Python 3.13 for you, and the lab uses the standard
            library only. No accounts, no API keys, no Docker.
          </SectionHead>
          <div className="flex flex-col gap-3 border-t border-rule pt-5">
            <p className="display text-[19px] text-ink">Then scan your own projects</p>
            <p className="text-[15.5px] leading-relaxed text-ink-2">
              The scanner from the lab works on any folder: it reads LICENSE, the README and every
              manifest, and tells you where they disagree.
            </p>
            <div className="code flex items-center justify-between gap-2 overflow-hidden border-l-4 border-signal py-1 pr-1 pl-4">
              <code className="truncate text-[13px]">{SCAN_COMMAND}</code>
              <CopyButton text={SCAN_COMMAND} />
            </div>
          </div>
        </div>
        <div className="code border-2 border-ink">
          <div className="flex items-center justify-between border-b border-code-rule py-1 pr-1 pl-4">
            <span className="font-sans text-[11.5px] font-bold tracking-[0.12em] text-code-muted uppercase">
              shell
            </span>
            <CopyButton text={QUICKSTART} />
          </div>
          <pre className="overflow-x-auto px-4 py-4 text-[13px] leading-relaxed">{QUICKSTART}</pre>
        </div>
      </section>

      <section
        id="checklist"
        aria-labelledby="checklist-title"
        className="mx-auto grid max-w-6xl scroll-mt-6 gap-10 px-4 pt-24 pb-24 lg:grid-cols-[minmax(0,20rem)_minmax(0,1fr)] lg:gap-14 [&>*]:min-w-0"
      >
        <div className="flex flex-col gap-6">
          <SectionHead id="checklist-title" eyebrow="Take it with you" title="The checklist">
            Ten rules, one per idea in the workshop. The last chapter ends with the same list.
          </SectionHead>
          <Maggie className="size-28" />
        </div>
        <ol className="ruled flex flex-col">
          {CHECKLIST.map((item, index) => (
            <li
              key={item}
              className="grid grid-cols-[2.75rem_minmax(0,1fr)] items-baseline gap-3 border-b border-rule py-3.5"
            >
              <span className="folio text-[13px]">{String(index + 1).padStart(2, '0')}</span>
              <span className="checklist-item text-[16px] leading-relaxed text-ink">
                <Markdown>{item}</Markdown>
              </span>
            </li>
          ))}
        </ol>
      </section>
    </>
  )
}
